from .DnaOptimizationProblem import (
    DnaOptimizationProblem,
    NoSolutionError
)
from .CircularDnaOptimizationProblem import CircularDnaOptimizationProblem
from .Location import Location

from .builtin_specifications import (
    AllowPrimer,
    AvoidBlastMatches,
    AvoidChanges,
    AvoidHairpins,
    AvoidMatches,
    AvoidNonUniqueSegments,
    AvoidPattern,
    AvoidStopCodons,
    CodonOptimize,
    EnforceChanges,
    EnforceChoice,
    EnforceGCContent,
    EnforceMeltingTemperature,
    EnforcePatternOccurence,
    EnforceRegionsCompatibility,
    EnforceSequence,
    EnforceTerminalGCContent,
    EnforceTranslation,
    SequenceLengthBounds,
    DEFAULT_SPECIFICATIONS_DICT
)

from .Specification import Specification, SpecificationsSet
from .SpecEvaluation import SpecEvaluation

from .SequencePattern import (
    SequencePattern,
    DnaNotationPattern,
    HomopolymerPattern,
    RepeatedKmerPattern,
    EnzymeSitePattern,
)

from .biotools import (
    blast_sequence,
    complement,
    list_common_enzymes,
    load_record,
    write_record,
    random_dna_sequence,
    random_protein_sequence,
    reverse_complement,
    reverse_translate,
    sequences_differences,
    translate,
    change_biopython_record_sequence,
    annotate_differences,
    annotate_pattern_occurrences,
    annotate_record,
    sequence_to_biopython_record,
    sequences_differences_segments,
)

from .utils import random_compatible_dna_sequence


from .version import __version__

__all__ = [
    "DnaOptimizationProblem",
    "NoSolutionError",
    "CircularDnaOptimizationProblem",
    "Location",
    "AllowPrimer",
    "AvoidBlastMatches",
    "AvoidChanges",
    "AvoidHairpins",
    "AvoidMatches",
    "AvoidNonUniqueSegments",
    "AvoidPattern",
    "AvoidStopCodons",
    "CodonOptimize",
    "EnforceChoice",
    "EnforceGCContent",
    "EnforceMeltingTemperature",
    "EnforcePatternOccurence",
    "EnforceRegionsCompatibility",
    "EnforceSequence",
    "EnforceTerminalGCContent",
    "EnforceTranslation",
    "SequenceLengthBounds",
    "Specification",
    "SpecificationsSet",
    "SpecEvaluation",
    "SequencePattern",
    "DnaNotationPattern",
    "HomopolymerPattern",
    "RepeatedKmerPattern",
    "EnzymeSitePattern",
    "blast_sequence",
    "complement",
    "list_common_enzymes",
    "load_record",
    "write_record",
    "random_dna_sequence",
    "random_protein_sequence",
    "reverse_complement",
    "reverse_translate",
    "sequences_differences",
    "translate",
    "change_biopython_record_sequence",
    "annotate_differences",
    "annotate_pattern_occurrences",
    "annotate_record",
    "sequence_to_biopython_record",
    "sequences_differences_segments",
    "random_compatible_dna_sequence",
    "__version__",
    "DEFAULT_SPECIFICATIONS_DICT",
]
