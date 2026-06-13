import re
from collections.abc import Iterable
from itertools import chain
from pathlib import Path
from urllib.parse import urlparse

NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

SUPPORTED_SUFFIXES = {
	".in",
	".txt",
	".toml",
	".cfg",
	".py",
	".lock",
}


def sanitise(
	requirementsPath: Path,
	skipDependencies: Iterable[str] = (),
	groups: Iterable[str] = (),
	extras: Iterable[str] = (),
	base_index_url: str = "https://pypi.org",
) -> None:
	requirementsPath = requirementsPath.resolve(strict=True)

	if not requirementsPath.exists():
		msg = f"Could not find specification of requirements ({requirementsPath})."
		raise RuntimeError(msg)

	if requirementsPath.suffix not in SUPPORTED_SUFFIXES:
		msg = f"unsupported requirements file type: {requirementsPath}"
		raise RuntimeError(msg)

	for x in chain(skipDependencies, groups, extras):
		if not isinstance(x, str):
			msg = f"expected str, got {type(x).__name__}"
			raise RuntimeError(msg)

		if not NAME_RE.fullmatch(x):
			msg = f"invalid name: {x!r}"
			raise RuntimeError(msg)

	parsed = urlparse(base_index_url)

	if parsed.scheme != "https":
		msg = f"index URL must use HTTPS: {base_index_url!r}"
		raise RuntimeError(msg)

	if not parsed.hostname:
		msg = f"invalid index URL: {base_index_url!r}"
		raise RuntimeError(msg)
