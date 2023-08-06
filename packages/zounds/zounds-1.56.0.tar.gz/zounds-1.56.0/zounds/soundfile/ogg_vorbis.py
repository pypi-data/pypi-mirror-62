
from featureflow import IdentityEncoder, Node, Decoder, Feature
from .audiostream import MemoryBuffer
from zounds.timeseries import audio_sample_rate, TimeSlice, AudioSamples
from soundfile import *
from .byte_depth import chunk_size_samples
from zounds.timeseries import Picoseconds, Seconds


class OggVorbisWrapper(object):
    def __init__(self, flo):
        self._flo = flo
        self._sf = SoundFile(self._flo)
        self._freq = Picoseconds(int(1e12)) / self._sf.samplerate

    @property
    def samplerate(self):
        return self._sf.samplerate

    @property
    def channels(self):
        return self._sf.channels

    @property
    def duration_seconds(self):
        return len(self._sf) / self.samplerate

    def _n_samples(self, duration):
        if duration is None:
            return -1
        return int(duration / self._freq)

    def __getitem__(self, timeslice):
        sr = audio_sample_rate(self.samplerate)

        if timeslice == slice(None):
            self._sf.seek(0)
            return AudioSamples(self._sf.read(len(self._sf)), sr)

        start_sample = int(timeslice.start / self._freq)
        n_samples = self._n_samples(timeslice.duration)

        self._sf.seek(start_sample)
        return AudioSamples(self._sf.read(n_samples), sr)

    def iter_chunks(self):
        chunksize = Seconds(1)
        ts = TimeSlice(chunksize)
        sl = self[ts]
        yield sl
        while len(sl) >= self._n_samples(chunksize):
            ts += chunksize
            sl = self[ts]
            yield sl


class OggVorbisEncoder(IdentityEncoder):
    content_type = 'audio/ogg'


class OggVorbisDecoder(Decoder):
    def __init__(self):
        super(OggVorbisDecoder, self).__init__()

    def __call__(self, flo):
        return OggVorbisWrapper(flo)

    def __iter__(self, flo):
        yield self(flo)


class OggVorbisFeature(Feature):
    def __init__(
            self,
            extractor,
            needs=None,
            store=False,
            key=None,
            **extractor_args):
        super(OggVorbisFeature, self).__init__( \
                extractor,
                needs=needs,
                store=store,
                encoder=OggVorbisEncoder,
                decoder=OggVorbisDecoder(),
                key=key,
                **extractor_args)


class OggVorbis(Node):
    """
    `OggVorbis` expects to process a stream of raw bytes (e.g. one produced by
    :class:`featureflow.ByteStream`) and produces a new byte stream where the
    original audio samples are `ogg-vorbis <https://xiph.org/vorbis/>`_ encoded

    Args:
        needs (Feature): a feature that produces a byte stream
            (e.g. :class:`featureflow.Bytestream`)

    Here's how you'd typically see :class:`OggVorbis` used in a processing
    graph.

    .. code:: python

        import featureflow as ff
        import zounds


        chunksize = zounds.ChunkSizeBytes(
            samplerate=zounds.SR44100(),
            duration=zounds.Seconds(30),
            bit_depth=16,
            channels=2)

        @zounds.simple_in_memory_settings
        class Document(ff.BaseModel):
            meta = ff.JSONFeature(
                zounds.MetaData,
                store=True,
                encoder=zounds.AudioMetaDataEncoder)

            raw = ff.ByteStreamFeature(
                ff.ByteStream,
                chunksize=chunksize,
                needs=meta,
                store=False)

            ogg = zounds.OggVorbisFeature(
                zounds.OggVorbis,
                needs=raw,
                store=True)


        synth = zounds.NoiseSynthesizer(zounds.SR11025())
        samples = synth.synthesize(zounds.Seconds(10))
        raw_bytes = samples.encode()
        _id = Document.process(meta=raw_bytes)
        doc = Document(_id)
        # fetch and decode a section of audio
        ts = zounds.TimeSlice(zounds.Seconds(2))
        print doc.ogg[ts].shape  # 22050
    """
    def __init__(self, needs=None):
        super(OggVorbis, self).__init__(needs=needs)
        self._in_buf = None
        self._in_sf = None
        self._out_buf = None
        self._out_sf = None
        self._already_ogg = None
        self._chunk_size_samples = None

    def _enqueue(self, data, pusher):
        if self._in_buf is None:
            self._in_buf = MemoryBuffer(data.total_length)
            self._in_buf.write(data)
            self._in_sf = SoundFile(self._in_buf)
            self._already_ogg = 'OGG' in self._in_sf.format

        if not self._chunk_size_samples:
            self._chunk_size_samples = chunk_size_samples(self._in_sf, data)

        if self._already_ogg:
            super(OggVorbis, self)._enqueue(data, pusher)
            return

        if self._out_buf is None:
            self._out_buf = MemoryBuffer(data.total_length)
            self._out_sf = SoundFile(
                    self._out_buf,
                    format='OGG',
                    subtype='VORBIS',
                    mode='w',
                    samplerate=self._in_sf.samplerate,
                    channels=self._in_sf.channels)
        else:
            self._in_buf.write(data)

    def _dequeue(self):

        if self._already_ogg:
            return super(OggVorbis, self)._dequeue()

        samples = self._in_sf.read(self._chunk_size_samples)
        factor = 20
        while samples.size:
            # KLUDGE: Trying to write too-large chunks to an ogg file seems to
            # cause a segfault in libsndfile
            for i in range(0, len(samples), self._in_sf.samplerate * factor):
                self._out_sf.write(
                        samples[i: i + self._in_sf.samplerate * factor])
            samples = self._in_sf.read(self._chunk_size_samples)
        return self._out_buf

    def _process_other(self, data):
        if self._finalized:
            self._out_sf.close()
        o = data.read(count=-1)
        return o

    def _process_ogg(self, data):
        return data

    def _process(self, data):
        if self._already_ogg:
            yield self._process_ogg(data)
        else:
            yield self._process_other(data)
