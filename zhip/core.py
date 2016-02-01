from collections import MutableMapping
import zipfile


class Zhip(MutableMapping):
    """ Mutable Mapping interface to a Zip file

    Keys must be strings, values must be bytes

    Parameters
    ----------
    filename: string
    mode: string, ('r', 'w', 'a'), defaults to 'a'

    Examples
    --------
    >>> z = Zhip('myfile.zip')
    >>> z['x'] = b'123'
    >>> z['x']
    b'123'
    >>> z.flush()  # flush and write metadata to disk
    """
    def __init__(self, filename, mode='a'):
        self.filename = filename
        self.mode = mode
        self._file = None

    @property
    def file(self):
        if not self._file or not self._file.fp:
            self._file = zipfile.ZipFile(self.filename, mode=self.mode)
        return self._file

    def __getitem__(self, key):
        return self.file.read(key)

    def __setitem__(self, key, value):
        if not isinstance(value, bytes):
            raise TypeError("Value must be of type bytes")
        self.file.writestr(key, value)

    def keys(self):
        return (zi.filename for zi in self.file.filelist)

    def values(self):
        return map(self.file.read, self.keys())

    def items(self):
        return ((zi.filename, self.file.read(zi.filename))
                for zi in self.file.filelist)

    def __iter__(self):
        return self.keys()

    def __delitem__(self):
        raise NotImplementedError("Not supported by stdlib zipfile")

    def __len__(self):
        return len(self.file.filelist)

    def flush(self):
        self.file.fp.flush()
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.flush()
