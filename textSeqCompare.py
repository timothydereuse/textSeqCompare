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
gap_open = -5
gap_extend = -1

if __name__ == '__main__':
    files = ['einsiedeln_001r', 'einsiedeln_001v', 'einsiedeln_002r',
        'einsiedeln_002v', 'einsiedeln_003r', 'einsiedeln_003v']

    item = files[4]
    transcript = read_file('./txt/' + item + '_transcript.txt')
    ocr = read_file('./txt/' + item + '_ocr.txt')

    # y_mat and x_mat keep track of gaps in horizontal and vertical directions
    mat = np.zeros((len(transcript), len(ocr)))
    y_mat = np.zeros((len(transcript), len(ocr)))
    x_mat = np.zeros((len(transcript), len(ocr)))
    mat_ptr = np.zeros((len(transcript), len(ocr)))
    y_mat_ptr = np.zeros((len(transcript), len(ocr)))
    x_mat_ptr = np.zeros((len(transcript), len(ocr)))

    for i in range(len(transcript)):
        mat[i][0] = gap_extend * i
        y_mat[i][0] = gap_extend * i
        x_mat[i][0] = -1000000
    for j in range(len(ocr)):
        mat[0][j] = gap_extend * j
        x_mat[0][j] = gap_extend * i
        y_mat[0][j] = -1000000

    for i in range(1, len(transcript)):
        for j in range(1, len(ocr)):

            match_score = match if transcript[i-1] == ocr[j-1] else mismatch
            mat_vals = [mat[i-1][j-1], x_mat[i-1][j-1], y_mat[i-1][j-1]]
            mat[i][j] = max(mat_vals) + match_score
            mat_ptr[i][j] = mat_vals.index(max(mat_vals))

            y_mat_vals = [mat[i][j-1] + gap_open + gap_extend,
                        x_mat[i][j-1] + gap_open + gap_extend,
                        y_mat[i][j-1] + gap_extend]

            y_mat[i][j] = max(y_mat_vals)
            y_mat_ptr[i][j] = y_mat_vals.index(max(y_mat_vals))

            x_mat_vals = [mat[i-1][j] + gap_open + gap_extend,
                        x_mat[i-1][j] + gap_extend,
                        y_mat[i-1][j] + gap_open + gap_extend]

            x_mat[i][j] = max(x_mat_vals)
            x_mat_ptr[i][j] = x_mat_vals.index(max(x_mat_vals))

    # asymetric indel?

    plt.imshow(mat[1:200, 1:200])
    plt.colorbar()
    plt.show()

    # TRACEBACK
    # current matrix we're in tells us which direction to head back (diagonally, y, or x)
    # value of pointer matrix tells us which matrix to go to (mat, y_mat, or x_mat)
    tra_align = ''
    ocr_align = ''
    xpt = len(transcript) - 1
    ypt = len(ocr) - 1

    while(xpt > 0 or ypt > 0):
        if(xpt > 0 and ypt > 0):
            val_to_match = val[i-1][j-1]
            if transcript[i-1] == ocr[j-1]:
                val_to_match += match
            else:
                val_to_match += mismatch

            if mat[i][j] == val_to_match:
                tra_align += transcript[i-1]
