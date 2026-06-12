import contextlib
from pathlib import Path

from depgather.native import NativeInfer
from tests.utils import assert_eq_packages, assert_in_packages, assert_not_in_packages

THISDIR = Path(__file__).resolve().parent


def test_uvlock() -> None:
	requirementsPath: Path = THISDIR / "data/exampleuv.lock"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)

	assert_eq_packages(
		deps,
		{
			"APPDIRS",
			"ATTRS",
			"BOOLEAN-PY",
			"BOOLEAN.PY",
			"CATTRS",
			"CERTIFI",
			"CHARSET-NORMALIZER",
			"COLORAMA",
			"CONFIGURATOR",
			"COVERAGE",
			"DEPGATHER",
			"EXCEPTIONGROUP",
			"IDNA",
			"IMPORTLIB-METADATA",
			"INICONFIG",
			"LICENSE-EXPRESSION",
			"LOGURU",
			"MARKDOWN",
			"MARKDOWN-IT-PY",
			"MDURL",
			"PACKAGING",
			"PLATFORMDIRS",
			"PLUGGY",
			"PYGMENTS",
			"PYTEST",
			"PYTEST-LOGURU",
			"REQUESTS",
			"REQUESTS-CACHE",
			"REQUIREMENTS-PARSER",
			"RICH",
			"RUFF",
			"SETUPTOOLS",
			"SIX",
			"TOMLI",
			"TYPES-SETUPTOOLS",
			"TYPING-EXTENSIONS",
			"URL-NORMALIZE",
			"URLLIB3",
			"UV",
			"WIN32-SETCTIME",
			"ZIPP",
		},
	)


def test_PEP631() -> None:
	extras: set[str] = {"socks"}
	requirementsPath: Path = THISDIR / "data/pep631_socks.toml"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies=skipDependencies,
		extras=extras,
		groups=set(),
		requirementsPath=requirementsPath,
	)

	assert_eq_packages(
		deps,
		{
			"DOCKERPTY",
			"ATTRS",
			"JSONSCHEMA",
			"PYYAML",
			"PYSOCKS",
			"CERTIFI",
			"DOCKER",
			"TEXTTABLE",
			"DOCOPT",
			"PARAMIKO",
			"IDNA",
			"CACHED-PROPERTY",
			"DISTRO",
			"CHARSET-NORMALIZER",
			"URLLIB3",
			"WEBSOCKET-CLIENT",
			"REQUESTS",
			"PYTHON-DOTENV",
			"CFFI",
			"PYNACL",
			"BCRYPT",
			"SIX",
			"PYCPARSER",
			"CRYPTOGRAPHY",
			"PYRSISTENT",
			"SETUPTOOLS",
			"INVOKE",
		},
	)


def test_requirements() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements.txt"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies, extras=set(), groups=set(), requirementsPath=requirementsPath
	)

	assert_eq_packages(
		deps,
		{
			"NUMPY",
			"ODFPY",
			"OPENPYXL",
			"PANDAS",
			"SIX",
			"DEFUSEDXML",
			"ET-XMLFILE",
			"PYTHON-DATEUTIL",
			"PYTZ",
			"PYXLSB",
			"TZDATA",
			"XLRD",
			"XLSXWRITER",
		},
	)
	assert_in_packages(deps, "OPENPYXL")
	assert_not_in_packages(deps, "XARRAY")
	# xarray is an optional dependency of pandas associated with 'computation' key that is not
	# tracked in test_requirements.txt


def test_requirements_with_hashes() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements_hash.txt"
	skipDependencies = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies, extras=set(), groups=set(), requirementsPath=requirementsPath
	)
	assert_eq_packages(deps, {"PACKAGING"})
	assert_not_in_packages(deps, "TOSKIP")


def test_issue_62() -> None:
	requirementsPath = THISDIR / "data/issue_62.toml"

	deps = NativeInfer.gather(
		skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
	)

	assert_not_in_packages(deps, "PYQT5")

	assert_eq_packages(
		deps,
		{
			"CERTIFI",
			"CHARSET-NORMALIZER",
			"DEPRECATED",
			"EARTHENGINE-API",
			"GOOGLE-API-CORE",
			"GOOGLE-API-PYTHON-CLIENT",
			"GOOGLE-AUTH",
			"GOOGLE-AUTH-HTTPLIB2",
			"GOOGLE-CLOUD-CORE",
			"GOOGLE-CLOUD-STORAGE",
			"GOOGLE-CRC32C",
			"GOOGLE-RESUMABLE-MEDIA",
			"GOOGLEAPIS-COMMON-PROTOS",
			"HTTPLIB2",
			"IDNA",
			"NUMPY",
			"PANDAS",
			"PROTO-PLUS",
			"PROTOBUF",
			"PYARROW",
			"PYASN1",
			"PYASN1-MODULES",
			"PYPARSING",
			"PYTHON-DATEUTIL",
			"PYTZ",
			"REQUESTS",
			"SIX",
			"URITEMPLATE",
			"URLLIB3",
			"WRAPT",
			"CFFI",
			"CRYPTOGRAPHY",
			"PYCPARSER",
		},
	)


def test_issue_81() -> None:
	requirementsPath = THISDIR / "data/issue_81.txt"
	with contextlib.suppress(Exception):
		_deps = NativeInfer.gather(
			skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
		)

	#     RuntimeError:    No solution found when resolving dependencies:
	#        Because nvidia-cudnn-cu12==8.9.2.26 has no wheels with a matching
	#           platform tag and you require nvidia-cudnn-cu12==8.9.2.26, we can
	#           conclude that your requirements are unsatisfiable.


def test_issue_84() -> None:
	requirementsPath = THISDIR / "data/issue_84.txt"

	deps = NativeInfer.gather(
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
			"Packaging",
		},
	)
