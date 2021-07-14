import random
import pygame
from settings import *
from Sprites import *
from os import path

pygame.init()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(Font)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0


    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORMS_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < hits[0].rect.bottom:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 1      #TODO Originally was 0
        if self.player.rect.top <= SCREEN_HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)


            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()
                    self.score += 50

        if self.player.rect.bottom > SCREEN_HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        while len(self.platforms) < 8:
            width = random.randrange(50, 100) #TODO Might be redundant once sprite loaded
            p = Platform(random.randrange(0, SCREEN_WIDTH - width),
                         random.randrange(0, 20),  #TODO needs more adjustment for spawning and top congestion
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                    self.jumped = True

    def draw(self):
        self.screen.blit(background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 20, Blue, 30, 30)
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(Midblue)
        self.draw_text("Amogus Jump", 30, Red, SCREEN_WIDTH /2, SCREEN_HEIGHT/ 3)
        self.draw_text("Arrows to move, Space to jump", 15, Black, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40)
        self.draw_text("Press any key to play", 20, White, SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2)
        pygame.display.flip()
        self.wait_for_any_key()


    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(Midblue)
        self.draw_text("Game Over", 30, Red, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.draw_text("Score: " + str(self.score), 20, Black, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20)
        self.draw_text("Press any key to play again", 15, Black, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20)
        self.screen.blit(dead, ((SCREEN_WIDTH/ 2) - 25, SCREEN_HEIGHT / 2))

        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, Green, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, Green, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60)

        pygame.display.flip()
        self.wait_for_any_key()

    def wait_for_any_key(self):
        waiting = True
        while waiting:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rec = text_surface.get_rect()
        text_rec.midtop = (x, y)
        self.screen.blit(text_surface, text_rec)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
