from io import BytesIO
from lamedec.hipdecoder import HipDecoder
from ._sample_mp3 import sample_mp3


def test_create():
    # Given
    mp3 = BytesIO(bytes(sample_mp3))

    # When
    with HipDecoder.create(mp3) as instance:

        # Then
        assert isinstance(instance, HipDecoder)


def test_parse_header():
    # Given
    mp3 = BytesIO(bytes(sample_mp3))

    with HipDecoder.create(mp3) as instance:
        # When
        mp3data = instance.parse_header()

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


def test_decode():
    # Given
    mp3 = BytesIO(bytes(sample_mp3))
    with HipDecoder.create(mp3) as instance:
        count = 0

        # When
        for (l, r) in instance.decode():

            # Then
            # TODO: efficient test
            assert l is not None
            assert r is not None
            count += 1
        assert count == 2
