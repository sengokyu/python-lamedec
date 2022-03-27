from io import RawIOBase
from lame_ctypes import *


class HipDecoderError(RuntimeError):
    pass


class HipDecoder:
    READING_BUF_SIZE = 4096
    DECODING_BUF_SIZE = 16384

    @staticmethod
    def create(src: RawIOBase):
        this = HipDecoder()
        this.src = src
        this.hip = hip_decode_init()
        return this

    def parse_header(self) -> mp3data_struct:
        """ Return MP3 header """
        self.src.seek(0)

        pcm_buf_l = (c_short * HipDecoder.DECODING_BUF_SIZE)()
        pcm_buf_r = (c_short * HipDecoder.DECODING_BUF_SIZE)()
        mp3data = mp3data_struct()

        (buf_len, buf) = self._read()

        while(buf_len > 0):
            nout = hip_decode1_headers(
                self.hip, buf, buf_len, pcm_buf_l, pcm_buf_r, byref(mp3data)
            )

            if nout == -1:
                raise HipDecoderError()

            if mp3data.header_parsed == 1:
                return mp3data

            (buf_len, buf) = self._read()

    def decode(self):
        """ Return PCM data generator """
        self.src.seek(0)

        (buf_len, buf) = self._read()

        while(buf_len > 0):
            nout = 1

            while(nout > 0):
                pcm_buf_l = (c_short * HipDecoder.DECODING_BUF_SIZE)()
                pcm_buf_r = (c_short * HipDecoder.DECODING_BUF_SIZE)()

                nout = hip_decode1(
                    self.hip, buf, buf_len, pcm_buf_l, pcm_buf_r)

                if nout == -1:
                    raise HipDecoderError()

                yield (pcm_buf_l[:nout], pcm_buf_r[:nout])

                # re-execute hip_docode with empty buf
                # cause decoding is incomplete
                buf_len = 0

            (buf_len, buf) = self._read()

    def _read(self):
        buf = self.src.read(HipDecoder.READING_BUF_SIZE)
        buf_len = len(buf)
        return (buf_len, (ctypes.c_ubyte * buf_len).from_buffer(bytearray(buf)))

    def _close(self) -> None:
        if self.hip is not None:
            hip_decode_exit(self.hip)
            self.hip = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._close
