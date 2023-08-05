""" Read bam files"""
import copy

import mirtop.libs.logger as mylog

logger = mylog.getLogger(__name__)


def _coord(sequence, start, mirna, precursor, iso):
    """
    Define t5 and t3 isomirs
    """
    insertion = 0
    deletion = 0
    add = 0
    if iso.subs:
        insertion = sum([1  if s[-1] == "-" else 0 for s in iso.subs])
    if iso.subs:
        deletion = sum([1  if s[1] == "-" else 0 for s in iso.subs])
    if iso.add:
        add = len(iso.add)
    end = (iso.end - add - insertion + deletion)

    logger.debug("COOR:: s:%s len:%s end:%s fixedEnd:%s mirna:%s iso:%s" % (
        start, len(sequence), iso.end, end, mirna, iso.format())
        )
    dif = abs(mirna[0] - start)
    if start < mirna[0]:
        iso.t5 = sequence[:dif].upper()
    elif start > mirna[0]:
        iso.t5 = precursor[mirna[0]:mirna[0] + dif].lower()
    elif start == mirna[0]:
        iso.t5 = 0
    if dif > 6:
        logger.debug("COOR::start > 6 start:%s len:%s dif:%s mirna:%s iso:%s" % (
                        start, len(sequence),
                        dif, mirna, iso.format()))
        return None

    dif = abs(mirna[1] - iso.end)
    if iso.add:
        iso.add = iso.add.replace("-", "")
        sequence = sequence[:-len(iso.add)]
    if end > mirna[1]:
        iso.t3 = sequence[-dif:].upper()
    elif end < mirna[1]:
        iso.t3 = precursor[mirna[1] + 1 - dif:(mirna[1] + 1)].lower()
    elif end == mirna[1]:
        iso.t3 = 0

    if dif > 7:
        logger.debug("COOR::end > 7 len:%s end:%s dif:%s mirna:%s iso:%s" % (
            len(sequence), end, dif, mirna, iso.format()))
        return None
    return True


def annotate(reads, mature_ref, precursors, quiet=False):
    """
    Using coordinates, mismatches and realign to annotate isomiRs

    Args:
        *reads(dicts of hits)*:
            dict object that comes from *mirotp.bam.bam.read_bam()*

        *mirbase_ref (dict of mirna positions)*:
            dict object that comers from *mirtop.mirna.read_mature()*

        *precursors dict object (key : fasta)*:
            that comes from *mirtop.mirna.fasta.read_precursor()*
        *quiet(boolean)*:
            verbosity state
    Return:
        *reads (dict)*:
            dictionary where keys are read_id and
            values are *mirtop.realign.hits*
    """
    n_iso = 0
    n_skip_precursor = 0
    for r in reads:
        logger.debug(("\nANN::READ::read {r}").format(**locals()))
        for ps in reads[r].precursors:
            p = list(ps)[0]
            start = reads[r].precursors[ps].start
            end = reads[r].precursors[ps].end
            logger.debug(("\nANN::READ::precursor {start} {end}").format(**locals()))
            for mature in mature_ref[p]:
                mi = mature_ref[p][mature]
                logger.debug(("\nANN::NEW::read:{s}\n pre:{p} start:{start} end: {end} "
                              "cigar: {cigar} "
                              "\n mir:{mature} mir_pos:{mi}\n mir_seqs:{mature_s}"
                              ).format(s=reads[r].sequence,
                                       mature_s = precursors[ps][mi[0]:mi[1] + 1],
                                       cigar = reads[r].precursors[ps].cigar,
                                       **locals()))
                iso_copy = copy.deepcopy(reads[r].precursors[ps])
                if not precursors[ps[0]]:
                    n_skip_precursor += 1
                    continue
                is_iso = _coord(reads[r].sequence, start, mi, precursors[ps[0]], iso_copy)
                logger.debug(("ANN::is_iso:{is_iso}").format(**locals()))
                logger.debug("ANN::annotation:%s iso:%s" % (r, reads[r].precursors[ps].format()))
                logger.debug("ANN::annotation:%s Variant:%s" % (r, reads[r].precursors[ps].formatGFF()))
                if is_iso:
                    n_iso += 1
                    reads[r].precursors[ps] = iso_copy
                    reads[r].precursors[ps].mirna = mature
                    # break
    if not quiet:
        logger.info("Valid hits (+/- reference miRNA): %s" % n_iso)
        logger.info("Skipped due to not precursor sequence: %s" % n_skip_precursor)
    return reads
