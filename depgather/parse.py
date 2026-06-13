from collections.abc import Iterable
from pathlib import Path

from packaging.requirements import Requirement

from depgather.native import NativeInfer
from depgather.pip_cli import PipResolver
from depgather.uv_cli import UvCli


def gather(
	requirementsPath: Path,
	skipDependencies: Iterable[str] = (),
	groups: Iterable[str] = (),
	extras: Iterable[str] = (),
	base_index_url: str = "https://pypi.org",
) -> set[Requirement]:
	"""
	Resolve dependencies from a Python project specification.

	Attempts to resolve dependencies using uv; pip; and a native resolver if those fail.

	:param Iterable[str] skipDependencies: pkg names to exclude from the returned dependency set.
		Comparison is case-insensitive and applies to resolved package names. , defaults to ()
	:param Iterable[str] groups: Dependency groups to include during resolution. , defaults to ()

		Groups are named collections of dependencies defined by a build
		tool. They are typically used to separate runtime dependencies
		from development, test, documentation, or CI dependencies.
			- "dev"
			- "test"
			- "docs"

	:param Iterable[str] extras: Optional dependency sets. defaults to ()
		Extras allow a package to expose additional functionality that
		requires extra dependencies. They are commonly specified using
		bracket notation such as::

			requests[socks]
			sqlalchemy[postgresql]

			Enabling an extra causes its additional dependencies to be
			included in the resolved dependency graph.
	:param Path requirementsPath: path to a dependency specification file such as:

			- pyproject.toml
			- poetry.toml
			- requirements.txt
			- uv.lock
	:param str base_index_url: Package index URL used for dependency resolution.
		defaults to "https://pypi.org"
	:return set[Requirement]: set of resolved package requirements. Returned requirements are
		typically pinned to specific versions when the resolver is able to
		determine them.

	:raises runtimeError: If dependency resolution fails in all resolvers.
	"""
	# logic to run each depending on conditions, implicit behaviour here

	try:
		return UvCli.gather(
			skipDependencies=skipDependencies,
			groups=groups,
			extras=extras,
			requirementsPath=requirementsPath,
			base_index_url=base_index_url,
		)

	except RuntimeError:
		try:
			return PipResolver.gather(
				skipDependencies=skipDependencies,
				groups=groups,
				extras=extras,
				requirementsPath=requirementsPath,
				base_index_url=base_index_url,
			)
		except RuntimeError:
			# Fallback to the old resolver
			return NativeInfer.gather(
				skipDependencies=skipDependencies,
				groups=groups,
				extras=extras,
				requirementsPath=requirementsPath,
				base_index_url=base_index_url,
			)
