"""
Define NativeInferState with a static gather method, which takes a requirementsPath.

In addition to a series of optional arguments for gathering requirements/ deps based on the
requirementsPath.
"""

from __future__ import annotations

from collections.abc import Iterable
from configparser import ConfigParser, ParsingError
from importlib import metadata
from importlib.metadata._meta import PackageMetadata
from pathlib import Path
from typing import Any, override

import tomli
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from depgather.interface import DepGatherInterface


class NativeInferState:
	def __init__(self) -> None:
		self.reqs: set[Requirement] = set()
		self.enabledExtras: set[str] = set()

	def resolveWithExtras(
		self,
		skipDependencies: Iterable[str],
	) -> set[Requirement]:
		skip_names: set[str] = {
			canonicalize_name("PYTHON"),
			*(canonicalize_name(d) for d in skipDependencies),
		}
		reqs: set[Requirement] = {req for req in self.reqs if canonicalize_name(req.name) not in skip_names}
		requirementsWithDeps: set[Requirement] = set(reqs)

		for requirement in reqs:
			try:
				pkgMetadata: PackageMetadata = metadata.metadata(requirement.name)
			except metadata.PackageNotFoundError:
				continue

			for dependency_str in pkgMetadata.get_all("Requires-Dist") or []:
				dependency = Requirement(dependency_str)

				# Ignore dependencies that have already been discovered.
				if canonicalize_name(dependency.name) in skip_names:
					continue

				marker = dependency.marker

				if marker is not None:
					# First try enabled extras
					if self.enabledExtras:
						matched = any(
							marker.evaluate({"extra": extra}) for extra in self.enabledExtras
						)

						# If the marker only matches an extra we didn't enable,
						# skip it.
						if not matched and not marker.evaluate({"extra": ""}):
							continue

					elif not marker.evaluate({"extra": ""}):
						continue

				if canonicalize_name(dependency.name) not in (
					canonicalize_name(x.name) for x in requirementsWithDeps
				):
					requirementsWithDeps.add(dependency)

		return requirementsWithDeps

	def gather_infer(
		self,
		groups: Iterable[str],
		extras: Iterable[str],
		requirementsPath: Path,
	) -> bool:
		self.enabledExtras = {e.lower() for e in extras}

		# determine using based on file type
		try:
			pyproject = tomli.loads(requirementsPath.read_text("utf-8"))

			if pyproject.get("project", {}).get("dependencies") is not None:
				return self.gather_pep631_requirements(
					groups=groups,
					extras=extras,
					pyproject=pyproject,
				)
			if pyproject.get("tool", {}).get("poetry", {}).get("dependencies") is not None:
				return self.gather_poetry_requirements(
					groups=groups,
					pyproject=pyproject,
				)

			return self.gather_requirements(
				requirementsPath=requirementsPath,
			)

		except tomli.TOMLDecodeError:
			# Parse setup.cfg
			try:
				cfg: ConfigParser = ConfigParser()
				cfg.read(requirementsPath)
				return self.gather_setupcfg(cfg, groups)
			except ParsingError:
				# Ohterwise its requirements.txt
				return self.gather_requirements(
					requirementsPath=requirementsPath,
				)

	def gather_lock_requirements(
		self, pyproject: dict[str, Any], pakagekey: str = "package"
	) -> bool:
		for pkg in pyproject[pakagekey]:
			if pkg.get("version"):
				self.appendRequirement(f"{pkg['name']}=={pkg['version']}")
			else:
				self.appendRequirement(pkg["name"])

		return True

	def gather_setupcfg(
		self,
		cfg: ConfigParser,
		groups: Iterable[str],
	) -> bool:
		requirements = [
			line.strip()
			for line in cfg.get("options", "install_requires", fallback="").splitlines()
			if line.strip()
		]
		for req in requirements:
			self.appendRequirement(req)
		_groups = {
			key: [line.strip() for line in value.splitlines() if line.strip()]
			for key, value in cfg["options.extras_require"].items()
		}
		for group in groups:
			group_reqs = _groups.get(group)
			if group_reqs:
				for req in group_reqs:
					self.appendRequirement(req)
		return True

	def gather_pep631_requirements(
		self,
		groups: Iterable[str],
		extras: Iterable[str],
		pyproject: dict[str, Any],
	) -> bool:
		try:
			project = pyproject["project"]
			reqLists: list[str] = project["dependencies"]
		except KeyError as error:
			msg = "Could not find specification of requirements (pyproject.toml)."
			raise RuntimeError(msg) from error

		for extra in extras:
			extra_info = project.get("optional-dependencies", {}).get(extra)
			if extra_info:
				reqLists.extend(extra_info)
		for group in groups:
			group_info = pyproject.get("dependency-groups", {}).get(group)
			if group_info:
				reqLists.extend(group_info)

		for req in reqLists:
			self.appendRequirement(req)

		return True

	def gather_poetry_requirements(
		self,
		groups: Iterable[str],
		pyproject: dict[str, Any],
	) -> bool:
		try:
			project = pyproject["tool"]["poetry"]
		except KeyError as error:
			msg = "Could not find specification of requirements (pyproject.toml)."
			raise RuntimeError(msg) from error

		dependency_sections = [project.get("dependencies", {})]

		for group in groups:
			dependency_sections.append(  # noqa: PERF401 # ignore suggestion to use list.extend here
				project.get("group", {}).get(group, {}).get("dependencies", {})
			)

		if "dev" in groups:
			dependency_sections.append(project.get("dev-dependencies", {}))

		for section in dependency_sections:
			for name in section:
				self.appendRequirement(name)

		return True

	def gather_requirements(
		self,
		requirementsPath: Path,
	) -> bool:
		if not requirementsPath.exists():
			msg = f"Could not find specification of requirements ({requirementsPath})."
			raise RuntimeError(msg)

		for _line in requirementsPath.read_text(encoding="utf-8").splitlines():
			line = _line.rstrip("\\").strip()
			if not line or line[0] in {"#", "-"}:
				continue
			self.appendRequirement(line.split("#")[0])

		return True

	def appendRequirement(self, req: str) -> None:
		requirement = Requirement(req)
		if canonicalize_name(requirement.name) not in (
			canonicalize_name(x.name) for x in self.reqs
		):
			self.reqs.add(requirement)


