import hashlib
import re

from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

from .exceptions import FieldCreationError, MessageBuildError
from .field_handlers import BooleanFieldHandler, DoubleFieldHandler, Int64FieldHandler, StringFieldHandler
from .mixins import SchemaValidatorMixin


class ProtobufMessageBuilder(SchemaValidatorMixin):
    def __init__(self, schema):
        self.field_handlers = {
            "STRING": StringFieldHandler(),
            "DOUBLE": DoubleFieldHandler(),
            "INT64": Int64FieldHandler(),
            "BOOL": BooleanFieldHandler(),
        }
        self.supported_field_types = self.field_handlers.keys()
        self.validate_schema(schema)
        self.schema = schema
        self.message_descriptor_proto = descriptor_pb2.DescriptorProto()
        self.message_descriptor_proto.name = "DynamicMessage"
        self.field_num = 0
        self.field_name_mapping = {}

    def add_field(self, field_name, field_def):
        try:
            self.field_num += 1
            proto_field_name = self.generate_protobuf_safe_field_name(field_name)
            self.field_name_mapping[field_name] = proto_field_name

            field_type = field_def["type"]
            handler = self.field_handlers.get(field_type)
            handler.add_field(self.message_descriptor_proto, self.field_num, proto_field_name)
        except Exception as e:
            raise FieldCreationError(f"Unexpected error creating field '{field_name}': {str(e)}")

    def build(self):
        try:
            for field_name, field_def in self.schema.items():
                self.add_field(field_name, field_def)

            file_descriptor_proto = descriptor_pb2.FileDescriptorProto()
            file_descriptor_proto.name = "dp_message.proto"
            file_descriptor_proto.package = "dp_package"
            file_descriptor_proto.message_type.add().CopyFrom(self.message_descriptor_proto)

            pool = descriptor_pool.DescriptorPool()
            pool.Add(file_descriptor_proto)

            message_class = message_factory.GetMessages([file_descriptor_proto])["dp_package.DynamicMessage"]

            return message_class, self.field_name_mapping
        except FieldCreationError:
            raise
        except Exception as e:
            raise MessageBuildError(f"Failed to build protobuf message: {str(e)}")

    @staticmethod
    def generate_protobuf_safe_field_name(field_name):
        # Make field name compatible with protobuf requirements
        masked = re.sub(r"[^a-zA-Z0-9]", "_", field_name)

        if not masked:
            return f"field_{hashlib.sha1(field_name.encode()).hexdigest()[:8]}"

        if masked[0].isdigit():
            masked = f"f_{masked}"

        # Add hash suffix to avoid collisions
        hash_suffix = hashlib.sha1(field_name.encode()).hexdigest()[:8]
        return f"{masked}_{hash_suffix}"
