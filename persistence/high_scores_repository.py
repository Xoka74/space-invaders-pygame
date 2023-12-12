import json

from persistence.models import LevelHighScores, HighScore
from pathlib import Path


class HighScoreRepository:

    def __init__(self, json_path):
        self.path = Path(json_path)
        if not self.path.exists():
            self.path.write_text('{}')
        self.json = self._get_json()
        self.get_all()

    def _get_json(self):
        with open(str(self.path), 'r') as json_data:
            return json.load(json_data)

    def get_all(self) -> list[LevelHighScores]:
        objects = []
        for obj in self.json:
            scores = self.json[obj]
            high_scores = [HighScore(score, scores[score]) for score in scores]
            objects.append(LevelHighScores(obj, high_scores))
        return objects

    def _update(self):
        with open(str(self.path), 'w') as f:
            json.dump(self.json, f, indent=4)

    def add_or_update_high_score(self, level_name: str, high_score: HighScore):
        if not self.json.get(level_name):
            self.json[level_name] = {}

        if not self.json[level_name].get(high_score.name):
            self.json[level_name][high_score.name] = 0
        current = self.json[level_name][high_score.name]

        if current < high_score.value:
            self.json[level_name][high_score.name] = high_score.value

        self._update()
