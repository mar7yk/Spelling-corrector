import unittest
import SpellingCorrector as sc
from nltk.corpus import PlaintextCorpusReader

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
            'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ь', 'ю', 'я']

corpus_root = './Tests/TestFiles/'
original = PlaintextCorpusReader(corpus_root, 'corpus_original.txt')
fullSentCorpusOriginal = [[w.lower() for w in sent] for sent in original.sents()]
typos = PlaintextCorpusReader(corpus_root, 'corpus_typos.txt')
fullSentCorpusTypos = [[w.lower() for w in sent] for sent in typos.sents()]

Corrector = sc.SpellingCorrector(alphabet, fullSentCorpusOriginal, fullSentCorpusTypos)


class SpellingCorrectorTest(unittest.TestCase):

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