class NativeInfer(DepGatherInterface):
	@staticmethod
	@override
	def gather(
		requirementsPath: Path,
		skipDependencies: Iterable[str] = (),
		groups: Iterable[str] = (),
		extras: Iterable[str] = (),
		base_index_url: str = "https://pypi.org",
	) -> set[Requirement]:
		"""
		Static getter method, used to gather requirements/ deps based on the requirementsPath.

		:param Path requirementsPath: path to some requirements file. e.g. requirements.txt;
			pyproject.toml; uv.lock etc
		:param Iterable[str] skipDependencies: optional dependencies to ignore/ skip. for example
			explicitly choosing to ignore the project. e.g. {'depgather'}, defaults to ()
		:param Iterable[str] groups: dependency groups to include during resolution.
			e.g. {'dev', 'test', 'docs'}, defaults to ()
		:param Iterable[str] extras: dependency sets to enable during resolution. e.g. for depgather
			{"uv", "pip"}, defaults to ()
		:param str base_index_url: pypi index to reach out to to resolve deps,
			defaults to "https://pypi.org"
		:raises RuntimeError: in the event that NativeInfer fails to parse the requirementsPath, or
			encounters some other RuntimeError

		:return set[Requirement]: set of requirements/ deps based on the requirementsPath and
			optional args
		"""
		state: NativeInferState = NativeInferState()

		# when using a lockfile then gatherinfer only

		try:
			pyproject = tomli.loads(requirementsPath.read_text("utf-8"))
			if pyproject.get("package") is not None and state.gather_lock_requirements(
				pyproject=pyproject,
			):
				return state.reqs
			if pyproject.get("packages") is not None and state.gather_lock_requirements(
				pyproject=pyproject, pakagekey="packages"
			):
				return state.reqs

		except tomli.TOMLDecodeError:
			pass

		if not state.gather_infer(groups, extras, requirementsPath):
			msg = f"Unable to find requirements for ({requirementsPath})."
			raise RuntimeError(msg)
		return state.resolveWithExtras(skipDependencies)
