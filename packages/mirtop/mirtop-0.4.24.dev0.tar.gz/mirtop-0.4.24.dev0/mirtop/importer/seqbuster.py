""" Read seqbuster files"""

from collections import defaultdict

import mirtop.libs.logger as mylog
from mirtop.mirna.realign import isomir, hits
from mirtop.bam import filter
from mirtop.gff import body
from mirtop.mirna.annotate import annotate

logger = mylog.getLogger(__name__)


def header():
    """
    Custom header for seqbuster importer.

    Returns:
        *(str)*: seqbuster header string.
    """
    h = ("## CMD: seqbuster: http://seqcluster.readthedocs.io/mirna_annotation.html#mirna-isomir-annotation-with-java\n"
        "# iso_snp are not filtered yet. Use isomiRs R pacakge to correct for error sequencing\n")
    return h


def read_file(fn, args):
    """
    Read seqbuster file and convert to mirtop GFF format.

    Args:
        *fn(str)*: file name with seqbuster output information.

        *database(str)*: database name.

        *args(namedtuple)*: arguments from command line.
            See *mirtop.libs.parse.add_subparser_gff()*.

    Returns:
        *reads*: dictionary where keys are read_id and values are *mirtop.realign.hits*

    """
    precursors = args.precursors
    reads = defaultdict(hits)
    col_fix = 0
    with open(fn) as handle:
        header = handle.readline()
        if header.find("freq") < 0:
            col_fix = 1
        for line in handle:
            reads.update(_read_line(line, col_fix, precursors))
    logger.info("Hits: %s" % len(reads))
    return reads


def read_file_low_memory(fn, sample, args, out_handle):
    precursors = args.precursors
    reads = defaultdict(hits)
    col_fix = 0
    with open(fn) as handle:
        header = handle.readline()
        if header.find("freq") < 0:
            col_fix = 1
        for line in handle:
            reads = _read_line(line, col_fix, precursors)
            ann = annotate(reads, args.matures, args.precursors, quiet=True)
            gff_lines = body.create(ann, args.database, sample, args, quiet=True)
            body.write_body_on_handle(gff_lines, out_handle)


def _read_line(line, col_fix, precursors):
    reads = defaultdict(hits)
    cols = line.strip().split("\t")
    query_name = cols[1]
    query_sequence = cols[0]
    reference_start = int(cols[4-col_fix]) - 1
    seqbuster_iso = ":".join(cols[6-col_fix:10-col_fix])
    if query_sequence and query_sequence.find("N") > -1:
        return reads
    if query_name not in reads:
        reads[query_name].set_sequence(query_sequence)
        reads[query_name].counts = _get_freq(query_name)
    chrom = cols[13-col_fix]
    logger.debug("\nSEQBUSTER::NEW::query: {query_sequence}\n"
                 "  precursor: {chrom}\n"
                 "  name:  {query_name}\n"
                 "  start: {reference_start}\n"
                 "  iso: {seqbuster_iso}".format(**locals()))
    # logger.debug("SEQBUSTER:: cigar {cigar}".format(**locals()))
    iso = isomir()
    iso.align = line
    iso.set_pos(reference_start, len(reads[query_name].sequence))
    logger.debug("\nSEQBUSTER:: start %s end %s" % (iso.start, iso.end))
    if len(precursors[chrom]) < reference_start + len(reads[query_name].sequence):
        logger.debug("\nSEQBUSTER::len precursor" % len(precursors[chrom]))
        return reads
    iso.subs, iso.add, iso.cigar = filter.tune(reads[query_name].sequence,
                                               precursors[chrom],
                                               reference_start, None)
    logger.debug("\nSEQBUSTER::After tune start %s end %s" % (iso.start, iso.end))
    if len(iso.subs) < 6:
        logger.debug("\nSEQBUSTER::iso.subs %s - length %s" % (iso.subs, len(iso.subs)))
        reads[query_name].set_precursor(chrom, iso)
    return reads


def _get_freq(name):
    """
    Check if name read contains counts (_xNumber)
    """
    try:
        counts = int(name.split("_x")[1])
    except:
        return 0
    return counts
