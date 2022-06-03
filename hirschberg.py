import sys
import argparse


parser = argparse.ArgumentParser(description = 'hirschberg')

#optional arguments
parser.add_argument('-t', action = "store_true")
parser.add_argument('-f', action = "store_true")
parser.add_argument('-l', action = "store_true")

#mandatory arguments
parser.add_argument('gap', type = int)
parser.add_argument('match', type = int)
parser.add_argument('differ', type = int)
parser.add_argument('a')
parser.add_argument('b')

args = parser.parse_args()

gap = args.gap
match = args.match
differ = args.differ
a = args.a
b = args.b
switch_t = args.t
switch_f = args.f
switch_l = args.l

def Swap_Array(A, B):
    for i in range(len(A)):
        temp = A[i]
        A[i] = B[i]
        B[i] = temp

def Compare(char_A, char_B):
    """a fucntion calculating the match or difference score between sequence items"""

    if char_A == char_B:
        return match
    else:
        return differ

def UpdateAlignments(WW, ZZ, Wlr, Zlr):
    WW.append(Wlr)
    ZZ.append(Zlr)

def EnumerateAlignments(A, B, F, W, Z):

    i = len(A)
    j = len(B)

    if (i == 0) and (j == 0):
        WW.append(W)
        ZZ.append(Z)
        return

    if (i > 0) and (j > 0):
        value = Compare(A[i - 1], B[i - 1])
        if F[i, j] == (F[i - 1, j - 1] + value):
            EnumerateAlignments(A[:i], B[:j], F, A[i - 1] + W, B[j - 1] + Z)
    if (i > 0) and (F[i, j] == F[i - 1] + gap):
        EnumerateAlignments(A[:i], B, F, A[i - 1] + W, '-' + Z)
    if (j > 0) and (F[i, j] == F[i, j - 1] + gap):
        EnumerateAlignments(A, B[:j], F, '-' + W, B[j - 1] + Z)

def ComputeAlignmentScore(A, B, Compare, g):
    """returns the last line of the alignment matrix"""

    L = [int] * (len(B) + 1)

    for j in range(len(L)):
        L[j] = j * g

    K = [int] * (len(B) + 1)
    for i in range(1, len(A) + 1):
        Swap_Array(L, K)
        L[0] = i * g
        for j in range(1, len(B) + 1):
            md = Compare(A[i - 1], B[j - 1])
            L[j] = max((L[j - 1] + g), (K[j] + g), (K[j - 1] + md))

    return L


def NeedlemanWunsch(A, B):

    F = [[0] * (len(A) + 1)] * (len(B) + 1)

    for i in range(len(A) + 1):
        F[0][i] = i * gap
    for i in range(len(B) + 1):
        F[i][0] = i * gap

    for i in range(1, len(A) + 1):
        for j in range(1, len(B) + 1):
            if A[i] == B[j]:
                value = match
            else:
                value = differ
            F[i][j] = max(F[i - 1, j] + gap, F[i, j - 1] + gap, F[i - 1, j - i] + value)

    W = ''
    Z = ''

    EnumerateAlignments(A, B, F, W, Z)

    print(W, Z)

def Hirschberg(A, B):
    """hirscherg"""

    if len(A) == 0:
        WW = [('–' * len(B))]
        #print("firstA WW = ", WW)
        ZZ = [B]
    elif len(B) == 0:
        WW = [A]
        print("firstB WW = ", WW)
        ZZ = [('-' * len(A))]
        print("firstB ZZ = ", ZZ)
    elif (len(A) == 1) or (len(B) == 1):
        print("hi")
        NeedlemanWunsch(A, B)
    else:
        i = int(len(A) / 2)

        print("i = ", i)

        s_left = ComputeAlignmentScore(A[:i], B, Compare, gap)
        s_right = ComputeAlignmentScore(A[-1:-(i + 1):-1], B[::-1], Compare, gap)

        #print(s_left, s_right)

        temp_max = 0
        list_len = max(i, (len(A) - i))
        S = [int] * list_len

        s_right.reverse()

        for s in range(list_len):
            S[s] = s_left[s] + s_right[s]
            if S[s] > temp_max:
                temp_max = S[s]

        J = list()
        for s in range(list_len):
            if S[s] == temp_max:
                J.append(s)

        WW = list()
        ZZ = list()

        for j in J:
            list_1 = Hirschberg(A[:i], B[:j])
            list_2 = Hirschberg(A[i:], B[j:])

            print("lists = ", list_1, list_2)

            UpdateAlignments(WW, ZZ, list_1[0] + list_2[0], list_1[1] + list_2[1])

    return [WW, ZZ]

#main program body
WW_final = list()
ZZ_final = list()

if switch_f == True:
    pass

final = Hirschberg(a, b)
WW_final = final[0]
ZZ_final = final[1]
print("final = ", WW_final, ZZ_final)
