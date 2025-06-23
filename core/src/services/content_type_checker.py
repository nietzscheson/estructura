class ContentTypeChecker:
    def __init__(self, content_type: list[str]) -> None:
        self.content_type = content_type

    def __call__(self, content_type: str) -> bool:
        if content_type in self.content_type:
            return True
        return False
