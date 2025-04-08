from google.protobuf import descriptor_pb2


# ToDo simplify it!!!!
class BooleanFieldHandler:
    def add_field(self, message_proto, field_num, proto_field_name):
        message_proto.field.add(
            name=proto_field_name,
            number=field_num,
            type=descriptor_pb2.FieldDescriptorProto.TYPE_BOOL,
        )


class DoubleFieldHandler:
    def add_field(self, message_proto, field_num, proto_field_name):
        message_proto.field.add(
            name=proto_field_name,
            number=field_num,
            type=descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE,
        )


class Int64FieldHandler:
    def add_field(self, message_proto, field_num, proto_field_name):
        message_proto.field.add(
            name=proto_field_name,
            number=field_num,
            type=descriptor_pb2.FieldDescriptorProto.TYPE_INT64,
        )


class StringFieldHandler:
    def add_field(self, message_proto, field_num, proto_field_name):
        message_proto.field.add(
            name=proto_field_name,
            number=field_num,
            type=descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
        )
