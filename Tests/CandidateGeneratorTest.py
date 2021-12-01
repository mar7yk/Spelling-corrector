import unittest
import CandidateGenerator as cg
from nltk.corpus import PlaintextCorpusReader

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
            'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я']

corpus_root = './Tests/TestFiles/'
original = PlaintextCorpusReader(corpus_root, 'corpus_original.txt')
fullSentCorpusOriginal = [[w.lower() for w in sent] for sent in original.sents()]
typos = PlaintextCorpusReader(corpus_root, 'corpus_typos.txt')
fullSentCorpusTypos = [[w.lower() for w in sent] for sent in typos.sents()]

candidateGenerator = cg.CandidateGenerator(alphabet, fullSentCorpusOriginal, fullSentCorpusTypos)


class CandidateGeneratorTest(unittest.TestCase):

    def test_generateEdits(self):
        self.assertEqual(len(candidateGenerator.generateEdits("тест")), 269)

    def test_generateCandidates(self):
        self.assertEqual(len(candidateGenerator.generateCandidates("такяива")), 4)


if __name__ == '__main__':
    unittest.main()
