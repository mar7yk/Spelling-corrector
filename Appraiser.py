import numpy as np
import Equalizer


class Appraiser:
    def __init__(self, alphabet, corrected_corpus, uncorrected_corpus):
        self.alphabet = alphabet
        self.operationProbs = self.computeOperationProbs(corrected_corpus, uncorrected_corpus)

    def isWord(self, word):
        for c in word:
            if c not in self.alphabet:
                return False
        return True

    def computeOperationProbs(self, corrected_corpus, uncorrected_corpus, smoothing=0.2):

        operations = {}
        operationsProb = {}
        for c in self.alphabet:
            operations[(c, '')] = smoothing  # deletions
            operations[('', c)] = smoothing  # insertions
            for s in self.alphabet:
                operations[(c, s)] = smoothing  # substitution and identity
                if c == s:
                    continue
                operations[(c + s, s + c)] = smoothing  # transposition

        for i in range(len(corrected_corpus)):
            for j in range(len(corrected_corpus[i])):
                if self.isWord(corrected_corpus[i][j]) and self.isWord(uncorrected_corpus[i][j]):
                    if corrected_corpus[i][j] == uncorrected_corpus[i][j]:
                        for c in corrected_corpus[i][j]:
                            operations[(c, c)] += 1
                    else:
                        editOperationsForWord = Equalizer.editOperations(corrected_corpus[i][j],
                                                                         uncorrected_corpus[i][j])
                        for editOperation in editOperationsForWord:
                            operations[editOperation] += 1

        totalOperations = sum([operations[i] for i in operations.keys()])

        for k in operations.keys():
            operationsProb[k] = operations[k] / totalOperations

        return operationsProb

    def operationWeight(self, a, b):

        if (a, b) in self.operationProbs.keys():
            return -np.log(self.operationProbs[(a, b)])
        else:
            print("Wrong parameters ({},{}) of operationWeight call encountered!".format(a, b))

    def editWeight(self, s1, s2):

        d = np.empty([len(s1) + 1, len(s2) + 1], dtype=float)

        max_dist = float("inf")

        d[-1, -1] = 0

        for i in range(len(s1)):
            d[i, -1] = d[i - 1, -1] + self.operationWeight(s1[i], '')

        for i in range(len(s2)):
            d[-1, i] = d[-1, i - 1] + self.operationWeight('', s2[i])

        for i in range(len(s1)):
            for j in range(len(s2)):
                t = max_dist

                if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                    t = d[i - 2, j - 2] + self.operationWeight(s1[i - 1:i + 1], s2[j - 1:j + 1])

                d[i, j] = min(
                    d[i, j - 1] + self.operationWeight('', s2[j]),  # insertion
                    d[i - 1, j] + self.operationWeight(s1[i], ''),  # deletion
                    d[i - 1, j - 1] + self.operationWeight(s1[i], s2[j]),  # substitution
                    t,  # transposition
                )

        return d[len(s1) - 1, len(s2) - 1]
