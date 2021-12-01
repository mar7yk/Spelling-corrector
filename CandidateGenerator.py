import Appraiser as a


def extractDictionary(corpus):
    dictionary = set()
    for doc in corpus:
        for w in doc:
            if w not in dictionary:
                dictionary.add(w)
    return dictionary


class CandidateGenerator:
    def __init__(self, alphabet, corrected_corpus, uncorrected_corpus):
        self.alphabet = alphabet
        self.dictionary = extractDictionary(corrected_corpus)
        self.appraiser = a.Appraiser(alphabet, corrected_corpus, uncorrected_corpus)

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

        if not self.appraiser.isWord(query) or query in self.dictionary:
            return set()

        candidates = set()
        if query in self.dictionary:
            weight = self.appraiser.editWeight(query, query)
            candidates.add((query, weight))

        def isInCandidates(edit):
            for c in candidates:
                if edit == c[0]:
                    return True
            return False

        oneEdits = self.generateEdits(query)
        for oneEdit in oneEdits:
            if oneEdit in self.dictionary:
                weight = self.appraiser.editWeight(query, oneEdit) - 1
                candidates.add((oneEdit, weight))

        for oneEdit in oneEdits:
            for twoEdit in self.generateEdits(oneEdit):
                if twoEdit in self.dictionary and not isInCandidates(twoEdit):
                    weight = self.appraiser.editWeight(query, twoEdit) - 2
                    candidates.add((twoEdit, weight))

        return candidates
