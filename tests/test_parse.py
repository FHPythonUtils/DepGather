from pathlib import Path

import pytest

from depgather.parse import ResolverName, gather
from depgather.utils import enable_verbose

THISDIR = Path(__file__).resolve().parent
enable_verbose()


def test_file_not_exists() -> None:
	requirementsPath: Path = THISDIR / "file_does_not_exist.toml"
	with pytest.raises(RuntimeError):
		gather(
			requirementsPath=requirementsPath,
		)


@pytest.mark.parametrize(
	("resolvername"),
	[
		(ResolverName.NATIVE),
		(ResolverName.UV),
		(ResolverName.PIP),
	],
)
def test_lockfiles(resolvername: ResolverName) -> None:
	requirementsPath: Path = THISDIR / "data/example1" / "pylock.toml"
	skipDependencies: set[str] = {"TOSKIP"}

	gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
		preferred_resolver=resolvername,
	)
