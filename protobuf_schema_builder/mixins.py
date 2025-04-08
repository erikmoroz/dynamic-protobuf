from .exceptions import SchemaValidationError


class SchemaValidatorMixin:
    def validate_schema(self, schema):
        self._validate_schema_not_empty(schema)
        self._validate_field_definitions(schema)

    def _validate_schema_not_empty(self, schema):
        if not schema:
            raise SchemaValidationError("Schema cannot be empty")

    def _validate_field_definitions(self, schema):
        for field_name, field_def in schema.items():
            self._validate_field_type(field_name, field_def)

    def _validate_field_type(self, field_name, field_def):
        if "type" not in field_def:
            raise SchemaValidationError(f"Field '{field_name}' is missing required 'type' attribute")

        field_type = field_def["type"]
        if field_type not in self.supported_field_types:
            supported_types_str = ", ".join(self.supported_field_types)
            raise SchemaValidationError(
                f"Field '{field_name}' has unsupported type: {field_type}. Supported types are: {supported_types_str}"
            )
