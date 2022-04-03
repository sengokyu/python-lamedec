import io
import wave
from lamedec import __version__, decode
from ._sample_mp3 import sample_mp3


def test_version():
    assert __version__ == '0.1.1'


def test_decode():
    # Given
    src = io.BytesIO(bytes(sample_mp3))
    dst = io.BytesIO()

    # When
    decode(src, dst)
    dst.seek(0)
    wav = dst.read(None)

    # Then
    assert len(wav) != 0
    assert wav[0:4] == b'RIFF'
    assert wav[8:12] == b'WAVE'
    assert wav[12:16] == b'fmt '
