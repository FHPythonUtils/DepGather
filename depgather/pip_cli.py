from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import override

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from depgather.interface import DepGatherInterface


class PipResolver(DepGatherInterface):
	@override
	@staticmethod
	def gather(
		skipDependencies: set[str],
		groups: set[str],  # ignored
		extras: set[str],  # ignored
		requirementsPath: Path,
		base_index_url: str = "https://pypi.org/simple",
	) -> set[Requirement]:
		if not requirementsPath.exists():
			msg = f"Could not find specification of requirements ({requirementsPath})."
			raise RuntimeError(msg)
		requirementsPathName = requirementsPath.as_posix()

		if requirementsPathName.endswith((".lock", ".toml")):
			msg = "pyproject toml, and lock files are not supported."
			raise RuntimeError(msg)

		skip_names = {x.upper() for x in skipDependencies}

		with tempfile.TemporaryDirectory() as tmp:
			report_path = Path(tmp) / "report.json"

			command = [
				"pip",
				"install",
				"--no-color",
				"--dry-run",
				"--quiet",
				"--report",
				str(report_path),
				"--index-url",
				base_index_url,
				"-r",
				str(requirementsPath),
			]

			result = subprocess.run(
				command,
				capture_output=True,
				text=True,
				check=False,
			)

			if result.returncode != 0:
				raise RuntimeError(result.stderr)

			report = json.loads(report_path.read_text())

			return {
				Requirement(
					f"{canonicalize_name(pkg['metadata']['name'])}=={pkg['metadata']['version']}"
				)
				for pkg in report.get("install", [])
				if pkg["metadata"]["name"].upper() not in skip_names
			}
