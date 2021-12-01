import CandidateGenerator as cg


class SpellingCorrector:

    def __init__(self, alphabet, corrected_corpus, uncorrected_corpus):
        self.candidateGenerator = cg.CandidateGenerator(alphabet, corrected_corpus, uncorrected_corpus)

    def correctSpelling(self, r):

        c = []

        for row in r:
            c.append([])
            cRow = c[-1]

            for word in row:
                cWord = word

                candidates = self.candidateGenerator.generateCandidates(word)
                minWeight = float("inf")
                for candidate in candidates:
                    weight = candidate[1]
                    if weight < minWeight:
                        minWeight = weight
                        cWord = candidate[0]

                cRow.append(cWord)

        return c
