"""Implement AvoidNonuniqueSegments(Specification)"""

from collections import defaultdict

from ..Specification import Specification, VoidSpecification
from ..SpecEvaluation import SpecEvaluation
from dnachisel.biotools import reverse_complement
from dnachisel.Location import Location


class AvoidNonuniqueSegments(Specification):
    """Avoid sub-sequence which have repeats elsewhere in the sequence.

    Parameters
    ----------
    min_length
      Minimal length of sequences to be considered repeats

    location
      Segment of the sequence in which to look for repeats. If None, repeats
      are searched in the full sequence.

    include_reverse_complement
      If True, the sequence repeats are also searched for in the reverse
      complement of the sequence (or sub sequence if `location` is not None).

    Examples
    --------
    >>> from dnachisel import *
    >>> sequence = random_dna_sequence(50000)
    >>> constraint= AvoidNonuniqueSegments(10, include_reverse_complement=True)
    >>> problem = DnaOptimizationProblem(sequence, constraints= [contraint])
    >>> print (problem.constraints_summary())

    """

    def __init__(self, min_length, location=None,
                 include_reverse_complement=False):
        """Initialize."""
        self.min_length = min_length
        self.location = location
        self.include_reverse_complement = include_reverse_complement

    def initialize_on_problem(self, problem):
        """Location is the full sequence by default."""
        if self.location is None:
            self.location = Location(0, len(problem.sequence))

    def evaluate(self, problem):
        """Return 0 if the sequence has no repeats, else -number_of_repeats."""
        sequence = self.location.extract_sequence(problem.sequence)
        rev_complement = reverse_complement(sequence)
        kmers_locations = defaultdict(lambda: [])
        for i in range(len(sequence) - self.min_length):
            start, end = i, i + self.min_length
            kmers_locations[sequence[start:end]].append((start, end))
        if self.include_reverse_complement:
            for i in range(len(sequence) - self.min_length):
                start, end = i, i + self.min_length
                kmers_locations[rev_complement[start:end]].append(
                    (len(sequence) - end, len(sequence) - start)
                )

        locations = sorted([
            Location(*min(positions_list, key=lambda p: p[0]))
            for positions_list in kmers_locations.values()
            if len(positions_list) > 1
        ])

        if locations == []:
            return SpecEvaluation(
                self, problem, score=0,
                message="Passed: no nonunique %d-mer found." % self.min_length)

        return SpecEvaluation(
            self, problem, score=-len(locations),
            locations=locations,
            message="Failed, the following positions are the first occurences"
                    "of non-unique segments %s" % locations)

    def localized(self, location):
        """Localize the evaluation."""
        new_location = self.location.overlap_region(location)
        if new_location is None:
            return VoidSpecification(parent_specification=self)
        else:
            return self

    def __repr__(self):
        """Represent."""
        return "AvoidNonUniqueSegments(%d)" % (self.min_length)

    def __str__(self):
        """Represent."""
        return "AvoidNonUniqueSegments(%d)" % (self.min_length)
