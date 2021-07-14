import pygame
from settings import *
vec = pygame.math.Vector2




class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = standing
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2 , SCREEN_HEIGHT/2)
        self.pos = vec(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -12

    def update(self):
          self.acc = vec(0, 0.5)
          keys = pygame.key.get_pressed()
          if keys[pygame.K_LEFT]:
              self.image = l_standing
              self.acc.x = -PLAYER_ACC
          if keys[pygame.K_RIGHT]:
              self.image = standing
              self.acc.x = PLAYER_ACC


          self.acc.x += self.vel.x * PLAYER_FRI

          self.vel += self.acc
          self.pos += self.vel + 0.5 * self.acc

          if self.pos.x > SCREEN_WIDTH:
              self.pos.x = 0
          if self.pos.x < 0:
              self.pos.x = SCREEN_WIDTH
          self.rect.midbottom = self.pos



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y ,w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = new_platform
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

