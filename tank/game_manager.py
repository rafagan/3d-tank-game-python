from util.decorator.singleton import singleton


@singleton
class GameManager:
    def __init__(self):
        self.score = 0

    def __update_score(self, amount):
        self.score += amount
        print(f'Score updated: {self.score}')

    def score_killed_enemy(self):
        self.__update_score(10)

    def score_killed_friend(self):
        self.__update_score(10)

    def score_killed_ground_tile(self):
        self.__update_score(-5)

    def score_killed_wall_tile(self):
        self.__update_score(5)

    @staticmethod
    def killed_myself():
        exit(0)
