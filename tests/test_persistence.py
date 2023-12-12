from pathlib import Path
from unittest import TestCase
from persistence import HighScoreRepository, HighScore, LevelHighScores


class TestHighScoresRepository(TestCase):

    def setUp(self):
        self.test_path = 'zero_scores.json'
        self.test_repo = HighScoreRepository(self.test_path)
        self.addCleanup(self.delete_test_json)

    def delete_test_json(self):
        Path(self.test_path).unlink()

    def test_add_or_update_high_score(self):
        initial_value = LevelHighScores('Easy', [HighScore('xoka74', 0)])
        updated_value = LevelHighScores('Easy', [HighScore('xoka74', 20)])
        self.assertFalse(initial_value in self.test_repo.get_all())
        self.test_repo.add_or_update_high_score('Easy',
                                                HighScore('xoka74', 0))
        self.assertTrue(initial_value in self.test_repo.get_all())
        self.test_repo.add_or_update_high_score('Easy',
                                                HighScore('xoka74', 20))
        self.assertFalse(initial_value in self.test_repo.get_all())
        self.assertTrue(updated_value in self.test_repo.get_all())

    def test_get_all(self):
        self.test_repo.add_or_update_high_score('Easy',
                                                HighScore('xoka74_1', 40))
        self.test_repo.add_or_update_high_score('Medium',
                                                HighScore('xoka74_2', 20))
        self.test_repo.add_or_update_high_score('Hard',
                                                HighScore('xoka74_3', 10))
        self.assertTrue(LevelHighScores('Easy', [HighScore('xoka74_1', 40)])
                        in self.test_repo.get_all())
        self.assertTrue(LevelHighScores('Medium', [HighScore('xoka74_2', 20)])
                        in self.test_repo.get_all())
        self.assertTrue(LevelHighScores('Hard', [HighScore('xoka74_3', 10)])
                        in self.test_repo.get_all())
