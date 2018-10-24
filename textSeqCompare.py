import numpy as np
import matplotlib.pyplot as plt

def read_file(fname):
    file = open(fname, 'r', encoding='utf8')
    lines = file.readlines()
    file.close()
    lines = ' '.join(lines)
    lines = lines.replace('\n', '')
    return lines


# scoring system
match = 5
mismatch = -5
gap_open = -3
gap_extend = -3

gap_open_x = -10
gap_extend_x = -5
gap_open_y = -5
gap_extend_y = -2

# display length
line_len = 90

if __name__ == '__main__':
    files = ['einsiedeln_001r', 'einsiedeln_001v', 'einsiedeln_002r',
        'einsiedeln_002v', 'einsiedeln_003r', 'einsiedeln_003v']

    item = files[5]
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

            # update main matrix (for matches)
            match_score = match if transcript[i-1] == ocr[j-1] else mismatch
            mat_vals = [mat[i-1][j-1], x_mat[i-1][j-1], y_mat[i-1][j-1]]
            mat[i][j] = max(mat_vals) + match_score
            mat_ptr[i][j] = int(mat_vals.index(max(mat_vals)))

            # update matrix for y gaps
            y_mat_vals = [mat[i][j-1] + gap_open_y + gap_extend_y,
                        x_mat[i][j-1] + gap_open_y + gap_extend_y,
                        y_mat[i][j-1] + gap_extend_y]

            y_mat[i][j] = max(y_mat_vals)
            y_mat_ptr[i][j] = int(y_mat_vals.index(max(y_mat_vals)))

            # update matrix for x gaps
            x_mat_vals = [mat[i-1][j] + gap_open_x + gap_extend_x,
                        x_mat[i-1][j] + gap_extend_x,
                        y_mat[i-1][j] + gap_open_x + gap_extend_x]

            x_mat[i][j] = max(x_mat_vals)
            x_mat_ptr[i][j] = x_mat_vals.index(max(x_mat_vals))

    # asymetric indel?

    # TRACEBACK
    # current matrix we're in tells us which direction to head back (diagonally, y, or x)
    # value of pointer matrix tells us which matrix to go to (mat, y_mat, or x_mat)
    # mat of 0 = match, 1 = x gap, 2 = y gap
    tra_align = ''
    ocr_align = ''
    align_record = ''
    xpt = len(transcript) - 1
    ypt = len(ocr) - 1
    mpt = 0

    while(xpt >= 0 and ypt >= 0):
        if mpt == 0:
            tra_align += transcript[xpt]
            ocr_align += ocr[ypt]
            align_record += 'O' if(transcript[xpt] == ocr[ypt]) else 'X'

            mpt = mat_ptr[xpt][ypt]
            xpt -= 1
            ypt -= 1

        elif mpt == 1:
            tra_align += transcript[xpt]
            ocr_align += '_'
            align_record += ' '
            mpt = x_mat_ptr[xpt][ypt]
            xpt -= 1

        elif mpt == 2:
            tra_align += '_'
            ocr_align += ocr[ypt]
            align_record += ' '
            mpt = y_mat_ptr[xpt][ypt]
            ypt -= 1

        # print(mpt, xpt, ypt)

    tra_align = tra_align[::-1]
    ocr_align = ocr_align[::-1]
    align_record = align_record[::-1]

    for n in range(int(np.ceil(len(tra_align) / line_len))):
        start = n * line_len
        end = (n + 1) * line_len
        print(tra_align[start:end])
        print(ocr_align[start:end])
        print(align_record[start:end] + '\n')

    # plt.imshow(x_mat_ptr[1:200, 1:200])
    # plt.colorbar()
    # plt.show()
