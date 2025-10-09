
class CustomExceptionHandler(Exception):
    def __init__(self, name: str, message: str, status_code: int, extra: dict | None = None):
        self.name = name
        self.message = message
        self.status_code = status_code
        self.extra = extra

    @property
    def content(self):
        return {
            "message": self.message,
            "name": self.name,
            "extra": self.extra if self.extra is not None else {}
        }