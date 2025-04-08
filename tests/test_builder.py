import unittest

from protobuf_schema_builder import ProtobufMessageBuilder, serialize_record
from protobuf_schema_builder.exceptions import SchemaValidationError


class TestProtobufMessageBuilder(unittest.TestCase):
    def test_build_simple_schema(self):
        schema = {"name": {"type": "STRING"}, "age": {"type": "INT64"}, "active": {"type": "BOOL"}}

        builder = ProtobufMessageBuilder(schema)
        message_class, field_mapping = builder.build()

        self.assertIn("name", field_mapping)
        self.assertIn("age", field_mapping)
        self.assertIn("active", field_mapping)

        self.assertIsNotNone(message_class)

    def test_serialize_and_deserialize(self):
        schema = {
            "name": {"type": "STRING"},
            "age": {"type": "INT64"},
            "active": {"type": "BOOL"},
            "score": {"type": "DOUBLE"},
        }

        builder = ProtobufMessageBuilder(schema)
        message_class, field_mapping = builder.build()

        record = {"name": "Jan Kowalski", "age": 30, "active": True, "score": 95.5}

        serialized = serialize_record(message_class, field_mapping, record)

        message = message_class()
        message.ParseFromString(serialized)

        self.assertEqual("Jan Kowalski", getattr(message, field_mapping["name"]))
        self.assertEqual(30, getattr(message, field_mapping["age"]))
        self.assertEqual(True, getattr(message, field_mapping["active"]))
        self.assertEqual(95.5, getattr(message, field_mapping["score"]))

    def test_invalid_field_type(self):
        schema = {"field1": {"type": "UNKNOWN_TYPE"}}
        with self.assertRaises(SchemaValidationError):
            _ = ProtobufMessageBuilder(schema)

    def test_missing_field_type(self):
        schema = {"field1": {"not_type": "STRING"}}
        with self.assertRaises(SchemaValidationError):
            _ = ProtobufMessageBuilder(schema)

    def test_field_name_mapping(self):
        schema = {"user-name": {"type": "STRING"}, "123field": {"type": "INT64"}, "normal_field": {"type": "BOOL"}}

        builder = ProtobufMessageBuilder(schema)
        message_class, field_mapping = builder.build()

        self.assertIn("user-name", field_mapping)
        self.assertIn("123field", field_mapping)
        self.assertIn("normal_field", field_mapping)

        for original, mapped in field_mapping.items():
            self.assertFalse(mapped[0].isdigit())
            self.assertRegex(mapped, r"^[a-zA-Z0-9_]+$")

    def test_partial_record(self):
        schema = {"name": {"type": "STRING"}, "age": {"type": "INT64"}, "active": {"type": "BOOL"}}

        builder = ProtobufMessageBuilder(schema)
        message_class, field_mapping = builder.build()

        record = {"name": "Jan Kowalski", "active": False}

        serialized = serialize_record(message_class, field_mapping, record)

        message = message_class()
        message.ParseFromString(serialized)

        self.assertEqual("Jan Kowalski", getattr(message, field_mapping["name"]))
        self.assertEqual(False, getattr(message, field_mapping["active"]))
        self.assertEqual(0, getattr(message, field_mapping["age"]))

    def test_extra_fields_in_record(self):
        schema = {"name": {"type": "STRING"}, "age": {"type": "INT64"}}

        builder = ProtobufMessageBuilder(schema)
        message_class, field_mapping = builder.build()

        record = {"name": "Patryk", "age": 25, "extra_field": "should be ignored"}

        serialized = serialize_record(message_class, field_mapping, record)

        message = message_class()
        message.ParseFromString(serialized)

        self.assertEqual("Patryk", getattr(message, field_mapping["name"]))
        self.assertEqual(25, getattr(message, field_mapping["age"]))

        with self.assertRaises(AttributeError):
            getattr(message, "extra_field")


if __name__ == "__main__":
    unittest.main()
