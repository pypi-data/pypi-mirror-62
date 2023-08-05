from abc import ABC, abstractmethod

import numpy as np

from .._utils import euclidean, perm_test


class IndependenceTest(ABC):
    r"""
    A base class for an independence test.

    Parameters
    ----------
    compute_distance : callable(), optional (default: euclidean)
        A function that computes the distance or similarity among the samples
        within each data matrix. Set to `None` if `x` and `y` are already
        distance matrices. To call a custom function, either create the
        distance matrix before-hand or create a function of the form
        ``compute_distance(x)`` where `x` is the data matrix for which
        pairwise distances are calculated.
    """

    def __init__(self, compute_distance=euclidean):
        # set statistic and p-value
        self.stat = None
        self.pvalue = None
        self.compute_distance = compute_distance

        super().__init__()

    @abstractmethod
    def _statistic(self, x, y):
        r"""
        Calulates the independence test statistic.

        Parameters
        ----------
        x, y : ndarray
            Input data matrices.
        """

    @abstractmethod
    def test(self, x, y, reps=1000, workers=1):
        r"""
        Calulates the independence test p-value.

        Parameters
        ----------
        x, y : ndarray
            Input data matrices.
        reps : int, optional
            The number of replications used in permutation, by default 1000.
        workers : int, optional (default: 1)
            Evaluates method using `multiprocessing.Pool <multiprocessing>`).
            Supply `-1` to use all cores available to the Process.

        Returns
        -------
        stat : float
            The computed independence test statistic.
        pvalue : float
            The pvalue obtained via permutation.
        """
        self.x = x
        self.y = y

        # calculate p-value
        stat, pvalue = perm_test(self._statistic, x, y, reps=reps, workers=workers)
        self.stat = stat
        self.pvalue = pvalue

        return stat, pvalue
