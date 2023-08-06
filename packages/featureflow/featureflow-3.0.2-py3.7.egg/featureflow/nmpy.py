import numpy as np
# KLUDGE: numpy recarray dtypes are serialized as "numpy.record", which means
# that the symbol "numpy" must be defined when we call eval().  This is a
# terrible kludge; we should not be using eval() at all.
import numpy
from .extractor import Node
from .feature import Feature
from .util import chunked
from .decoder import Decoder
import struct


class NumpyMetaData(object):
    def __init__(self, dtype=None, shape=None):
        self.dtype = np.uint8 if dtype is None else dtype
        self.shape = shape or ()

        try:
            self.itemsize
        except:
            self.dtype = eval(self.dtype)

    @property
    def itemsize(self):
        return np.dtype(self.dtype).itemsize

    @property
    def size(self):
        return np.product(self.shape)

    @property
    def totalsize(self):
        return self.itemsize * self.size

    def __repr__(self):
        return repr((str(np.dtype(self.dtype)), self.shape))

    def __str__(self):
        return self.__repr__()

    def pack(self):
        s = str(self).encode()
        l = len(s)
        return struct.pack('B{n}s'.format(n=l), l, s)

    @classmethod
    def unpack(cls, flo):
        l = struct.unpack('B', flo.read(1))[0]
        bytes_read = 1 + l
        return cls(*eval(flo.read(l))), bytes_read


class NumpyEncoder(Node):
    content_type = 'application/octet-stream'

    def __init__(self, needs=None):
        super(NumpyEncoder, self).__init__(needs=needs)
        self.metadata = None

    def _prepare_data(self, data):
        return data

    def _prepare_metadata(self, data):
        return NumpyMetaData(dtype=data.dtype, shape=data.shape[1:])

    def _process(self, data):
        data = self._prepare_data(data)
        if not self.metadata:
            self.metadata = self._prepare_metadata(data)
            yield self.metadata.pack()

        encoded = data.tostring()
        yield encoded


class PackedNumpyEncoder(NumpyEncoder):
    def __init__(self, needs=None):
        super(PackedNumpyEncoder, self).__init__(needs=needs)

    def _pack_recarray(self, recarr):
        fields = recarr.dtype.fields

        packed_data = dict()
        new_dtype = []

        for name in list(fields.keys()):
            view = recarr[name].copy().view(np.uint8) \
                .reshape(recarr.shape + (-1,))
            packed_data[name] = view
            new_dtype.append((name, np.uint8, view.shape[1:]))

        packed_recarray = np.recarray(recarr.shape, dtype=new_dtype)

        for name, value in list(packed_data.items()):
            packed_recarray[name] = value
        return packed_recarray

    def _prepare_data(self, data):
        try:
            return np.packbits(data.astype(np.uint8), axis=-1)
        except TypeError:
            return self._pack_recarray(data)


def _np_from_buffer(b, shape, dtype):
    return np.frombuffer(b, dtype=dtype).reshape(tuple(int(x) for x in shape))


class BaseNumpyDecoder(Decoder):
    def __init__(self):
        super(BaseNumpyDecoder, self).__init__()

    def _unpack_metadata(self, flo):
        return NumpyMetaData.unpack(flo)

    def _wrap_array(self, raw, metadata):
        return raw

    def __call__(self, flo):
        metadata, bytes_read = self._unpack_metadata(flo)
        leftovers = flo.read()
        leftover_bytes = len(leftovers)
        first_dim = leftover_bytes / metadata.totalsize
        dim = (first_dim,) + metadata.shape
        raw = _np_from_buffer(leftovers, dim, metadata.dtype)
        return self._wrap_array(raw, metadata)

    def __iter__(self, flo):
        yield self(flo)


class GreedyNumpyDecoder(BaseNumpyDecoder):
    def __init__(self):
        super(GreedyNumpyDecoder, self).__init__()


class StreamingNumpyDecoder(Decoder):
    def __init__(self, n_examples=100):
        super(StreamingNumpyDecoder, self).__init__()
        self.n_examples = n_examples

    def __call__(self, flo):
        return self.__iter__(flo)

    def __iter__(self, flo):
        metadata, _ = NumpyMetaData.unpack(flo)
        example_size = metadata.totalsize
        chunk_size = int(example_size * self.n_examples)
        count = 0

        for chunk in chunked(flo, chunk_size):
            n_examples = len(chunk) // example_size
            yield _np_from_buffer(
                    chunk,
                    (n_examples,) + metadata.shape,
                    metadata.dtype)
            count += 1

        if count == 0:
            yield _np_from_buffer(
                    memoryview(b''),
                    (0,) + metadata.shape,
                    metadata.dtype)


class NumpyFeature(Feature):
    def __init__(
            self,
            extractor,
            needs=None,
            store=False,
            key=None,
            encoder=NumpyEncoder,
            decoder=GreedyNumpyDecoder(),
            **extractor_args):
        super(NumpyFeature, self).__init__(
                extractor,
                needs=needs,
                store=store,
                encoder=encoder,
                decoder=decoder,
                key=key,
                **extractor_args)
