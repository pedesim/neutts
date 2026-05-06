from neutts.neutts import NeuTTS, BACKBONE_LANGUAGE_MAP  # noqa

# Also expose the version for convenience when debugging
try:
    from neutts._version import __version__  # noqa
except ImportError:
    __version__ = "unknown"

# Personal note: BACKBONE_LANGUAGE_MAP maps language codes to backbone model names.
# Useful reference when adding support for new languages in downstream projects.
__all__ = ["NeuTTS", "BACKBONE_LANGUAGE_MAP", "__version__"]
