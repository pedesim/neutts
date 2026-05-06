from neutts.neutts import NeuTTS, BACKBONE_LANGUAGE_MAP  # noqa

# Also expose the version for convenience when debugging
try:
    from neutts._version import __version__  # noqa
except ImportError:
    __version__ = "unknown"
