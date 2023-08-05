import unittest2
from .timeseries import TimeDimension, TimeSlice
from .duration import Seconds, Milliseconds
from .samplerate import SR44100


class TimeDimensionTests(unittest2.TestCase):
    def test_equals(self):
        td1 = TimeDimension(Seconds(1), Milliseconds(900))
        td2 = TimeDimension(Seconds(1), Milliseconds(900))
        self.assertEqual(td1, td2)

    def test_not_equal(self):
        td1 = TimeDimension(Seconds(2), Milliseconds(900))
        td2 = TimeDimension(Seconds(1), Milliseconds(900))
        self.assertNotEqual(td1, td2)

    def test_raises_if_frequency_is_not_timedelta_instance(self):
        self.assertRaises(ValueError, lambda: TimeDimension('s'))

    def test_raises_if_duration_is_not_timedelta_instance(self):
        self.assertRaises(ValueError, lambda: TimeDimension(Seconds(2), 's'))

    def test_duration_is_equal_to_frequency_if_not_provided(self):
        td = TimeDimension(Seconds(1))
        self.assertEqual(Seconds(1), td.frequency)
        self.assertEqual(Seconds(1), td.duration)

    def test_integer_based_slice(self):
        td = TimeDimension(*SR44100(), size=44100 * 5)
        sl = td.integer_based_slice(TimeSlice(duration=Seconds(1)))
        self.assertEqual(slice(0, 44100), sl)