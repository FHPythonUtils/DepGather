"""Use uv to get packages from project/ requirements.txt."""

from __future__ import annotations

from abc import ABC
from pathlib import Path

from packaging.requirements import Requirement


class DepGatherInterface(ABC):
	@staticmethod
	def gather(
		skipDependencies: set[str],
		groups: set[str],
		extras: set[str],
		requirementsPath: Path,
		base_index_url: str = "https://pypi.org",
	) -> set[Requirement]:
		NotImplementedError("This is the interface, call from an implemented ")
