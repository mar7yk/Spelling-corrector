import unittest
import Appraiser as a
from nltk.corpus import PlaintextCorpusReader

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
            'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я']
corpus_root = './Tests/TestFiles/'
original = PlaintextCorpusReader(corpus_root, 'corpus_original.txt')
fullSentCorpusOriginal = [[w.lower() for w in sent] for sent in original.sents()]
typos = PlaintextCorpusReader(corpus_root, 'corpus_typos.txt')
fullSentCorpusTypos = [[w.lower() for w in sent] for sent in typos.sents()]

appraiser = a.Appraiser(alphabet, fullSentCorpusOriginal, fullSentCorpusTypos)

L1 = ['заявката', 'заявката', 'заявката', 'заявката', 'заявката', 'заявката']
L2 = ['заявката', 'заявьата', 'завякатва', 'заявкатаа', 'вя', 'язвката']
D = [22.75, 32.06, 35.93, 32.02, 62.03, 43.71]


class AppraiserTest(unittest.TestCase):

    def test_operationProbs_isGoodAndSmoothed(self):
        ps = [appraiser.operationProbs[k] for k in appraiser.operationProbs.keys()]
        self.assertGreater(0.2, max(ps))
        self.assertGreater(min(ps), 0.0)

    def test_operationProbs_isIDHaveMostProb(self):
        id_prob = 0
        for c in appraiser.alphabet:
            id_prob += appraiser.operationProbs[(c, c)]
        self.assertGreater(id_prob, 0.95)

    def test_editWeight(self):
        for s1, s2, d in zip(L1, L2, D):
            self.assertGreater(1, abs(appraiser.editWeight(s1, s2) - d))


if __name__ == '__main__':
    unittest.main()
