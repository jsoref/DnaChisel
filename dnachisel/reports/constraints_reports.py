"""Misc. plotting and reporting methods, some of which are really arbitrary.
"""

from copy import deepcopy

from Bio.SeqRecord import SeqRecord
import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from dna_features_viewer import BiopythonTranslator
    DFV_AVAILABLE = True
except:
    BiopythonTranslator = object
    DFV_AVAILABLE = False


from ..DnaOptimizationProblem import DnaOptimizationProblem
from ..biotools import gc_content
from ..SequencePattern import repeated_kmers, homopolymer_pattern
from ..builtin_specifications import (EnforceGCContent, AvoidPattern,
                                      AvoidHairpins)


def plot_constraint_breaches(constraint, sequence, title=None, ax=None,
                             show_locations=False, show_feature_labels=False):
    """Plot all breaches in a sequence for a single constraint.

    Parameters
    -----------
    constraint
      A DnaChisel Specification, to be used as a constraint.

    sequence
      An ATGC string, or a record. If it is a record, its annotations will also
      be shown in the plot.

    title
      Title to be added to the plot

    ax
      Matplotlib ax on which to plot the result. If no ax is provided, one
      will be created, and it will be returned at the end

    show_locations
      Whether or not to label the breach features with their coordinates

    show_feature_labels
      Whether or not to show the labels of all features.


    Returns
    -------
    ax
      The matplotlib ax on which the plot was drawn

    """
    class Translator(BiopythonTranslator):
        """A Biopython record translator for DNA Features Viewer.

        This translator produces label-free plots.
        """

        default_feature_color = "#ffaaaa"

        def compute_feature_label(self, f):
            if f.type != "original" and show_locations:
                return str(int(f.location.start))
            elif show_feature_labels and f.type == "original":
                return BiopythonTranslator.compute_feature_label(f)
            else:
                return None

        def compute_feature_color(self, f):
            return "#ffffff" if f.type == "original" else "#ff9999"

    if isinstance(sequence, SeqRecord):
        record = sequence
        sequence = str(sequence.seq).upper()
    else:
        record = None

    problem = DnaOptimizationProblem(sequence, constraints=[constraint])
    evals = problem.constraints_evaluations().filter("failing")
    breaches_record = problem.to_record(
        with_original_features=False, with_objectives=False,
        with_constraints=False
    )
    breaches_record.features = evals.locations_as_features()

    if record is not None:
        for feature in record.features:
            feature = deepcopy(feature)
            feature.type = "original"
            breaches_record.features.append(feature)

    translator = Translator()
    graphic_record = translator.translate_record(breaches_record)
    ax, _ = graphic_record.plot(ax=ax)
    ax.set_ylim(ymin=-1, ymax=min(5, ax.get_ylim()[1]))
    if title is not None:
        ax.set_title(title, fontweight="bold", loc="left")
    return ax

def plot_constraints_breaches(record, constraints, color="red",
                              ax=None, figure_width=20):
    """Plot the record and highlight locations of constraints breaches.

    Requires "DNA Features Viewer" installed.

    Parameters
    ----------
    record
      A Biopython record

    constraints
      A list or tuple of DnaChisel specifications to use as constraints

    color
      Color for highlighting the constraint breaches in the plot. All
      other features will appear in white.

    ax
       Matplotlib ax on which to plot. If none is provided, one is created,
       and returned at the end.

    figure_width
      Width of the final figure in inches, if no ax is provided

    Returns
    -------
    ax
      The matplotlib ax on which the plot was drawn

    """
    if not DFV_AVAILABLE:
        raise ImportError("Plotting constraint breaches requires "
                          "Matplotlib and dna_features_viewer installed.")

    class MyTranslator(BiopythonTranslator):

        def compute_feature_color(self, f):
            return color if (f.type == "breach") else "white"

    new_record = deepcopy(record)
    sequence = str(record.seq).upper()
    pb = DnaOptimizationProblem(sequence, constraints=constraints)
    rec = pb.constraints_breaches_as_biopython_record("breach")
    for f in rec.features:
        new_record.features.append(f)
    gr_record = MyTranslator().translate_record(new_record)
    ax, _ = gr_record.plot(ax=ax, figure_width=20)
    return ax


def make_constraints_breaches_pdf(constraints_sets, record, pdf_path):
    """Plot different constraint breach plots in a multi-page PDF.

    Parameters
    ----------

    constraints_set
      List of DnaChisel Specifications to be used as constraints.

    record
      Color for highlighting the constraint breaches in the plot. All
      other features will appear in white.

    ax
       Matplotlib ax on which to plot. If none is provided, one is created.

    figure_width
      Width of the final figure in inches, if no ax is provided

    """
    if not DFV_AVAILABLE:
        raise ImportError("Package ``dna_features_viewer`` must be installed"
                          "to use method ``make_constraints_breaches_pdf``")
    with PdfPages(pdf_path) as pdf:
        for title, constraints in constraints_sets.items():
            ax = plot_constraints_breaches(record, constraints,
                                           figure_width=20)
            ax.set_title(title, fontsize=16, fontweight="bold")
            pdf.savefig(ax.figure, bbox_inches="tight")
            plt.close(ax.figure)


