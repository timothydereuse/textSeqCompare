import numpy as np
import matplotlib.pyplot as plt

def read_file(fname):
    file = open(fname, 'r')
    lines = file.readlines()
    file.close()
    lines = ' '.join(lines)
    lines = lines.replace('\n', '')
    return lines

# scoring system
match = 2
mismatch = -2
gap_open = -20
gap_extend = -0

if __name__ == '__main__':
    files = ['einsiedeln_001r', 'einsiedeln_001v', 'einsiedeln_002r',
        'einsiedeln_002v', 'einsiedeln_003r', 'einsiedeln_003v']

    item = files[4]
    transcript = read_file('./txt/' + item + '_transcript.txt')
    ocr = read_file('./txt/' + item + '_ocr.txt')

    # ins_mat and del_mat keep track of gaps in horizontal and vertical directions
    mat = np.zeros((len(transcript), len(ocr)))
    ins_mat = np.zeros((len(transcript), len(ocr)))
    del_mat = np.zeros((len(transcript), len(ocr)))

    for i in range(len(transcript)):
        mat[i][0] = gap_extend * i
        del_mat[i][0] = -1000000
    for i in range(len(ocr)):
        mat[0][i] = gap_extend * i
        ins_mat[0][i] = -1000000

    for i in range(1, len(transcript)):
        for j in range(1, len(ocr)):

            ins_mat[i][j] = max(ins_mat[i-1][j] + gap_extend, mat[i-1][j] + gap_open)
            del_mat[i][j] = max(del_mat[i][j-1] + gap_extend, mat[i][j-1] + gap_open)

            match_score = mat[i - 1][j - 1]
            if transcript[i-1] == ocr[j-1]:
                match_score += match
            else:
                match_score += mismatch

            mat[i][j] = max(match_score, ins_mat[i][j], del_mat[i][j])

    # asymetric indel?

    plt.imshow(mat[1:200, 1:200]);
    plt.colorbar()
    plt.show()
