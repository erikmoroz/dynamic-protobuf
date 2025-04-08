from protobuf_schema_builder import ProtobufMessageBuilder, serialize_record


def basic_example():
    schema = {
        "name": {"type": "STRING"},
        "age": {"type": "INT64"},
        "active": {"type": "BOOL"},
        "score": {"type": "DOUBLE"},
    }

    builder = ProtobufMessageBuilder(schema)
    message_class, field_mapping = builder.build()

    print("Field name mapping:")
    for original, proto_name in field_mapping.items():
        print(f"  {original} -> {proto_name}")

    record = {"name": "Jan Kowalski", "age": 30, "active": True, "score": 95.5}

    serialized = serialize_record(message_class, field_mapping, record)
    print(f"\nSerialized data size: {len(serialized)} bytes")

    message = message_class()
    message.ParseFromString(serialized)

    print("\nDeserialized data:")
    print(f" Name: {getattr(message, field_mapping['name'])}")
    print(f" Age: {getattr(message, field_mapping['age'])}")
    print(f" Active: {getattr(message, field_mapping['active'])}")
    print(f" Score: {getattr(message, field_mapping['score'])}")


def special_field_names_example():
    schema = {"user-name": {"type": "STRING"}, "123field": {"type": "INT64"}, "normal_field": {"type": "BOOL"}}

    builder = ProtobufMessageBuilder(schema)
    message_class, field_mapping = builder.build()

    print("\nSpecial field name mapping:")
    for original, proto_name in field_mapping.items():
        print(f"  {original} -> {proto_name}")

    record = {"user-name": "Jan Kowalski", "123field": 42, "normal_field": False}

    serialized = serialize_record(message_class, field_mapping, record)

    message = message_class()
    message.ParseFromString(serialized)

    print("\nDeserialized special fields data:")
    for field in record:
        value = getattr(message, field_mapping[field])
        print(f"  {field}: {value}")


def partial_data_example():
    schema = {"name": {"type": "STRING"}, "age": {"type": "INT64"}, "active": {"type": "BOOL"}}

    builder = ProtobufMessageBuilder(schema)
    message_class, field_mapping = builder.build()

    record = {"name": "Partial Data", "active": True}

    serialized = serialize_record(message_class, field_mapping, record)

    message = message_class()
    message.ParseFromString(serialized)

    print("\nPartial data example:")
    print(f" Name: {getattr(message, field_mapping['name'])}")
    print(f" Active: {getattr(message, field_mapping['active'])}")
    print(f" Age (default): {getattr(message, field_mapping['age'])}")


def ignored_fields_example():
    schema = {"name": {"type": "STRING"}, "age": {"type": "INT64"}}

    builder = ProtobufMessageBuilder(schema)
    message_class, field_mapping = builder.build()

    record = {"name": "Extra Fields", "age": 25, "extra_field": "This will be ignored", "another_extra": 42}

    serialized = serialize_record(message_class, field_mapping, record)

    message = message_class()
    message.ParseFromString(serialized)

    print("\nIgnored fields example:")
    print(f" Name: {getattr(message, field_mapping['name'])}")
    print(f" Age: {getattr(message, field_mapping['age'])}")
    print(" 'extra_field' and 'another_extra' are ignored in serialization")


if __name__ == "__main__":
    print("=== Basic Protobuf Schema Builder Example ===")
    basic_example()
    special_field_names_example()
    partial_data_example()
    ignored_fields_example()
