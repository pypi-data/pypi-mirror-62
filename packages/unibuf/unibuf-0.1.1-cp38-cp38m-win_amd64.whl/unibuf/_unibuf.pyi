import typing as t

class UnicodeBuffer(t.SupportsBytes):
    encoding: str
    def __init__(self, string: str) -> None:
        pass
    def __bytes__(self) -> bytes:
        pass
