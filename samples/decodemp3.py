import io
import logging
import sys
import lamedec

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def main(src, dst):
    with io.FileIO(src, "rb") as src:
        lamedec.decode(src, dst)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: %s <input.mp3> <output.wav>" % (sys.argv[0]))
        sys.exit()
    main(sys.argv[1], sys.argv[2])
