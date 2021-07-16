import attr


@attr.s(auto_attribs=True)
class StacktraceLine:
    path: str
    line_no: str
    func: str
    code: str

    def __str__(self) -> str:
        return f"{self.location()}\n    {self.code}"

    @classmethod
    def null(cls) -> "StacktraceLine":
        """Return the equivalent of an empty StacktraceLine."""
        return cls(path="", line_no="", func="", code="")

    def location(self) -> str:
        return f"{self.path}:{self.line_no} in {self.func}"
