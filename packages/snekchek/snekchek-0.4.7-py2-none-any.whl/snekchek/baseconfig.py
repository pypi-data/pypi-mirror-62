"""Base config for entry points."""

# __future__ imports
from __future__ import unicode_literals

# Stdlib
import os

# External Libraries
import configobj

__all__ = ("config", )

config = configobj.ConfigObj(  # pylint: disable=invalid-name
    {
        "all": {
            "linters": [
                "flake8",
                "pylint",
                "yapf",
                "isort",
                "pyroma",
                "safety",
                "dodgy",
                "vulture",
                "pytest",
                "pypi",
            ]
        },
        "pypi": {
            "TWINE_USERNAME": os.environ.get("TWINE_USERNAME", "abc"),
            "TWINE_PASSWORD": os.environ.get("TWINE_PASSWORD", "abc"),
            "sign": False,
            "TWINE_REPOSITORY": "pypi",
            "quiet": False,
        },
        "flake8": {
            "max-line-length": 79,
            "exclude": ["build", "dist"],
            "ignore": [],
            "quiet": False,
        },
        "pylint": {"quiet": False},
        "yapf": {"inplace": True, "quiet": False},
        "isort": {
            "line_length": 79,
            "multi_line_output": True,
            "inplace": True,
            "indent": "    ",
            "sections": "FUTURE,STDLIB,THIRDPARTY,FIRSTPARTY,LOCALFOLDER".split(
                ","
            ),
            "quiet": False,
        },
        "bandit": {"quiet": False},
        "style": {"inplace": True, "quiet": False},
        "pyroma": {"quiet": False},
        "vulture": {
            "min-confidence": 60,
            "verbose": False,
            "exclude": [],
            "sort-by-size": False,
            "quiet": False,
        },
        "safety": {
            "quiet": False,
            "ignore": [],
            "pyup_key": "",
            "db_path": "",
        },
        "dodgy": {"quiet": False, "ignore_paths": []},
        "pytest": {"quiet": False, "testpaths": "tests"},
        "unittest": {"quiet": False, "testpaths": "tests"},
        "black": {
            "quiet": False,
            "line_length": 79,
            "exclude": "",
            "versions": [
                "PY" + version
                for version in ("27", "33", "34", "35", "36", "37", "38")
            ],
        },
    }
)
