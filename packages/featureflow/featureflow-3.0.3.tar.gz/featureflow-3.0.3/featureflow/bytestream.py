from .extractor import Node
from .decoder import Decoder
from .feature import Feature
from .util import chunked
import requests
from urllib.parse import urlparse
import os
import struct
import zipfile


class ByteStream(Node):
    def __init__(self, chunksize=4096, needs=None):
        super(ByteStream, self).__init__(needs=needs)
        self._chunksize = int(chunksize)

    def _generator(self, stream, content_length):
        if not content_length:
            raise ValueError('content_length should be greater than zero')
        for chunk in chunked(stream, chunksize=self._chunksize):
            yield BytesWithTotalLength(chunk, content_length)

    def _from_http_response(self, resp):
        resp.raise_for_status()
        content_length = int(resp.headers['Content-Length'])
        return self._generator(resp.raw, content_length)

    def _handle_simple_get(self, data):
        parsed = urlparse(data)
        if parsed.scheme and parsed.netloc:
            resp = requests.get(data, stream=True)
            return self._from_http_response(resp)
        else:
            raise ValueError

    def _handle_http_request(self, data):
        s = requests.Session()
        prepped = data.prepare()
        resp = s.send(prepped, stream=True)
        return self._from_http_response(resp)

    def _handle_file_like_object(self, data):
        content_length = data.seek(0, 2)
        data.seek(0)
        return self._generator(data, content_length)

    def _handle_zip_file(self, data):
        return self._generator(data.zipfile, data.file_size)

    def _handle_file(self, data):
        with open(data, 'rb') as f:
            content_length = int(os.path.getsize(data))
            for chunk in self._generator(f, content_length):
                yield chunk

    def _get_strategy(self, data):
        if isinstance(data, ZipWrapper):
            return self._handle_zip_file
        if isinstance(data, requests.Request):
            return self._handle_http_request
        if isinstance(data, str):
            parsed = urlparse(data)
            is_url = parsed.netloc and parsed.scheme
            return self._handle_simple_get if is_url else self._handle_file
        return self._handle_file_like_object

    def _process(self, data):
        try:
            data = data.uri
        except AttributeError:
            pass
        strategy = self._get_strategy(data)
        for chunk in strategy(data):
            yield chunk


def iter_zip(fn):
    with zipfile.ZipFile(fn) as zf:
        for info in zf.filelist:
            if not info.file_size:
                continue
            f = zf.open(info.filename)
            yield ZipWrapper(f, info)


class ZipWrapper(object):
    def __init__(self, zipfile, zipinfo):
        self.zipinfo = zipinfo
        self.zipfile = zipfile

    def __enter__(self):
        self.zipfile.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.zipfile.__exit__(exc_type, exc_val, exc_tb)

    @property
    def file_size(self):
        return self.zipinfo.file_size

    @property
    def filename(self):
        return self.zipinfo.filename


class BytesWithTotalLength(bytes):
    def __new__(cls, s, total_length):
        o = bytes.__new__(cls, s)
        o.total_length = int(total_length)
        return o

    def __radd__(self, other):
        return BytesWithTotalLength(other + bytes(self), self.total_length)


class BytesWithTotalLengthEncoder(Node):
    content_type = 'application/octet-stream'

    def __init__(self, needs=None):
        super(BytesWithTotalLengthEncoder, self).__init__(needs=needs)
        self._metadata_written = False

    def _process(self, data):
        if not self._metadata_written:
            yield struct.pack('I', data.total_length)
            self._metadata_written = True
        yield data


class BytesWithTotalLengthDecoder(Decoder):
    def __init__(self, chunksize=4096):
        super(BytesWithTotalLengthDecoder, self).__init__()
        self._chunksize = chunksize
        self._total_length = None

    def __call__(self, flo):
        return self.__iter__(flo)

    def __iter__(self, flo):
        self._total_length = struct.unpack('I', flo.read(4))[0]
        for chunk in chunked(flo, self._chunksize):
            yield BytesWithTotalLength(chunk, self._total_length)


class ByteStreamFeature(Feature):
    def __init__(
            self,
            extractor,
            needs=None,
            store=False,
            key=None,
            **extractor_args):
        super(ByteStreamFeature, self).__init__(
            extractor,
            needs=needs,
            store=store,
            encoder=BytesWithTotalLengthEncoder,
            decoder=BytesWithTotalLengthDecoder(
                chunksize=extractor_args['chunksize']),
            key=key,
            **extractor_args)
