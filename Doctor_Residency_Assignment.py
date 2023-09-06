import random
import numpy as np


class HM:
    """
    initialize the matrix of ratings
    """

    def __init__(self):
        self.matrix = None
        self.row_cancelled = []
        self.col_cancelled = []
        self.n = 0
        self.diff = 0

    """
    reshape the matrix to a squared one by filling zeros
    """

    def calculate(self):
        r = len(self.matrix)
        c = len(self.matrix[0])
        r_v = np.zeros(r)
        self.diff = r - c

        # add columns filled with zero when the number of doctor is bigger
        if self.diff > 0:
            for i in range(self.diff):
                self.matrix = np.c_[self.matrix, r_v.T]

        # create assignment matrix and cancellation vector with all elements being zero
        self.n = len(self.matrix[0])
        self.row_cancelled = [False for i in range(self.n)]
        self.col_cancelled = [False for j in range(self.n)]

    """
    cancel(mask) the corresponding column when there is a single uncancelled zero in the row
    
    @:param M: a numpy array of integers for doctor assignment (0 - unassigned, 1 - assignment) 
    
    @:return cancel_count_col: number of columns cancelled during this process
    @:return M: updated assignment array
    """

    def makecancelrow(self, M):
        n = self.n
        m = self.matrix
        cancel_count_col = 0

        for i in range(n):

            # count the number of uncancelled zero(s) in the row
            r_count0 = 0
            for j in range(n):
                if (
                    np.abs(m[i][j]) < 0.001
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    r_count0 += 1

            # if there is exactly one uncanceled zero
            # cancel the column of the uncancelled zero and mark the zero as an assignment
            if r_count0 == 1:
                for j in range(n):
                    if np.abs(m[i][j]) < 0.001 and (not self.col_cancelled[j]):
                        M[i][j] = 1
                        self.col_cancelled[j] = True
                        cancel_count_col += 1

        return cancel_count_col, M

    """
    cancel(mask) the corresponding row when there is a single uncancelled zero in the column

    @:param M: a numpy array of integers for doctor assignment (0 - unassigned, 1 - assignment) 

    @:return cancel_count_row: number of rows cancelled during this process
    @:return M: updated assignment array
    """

    def makecancelcol(self, M):
        n = self.n
        m = self.matrix
        cancel_count_row = 0

        for j in range(n):

            # count the number of uncancelled zero(s) in the column
            c_count0 = 0
            for i in range(n):
                if (
                    np.abs(m[i][j]) < 0.001
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    c_count0 += 1

            # if there is exactly one uncanceled zero
            # cancel the row of the uncancelled zero and mark the zero as an assignment
            if c_count0 == 1:
                for i in range(n):
                    if np.abs(m[i][j]) < 0.001 and (not self.row_cancelled[i]):
                        self.row_cancelled[i] = True
                        M[i][j] = 1
                        cancel_count_row += 1

        return cancel_count_row, M

    """
    determine whether there is uncancelled zero in matrix, which indicates incomplete assignment
    
    @:return zerostatus: True if there is uncancelled zero in the matrix, False otherwise
    """

    def find0(self):
        n = self.n
        zerostatus = False
        for i in range(n):
            for j in range(n):
                if (
                    np.abs(self.matrix[i][j]) < 0.001
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    zerostatus = True
                    break
        return zerostatus

    """
    during the assignment process, subtract the uncancelled elements by the smallest one
    if there is an element cancelled twice, add the smallest uncancelled element to that position
    """

    def changematrix(self):
        n = self.n
        minim = self.matrix[0][0]

        # Find the smallest uncancelled element
        for i in range(n):
            for j in range(n):
                if (
                    self.matrix[i][j] < minim
                    and self.matrix[i][j] != 0
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    minim = self.matrix[i][j]

        # subtract all uncancelled element by the smallest one, add the value to double-cancelled elements
        for i in range(n):
            for j in range(n):
                if (
                    self.matrix[i][j] != 0
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    self.matrix[i][j] = self.matrix[i][j] - minim
                if self.col_cancelled[j] and self.row_cancelled[i]:
                    self.matrix[i][j] += minim

    """
    random assign doctors to residential positions when there are multiple uncancelled zeros (extreme preference) to
    the same position
    
    @:param M_a: current rating array
    
    @:return M: assignment array after random assignment
    """

    def random_assign(self, M_a):
        n = self.n
        m = M_a
        M = np.zeros((n, n))
        count = [0 for i in range(n - self.diff)]

        # count and rank the number of uncancelled zeros (pending assignment) for each column (hospital)
        for j in range(n - self.diff):
            for i in range(n):
                if np.abs(m[i][j]) < 0.001:
                    count[j] += 1
        count = np.array(count)
        order = count.argsort()
        rowlist = []
        for i in range(n):
            rowlist.append(i)

        # beginning with the column with the fewest number of conflict, randomly assign candidates with uncancelled
        # zero to the hospital
        for j in order:
            zerolist = []
            for i in range(n):
                if np.abs(m[i][j]) < 0.001 and (i in rowlist):
                    zerolist.append(i)
            random.shuffle(zerolist)
            i = zerolist[0]
            rowlist.remove(i)
            M[i][j] = 1

        return M

    """
    initialize the rating array based on raw data, including:
        1. normalization by row
        2. column reduction
    """

    def initialmatrix(self):
        # normalize the rating of each row
        n = self.n
        row_sums = self.matrix.sum(axis=1)
        self.matrix = self.matrix / row_sums[:, np.newaxis]

        # column reduction by subtracting the smallest column entry from each element in the column
        minv = []
        for j in range(n):
            m = self.matrix[0][j]
            minv.append(m)
        for j in range(n):
            for i in range(n):
                if self.matrix[i][j] < minv[j] and self.matrix[i][j] != 0:
                    minv[j] = self.matrix[i][j]
        for i in self.matrix:
            for j in range(len(i) - self.diff):
                i[j] = i[j] - minv[j]

    """
    clear zero cancellation after each attempt of zero cancellation
    """

    def clear_cancels(self):
        for i in range(len(self.row_cancelled)):
            self.col_cancelled[i] = False
            self.row_cancelled[i] = False

    """
    main function that takes an array of raw rating, process it according to the Hungarian algorithm
    
    @:param matrix: array that contains raw data of rating from each candidate on the hospitals
    
    @:return M: an assignment matrix that for each entry of '1', assign the candidate in the row to the hospital 
                in the column
    """

    def main(self, matrix):
        # initialize processing on the raw data, check if assignment can be made from this first step
        self.matrix = matrix
        self.calculate()
        n = self.n
        diff = self.diff  # FIXED
        cancel_count = 0
        cancel_count1 = 0
        M = np.zeros((n, n))
        self.initialmatrix()
        recordM = np.copy(self.matrix)
        cancel_count_row, M = self.makecancelrow(M)
        cancel_count_col, M = self.makecancelcol(M)
        cancel_count = cancel_count + cancel_count_col + cancel_count_row
        zeroexist = self.find0()

        # cancel columns and rows with exactly one uncancelled zero as long as cancellation can be made
        while zeroexist:
            cancel_count_row, M = self.makecancelrow(M)
            cancel_count_col, M = self.makecancelcol(M)

            # keep track of number of zeros being cancelled; if the number does not change, the program enters an
            # infinite loop and shall break from the cancellation process
            cancel_count0 = cancel_count1
            cancel_count1 = cancel_count1 + cancel_count_col + cancel_count_row
            if cancel_count1 == cancel_count0:
                break

        # count cancel
        # if number of zero cancellation matches the number of hospitals, the assignment is completed
        # otherwise continue with reduction and cancellation
        cancel_count = cancel_count + cancel_count1
        if cancel_count < (n - diff):  # FIXED
            done = False
            self.changematrix()
        else:
            done = True

        # repetitively perform matrix reduction and row/column cancellation when the assignment is incomplete
        while not done:
            self.clear_cancels()
            M = np.zeros((self.n, self.n))
            cancel_count_row, M = self.makecancelrow(M)
            cancel_count_col, M = self.makecancelcol(M)
            zeroexist = self.find0()
            cancel_count = cancel_count_row + cancel_count_col
            cancel_count1 = 0

            # cancel columns and rows with exactly one uncancelled zero as long as cancellation can be made
            while zeroexist:
                cancel_count_row, M = self.makecancelrow(M)
                cancel_count_col, M = self.makecancelcol(M)
                zeroexist = self.find0()
                cancel_count0 = cancel_count1
                cancel_count1 = cancel_count1 + cancel_count_col + cancel_count_row
                if cancel_count1 == cancel_count0:
                    break
            cancel_count = cancel_count + cancel_count1

            # check if assignment is completed; if so, then return the assignment
            # otherwise there are multiple uncancelled zeros in the same column, retrieve the first processed matrix
            # and randomly make assignments for the uncancelled zeros
            if cancel_count == (n - diff): # FIXED
                done = True
            else:
                done = False
                self.changematrix()
                if zeroexist:
                    M = self.random_assign(recordM)
                    break

        return M


if __name__ == "__main__":
    # 矩阵输入
    # 注释 DONE
    # assessment

    Matrix = [[1, 1, 3], [1, 2, 7], [1, 2, 3], [1, 2, 3]]
    result = HM().main(Matrix)
    print(result)
