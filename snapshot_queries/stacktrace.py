import attr
import os
import pkgutil
import traceback
import typing

from .sliceable_list import SliceableList


class StackTrace(SliceableList):
    def __repr__(self) -> str:
        return "[" + ",\n ".join([repr(line) for line in self]) + "]"

    def __str__(self) -> str:
        return "\n".join([str(line) for line in self])

    EXCLUDED_MODULES = (
        "snapshot_queries",
        "debug_toolbar",
        "django.core.management",
        "django.core.handlers",
        "django.core.servers",
        "django.db",
        "django.utils.decorators",
        "django.utils.deprecation",
        "django.utils.functional",
        "IPython",
        "threading",
    )

    @classmethod
    def load(
        cls, exclude_modules: typing.Optional[typing.Iterable] = None
    ) -> "StackTrace":
        """Return current stacktrace minus lines in EXCLUDED_MODULES."""
        exclude_modules = exclude_modules or cls.EXCLUDED_MODULES
        exclude_module_paths = []
        for m in exclude_modules:
            path = cls._get_module_path(m)
            if path:
                exclude_module_paths.append(path)

        stacktrace = cls()

        # Iterate through each line in the stacktrace.
        # Skip lines of code that are from excluded modules.
        for frame in traceback.extract_stack():
            if any(
                frame.filename.startswith(excluded) for excluded in exclude_module_paths
            ):
                continue

            stacktrace.append(
                StacktraceLine(
                    path=frame.filename,
                    line_no=str(frame.lineno),
                    func=frame.name,
                    code="".join(frame.line or []).strip(),
                )
            )

        return stacktrace

    @staticmethod
    def _get_module_path(module_name) -> typing.Optional[str]:
        try:
            print(module_name)
            package = pkgutil.get_loader(module_name)
        except ImportError:
            return None
        if not package:
            return None

        source_path = package.path
        if source_path.endswith("__init__.py"):
            source_path = os.path.dirname(source_path)
        return os.path.realpath(source_path)


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
