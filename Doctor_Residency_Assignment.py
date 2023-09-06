import random
import numpy as np


# rate all
# "tie" is allowed
# there are more or less doctors than slots  # only more


# mark starred 0's position in M matrix (M->Mark)


class HM:
    def __init__(self):
        self.matrix = None
        self.row_cancelled = []
        self.col_cancelled = []
        self.n = 0
        self.Z0_r = 0
        self.Z0_c = 0
        self.diff = 0
        self.step = 0  # FIX
        self.sum_matrix = -1

    def calculate(self):
        r = len(self.matrix)
        c = len(self.matrix[0])
        R_v = np.zeros(r)
        cancel_count = 0
        # zeroexist = True
        # print(c)
        self.diff = r - c
        # add columns filled with zero when the number of doctor is bigger
        if self.diff > 0:
            for i in range(self.diff):
                self.matrix = np.c_[self.matrix, R_v.T]

        # create matrix and vector with all elements being zero
        self.n = len(self.matrix[0])
        self.row_cancelled = [False for i in range(self.n)]
        self.col_cancelled = [False for j in range(self.n)]

        # set capacity of hospital
        # cap = r//c
        # if r%c > 0:
        #     cap+=1

        # find the minimum number in each row,and make every elements in this row minus this number

    def makecancelrow(self, M):
        # make cancel based on row, column is actually cancelled here
        n = self.n
        m = self.matrix
        # print(m)
        cancel_count_col = 0

        for i in range(n):
            # Z_r = 0
            # Z_c = 0
            r_count0 = 0
            for j in range(n):
                # print(m[i][j])
                # print(self.col_cancelled[3]) # FIX
                if (
                    m[i][j] - 0 < 0.001
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    r_count0 += 1
                    # print(r_count0) # FIX

            if r_count0 == 1:

                for j in range(n):
                    if self.matrix[i][j] - 0 < 0.001 and (
                        not self.col_cancelled[j]
                    ):  # FIX
                        M[i][j] = 1

                        self.col_cancelled[j] = True

                        cancel_count_col += 1

        # print(M)
        return cancel_count_col, M

    def makecancelcol(self, M):
        n = self.n

        cancel_count_row = 0
        for j in range(n):
            # Z_r = 0
            # Z_c = 0
            c_count0 = 0
            for i in range(n):
                if (
                    self.matrix[i][j] - 0 < 0.001
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    c_count0 += 1
            if c_count0 == 1:
                for i in range(n):
                    if self.matrix[i][j] - 0 < 0.001 and (
                        not self.row_cancelled[i]
                    ):  # FIX
                        # print(Z_r)
                        self.row_cancelled[i] = True
                        M[i][j] = 1
                        cancel_count_row += 1

        # print(cancel_count_row)
        # print(M)
        return cancel_count_row, M

    # determine whether there is uncancelled zero in matrix
    def find0(self):
        n = self.n
        print("probe8")
        zerostatus = False
        for i in range(n):
            for j in range(n):
                if (
                    self.matrix[i][j] - 0 < 0.001
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    # FIX
                    zerostatus = True
                    break
                # else:
                # zerostatus = False
                # break
            # zerostatus = False  # FIX
        return zerostatus

    def changematrix(self):
        n = self.n
        minim = self.matrix[0][0]
        for i in range(n):
            for j in range(n):
                if (
                    self.matrix[i][j] < minim
                    and self.matrix[i][j] != 0
                    and (not self.col_cancelled[j])
                    and (not self.row_cancelled[i])
                ):
                    minim = self.matrix[i][j]

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

    def random_assign(self, M_a):
        print("probe10")
        n = self.n
        m = M_a
        M = np.zeros((n, n))
        row_cancelled = [False for i in range(n)]
        count = [0 for i in range(n - self.diff)]
        for j in range(n - self.diff):
            for i in range(n):
                if m[i][j] - 0 < 0.001:
                    count[j] += 1
        count = np.array(count)
        order = count.argsort()
        # order = np.flip(order)
        rowlist = []
        for i in range(n):
            rowlist.append(i)
        for j in order:
            zerolist = []
            print(j)
            for i in range(n):
                if m[i][j] < 0.001 and (i in rowlist):
                    zerolist.append(i)
            random.shuffle(zerolist)
            i = zerolist[0]
            print(zerolist)
            rowlist.remove(i)

            M[i][j] = 1
            print(M)

        return M

    def initialmatrix(self):
        n = self.n
        row_sums = self.matrix.sum(axis=1)
        self.matrix = self.matrix / row_sums[:, np.newaxis]
        minv = []
        for j in range(n):
            m = self.matrix[0][j]
            minv.append(m)
        for j in range(n):
            for i in range(n):
                if self.matrix[i][j] < minv[j] and self.matrix[i][j] != 0:
                    minv[j] = self.matrix[i][j]
        for i in self.matrix:
            for j in range(len(i) - self.diff):  # potential bug
                i[j] = i[j] - minv[j]

    def clear_cancels(self):
        for i in range(len(self.row_cancelled)):
            self.col_cancelled[i] = False
            self.row_cancelled[i] = False

    def main(self, matrix):
        self.matrix = matrix
        self.calculate()
        # diagnose
        print(self.step)
        print(self.matrix)
        print(self.row_cancelled)
        print(self.col_cancelled)
        n = self.n
        cancel_count = 0
        cancel_count1 = 0
        M = np.zeros((n, n))
        self.initialmatrix()
        # diagnose
        recordM = np.copy(self.matrix)

        self.step += 1
        print("probe 1")
        print(self.step)
        print(self.matrix)
        print(self.row_cancelled)
        print(self.col_cancelled)
        cancel_count_row, M = self.makecancelrow(M)
        # diagnose
        print(self.step)
        print(M)
        print(self.row_cancelled)
        print(self.col_cancelled)
        cancel_count_col, M = self.makecancelcol(M)
        # diagnose
        print(self.step)
        print(M)
        print(self.row_cancelled)
        print(self.col_cancelled)
        cancel_count = cancel_count + cancel_count_col + cancel_count_row
        # diagnose

        print(self.step)
        print(self.matrix)
        # print(self.matrix)
        # print(self.matrix)
        # minvl = []
        # for i in matrix:
        #     minv = i[0]
        #     for j in range(len(i)):
        #         if i[j] < minv and i[j] != 0:
        #             minv = i[j]
        #     for j in range(len(i)-diff):
        #         i[j] = i[j] - minv
        # print(M)
        zeroexist = self.find0()
        print(zeroexist)
        # print(self.matrix)
        # cancel columns and rows with only one zero one by one
        while zeroexist:  # potential error
            cancel_count_row, M = self.makecancelrow(M)
            # diagnose
            # print("probe7")
            self.step += 1
            print("probe 2")
            print(self.step)
            print(M)
            print(self.row_cancelled)
            print(self.col_cancelled)
            cancel_count_col, M = self.makecancelcol(M)
            # diagnose
            print(self.step)
            print(M)
            print(self.row_cancelled)
            print(self.col_cancelled)
            cancel_count0 = cancel_count1
            cancel_count1 = cancel_count1 + cancel_count_col + cancel_count_row
            if cancel_count1 == cancel_count0:
                break
            # diagnose
            print(self.step)
            print(self.matrix)
        # count cancel, if cancels = n, then game over, otherwise we should continue
        cancel_count = cancel_count + cancel_count1
        # print(cancel_count)
        if cancel_count < n:
            done = False
            self.changematrix()

            # diagnose
            self.step += 1
            print("probe 3")
            print(self.step)
            print(self.matrix)

        else:
            done = True
        # print(self.matrix)
        while not done:
            # print(self.matrix)
            self.clear_cancels()
            M = np.zeros((self.n, self.n))  # FIX
            cancel_count_row, M = self.makecancelrow(M)
            # diagnose
            self.step += 1
            print("probe 4")
            print(self.step)
            print(self.matrix)
            print(M)
            print(self.row_cancelled)
            print(self.col_cancelled)
            cancel_count_col, M = self.makecancelcol(M)
            self.step += 1
            print("probe 5")
            # diagnose
            print(self.step)
            print(self.matrix)
            print(M)
            print(self.row_cancelled)
            print(self.col_cancelled)
            # print(self.matrix)
            zeroexist = self.find0()
            # print(self.matrix)
            cancel_count = cancel_count_row + cancel_count_col
            # print(M)
            cancel_count1 = 0
            print(zeroexist)

            # diagnose
            print(self.step)
            print(self.matrix)
            # cancel columns and rows with only one zero one by one
            while zeroexist:
                print("probe 6")
                cancel_count_row, M = self.makecancelrow(M)
                # diagnose
                self.step += 1
                print(self.step)
                print(M)
                print(self.row_cancelled)
                print(self.col_cancelled)
                cancel_count_col, M = self.makecancelcol(M)
                # diagnose
                print(self.step)
                print(M)
                print(self.row_cancelled)
                print(self.col_cancelled)
                zeroexist = self.find0()
                # print(zeroexist)
                # print(cancel_count)
                cancel_count0 = cancel_count1
                cancel_count1 = cancel_count1 + cancel_count_col + cancel_count_row
                if cancel_count1 == cancel_count0:
                    break
                # diagnose
                print(self.step)
                print(self.matrix)
            cancel_count = cancel_count + cancel_count1
            # print(cancel_count)
            if cancel_count == n:
                done = True
            else:
                done = False
                # m0 = np.matrix(self.matrix)
                # s0 = np.sum(m0)
                self.changematrix()
                # m = np.matrix(self.matrix)
                # s1 = np.sum(m)
                # print(s0)
                if zeroexist:

                    M = self.random_assign(recordM)
                    print("probe22")
                    print(recordM)
                    print(self.matrix)
                    print(M)
                    break

                # diagnose
                self.step += 1
                print(self.step)
                print(self.matrix)

        return M


if __name__ == "__main__":
    # 矩阵输入
    # 注释
    # assessment

    Matrix = [[1, 1, 3], [1, 2, 7], [1, 2, 3], [1, 2, 3]]
    result = HM().main(Matrix)
    print(result)
