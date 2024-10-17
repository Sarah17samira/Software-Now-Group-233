import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_LEVEL = SCREEN_HEIGHT - 100
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Animal Hero Game')

# Load assets (replace with your own image files)
player_image = pygame.Surface((50, 50))
player_image.fill(RED)

enemy_image = pygame.Surface((50, 50))
enemy_image.fill((0, 255, 0))

projectile_image = pygame.Surface((10, 10))
projectile_image.fill((0, 0, 255))

collectible_image = pygame.Surface((20, 20))
collectible_image.fill((255, 255, 0))

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = GROUND_LEVEL - self.rect.height
        self.speed = 5
        self.jump_power = 15
        self.velocity_y = 0
        self.is_jumping = False
        self.health = 100
        self.lives = 3
        self.score = 0

    def move(self, dx):
        self.rect.x += dx * self.speed

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_power

    def update(self):
        # Gravity
        self.velocity_y += 1
        self.rect.y += self.velocity_y

        # Stop at ground level
        if self.rect.y >= GROUND_LEVEL - self.rect.height:
            self.rect.y = GROUND_LEVEL - self.rect.height
            self.is_jumping = False

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.lives -= 1
            self.health = 100

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = projectile_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.health = 50

    def patrol(self):
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed = -self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = collectible_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def collect(self, player):
        if self.type == 'health':
            player.health = min(player.health + 20, 100)
        elif self.type == 'life':
            player.lives += 1
        player.score += 10
        self.kill()

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)

        # Limit scrolling to bounds of the level
        x = min(0, x)  # Left side
        x = max(-(self.width - SCREEN_WIDTH), x)  # Right side

        self.camera = pygame.Rect(x, y, self.width, self.height)

# Helper Functions
def draw_health_bar(surface, x, y, health, max_health):
    bar_length = 100
    bar_height = 10
    fill = (health / max_health) * bar_length
    border = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, RED, fill_rect)
    pygame.draw.rect(surface, WHITE, border, 2)

def game_over_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    pygame.display.flip()
    pygame.time.wait(2000)

# Main Game Loop
def main_game():
    player = Player()
    camera = Camera(SCREEN_WIDTH * 3, SCREEN_HEIGHT)
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    # Create enemies
    for i in range(5):
        enemy = Enemy(random.randint(200, 800), GROUND_LEVEL - 50)
        enemies.add(enemy)
        all_sprites.add(enemy)

    # Create collectibles
    for i in range(3):
        collectible = Collectible(random.randint(200, 800), GROUND_LEVEL - 20, random.choice(['health', 'life']))
        collectibles.add(collectible)
        all_sprites.add(collectible)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectile = Projectile(player.rect.centerx, player.rect.centery, 1)
                    projectiles.add(projectile)
                    all_sprites.add(projectile)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1)
        if keys[pygame.K_UP]:
            player.jump()

        # Update all sprites
        all_sprites.update()

        # Check for player-enemy collisions
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                player.take_damage(10)

        # Check for projectile-enemy collisions
        for projectile in projectiles:
            enemy_hit = pygame.sprite.spritecollideany(projectile, enemies)
            if enemy_hit:
                enemy_hit.take_damage(25)
                projectile.kill()

        # Check for player-collectible collisions
        collectible_hit = pygame.sprite.spritecollideany(player, collectibles)
        if collectible_hit:
            collectible_hit.collect(player)

        # Update camera
        camera.update(player)

        # Draw everything
        screen.fill((0, 0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        # Draw player health and lives
        draw_health_bar(screen, 10, 10, player.health, 100)
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
        screen.blit(lives_text, (10, 50))
        score_text = font.render(f'Score: {player.score}', True, WHITE)
        screen.blit(score_text, (10, 90))

        pygame.display.flip()

        # Check for game over
        if player.lives <= 0:
            game_over_screen()
            running = False

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main_game()
