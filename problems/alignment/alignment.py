import math

def get_banded_range(i, row_length, banded_width):
    if banded_width == -1:
        return range(0, row_length)
    else:
        lower = i - banded_width
        upper = i + banded_width + 1
        if lower < 0:
            lower = 0
        if upper > row_length:
            upper = row_length
        return range(lower, upper)

def find_alignment_strings(matrix, left_string, right_string, gap):
    left_alignment_string = ''
    right_alignment_string = ''
    current_cell = matrix[len(left_string), len(right_string)]
    while current_cell[2] is not None:
        if current_cell[2] == 'diagonal':
            left_alignment_string = left_string[-1] + left_alignment_string
            left_string = left_string[:-1]
            right_alignment_string = right_string[-1] + right_alignment_string
            right_string = right_string[:-1]
        if current_cell[2] == 'left':
            left_alignment_string = gap + left_alignment_string
            right_alignment_string = right_string[-1] + right_alignment_string
            right_string = right_string[:-1]
        if current_cell[2] == 'up':
            left_alignment_string = left_string[-1] + left_alignment_string
            left_string = left_string[:-1]
            right_alignment_string = gap + right_alignment_string
        current_cell = matrix[current_cell[1]]
    return left_alignment_string, right_alignment_string

def align(seq1: str, seq2: str, match_award=-3, indel_penalty=5, sub_penalty=1,
          banded_width=-1, gap='-') -> tuple[float, str | None, str | None]:
    mod_seq1 = "_" + seq1
    mod_seq2 = "_" + seq2
    len1 = len(mod_seq1)
    len2 = len(mod_seq2)
    matrix = {(0, 0): (0, None, None)}
    for i in range(len1):
        for j in get_banded_range(i, len2, banded_width):
            if i == 0 and j == 0:
                pass
            elif i == 0:
                matrix[(i,j)] = (j * indel_penalty, (i, j-1), 'left')
            elif j == 0:
                matrix[(i,j)] = (i * indel_penalty, (i-1, 0), 'up')
            else:
                diag_cost = sub_penalty + matrix[(i-1, j-1)][0]
                if mod_seq1[i] == mod_seq2[j]:
                    diag_cost = match_award + matrix[(i-1, j-1)][0]
                left_cost = math.inf
                if (i,j-1) in matrix:
                    left_cost = indel_penalty + matrix[(i, j-1)][0]
                up_cost = math.inf
                if (i-1, j) in matrix:
                    up_cost = indel_penalty + matrix[(i-1, j)][0]
                if min(diag_cost, left_cost, up_cost) == diag_cost:
                    matrix[(i,j)] = (diag_cost, (i-1, j-1), 'diagonal')
                elif min(left_cost, up_cost) == left_cost:
                    matrix[(i,j)] = (left_cost, (i, j-1), 'left')
                else:
                    matrix[(i,j)] = (up_cost, (i-1, j), 'up')
    alignment_cost = matrix[(len1-1, len2-1)][0]
    left_alignment_string, right_alignment_string = find_alignment_strings(matrix, seq1, seq2, gap)
    return alignment_cost, left_alignment_string, right_alignment_string


print(align('ctgcataaggtcagtcat', 'tacgcaggtcacggt', banded_width=-1))
