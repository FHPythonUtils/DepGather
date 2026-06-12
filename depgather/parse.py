from pathlib import Path

from packaging.requirements import Requirement

from depgather.native import NativeInfer
from depgather.pip_cli import PipResolver
from depgather.uv_cli import UvCli


def gather(
	skipDependencies: set[str],
	groups: set[str],
	extras: set[str],
	requirementsPath: Path,
	base_index_url: str = "https://pypi.org",
) -> set[Requirement]:
	"""
	Resolve dependencies from a Python project specification.

	Attempts to resolve dependencies using ``uv`` first and falls back to a
	native parser when ``uv`` is unavailable or resolution fails.

	Args:
		skipDependencies:
			Package names to exclude from the returned dependency set.
			Comparison is case-insensitive and applies to resolved package
			names.

		groups:
			Dependency groups to include during resolution.

			Groups are named collections of dependencies defined by a build
			tool. They are typically used to separate runtime dependencies
			from development, test, documentation, or CI dependencies.

			Examples:
				- "dev"
				- "test"
				- "docs"

			For example, a project may define a ``dev`` group containing
			pytest, mypy, and ruff which should not be installed in
			production environments.

		extras:
			Optional dependency sets to enable during resolution.

			Extras allow a package to expose additional functionality that
			requires extra dependencies. They are commonly specified using
			bracket notation such as::

				requests[socks]
				sqlalchemy[postgresql]

			Enabling an extra causes its additional dependencies to be
			included in the resolved dependency graph.

		requirementsPath:
			Path to a dependency specification file such as:

			- pyproject.toml
			- poetry.toml
			- requirements.txt
			- uv.lock

		base_index_url:
			Package index URL used for dependency resolution.

	Returns:
		A set of resolved package requirements. Returned requirements are
		typically pinned to specific versions when the resolver is able to
		determine them.

	Raises:
		RuntimeError:
			If dependency resolution fails in both the primary and fallback
			resolvers.

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
