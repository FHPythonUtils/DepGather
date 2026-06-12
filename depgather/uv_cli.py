"""Use uv to get packages from project/ requirements.txt."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import override

import requirements
from packaging.requirements import Requirement

from depgather.interface import DepGatherInterface


class UvCli(DepGatherInterface):
	@staticmethod
	@override
	def gather(
		skipDependencies: set[str],
		groups: set[str],
		extras: set[str],
		requirementsPath: Path,
		base_index_url: str = "https://pypi.org",
	) -> set[Requirement]:
		if not requirementsPath.exists():
			msg = f"Could not find specification of requirements ({requirementsPath})."
			raise RuntimeError(msg)

		requirementsPathName = requirementsPath.as_posix()

		if requirementsPathName.endswith(".lock"):
			msg = "Ironically uv lock are not supported, use `NativeInfer.gather`."
			raise RuntimeError(msg)

		if not requirementsPathName.endswith("pyproject.toml") and requirementsPathName.endswith(
			".toml"
		):
			temp_dir_path = Path(tempfile.mkdtemp())
			destination_file = temp_dir_path / "pyproject.toml"
			shutil.copy(requirementsPath, destination_file)
			requirementsPathName = destination_file.as_posix()

		command = [
			"uv",
			"pip",
			"compile",
			"--index",
			base_index_url,
			requirementsPathName,
		]

		for group in groups:
			command.extend(["--group", group])

		for extra in extras:
			command.extend(["--extra", extra])

		result = subprocess.run(
			command,
			capture_output=True,
			text=True,
			check=False,
		)
		if result.returncode != 0:
			raise RuntimeError(result.stderr, result.stdout)

		# outputs a requirements.txt file
		reqs = requirements.parse(result.stdout)

		skipDependenciesUpper = [x.upper() for x in skipDependencies]

		return {
			Requirement(x.line)
			for x in reqs
			if x.name and x.name.upper() not in skipDependenciesUpper
		}
