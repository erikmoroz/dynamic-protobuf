class ProtobufMessageBuilderError(Exception):
    pass


class SchemaValidationError(ProtobufMessageBuilderError):
    pass


class FieldCreationError(ProtobufMessageBuilderError):
    pass


class MessageBuildError(ProtobufMessageBuilderError):
    pass