def plot_gc_content_breaches(sequence, window=70, gc_min=0.35, gc_max=0.65,
                             ax=None, title=None):
    """Plot a profile of GC content along the sequence.
    The regions with out-of-bound GC are highlighted.

    Returns the Matplotlib ax on which the figure was plotted.

    Parameters
    ----------
    sequence
      An ATGC string

    window
      Number of nucleotides to use for local averaging of GC content

    gc_min
      minimal allowed proportion of gc (between 0 and 1)

    gc_max
      maximal allowed proportion of gc (between 0 and 1)

    ax
      Matplotlib ax on which to plot the figure. If none is provided, one
      is created and returned in the end.

    title
      Title to be added to the figure.

    """
    gc = gc_content(sequence, window_size=window)
    xx = np.arange(len(gc)) + window / 2

    if ax is None:
        fig, ax = plt.subplots(1, figsize=(12, 3))
    gc_inbound = +gc
    gc_inbound[(gc < gc_min) | (gc > gc_max)] = np.nan
    ax.plot(xx, gc_inbound, alpha=0.2, c='b')

    for limit, whr in (gc_min, gc < gc_min), (gc_max, gc > gc_max):
        ax.axhline(limit, c="k", lw=0.5, ls=":")
        gc_bad = +gc
        gc_bad[1 - whr] = np.nan
        ax.plot(xx, gc_bad, alpha=0.1, c='r')
        ax.fill_between(xx, gc, y2=limit, where=whr, alpha=0.6,
                        facecolor="r")

    ax.set_xlim(0, len(gc))
    ax.set_ylim(0, 1)
    if title is not None:
        ax.set_title(title, fontweight="bold", loc="left")
    return ax


def plot_sequence_manufacturability_difficulties(sequence):
    """Plot a series of manufacturability factor checks, on a single figure.

    The factors considered are mostly arbitrary. Most users won't be interested
    by this function. The function looks for presence of Type IIs restriction
    sites, homopolymers, hairpins, extreme GC content, repeats.
    The breaches for each constraint type are plotted on separate axis.

    Parameters
    ----------
    sequence
      An ATGC string or a Biopythn sequence record (at which case the features
      will be drawn along with the constraints breaches).

    Returns
    -------

    axes
      List of the different axes (in a same figure) on which the plots were
      drawn
    """
    if isinstance(sequence, SeqRecord):
        record = sequence
        sequence = str(sequence.seq).upper()
    else:
        record = sequence

    nplots = 7
    fig, axes = plt.subplots(nplots, 1, figsize=(10, 1.4 * nplots),
                             sharex=True, facecolor="white")

    gc_min, gc_max, gc_window = 0.25, 0.80, 50
    plot_gc_content_breaches(
        sequence, window=gc_window, gc_min=gc_min,
        gc_max=gc_max, ax=axes[0],
        title="GC content (window= %d)" % gc_window
    )

    constraint = EnforceGCContent(gc_min=gc_min, gc_max=gc_max,
                                  gc_window=gc_window)
    plot_constraint_breaches(
        constraint, record, ax=axes[1],
        title="Zones of extreme GC content (Gen9-type short window)"
    )

    plot_constraint_breaches(
        AvoidPattern(enzyme="BsmBI"), sequence,
        title="BsmBI sites", ax=axes[2]
    )

    plot_constraint_breaches(
        AvoidPattern(enzyme="BsaI"),
        record, title="BsaI sites", ax=axes[3]
    )

    for l, n in [("A", 9), ("T", 9), ("G", 6), ("C", 6)]:
        constraint = AvoidPattern(homopolymer_pattern(l, n))
        plot_constraint_breaches(
            constraint, record,
            title="Homopolymers (6+ G or C | 9+ A or T)", ax=axes[4])

    for length, n_repeats in (3, 5), (2, 9):
        pattern = repeated_kmers(length, n_repeats=n_repeats)
        constraint = AvoidPattern(pattern)
        plot_constraint_breaches(
            constraint, record,
            title="Repeats (5 x 3bp, 9 x 2bp)", ax=axes[5]
        )

    plot_constraint_breaches(
        AvoidHairpins(stem_size=20, hairpin_window=200),
        record, title="Hairpins", ax=axes[6]
    )

    fig.tight_layout()
    return axes