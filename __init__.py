from neutts.neutts import NeuTTS, BACKBONE_LANGUAGE_MAP  # noqa

# Also expose the version for convenience when debugging
try:
    from neutts._version import __version__  # noqa
except ImportError:
    __version__ = "unknown"

# Personal note: BACKBONE_LANGUAGE_MAP maps language codes to backbone model names.
# Useful reference when adding support for new languages in downstream projects.
#
# Language codes I've confirmed working in my projects:
#   'en' - English (most stable)
#   'de' - German
#   'fr' - French
# See https://github.com/neuphonic/neutts for the full list.
__all__ = ["NeuTTS", "BACKBONE_LANGUAGE_MAP", "__version__"]
