from unittest import TestCase
import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        self.score.add_measure(TreeMeasure(time=(5, 8)))
        # sf = SimpleFormat(durations=[1.8, 0.2, 0.5])
        sf = SimpleFormat(durations=[2.5])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1, 1)

        result_path = path + '_test_1'
        self.score.finish()
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)

    def test_2(self):
        self.score.add_measure(TreeMeasure(time=(5, 8)))
        # sf = SimpleFormat(durations=[1.8, 0.2, 0.5])
        sf = SimpleFormat(durations=[Fraction(1, 7), Fraction(6, 7), Fraction(1, 14), Fraction(3, 14), Fraction(10, 14),
                                     Fraction(1, 2)])
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1, 1)
        v = sf.to_stream_voice(1)
        v.add_to_score(self.score, 1, 2)
        self.score.get_score_parts()[1].max_division = 7

        result_path = path + '_test_2'
        self.score.finish()
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)