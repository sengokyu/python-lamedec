# LAME MP3 decoding wrapper

## Usage

```python
import io
import lamedec

src = io.FileIO("src.mp3", "rb")
dst = "dst.mp3"

lamedec.decode(src, dst)
```

