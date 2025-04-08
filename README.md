# Protobuf Schema Builder


I created this package while working with BigQuery's Storage Write API, which uses gRPC and Protocol Buffers.
Building and managing .proto files for every data structure was time-consuming. This library lets you create Protocol Buffer message classes dynamically at runtime from Python dictionaries, eliminating the need to manually create and compile .proto files.
The package builds on the Protocol Buffers message factory functionality but makes it much easier to use.
https://github.com/protocolbuffers/protobuf/blob/main/python/google/protobuf/message_factory.py


## Overview

This library allows you to:
- Create Protocol Buffer message classes from Python dictionaries
- Map between your field names and protobuf-safe field names
- Serialize and deserialize data using the dynamically created classes
- Work with Protocol Buffers without generating or compiling .proto files

## Purpose

This library is designed for scenarios where:
- You need to create protobuf message structures dynamically at runtime
- Your data schema is only known at runtime
- You want to avoid creating, managing and compiling .proto files
- You need to handle field names that aren't protobuf-compatible

## Use Cases

- Create message classes on-the-fly based on incoming data formats
- Generate message formats based on service configurations
- Convert between different data formats with minimal setup
- Quickly test protobuf serialization without writing schema files
- Handle evolving schemas without recompiling protobuf definitions

## Installation

```bash
uv add git+https://github.com/erikmoroz/dynamic-protobuf.git
```

## Basic Usage

```python
from protobuf_schema_builder import ProtobufMessageBuilder, serialize_record

# Define your schema
schema = {
    "name": {"type": "STRING"},
    "age": {"type": "INT64"},
    "active": {"type": "BOOL"}
}

# Build message class
builder = ProtobufMessageBuilder(schema)
message_class, field_mapping = builder.build()

# Create a record
record = {
    "name": "John Doe",
    "age": 30,
    "active": True
}

# Serialize to protobuf
serialized = serialize_record(message_class, field_mapping, record)

# Deserialize
message = message_class()
message.ParseFromString(serialized)
print(f"Name: {getattr(message, field_mapping['name'])}")
```

## Schema Definition

The schema is a Python dictionary where:
- Keys are your field names
- Values are dictionaries with a required "type" key

Supported field types:
- `STRING`: For text data
- `INT64`: For integer values
- `DOUBLE`: For floating-point values
- `BOOL`: For boolean values

## Examples

### Working with Non-Standard Field Names

```python
schema = {
    "user-name": {"type": "STRING"},     # Contains hyphen
    "123field": {"type": "INT64"},       # Starts with number
    "normal_field": {"type": "BOOL"}
}

builder = ProtobufMessageBuilder(schema)
message_class, field_mapping = builder.build()

# Field names are automatically converted to be protobuf-compatible
print(field_mapping)
# Output: {'user-name': 'user_name_abcdef12', '123field': 'f_123field_34567890', 'normal_field': 'normal_field_12345678'}
```

### Partial Data Serialization

```python
schema = {
    "name": {"type": "STRING"},
    "age": {"type": "INT64"},
    "active": {"type": "BOOL"}
}

builder = ProtobufMessageBuilder(schema)
message_class, field_mapping = builder.build()

# Only include some fields in the record
record = {
    "name": "Partial Data",
    "active": True
    # "age" is missing
}

serialized = serialize_record(message_class, field_mapping, record)
message = message_class()
message.ParseFromString(serialized)

# Missing fields get default values (0, false, empty string)
print(getattr(message, field_mapping["age"]))  # Output: 0
```

### Extra Fields in Records

```python
schema = {
    "name": {"type": "STRING"},
    "age": {"type": "INT64"}
}

builder = ProtobufMessageBuilder(schema)
message_class, field_mapping = builder.build()

record = {
    "name": "Extra Fields Example",
    "age": 25,
    "extra_field": "This will be ignored",
    "another_extra": 42
}

# Fields not in the schema are ignored during serialization
serialized = serialize_record(message_class, field_mapping, record)
```

## Limitations

- Only supports basic field types (string, int64, double, bool)
- Doesn't support nested messages, enums, or repeated fields yet
- No direct support for protobuf Extensions or OneOf fields

## Requirements

- Python 3.13+
- protobuf 6.30.2+