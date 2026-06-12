from pathlib import Path

import pytest

from depgather.pip_cli import PipResolver
from tests.utils import assert_eq_packages, assert_not_in_packages

THISDIR = Path(__file__).resolve().parent


def test_requirements() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements.txt"
	skipDependencies: set[str] = {"TOSKIP"}

	# note: This error originates from a subprocess, and is likely not a problem with pip.
	# ERROR: Failed to build 'pandas' when getting requirements to build wheel
	with pytest.raises(RuntimeError, match="error: subprocess-exited-with-error"):
		deps = PipResolver.gather(
			skipDependencies, extras=set(), groups=set(), requirementsPath=requirementsPath
		)


def test_requirements_with_hashes() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements_hash.txt"
	skipDependencies = {"TOSKIP"}

	deps = PipResolver.gather(
		skipDependencies, extras=set(), groups=set(), requirementsPath=requirementsPath
	)
	assert_eq_packages(deps, {"PACKAGING"})
	assert_not_in_packages(deps, "TOSKIP")


def test_issue_84() -> None:
	requirementsPath = THISDIR / "data/issue_84.txt"

	deps = PipResolver.gather(
		skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
	)

	assert_eq_packages(
		deps,
		{
			"AMQP",
			"BILLIARD",
			"CELERY",
			"CLICK",
			"CLICK-DIDYOUMEAN",
			"CLICK-PLUGINS",
			"CLICK-REPL",
			"KOMBU",
			"PROMPT-TOOLKIT",
			"PYTZ",
			"TZDATA",
			"VINE",
			"WCWIDTH",
			# "Packaging",
		},
	)
