from collections import OrderedDict

import numpy as np
from featureflow import Node, NotEnoughData

from zounds.timeseries import VariableRateTimeSeries
from zounds.core import ArrayWithUnits


class Merge(Node):
    """
    Combine two or more sources into a single feature
    """

    def __init__(self, needs=None):
        super(Merge, self).__init__(needs=needs)
        exc_msg = 'you must supply two or more dependencies'
        if len(needs) < 2:
            raise ValueError(exc_msg)

        self._cache = OrderedDict((id(n), None) for n in list(needs.values()))

    def _enqueue(self, data, pusher):
        key = id(pusher)
        if self._cache[key] is None or self._cache[key].size == 0:
            self._cache[key] = data
        else:
            self._cache[key] = self._cache[key].concatenate(data)

    def _dequeue(self):
        if any(v is None or len(v) == 0 for v in self._cache.values()):
            raise NotEnoughData()
        shortest = min(len(v) for v in self._cache.values())
        output = OrderedDict(
            (k, v[:shortest]) for k, v in self._cache.items())
        self._cache = OrderedDict(
            (k, v[shortest:]) for k, v in self._cache.items())
        return output

    def _process(self, data):
        yield ArrayWithUnits.concat(list(data.values()), axis=1)


class Pooled(Node):
    def __init__(self, op=None, axis=None, needs=None):
        super(Pooled, self).__init__(needs=needs)
        self._timeslices = VariableRateTimeSeries(())
        self._timeseries = None
        self._op = op
        self._axis = axis

    def _enqueue(self, data, pusher):
        if isinstance(data, ArrayWithUnits):
            try:
                self._timeseries = self._timeseries.concatenate(data)
            except AttributeError:
                self._timeseries = data
        else:
            self._timeslices = self._timeslices.concat(data)

    def _dequeue(self):
        if not self._finalized:
            raise NotEnoughData()
        return self._timeslices, self._timeseries

    def _process(self, data):
        slices, series = data
        slices = slices.slices
        examples = [(ts, self._op(series[ts], axis=self._axis))
                    for ts in slices]
        yield VariableRateTimeSeries(examples)


class Slice(Node):
    def __init__(self, sl=None, needs=None):
        super(Slice, self).__init__(needs=needs)
        self._sl = sl

    def _process(self, data):
        print(np.array(data), self._sl)
        yield data[:, self._sl]


class Sum(Node):
    def __init__(self, axis=0, needs=None):
        super(Sum, self).__init__(needs=needs)
        self._axis = axis

    def _process(self, data):
        # TODO: This should be generalized.  Sum will have this same problem
        try:
            # data = np.sum(data, axis=self._axis)
            data = np.sum(axis=self._axis)
        except ValueError:
            print('ERROR')
            data = data
        if data.shape[0]:
            yield data


class Max(Node):
    def __init__(self, axis=0, needs=None):
        super(Max, self).__init__(needs=needs)
        self._axis = axis

    def _process(self, data):
        # TODO: This should be generalized.  Sum will have this same problem
        try:
            # data = np.max(data, axis=self._axis)
            data = data.max(axis=self._axis)
        except ValueError:
            print('ERROR')
            data = data
        if data.shape[0]:
            yield data


class Binarize(Node):
    def __init__(self, predicate=None, needs=None):
        super(Binarize, self).__init__(needs=needs)
        self.predicate = predicate

    def _process(self, data):
        yield self.predicate(data)
