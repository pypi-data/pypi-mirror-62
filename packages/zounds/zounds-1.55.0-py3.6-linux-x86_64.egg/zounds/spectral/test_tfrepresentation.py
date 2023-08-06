
import numpy as np
import unittest2
from .frequencyscale import LinearScale, FrequencyBand, Hertz
from .weighting import AWeighting
from zounds.timeseries import Seconds, TimeDimension, TimeSlice, SR11025
from zounds.spectral import FrequencyDimension, GeometricScale
from zounds.core import ArrayWithUnits, IdentityDimension


class TimeFrequencyRepresentationTests(unittest2.TestCase):

    def test_can_slice_frequency_dim_with_end_hz(self):
        scale = LinearScale(FrequencyBand(0, 100), 10)
        arr = ArrayWithUnits(
            np.zeros((13, 10)),
            [IdentityDimension(), FrequencyDimension(scale)])
        sliced = arr[:, :Hertz(50)]
        self.assertEqual((13, 5), sliced.shape)
        self.assertEqual(
            FrequencyDimension(LinearScale(FrequencyBand(0, 50), 5)),
            sliced.dimensions[-1])

    def test_can_slice_frequency_dim_with_start_hz(self):
        scale = LinearScale(FrequencyBand(0, 100), 10)
        arr = ArrayWithUnits(
            np.zeros((13, 10)),
            [IdentityDimension(), FrequencyDimension(scale)])
        sliced = arr[:, Hertz(50):]
        self.assertEqual((13, 6), sliced.shape)

    def test_can_slice_frequency_dim_with_start_and_end_hz(self):
        scale = LinearScale(FrequencyBand(0, 100), 10)
        arr = ArrayWithUnits(
            np.zeros((13, 10)),
            [IdentityDimension(), FrequencyDimension(scale)])
        sliced = arr[:, Hertz(20):Hertz(80)]
        self.assertEqual((13, 7), sliced.shape)

    def test_can_slice_frequency_dim_with_negative_start_hz(self):
        scale = LinearScale(FrequencyBand(0, 100), 10)
        arr = ArrayWithUnits(
            np.zeros((13, 10)),
            [IdentityDimension(), FrequencyDimension(scale)])
        sliced = arr[:, -Hertz(20):]
        self.assertEqual((13, 3), sliced.shape)

    def test_can_slice_frequency_dim_with_negative_stop_hz(self):
        scale = LinearScale(FrequencyBand(0, 100), 10)
        arr = ArrayWithUnits(
            np.zeros((13, 10)),
            [IdentityDimension(), FrequencyDimension(scale)])
        sliced = arr[:, :-Hertz(20)]
        self.assertEqual((13, 8), sliced.shape)
        self.assertEqual(
            FrequencyDimension(LinearScale(FrequencyBand(0, 80), 8)),
            sliced.dimensions[-1])

    def test_sliding_window_has_correct_dimensions(self):
        arr = np.random.randint(0, 255, (11025 * 2)).astype(np.int64)
        sr = SR11025()
        awu = ArrayWithUnits(arr, [TimeDimension(*sr)])
        ws = TimeSlice(duration=sr.frequency * 8192)
        ss = TimeSlice(duration=sr.frequency * 4096)
        l, x = awu.sliding_window_with_leftovers(ws, ss)
        self.assertEqual(8192, x.shape[1])

    def test_can_transpose(self):
        sr = SR11025()
        hl = sr.half_lapped()
        scale = GeometricScale(20, sr.nyquist, 0.175, 64)
        td = TimeDimension(frequency=hl.frequency, duration=hl.duration)
        fd = FrequencyDimension(scale)

        arr = ArrayWithUnits(np.zeros((99, 64)), [td, fd])
        transposed = arr.T
        self.assertEqual((64, 99), transposed.shape)
        self.assertEqual(arr.dimensions[0], transposed.dimensions[1])
        self.assertEqual(arr.dimensions[1], transposed.dimensions[0])

    @unittest2.skip('this requires that frequency scales be reversible')
    def test_can_rotate_90_degrees(self):
        sr = SR11025()
        hl = sr.half_lapped()
        scale = GeometricScale(20, sr.nyquist, 0.175, 64)
        td = TimeDimension(frequency=hl.frequency, duration=hl.duration)
        fd = FrequencyDimension(scale)

        arr = ArrayWithUnits(np.zeros((99, 64)), [td, fd])
        rotated = np.rot90(arr)
        self.assertEqual((64, 99), rotated.shape)
        self.assertEqual(arr.dimensions[0], rotated.dimensions[1])
        self.assertEqual(arr.dimensions[1], rotated.dimensions[0])

    def test_can_apply_sliding_window(self):
        sr = SR11025()
        hl = sr.half_lapped()
        scale = GeometricScale(20, sr.nyquist, 0.175, 64)
        td = TimeDimension(frequency=hl.frequency, duration=hl.duration)
        fd = FrequencyDimension(scale)

        arr = ArrayWithUnits(np.zeros((99, 64)), [td, fd])

        ts = TimeSlice(duration=hl.frequency * 64)
        fs = FrequencyBand(0, sr.nyquist)

        windowed = arr.sliding_window((ts, fs))
        self.assertEqual((1, 64, 64), windowed.shape)

    def test_can_iterate_over_time_frequency_representation(self):
        tf = ArrayWithUnits(
            np.ones((10, 10)),
            dimensions=[
                TimeDimension(Seconds(1), Seconds(1)),
                FrequencyDimension(LinearScale(FrequencyBand(0, 1000), 10))
            ])
        rows = [row for row in tf]
        self.assertEqual(10, len(rows))
        for row in rows:
            self.assertIsInstance(row, ArrayWithUnits)
            self.assertIsInstance(row.dimensions[0], FrequencyDimension)
            self.assertEqual((10,), row.shape)

    def test_can_iterate_over_timeseries(self):
        tf = ArrayWithUnits(
            np.ones((10, 10)),
            dimensions=[
                TimeDimension(Seconds(1), Seconds(1)),
                IdentityDimension()
            ])
        rows = [row for row in tf]
        self.assertEqual(10, len(rows))
        for row in rows:
            self.assertIsInstance(row, ArrayWithUnits)
            self.assertIsInstance(row.dimensions[0], IdentityDimension)
            self.assertEqual((10,), row.shape)

    def test_can_iterate_after_packbits(self):
        tf = ArrayWithUnits(
            np.random.binomial(1, 0.5, (10, 256)).astype(np.uint8),
            dimensions=[
                TimeDimension(Seconds(1), Seconds(1)),
                IdentityDimension()
            ])
        tf = tf.packbits(axis=1)
        self.assertIsInstance(tf, ArrayWithUnits)
        self.assertEqual((10, 32), tf.shape)
        self.assertIsInstance(tf.dimensions[0], TimeDimension)
        self.assertIsInstance(tf.dimensions[1], IdentityDimension)
        rows = [row for row in tf]
        self.assertEqual(10, len(rows))
        for row in rows:
            self.assertIsInstance(row, ArrayWithUnits)
            self.assertIsInstance(row.dimensions[0], IdentityDimension)
            self.assertEqual((32,), row.shape)

    def test_can_use_tuple_indices_for_first_dimension(self):
        tf = ArrayWithUnits(
            np.ones((10, 10)),
            dimensions=[
                TimeDimension(Seconds(1), Seconds(1)),
                FrequencyDimension(LinearScale(FrequencyBand(0, 1000), 10))
            ])
        subset = tf[tuple([2, 4, 6]), ...]
        self.assertEqual((3, 10), subset.shape)
        self.assertIsInstance(subset, ArrayWithUnits)
        self.assertIsInstance(subset.dimensions[0], TimeDimension)
        self.assertIsInstance(subset.dimensions[1], FrequencyDimension)

    def test_can_use_tuple_indices_for_first_dimension_id_dim_first(self):
        tf = ArrayWithUnits(
            np.ones((10, 9, 8)),
            dimensions=[
                IdentityDimension(),
                TimeDimension(Seconds(1), Seconds(1)),
                FrequencyDimension(LinearScale(FrequencyBand(0, 1000), 8))
            ])
        subset = tf[tuple([2, 4, 6]), ...]
        self.assertEqual((3, 9, 8), subset.shape)
        self.assertIsInstance(subset, ArrayWithUnits)
        self.assertIsInstance(subset.dimensions[0], IdentityDimension)
        self.assertIsInstance(subset.dimensions[1], TimeDimension)
        self.assertIsInstance(subset.dimensions[2], FrequencyDimension)

    def test_can_access_int_index_and_frequency_band(self):
        tf = ArrayWithUnits(
            np.ones((10, 10)),
            dimensions=[
                TimeDimension(Seconds(1), Seconds(1)),
                FrequencyDimension(LinearScale(FrequencyBand(0, 1000), 10))
            ])
        sliced = tf[0, FrequencyBand(201, 400)]
        self.assertEqual((2,), sliced.shape)
        self.assertIsInstance(sliced.dimensions[0], FrequencyDimension)

    def test_can_access_time_slice_and_int_index(self):
        tf = ArrayWithUnits(
            np.ones((10, 10)),
            dimensions=[
                TimeDimension(Seconds(1), Seconds(1)),
                FrequencyDimension(LinearScale(FrequencyBand(0, 1000), 10))
            ])
        sliced = tf[TimeSlice(start=Seconds(1), duration=Seconds(2)), 0]
        self.assertEqual((2,), sliced.shape)
        self.assertIsInstance(sliced.dimensions[0], TimeDimension)

    def test_can_add_axis_at_end(self):
        _id = IdentityDimension()
        td = TimeDimension(Seconds(1), Seconds(1))
        fd = FrequencyDimension(LinearScale(FrequencyBand(20, 22050), 100))
        tf = ArrayWithUnits(np.ones((3, 30, 100)), [_id, td, fd])
        tf2 = tf[..., None]
        self.assertEqual(4, tf2.ndim)
        self.assertIsInstance(tf2.dimensions[0], IdentityDimension)
        self.assertIsInstance(tf2.dimensions[1], TimeDimension)
        self.assertIsInstance(tf2.dimensions[2], FrequencyDimension)
        self.assertIsInstance(tf2.dimensions[3], IdentityDimension)

    def test_sum_along_frequency_axis(self):
        td = TimeDimension(Seconds(1), Seconds(1))
        fd = FrequencyDimension(LinearScale(FrequencyBand(20, 22050), 100))
        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])
        result = tf.sum(axis=1)
        self.assertIsInstance(result, ArrayWithUnits)
        self.assertEqual(1, len(result.dimensions))
        self.assertEqual((30,), result.shape)
        self.assertIsInstance(result.dimensions[0], TimeDimension)

    def test_can_use_negative_axis_indices(self):
        td = TimeDimension(Seconds(1), Seconds(1))
        fd = FrequencyDimension(LinearScale(FrequencyBand(20, 22050), 100))
        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])
        result = tf.sum(axis=-1)
        self.assertIsInstance(result, ArrayWithUnits)
        self.assertEqual(1, len(result.dimensions))
        self.assertEqual((30,), result.shape)
        self.assertIsInstance(result.dimensions[0], TimeDimension)

    def test_can_use_keepdims_with_sum(self):
        td = TimeDimension(Seconds(1), Seconds(1))
        fd = FrequencyDimension(LinearScale(FrequencyBand(20, 22050), 100))
        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])
        result = tf.sum(axis=-1, keepdims=True)
        self.assertIsInstance(result, ArrayWithUnits)
        self.assertEqual(2, len(result.dimensions))
        self.assertEqual((30, 1), result.shape)
        self.assertIsInstance(result.dimensions[0], TimeDimension)
        self.assertIsInstance(result.dimensions[1], IdentityDimension)

    def test_can_use_negative_axis_indices_max(self):
        td = TimeDimension(Seconds(1), Seconds(1))
        fd = FrequencyDimension(LinearScale(FrequencyBand(20, 22050), 100))
        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])
        result = tf.max(axis=-1)
        self.assertIsInstance(result, ArrayWithUnits)
        self.assertEqual(1, len(result.dimensions))
        self.assertEqual((30,), result.shape)
        self.assertIsInstance(result.dimensions[0], TimeDimension)

    def test_from_example(self):
        td = TimeDimension(Seconds(1), Seconds(1))
        fd = FrequencyDimension(LinearScale(FrequencyBand(20, 22050), 100))
        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])
        from_example = ArrayWithUnits.from_example(np.ones((30, 100)), tf)
        self.assertEqual(tf.shape, from_example.shape)
        self.assertSequenceEqual(tf.dimensions, from_example.dimensions)

    def test_can_multiply_by_frequency_weighting_linear_scale(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)

        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)

        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])
        result = tf * AWeighting()
        self.assertIsInstance(result, ArrayWithUnits)
        peak_frequency_band = FrequencyBand(9000, 11000)
        lower_band = FrequencyBand(100, 300)
        peak_slice = np.abs(result[:, peak_frequency_band]).max()
        lower_slice = np.abs(result[:, lower_band]).max()
        self.assertGreater(peak_slice, lower_slice)

    def test_can_multiply_by_frequency_weighting_log_scale(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = GeometricScale(20, 22050, 0.01, 100)

        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)

        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])

        result = tf * AWeighting()
        self.assertIsInstance(result, ArrayWithUnits)
        peak_frequency_band = FrequencyBand(9000, 11000)
        lower_band = FrequencyBand(100, 300)
        peak_slice = np.abs(result[:, peak_frequency_band]).max()
        lower_slice = np.abs(result[:, lower_band]).max()
        self.assertGreater(peak_slice, lower_slice)

    def test_can_multiply_by_array(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)
        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)
        tf = ArrayWithUnits(np.ones((30, 100)), [td, fd])
        result = tf * np.ones(100)
        self.assertIsInstance(result, ArrayWithUnits)
        np.testing.assert_allclose(tf, result)

    def test_can_use_list_of_integers_as_index(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)

        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)

        tf = ArrayWithUnits(np.zeros((30, 100)), [td, fd])

        indexed = tf[[0, 10, 14]]
        self.assertEqual((3, 100), indexed.shape)
        self.assertIsInstance(indexed, ArrayWithUnits)
        self.assertIsInstance(indexed.dimensions[0], IdentityDimension)
        self.assertIsInstance(indexed.dimensions[1], FrequencyDimension)

    def test_can_construct_instance(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)
        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)
        tf = ArrayWithUnits(np.zeros((30, 100)), [td, fd])
        self.assertIsInstance(tf, ArrayWithUnits)

    def test_raises_if_scale_length_does_not_match_frequency_dimension(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 1000)

        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)

        self.assertRaises(
            ValueError,
            lambda: ArrayWithUnits(np.ones((30, 100)), [td, fd]))

    def test_can_slice_frequency_dimension_with_integer_indices(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)
        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)
        tf = ArrayWithUnits(np.zeros((30, 100)), [td, fd])
        sliced = tf[:, 10: 20]
        self.assertEqual((30, 10), sliced.shape)
        self.assertIsInstance(sliced, ArrayWithUnits)

    def test_can_slice_frequency_dimensions_with_frequency_band(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)
        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)
        tf = ArrayWithUnits(np.zeros((30, 100)), [td, fd])
        bands = list(scale)
        sliced = tf[:, bands[0]]
        self.assertEqual((30, 1), sliced.shape)
        self.assertIsInstance(sliced, ArrayWithUnits)

    def test_can_slice_freq_dimension_with_freq_band_spanning_bins(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)
        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)
        tf = ArrayWithUnits(np.zeros((30, 100)), [td, fd])
        bands = list(scale)
        wide_band = FrequencyBand(bands[0].start_hz, bands[9].stop_hz)
        sliced = tf[:, wide_band]
        self.assertEqual((30, 10), sliced.shape)
        self.assertIsInstance(sliced, ArrayWithUnits)

    def test_scale_is_modified_after_slice(self):
        frequency = Seconds(1)
        duration = Seconds(1)
        scale = LinearScale(FrequencyBand(20, 22050), 100)
        td = TimeDimension(frequency, duration)
        fd = FrequencyDimension(scale)
        tf = ArrayWithUnits(np.zeros((30, 100)), [td, fd])
        bands = list(scale)
        wide_band = FrequencyBand(bands[0].start_hz, bands[9].stop_hz)
        sliced = tf[:, wide_band]
        self.assertEqual((30, 10), sliced.shape)
        self.assertIsInstance(sliced, ArrayWithUnits)
        self.assertLess(sliced.dimensions[1].scale.stop_hz, scale.stop_hz)
        self.assertEqual(10, sliced.dimensions[1].scale.n_bands)

    def test_ellipsis(self):
        scale = LinearScale(FrequencyBand(0, 10000), 100)
        arr = ArrayWithUnits(
            np.zeros((10, 3, 100)),
            [IdentityDimension(),
             TimeDimension(Seconds(1)),
             FrequencyDimension(scale)])
        sliced = arr[..., FrequencyBand(1000, 5000)]
        self.assertEqual((10, 3, 41), sliced.shape)
        self.assertIsInstance(sliced.dimensions[0], IdentityDimension)
        self.assertIsInstance(sliced.dimensions[1], TimeDimension)
        self.assertIsInstance(sliced.dimensions[2], FrequencyDimension)
