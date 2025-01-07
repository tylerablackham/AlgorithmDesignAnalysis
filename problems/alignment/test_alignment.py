from pathlib import Path

from byu_pytest_utils import with_import, max_score, test_files

from test_utils import timeout


def read_sequence(file: Path) -> str:
    return ''.join(file.read_text().splitlines())


@max_score(5)
@with_import('alignment')
def test_small_alignment(align):
    score, aseq1, aseq2 = align('polynomial', 'exponential')
    assert score == -1
    assert aseq1 == 'polyn-omial'
    assert aseq2 == 'exponential'


@max_score(2)
@with_import('alignment')
def test_tiny_dna_alignment(align):
    score, aseq1, aseq2 = align('ATGCATGC', 'ATGGTGC')
    assert score == -12
    assert aseq1 == 'ATGCATGC'
    assert aseq2 == 'ATG-GTGC'


@max_score(3)
@with_import('alignment')
def test_tiny_dna_alignment_gaps(align):
    score, aseq1, aseq2 = align('ATATATATAT', 'TATATATATA')
    assert score == -17
    assert aseq1 == 'ATATATATAT-'
    assert aseq2 == '-TATATATATA'


@max_score(8)
@with_import('alignment')
def test_small_dna_alignment_not_banded(align):
    score, aseq1, aseq2 = align('GGGGTTTTAAAACCCCTTTT', 'TTTTAAAACCCCTTTTGGGG')
    assert score == -8
    assert aseq1 == 'GGGGTTTTAAAACCCCTTTT----'
    assert aseq2 == '----TTTTAAAACCCCTTTTGGGG'


@max_score(8)
@with_import('alignment')
def test_small_dna_alignment_banded(align):
    score, aseq1, aseq2 = align('GGGGTTTTAAAACCCCTTTT', 'TTTTAAAACCCCTTTTGGGG', banded_width=2)
    assert score == 6
    assert aseq1 == 'GGGGTTTTAAAACCCCTT--TT'
    assert aseq2 == '--TTTTAAAACCCCTTTTGGGG'


@max_score(9)
@with_import('alignment')
def test_medium_dna_alignment(align):
    seq1 = 'ataagagtgattggcgatatcggctccgtacgtaccctttctactctcgggctcttccccgttagtttaaatctaatctctttataaacggcacttcc'
    seq2 = 'ataagagtgattggcgtccgtacgtaccctttctactctcaaactcttgttagtttaaatctaatctaaactttataaacggcacttcctgtgtgtccat'

    score, aseq1, aseq2 = align(seq1, seq2)

    expected_align1 = 'ataagagtgattggcgatatcggctccgtacgtaccctttctactctcgggctcttccccgttagtttaaatctaatct---ctttataaacggca----c----t-tcc--'
    expected_align2 = 'ataagagtgatt-g-g----c-g-tccgtacgtaccctttctactctcaaactctt----gttagtttaaatctaatctaaactttataaacggcacttcctgtgtgtccat'

    assert score == -116
    assert aseq1 == expected_align1
    assert aseq2 == expected_align2


@max_score(10)
@with_import('alignment')
@timeout(180)
def test_large_dna_alignment(align):
    seq1 = read_sequence(test_files / 'bovine_coronavirus.txt')[:3000]
    seq2 = read_sequence(test_files / 'murine_hepatitus.txt')[:3000]

    score, aseq1, aseq2 = align(seq1, seq2)

    expected_align1 = (test_files / 'large_bovine_murine_align1.txt').read_text()
    expected_align2 = (test_files / 'large_bovine_murine_align2.txt').read_text()

    assert score == -3666
    assert aseq1 == expected_align1
    assert aseq2 == expected_align2


@max_score(10)
@with_import('alignment')
@timeout(20)
def test_large_dna_alignment_banded(align):
    seq1 = read_sequence(test_files / 'bovine_coronavirus.txt')[:3000]
    seq2 = read_sequence(test_files / 'murine_hepatitus.txt')[:3000]

    score, aseq1, aseq2 = align(seq1, seq2, banded_width=3)

    expected_align1 = (test_files / 'large_banded_bovine_murine_align1.txt').read_text()
    expected_align2 = (test_files / 'large_banded_bovine_murine_align2.txt').read_text()

    assert score == -2735
    assert aseq1 == expected_align1
    assert aseq2 == expected_align2


@max_score(10)
@with_import('alignment')
@timeout(20)
def test_massive_dna_alignment_banded(align):
    seq1 = read_sequence(test_files / 'bovine_coronavirus.txt')[:31000]
    seq2 = read_sequence(test_files / 'murine_hepatitus.txt')[:31000]

    score, aseq1, aseq2 = align(seq1, seq2, banded_width=3)

    expected_align1 = (test_files / 'massive_bovine_murine_align1.txt').read_text()
    expected_align2 = (test_files / 'massive_bovine_murine_align2.txt').read_text()

    assert score == -17380
    assert aseq1 == expected_align1
    assert aseq2 == expected_align2