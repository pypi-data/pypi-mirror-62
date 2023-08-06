# mixture.py
# Author: Jacob Schreiber <jmschreiber91@gmail.com>

"""
This file contains code that implements mixtures of submodular functions.
"""

try:
	import cupy
except:
	import numpy as cupy
	
import numpy

from .base import BaseGraphSelection

from tqdm import tqdm

class MixtureSelection(BaseGraphSelection):
	"""A selection approach based on a mixture of submodular functions.

	This class implements a simple mixture of submodular functions for the
	purpose of selecting a representative subset of the data. The user passes
	in a list of instantiated submodular functions and their respective weights
	to the initialization. At each iteration in the selection procedure the 
	gains from each submodular functions will be scaled by their respective 
	weight and added together.

	This class can also be used to add regularizers to the selection procedure.
	If a submodular function is mixed with another submodular function that
	acts as a regularizer, such as feature based selection mixed with a
	custom function measuring some property of the selected subset.

	Parameters
	----------
	n_samples : int
		The number of samples to return.

	submodular_functions : list
		The list of submodular functions to mix together. The submodular
		functions should be instantiated.

	weights : list, numpy.ndarray or None, optional
		The relative weight of each submodular function. This is the value
		that the gain from each submodular function is multiplied by before
		being added together. The default is equal weight for each function.

	initial_subset : list, numpy.ndarray or None, optional
		If provided, this should be a list of indices into the data matrix
		to use as the initial subset, or a group of examples that may not be
		in the provided data should beused as the initial subset. If indices, 
		the provided array should be one-dimensional. If a group of examples,
		the data should be 2 dimensional.

	optimizer : string or optimizers.BaseOptimizer, optional
		The optimization approach to use for the selection. Default is
		'two-stage', which makes selections using the naive greedy algorithm
		initially and then switches to the lazy greedy algorithm. Must be
		one of

			'random' : randomly select elements (dummy optimizer)
			'modular' : approximate the function using its modular upper bound
			'naive' : the naive greedy algorithm
			'lazy' : the lazy (or accelerated) greedy algorithm
			'approximate-lazy' : the approximate lazy greedy algorithm
			'two-stage' : starts with naive and switches to lazy
			'stochastic' : the stochastic greedy algorithm
			'sample' : randomly take a subset and perform selection on that
			'greedi' : the GreeDi distributed algorithm
			'bidirectional' : the bidirectional greedy algorithm

		Default is 'two-stage'.

	optimizer_kwds : dict, optional
		Arguments to pass into the optimizer object upon initialization.
		Default is {}.

	n_jobs : int, optional
		The number of cores to use for processing. This value is multiplied
		by 2 when used to set the number of threads. If set to -1, use all
		cores and threads. Default is -1.

	random_state : int or RandomState or None, optional
		The random seed to use for the random selection process. Only used
		for stochastic greedy.

	verbose : bool, optional
		Whether to print output during the selection process.

	Attributes
	----------
	pq : PriorityQueue
		The priority queue used to implement the lazy greedy algorithm.

	n_samples : int
		The number of samples to select.

	submodular_functions : list
		A concave function for transforming feature values, often referred to as
		phi in the literature.

	weights : numpy.ndarray
		The weights of each submodular function.

	ranking : numpy.array int
		The selected samples in the order of their gain with the first number in
		the ranking corresponding to the index of the first sample that was
		selected by the greedy procedure.

	gains : numpy.array float
		The gain of each sample in the returned set when it was added to the
		growing subset. The first number corresponds to the gain of the first
		added sample, the second corresponds to the gain of the second added
		sample, and so forth.
	"""

	def __init__(self, n_samples, functions, weights=None, metric='ignore',
		initial_subset=None, optimizer='two-stage', optimizer_kwds={}, n_jobs=1, 
		random_state=None, verbose=False):

		if len(functions) < 2:
			raise ValueError("Must mix at least two functions.")

		self.m = len(functions)
		self.functions = functions

		if weights is None:
			self.weights = numpy.ones(self.m, dtype='float64')
		else:
			self.weights = weights

		super(MixtureSelection, self).__init__(n_samples=n_samples, 
			metric=metric, initial_subset=initial_subset, 
			optimizer=optimizer, optimizer_kwds=optimizer_kwds, 
			n_jobs=n_jobs, random_state=random_state, verbose=verbose)

		for function in self.functions:
			function.initial_subset = self.initial_subset
			function.random_state = self.random_state
			function.n_jobs = self.n_jobs
			function.verbose = self.verbose

			if isinstance(function, BaseGraphSelection):
				function.metric = self.metric

	def fit(self, X, y=None, sample_weight=None, sample_cost=None):
		"""Run submodular optimization to select the examples.

		This method is a wrapper for the full submodular optimization process.
		It takes in some data set (and optionally labels that are ignored
		during this process) and selects `n_samples` from it in the greedy
		manner specified by the optimizer.

		This method will return the selector object itself, not the transformed
		data set. The `transform` method will then transform a data set to the
		selected points, or alternatively one can use the ranking stored in
		the `self.ranking` attribute. The `fit_transform` method will perform
		both optimization and selection and return the selected items.

		Parameters
		----------
		X : list or numpy.ndarray, shape=(n, d)
			The data set to transform. Must be numeric.

		y : list or numpy.ndarray or None, shape=(n,), optional
			The labels to transform. If passed in this function will return
			both the data and th corresponding labels for the rows that have
			been selected.

		sample_weight : list or numpy.ndarray or None, shape=(n,), optional
			The weight of each example. Currently ignored in apricot but
			included to maintain compatibility with sklearn pipelines. 

		sample_cost : list or numpy.ndarray or None, shape=(n,), optional
			The cost of each item. If set, indicates that optimization should
			be performed with respect to a knapsack constraint.

		Returns
		-------
		self : MixtureSelection
			The fit step returns this selector object.
		"""

		return super(MixtureSelection, self).fit(X, y=y, 
			sample_weight=sample_weight, sample_cost=sample_cost)

	def _initialize(self, X):
		super(MixtureSelection, self)._initialize(X)

		for function in self.functions:
			function._initialize(X)

	def _calculate_gains(self, X, idxs=None):
		"""This function will return the gain that each example would give.

		This function will return the gains that each example would give if
		added to the selected set. When a matrix of examples is given, a
		vector will be returned showing the gain for each example. When
		a single element is passed in, it will return a singe value."""

		idxs = idxs if idxs is not None else self.idxs

		if self.cupy:
			gains = cupy.zeros(idxs.shape[0], dtype='float64')
		else:
			gains = numpy.zeros(idxs.shape[0], dtype='float64')

		for i, function in enumerate(self.functions):
			gains += function._calculate_gains(X, idxs) * self.weights[i]

		return gains

	def _select_next(self, X, gain, idx):
		"""This function will add the given item to the selected set."""

		for function in self.functions:
			function._select_next(X, gain, idx)

		super(MixtureSelection, self)._select_next(X, gain, idx)
