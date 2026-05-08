"""Utility functions for NeuTTS text processing and audio handling."""

import re
import unicodedata
from typing import Optional

import numpy as np


# Regex patterns for text normalization
_WHITESPACE_RE = re.compile(r'\s+')
_ABBREVIATION_RE = re.compile(r'\b([A-Z]{2,})\b')
_NUMBER_RE = re.compile(r'\b(\d+)\b')

# Common abbreviation expansions
_ABBREVIATIONS = {
    'mr': 'mister',
    'mrs': 'missus',
    'dr': 'doctor',
    'prof': 'professor',
    'sr': 'senior',
    'jr': 'junior',
    'etc': 'etcetera',
    'vs': 'versus',
    'approx': 'approximately',
}


def normalize_text(text: str, language: str = 'en') -> str:
    """Normalize input text for TTS synthesis.

    Performs unicode normalization, whitespace cleanup, and basic
    text normalization suitable for TTS input.

    Args:
        text: Raw input text to normalize.
        language: Language code for language-specific normalization.

    Returns:
        Normalized text string.
    """
    if not text or not text.strip():
        return ''

    # Normalize unicode characters
    text = unicodedata.normalize('NFC', text)

    # Collapse whitespace
    text = _WHITESPACE_RE.sub(' ', text).strip()

    # Expand common abbreviations (English only for now)
    if language == 'en':
        text = _expand_abbreviations(text)

    return text


def _expand_abbreviations(text: str) -> str:
    """Expand common abbreviations in text.

    Args:
        text: Input text with potential abbreviations.

    Returns:
        Text with abbreviations expanded.
    """
    words = text.split()
    expanded = []
    for word in words:
        lower = word.lower().rstrip('.')
        if lower in _ABBREVIATIONS:
            expanded.append(_ABBREVIATIONS[lower])
        else:
            expanded.append(word)
    return ' '.join(expanded)


def audio_float_to_int16(audio: np.ndarray) -> np.ndarray:
    """Convert float32 audio array to int16 PCM format.

    Args:
        audio: Float32 numpy array with values in [-1.0, 1.0].

    Returns:
        Int16 numpy array suitable for WAV file output.
    """
    # Clip to valid range before conversion
    audio = np.clip(audio, -1.0, 1.0)
    return (audio * 32767).astype(np.int16)


def audio_int16_to_float(audio: np.ndarray) -> np.ndarray:
    """Convert int16 PCM audio array to float32 format.

    Args:
        audio: Int16 numpy array.

    Returns:
        Float32 numpy array with values normalized to [-1.0, 1.0].
    """
    return audio.astype(np.float32) / 32767.0


def chunk_text(text: str, max_chars: int = 200) -> list[str]:
    """Split long text into smaller chunks for synthesis.

    Attempts to split on sentence boundaries (punctuation) to
    preserve natural prosody across chunks.

    Args:
        text: Input text to chunk.
        max_chars: Maximum characters per chunk.

    Returns:
        List of text chunks.
    """
    if len(text) <= max_chars:
        return [text]

    # Try to split on sentence-ending punctuation
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text)

    chunks = []
    current_chunk = ''

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk = (current_chunk + ' ' + sentence).strip()
        else:
            if current_chunk:
                chunks.append(current_chunk)
            # Handle sentences longer than max_chars
            if len(sentence) > max_chars:
                chunks.extend(_hard_split(sentence, max_chars))
                current_chunk = ''
            else:
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def _hard_split(text: str, max_chars: int) -> list[str]:
    """Split text at word boundaries when no sentence boundary is available."""
    words = text.split()
    chunks = []
    current = ''
    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current = (current + ' ' + word).strip()
        else:
            if current:
                chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks
