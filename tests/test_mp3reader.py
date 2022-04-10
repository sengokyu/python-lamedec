from io import BytesIO
from lamedec.mp3reader import Mp3Reader
from ._sample_mp3 import sample_mp3


def test_open():
    # Given
    mp3 = BytesIO(bytes(sample_mp3))

    # When
    with Mp3Reader.open(mp3) as instance:

        # Then
        assert isinstance(instance, Mp3Reader)


def test_header():
    # Given
    mp3 = BytesIO(bytes(sample_mp3))

    with Mp3Reader.open(mp3) as instance:
        # When
        mp3data = instance.header()

    # Then
    assert mp3data.stereo == 2
    assert mp3data.samplerate == 16000
    assert mp3data.bitrate == 48
    assert mp3data.mode == 1
    assert mp3data.mode_ext == 2
    assert mp3data.framesize == 576
    assert mp3data.nsamp == 17280
    assert mp3data.totalframes == 30
    assert mp3data.framenum == 0


def test_all_frames():
    # Given
    mp3 = BytesIO(bytes(sample_mp3))
    count = 0

    with Mp3Reader.open(mp3) as instance:
        _ = instance.header()

        # When
        for (l, r) in instance.all_frames():
            assert l is not None
            assert r is not None
            count += 1
    assert count == 30
