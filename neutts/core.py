"""Core TTS engine module for neutts.

Provides the main interface for text-to-speech synthesis,
wrapping the underlying C++ engine exposed via CMake/pybind11.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


class NeuTTS:
    """Main text-to-speech synthesis engine.

    This class provides a high-level Python interface to the neutts
    synthesis engine, handling model loading, text processing, and
    audio generation.

    Args:
        model_path: Path to the TTS model directory or file.
        sample_rate: Target audio sample rate in Hz. Defaults to 22050.
        device: Compute device to use ('cpu' or 'cuda'). Defaults to 'cpu'.
        verbose: Enable verbose logging. Defaults to False.

    Example:
        >>> tts = NeuTTS(model_path="/path/to/model")
        >>> audio = tts.synthesize("Hello, world!")
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        sample_rate: int = 22050,
        device: str = "cpu",
        verbose: bool = False,
    ) -> None:
        self.model_path = Path(model_path)
        self.sample_rate = sample_rate
        self.device = device
        self.verbose = verbose

        if verbose:
            logging.basicConfig(level=logging.DEBUG)

        self._engine = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the TTS model from disk.

        Raises:
            FileNotFoundError: If the model path does not exist.
            RuntimeError: If the model fails to load.
        """
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model path not found: {self.model_path}"
            )

        logger.debug("Loading model from %s", self.model_path)

        try:
            # Attempt to import the compiled C++ extension
            from neutts import _neutts_core as _core  # noqa: F401
            self._engine = _core.Engine(str(self.model_path), self.device)
            logger.info("Model loaded successfully from %s", self.model_path)
        except ImportError:
            logger.warning(
                "Native extension not available; falling back to Python engine."
            )
            self._engine = None

    def synthesize(
        self,
        text: str,
        speaker_id: Optional[int] = None,
        speed: float = 1.0,
        pitch: float = 1.0,
    ) -> bytes:
        """Synthesize speech from the given text.

        Args:
            text: Input text to synthesize.
            speaker_id: Optional speaker identity index for multi-speaker models.
            speed: Speech rate multiplier. 1.0 is normal speed.
            pitch: Pitch multiplier. 1.0 is normal pitch.

        Returns:
            Raw PCM audio bytes at the configured sample rate.

        Raises:
            ValueError: If text is empty or parameters are out of range.
            RuntimeError: If synthesis fails.
        """
        if not text or not text.strip():
            raise ValueError("Input text must not be empty.")

        if speed <= 0:
            raise ValueError(f"Speed must be positive, got {speed}.")

        if pitch <= 0:
            raise ValueError(f"Pitch must be positive, got {pitch}.")

        logger.debug("Synthesizing: %r (speaker=%s, speed=%s, pitch=%s)",
                     text, speaker_id, speed, pitch)

        if self._engine is None:
            raise RuntimeError(
                "TTS engine is not initialised. Ensure the native extension "
                "is built or a valid model is loaded."
            )

        audio: bytes = self._engine.synthesize(
            text,
            speaker_id=speaker_id if speaker_id is not None else 0,
            speed=speed,
            pitch=pitch,
        )
        return audio

    @property
    def is_ready(self) -> bool:
        """Return True if the engine is loaded and ready for synthesis."""
        return self._engine is not None

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"NeuTTS(model_path={str(self.model_path)!r}, "
            f"sample_rate={self.sample_rate}, device={self.device!r})"
        )
