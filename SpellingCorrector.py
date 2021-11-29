import numpy as np

def editOperations(s1, s2):

    d = [[None for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]

    d[-1][-1] = [0, None]

    for i in range(len(s1)):
        d[i][-1] = (i + 1, ((i - 1, -1), (s1[i], '')))

    for i in range(len(s2)):
        d[-1][i] = (i + 1, ((-1, i - 1), ('', s2[i])))

    max_dist = max(len(s1), len(s2))

    for i in range(len(s1)):
        for j in range(len(s2)):
            tLen = max_dist
            cost = 1

            if s1[i] == s2[j]:
                cost = 0
            elif i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                tLen = d[i - 2][j - 2][0]

            insertionKey = d[i][j - 1][0] + 1
            deletionKey = d[i - 1][j][0] + 1
            substitutionKey = d[i - 1][j - 1][0] + cost
            transpositionKey = tLen + 1

            options = {
                insertionKey: ((i, j - 1), ('', s2[j])),
                deletionKey: ((i - 1, j), (s1[i], '')),
                substitutionKey: ((i - 1, j - 1), (s1[i], s2[j])),
                transpositionKey: ((i - 2, j - 2), (s1[i - 1] + s1[i], s2[j - 1] + s2[j])),
            }

            key = min(
                insertionKey,
                deletionKey,
                substitutionKey,
                transpositionKey,
            )

            d[i][j] = (key, options[key])

    result = []

    curr = d[len(s1) - 1][len(s2) - 1][1]

    while curr != None:
        result.insert(0, curr[1])
        curr = d[curr[0][0]][curr[0][1]][1]

    return result


def extractDictionary(corpus):
    dictionary = set()
    for doc in corpus:
        for w in doc:
            if w not in dictionary:
                dictionary.add(w)
    return dictionary


class Corrector:

    def __init__(self, alphabet, corrected_corpus, uncorrected_corpus):
        self.alphabet = alphabet
        self.dictionary = extractDictionary(corrected_corpus)
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

        #############################################################################
        #### Начало на Вашия код.

        for i in range(len(corrected_corpus)):
            for j in range(len(corrected_corpus[i])):
                if self.isWord(corrected_corpus[i][j]) and self.isWord(uncorrected_corpus[i][j]):
                    if corrected_corpus[i][j] == uncorrected_corpus[i][j]:
                        for c in corrected_corpus[i][j]:
                            operations[(c, c)] += 1
                    else:
                        editOperationsForWord = editOperations(corrected_corpus[i][j], uncorrected_corpus[i][j])
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

                if s1[i] == s2[j]:
                    cost = 0
                elif i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                    t = d[i - 2, j - 2] + self.operationWeight(s1[i - 1:i + 1], s2[j - 1:j + 1])

                d[i, j] = min(
                    d[i, j - 1] + self.operationWeight('', s2[j]),  # insertion
                    d[i - 1, j] + self.operationWeight(s1[i], ''),  # deletion
                    d[i - 1, j - 1] + self.operationWeight(s1[i], s2[j]),  # substitution
                    t,  # transposition
                )

        return d[len(s1) - 1, len(s2) - 1]

    def generateEdits(self, q):

        edits = {q}

        # insertions
        for i in range(len(q) + 1):
            for letter in self.alphabet:
                edits.add(q[:i] + letter + q[i:])

        # deletions
        for i in range(1, len(q) + 1):
            edits.add(q[:i - 1] + q[i:])

        # substitution and identity
        for i in range(len(q)):
            for letter in self.alphabet:
                edits.add(q[:i] + letter + q[i + 1:])

        # transposition
        for i in range(1, len(q)):
            edits.add(q[:i - 1] + q[i] + q[i - 1] + q[i + 1:])

        edits.remove(q)

        return edits

    def generateCandidates(self, query):
        ### Започва от заявката query и генерира всички низове НА РАЗСТОЯНИЕ <= 2, за да се получат кандидатите за корекция. Връщат се единствено кандидати, които са в речника dictionary.

        ### Вход:
        ###     Входен низ query
        ###     Речник с допустими (правилни) думи: dictionary
        ###     речник с вероятностите на елементарните операции.

        ### Изход:
        ###     Списък от двойки (candidate, candidate_edit_log_probability), където candidate е низ на кандидат, а candidate_edit_log_probability е логаритъм от вероятността за редакция -- минус теглото.

        #############################################################################
        #### Начало на Вашия код. На мястото на pass се очакват 10-15 реда

        candidates = set()
        if query in self.dictionary:
            weight = self.editWeight(query, query)
            candidates.add((query, weight))

        def isInCandidates(edit):
            for c in candidates:
                if edit == c[0]:
                    return True
            return False

        oneEdits = self.generateEdits(query)
        for oneEdit in oneEdits:
            if oneEdit in self.dictionary:
                weight = self.editWeight(query, oneEdit) - 1
                candidates.add((oneEdit, weight))

        for oneEdit in oneEdits:
            for twoEdit in self.generateEdits(oneEdit):
                if twoEdit in self.dictionary and not isInCandidates(twoEdit):
                    weight = self.editWeight(query, twoEdit) - 2
                    candidates.add((twoEdit, weight))

        return candidates

    def correctSpelling(self, r):

        c = []

        for row in r:
            c.append([])
            cRow = c[-1]

            for word in row:
                if self.isWord(word) and word not in self.dictionary:
                    candidates = self.generateCandidates(word)
                    cWord = word
                    minWeight = float("inf")
                    for candidate in candidates:
                        weight = candidate[1]
                        if weight < minWeight:
                            minWeight = weight
                            cWord = candidate[0]
                    cRow.append(cWord)
                else:
                    cRow.append(word)

        return c
