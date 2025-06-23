class UserNotFoundException(Exception):
    pass


class DocumentNotFoundException(Exception):
    pass


class DocumentExtractIsNotSucceded(Exception):
    pass


class DocumentExtractError(Exception):
    pass


class UploadError(Exception):
    """Excepción personalizada para errores de subida a S3."""

    def __init__(self, message: str):
        super().__init__(message)


class LLMOutputNoFoundException(Exception):
    pass


class PageNotFoundException(Exception):
    pass
