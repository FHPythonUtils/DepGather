from pathlib import Path

import pytest

from depgather.native import NativeInfer
from tests.utils import assert_eq_packages, assert_in_packages, assert_not_in_packages

THISDIR = Path(__file__).resolve().parent


def test_poetrylock() -> None:
	requirementsPath: Path = THISDIR / "data/examplepoetry.lock"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)
	assert len(deps) == 38

	assert_eq_packages(
		deps,
		{
			"APPDIRS",
			"ATTRS",
			"BOOLEAN-PY",
			"CATTRS",
			"CERTIFI",
			"CHARSET-NORMALIZER",
			"COLORAMA",
			"CONFIGURATOR",
			"COVERAGE",
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
			"TOMLI",
			"TYPING-EXTENSIONS",
			"URL-NORMALIZE",
			"URLLIB3",
			"UV",
			"WIN32-SETCTIME",
			"ZIPP",
			"BASEDPYRIGHT",
			"NODEJS-WHEEL-BINARIES",
		},
	)


def test_uvlock() -> None:
	requirementsPath: Path = THISDIR / "data/exampleuv.lock"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)

	assert len(deps) == 40

	assert_eq_packages(
		deps,
		{
			"APPDIRS",
			"ATTRS",
			"BOOLEAN-PY",
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


@pytest.mark.skip("broken :(")
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


@pytest.mark.skip("broken :(")
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


@pytest.mark.skip("broken :(")
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
	deps = NativeInfer.gather(
		skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
	)
	assert_eq_packages(
		deps,
		{
			"AIOHTTP",
			"AIOSIGNAL",
			"ANNOTATED-TYPES",
			"ANYIO",
			"ATLASSIAN-PYTHON-API",
			"ATTRS",
			"BACKOFF",
			"BEAUTIFULSOUP4",
			"BLEACH",
			"BLIS",
			"CATALOGUE",
			"CERTIFI",
			"CFFI",
			"CHARDET",
			"CHARSET-NORMALIZER",
			"CHEVRON",
			"CLICK",
			"CLOUDPATHLIB",
			"CLOUDPICKLE",
			"COLOREDLOGS",
			"CONFECTION",
			"CRYPTOGRAPHY",
			"CUPY-CUDA12X",
			"CYMEM",
			"DATACLASSES-JSON",
			"DATACLASSES-JSON-SPEAKEASY",
			"DATASETS",
			"DEFUSEDXML",
			"DEPRECATED",
			"DILL",
			"DISKCACHE",
			"DISTRO",
			"ELASTIC-TRANSPORT",
			"ELASTICSEARCH",
			"EMOJI",
			"EXECUTING",
			"FAISS-CPU",
			"FASTAPI",
			"FASTEMBED",
			"FASTJSONSCHEMA",
			"FASTRLOCK",
			"FILELOCK",
			"FILETYPE",
			"FLASHRANK",
			"FLATBUFFERS",
			"FROZENLIST",
			"FSSPEC",
			"GREENLET",
			"GRPCIO",
			"GRPCIO-TOOLS",
			"H11",
			"H2",
			"HPACK",
			"HTTPCORE",
			"HTTPTOOLS",
			"HTTPX",
			"HUGGINGFACE-HUB",
			"HUMANFRIENDLY",
			"HYPERFRAME",
			"IDNA",
			"INICONFIG",
			"INTEREGULAR",
			"JINJA2",
			"JMESPATH",
			"JOBLIB",
			"JSONPATCH",
			"JSONPATH-PYTHON",
			"JSONPOINTER",
			"JSONSCHEMA",
			"JSONSCHEMA-SPECIFICATIONS",
			"JUPYTERLAB_PYGMENTS",
			"JUPYTER_CLIENT",
			"JUPYTER_CORE",
			"LANGCHAIN",
			"LANGCHAIN-COMMUNITY",
			"LANGCHAIN-CORE",
			"LANGCHAIN-ELASTICSEARCH",
			"LANGCHAIN-OPENAI",
			"LANGCHAIN-TEXT-SPLITTERS",
			"LANGCODES",
			"LANGDETECT",
			"LANGFUSE",
			"LANGSMITH",
			"LARK",
			"LLVMLITE",
			"LOGURU",
			"LXML",
			"MARKDOWN",
			"MARKDOWNIFY",
			"MARKUPSAFE",
			"MARSHMALLOW",
			"MISTUNE",
			"MPMATH",
			"MSGPACK",
			"MULTIDICT",
			"MULTIPROCESS",
			"MURMURHASH",
			"MYPY-EXTENSIONS",
			"NATSORT",
			"NBCLIENT",
			"NBCONVERT",
			"NBFORMAT",
			"NEST-ASYNCIO",
			"NETWORKX",
			"NINJA",
			"NLTK",
			"NUMBA",
			"NUMPY",
			"NVIDIA-CUBLAS-CU12",
			"NVIDIA-CUDA-CUPTI-CU12",
			"NVIDIA-CUDA-NVRTC-CU12",
			"NVIDIA-CUDA-RUNTIME-CU12",
			"NVIDIA-CUDNN-CU12",
			"NVIDIA-CUFFT-CU12",
			"NVIDIA-CURAND-CU12",
			"NVIDIA-CUSOLVER-CU12",
			"NVIDIA-CUSPARSE-CU12",
			"NVIDIA-NCCL-CU12",
			"NVIDIA-NVJITLINK-CU12",
			"NVIDIA-NVTX-CU12",
			"OAUTHLIB",
			"ONNX",
			"ONNXRUNTIME",
			"OPENAI",
			"ORJSON",
			"OUTLINES",
			"PACKAGING",
			"PANDAS",
			"PANDOCFILTERS",
			"PILLOW",
			"PLATFORMDIRS",
			"PLUGGY",
			"PORTALOCKER",
			"PRESHED",
			"PROMETHEUS_CLIENT",
			"PROTOBUF",
			"PSUTIL",
			"PYARROW",
			"PYARROW-HOTFIX",
			"PYCPARSER",
			"PYDANTIC",
			"PYDANTIC_CORE",
			"PYGMENTS",
			"PYNVML",
			"PYPDF",
			"PYTEST",
			"PYTHON-DATEUTIL",
			"PYTHON-DOTENV",
			"PYTHON-ISO639",
			"PYTHON-MAGIC",
			"PYTHON-MULTIPART",
			"PYTZ",
			"PYYAML",
			"PYZMQ",
			"QDRANT-CLIENT",
			"RANK-BM25",
			"RAPIDFUZZ",
			"RAY",
			"REFERENCING",
			"REGEX",
			"REQUESTS",
			"REQUESTS-OAUTHLIB",
			"RPDS-PY",
			"SAFETENSORS",
			"SCIKIT-LEARN",
			"SCIPY",
			"SENTENCE-TRANSFORMERS",
			"SENTENCEPIECE",
			"SIX",
			"SLACK-LOG-HANDLER",
			"SMART-OPEN",
			"SNIFFIO",
			"SOUPSIEVE",
			"SPACY",
			"SPACY-LEGACY",
			"SPACY-LOGGERS",
			"SQLALCHEMY",
			"SRSLY",
			"STARLETTE",
			"SYMPY",
			"TABULATE",
			"TENACITY",
			"THINC",
			"THREADPOOLCTL",
			"TIKTOKEN",
			"TINYCSS2",
			"TOKENIZERS",
			"TORCH",
			"TORNADO",
			"TQDM",
			"TRAITLETS",
			"TRANSFORMERS",
			"TRITON",
			"TYPER",
			"TYPING-INSPECT",
			"TYPING_EXTENSIONS",
			"TZDATA",
			"UNSTRUCTURED",
			"UNSTRUCTURED-CLIENT",
			"URLLIB3",
			"UVICORN",
			"UVLOOP",
			"WASABI",
			"WATCHFILES",
			"WEASEL",
			"WEBENCODINGS",
			"WEBSOCKETS",
			"WRAPT",
			"XFORMERS",
			"XXHASH",
			"YARL",
		},
	)

	#     RuntimeError:    No solution found when resolving dependencies:
	#        Because nvidia-cudnn-cu12==8.9.2.26 has no wheels with a matching
	#           platform tag and you require nvidia-cudnn-cu12==8.9.2.26, we can
	#           conclude that your requirements are unsatisfiable.


@pytest.mark.skip("broken :(")
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
