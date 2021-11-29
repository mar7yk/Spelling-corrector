import unittest
import SpellingCorrector as sc
from nltk.corpus import PlaintextCorpusReader

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у',
            'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я']

corpus_root = '.'
original = PlaintextCorpusReader(corpus_root, 'corpus_original.txt')
fullSentCorpusOriginal = [[w.lower() for w in sent] for sent in original.sents()]
typos = PlaintextCorpusReader(corpus_root, 'corpus_typos.txt')
fullSentCorpusTypos = [[w.lower() for w in sent] for sent in typos.sents()]
Corrector = sc.Corrector(alphabet, fullSentCorpusOriginal, fullSentCorpusTypos)

L1 = ['заявката', 'заявката', 'заявката', 'заявката', 'заявката', 'заявката']
L2 = ['заявката', 'заявьата', 'завякатва', 'заявкатаа', 'вя', 'язвката']
O = [[('з', 'з'), ('а', 'а'), ('я', 'я'), ('в', 'в'), ('к', 'к'), ('а', 'а'), ('т', 'т'), ('а', 'а')],
          [('з', 'з'), ('а', 'а'), ('я', 'я'), ('в', 'в'), ('к', 'ь'), ('а', 'а'), ('т', 'т'), ('а', 'а')],
          [('з', 'з'), ('а', 'а'), ('яв', 'вя'), ('к', 'к'), ('а', 'а'), ('т', 'т'), ('', 'в'), ('а', 'а')],
          [('з', 'з'), ('а', 'а'), ('я', 'я'), ('в', 'в'), ('к', 'к'), ('а', 'а'), ('т', 'т'), ('', 'а'),
           ('а', 'а')]]
D = [22.75, 32.06, 35.93, 32.02, 62.03, 43.71]


class SpellingCorrectorTest(unittest.TestCase):

    def test_editOperations(self):
        for s1, s2, o in zip(L1, L2, O):
            self.assertEqual(sc.editOperations(s1,s2), o)

    def test_operationProbs_isGoodAndSmoothed(self):
        ps = [Corrector.operationProbs[k] for k in Corrector.operationProbs.keys()]
        self.assertGreater(0.2, max(ps))
        self.assertGreater(min(ps), 0.0)

    def test_operationProbs_isIDHaveМostProb(self):
        id_prob = 0
        for c in Corrector.alphabet:
            id_prob += Corrector.operationProbs[(c, c)]
        self.assertGreater(id_prob, 0.95)

    def test_editWeight(self):
        for s1, s2, d in zip(L1, L2, D):
            self.assertGreater(1, abs(Corrector.editWeight(s1, s2) - d))

    def test_generateEdits(self):
        self.assertEqual(len(Corrector.generateEdits("тест")), 269)

    def test_generateCandidates(self):
        self.assertEqual(len(Corrector.generateCandidates("такяива")), 4)

    def test_correctSpelling(self):
        corr = Corrector.correctSpelling(fullSentCorpusTypos[3668:3669])
        self.assertEqual(' '.join(corr[0]), 'третата група ( нареченската ) бе ударила на камък : поради курортния '
                                            'характер на селото пръчовете от наречен били още миналата година '
                                            'премахнати , защото замърсявали околната среда със силната си миризма и '
                                            'създавали у чужденците впечатление за първобитност .', "Коригираната "
                                                                                                    "заявка следва да "
                                                                                                    "е 'третата група "
                                                                                                    "( нареченската ) "
                                                                                                    "бе ударила на "
                                                                                                    "камък : поради "
                                                                                                    "курортния "
                                                                                                    "характер на "
                                                                                                    "селото пръчовете "
                                                                                                    "от наречен били "
                                                                                                    "още миналата "
                                                                                                    "година "
                                                                                                    "премахнати , "
                                                                                                    "защото "
                                                                                                    "замърсявали "
                                                                                                    "околната среда "
                                                                                                    "със силната си "
                                                                                                    "миризма и "
                                                                                                    "създавали у "
                                                                                                    "чужденците "
                                                                                                    "впечатление за "
                                                                                                    "първобитност .'.")


if __name__ == '__main__':

    unittest.main()
