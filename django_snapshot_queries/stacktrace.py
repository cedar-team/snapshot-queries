import os
import pkgutil
import traceback
import typing

from .sliceable_list import SliceableList
from .stacktrace_line import StacktraceLine


class StackTrace(SliceableList):
    def __repr__(self) -> str:
        return "[" + ",\n ".join([repr(l) for l in self]) + "]"

    def __str__(self) -> str:
        return "\n".join([str(l) for l in self])

    EXCLUDED_MODULES = (
        "django_snapshot_queries",
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

        for frame in traceback.extract_stack():
            path = frame.filename
            line_no = frame.lineno
            func_name = frame.name
            text = frame.line

            if any(path.startswith(excluded) for excluded in exclude_module_paths):
                continue

            text = "".join(text).strip() if text else ""
            stacktrace.append(
                StacktraceLine(
                    path=frame.filename, line_no=line_no, func=func_name, code=text
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
