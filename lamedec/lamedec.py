from ctypes import *
from io import RawIOBase
from struct import pack
import wave
from lame_ctypes import *
from wave import Wave_write

from .hipdecoder import HipDecoder


def decode(src: RawIOBase, dst):
    """
    Read MP3 from src and output PCM to dst.
    """
    with (
        HipDecoder.create(src) as hip,
        wave.open(dst, "wb") as wav,
    ):
        header = hip.parse_header()

        wav.setnchannels(header.stereo)
        wav.setsampwidth(2)
        wav.setframerate(header.samplerate)

        for (pcm_l, pcm_r) in hip.decode():
            for (l, r) in zip(pcm_l, pcm_r):
                wav.writeframes(pack("<h", l))
                wav.writeframes(pack("<h", r))
