from argparse import ArgumentParser
from pathlib import Path

from alignment import align


def main(seq1: str, seq2: str):
    """
    Align the two sequences and print the score and alignment strings
    """
    score, alignment1, alignment2 = align(seq1, seq2)
    print(f'Score: {score}')
    print(alignment1)
    print(alignment2)


def _content_or_string(could_be_path):
    if (s1file := Path(could_be_path)).exists():
        return s1file.read_text()
    else:
        # assume it's the sequence string, not a file name
        return could_be_path


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('seq1_file', help='Path to file containing sequence 1')
    parser.add_argument('seq2_file', help='Path to file containing sequence 2')
    args = parser.parse_args()

    seq1 = _content_or_string(args.seq1_file)
    seq2 = _content_or_string(args.seq2_file)

    main(seq1, seq2)
