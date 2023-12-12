from unittest import TestCase
from levels import HardLevel, load_levels
from repositories import ImageRepository


class TestGameObjects(TestCase):

    def setUp(self):
        self.image_repo = ImageRepository("../data/images")
        self.levels = load_levels(self.image_repo)
        self.test_level = self.levels[2]
        self.player = self.test_level.player
        self.bunker = list(self.test_level.bunkers)[0]
        self.ship = self.test_level.ship
        self.addCleanup(self.restart_level)

    def restart_level(self):
        self.test_level = HardLevel(self.image_repo)

    def test_player_collisions(self):
        invader = list(self.test_level.invaders)[0]
        invader.shoot(self.test_level)
        bullet = list(self.test_level.bullets)[0]
        self.assertEqual(self.player.alive, True)
        self.player.on_invader_bullet_collision(bullet)
        self.assertEqual(self.player.alive, False)
        self.assertEqual(self.player.points, 0)
        self.assertEqual(self.player.health, 0)

    def test_invader_collisions(self):
        self.player.shoot(self.test_level)
        self.player.tick(self.test_level)
        bullet = list(self.test_level.bullets)[0]
        invader = list(self.test_level.invaders)[0]
        invader.tick(self.test_level)
        self.assertEqual(invader.alive(), True)
        invader.on_bullet_collision(bullet)
        self.assertEqual(invader.alive(), False)

    def test_bunker_collisions(self):
        self.player.shoot(self.test_level)
        bullet = list(self.test_level.bullets)[0]
        self.assertEqual(self.bunker.alive(), True)
        self.assertEqual(self.bunker.state, 0)
        self.bunker.on_bullet_collision(bullet)
        self.assertEqual(self.bunker.state, 1)
        for i in range(4):
            self.bunker.on_bullet_collision(bullet)
        self.assertEqual(self.bunker.alive(), False)

    def test_mystery_ship_collisions(self):
        self.player.shoot(self.test_level)
        bullet = list(self.test_level.bullets)[0]
        self.assertEqual(self.ship.started, False)
        self.ship.start()
        self.ship.tick(self.test_level)
        self.assertEqual(self.ship.started, True)
        self.ship.on_bullet_collision(bullet)
        self.assertEqual(self.player.points, self.ship.points)
        self.assertEqual(self.ship.started, False)

    def test_player_invader_collisions(self):
        self.assertEqual(self.player.alive, True)
        invader = list(self.test_level.invaders)[0]
        self.player.on_invader_collision(invader)
        self.assertEqual(self.player.alive, False)
