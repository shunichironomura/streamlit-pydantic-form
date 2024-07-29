__all__ = [
    "StreamlitPydanticFormError",
    "NotYetSubmittedError",
    "NoWidgetBuilderFoundError",
]


class StreamlitPydanticFormError(Exception):
    pass


class NotYetSubmittedError(StreamlitPydanticFormError):
    """Raised when trying to access the value of a form that has not been submitted yet."""

    def __init__(self) -> None:
        super().__init__("Form has not been submitted yet")


class NoWidgetBuilderFoundError(StreamlitPydanticFormError):
    """Raised when no widget builder is found in the metadata."""

    def __init__(self) -> None:
        super().__init__("No widget builder found in metadata")
