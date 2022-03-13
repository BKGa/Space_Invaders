import pygame as pg
from landing_page import LandingPage
from sys import exit
import game_functions as gf
from time import sleep
from game_stats import Stats
from scoreboard import Scoreboard
from laser import Lasers
from ship import Ship
from alien import AlienFleet
from settings import Settings
from sound import Sound
import barrier
from alien_laser import AlienLasers
from pygame.sprite import Group

class Game:
    RED = (255, 0, 0)


    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.stats = Stats(game=self)
        self.screen = pg.display.set_mode((self.settings.screen_width,
                                           self.settings.screen_height))
        self.bg_color = self.settings.bg_color
        self.sound = Sound()
        self.sb = Scoreboard(game=self)
        pg.display.set_caption("Alien Invasion")
        self.ship = Ship(game=self)
        self.alien_fleet = AlienFleet(game=self)
        self.lasers = Lasers(game=self, owner=self.ship)
        self.alien_lasers = AlienLasers(game=self, owner=self.alien_fleet)
        self.ship.set_alien_fleet(self.alien_fleet)
        self.ship.set_lasers(self.lasers)
        self.barrier = Group()


    def restart(self):
        if self.stats.ships_left == 0: 
          self.game_over()
        print("restarting game")
        while self.sound.busy():  # wait for explosion sound to finish
            pass
        self.lasers.empty()
        self.alien_fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship.center_bottom()
        self.ship.reset_timer()
        self.update()
        self.draw()

        sleep(0.5)

    def update(self):
        self.ship.update()
        self.alien_fleet.update()
        self.lasers.update()
        self.alien_lasers.update()
        self.sb.update()



    def draw(self):
        self.screen.fill(self.bg_color)
        self.ship.draw()
        self.alien_fleet.draw()
        self.lasers.draw()
        self.sb.draw()
        self.barrier.draw(self.screen)
        pg.display.flip()

    def collision_checks(self):

        #Check the ships lasers
        if self.lasers.lasers:
            for laser in self.laser.lasers:
                if pg.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill(self.blocks)
                aliens_hit = pg.sprite.spritecollide(laser, self.alien_fleet, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()

    def play(self):
        self.finished = False
        self.sound.play_bg()
        while not self.finished:
            self.update()
            self.draw()

            gf.check_events(game=self)   # exits game if QUIT pressed

        self.game_over()

    def game_over(self):
        self.sound.play_game_over()
        print('\nGAME OVER!\n\n')
        exit()    # can ask to replay here instead of exiting the game



def main():
    g = Game()
    lp = LandingPage(game=g)
    lp.show()
    g.play()




if __name__ == '__main__':
    main()
