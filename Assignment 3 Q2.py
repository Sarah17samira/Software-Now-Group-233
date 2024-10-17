import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desert Dash")  # Updated title to Desert Dash

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

# Load images and resize them
def load_and_scale_image(path, size):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except FileNotFoundError:
        print(f"File not found: {path}")
        pygame.quit()
        return None

# Load images (increased character size)
animal_image = load_and_scale_image("/Users/maritheresesalonga/Desktop/Software/animal.png", (120, 120))
human_image = load_and_scale_image("/Users/maritheresesalonga/Desktop/Software/human.png", (120, 120))
background_image = load_and_scale_image("/Users/maritheresesalonga/Desktop/Software/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, is_animal=True):
        super().__init__()
        self.image = animal_image if is_animal else human_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.jump_speed = -15
        self.gravity = 1
        self.velocity_y = 0
        self.health = 100
        self.lives = 3
        self.jumping = False
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Move player left and right
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity_y = self.jump_speed
            self.jumping = True
        
        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Stop falling if on ground
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.jumping = False
            self.velocity_y = 0

        # Keep player in bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
        pygame.draw.circle(self.image, BLACK, (5, 5), 5)  # Draw a black circle
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
        pygame.draw.circle(self.image, BLACK, (20, 20), 20)  # Draw a black circle
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100)
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed = random.randint(3, 6)
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
        pygame.draw.circle(self.image, BLACK, (15, 15), 15)  # Draw a black circle
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
        self.rect.y = SCREEN_HEIGHT - 100

    def update(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.kill()

# Game Over Screen
def show_game_over():
    screen.fill(BLACK)
    text = font.render("Game Over - Press R to Restart", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(1000)

# Character selection menu
def character_selection_menu():
    selected_character = None
    while selected_character is None:
        screen.blit(background_image, (0, 0))  # Draw background image on character selection screen
        text = font.render("Select Your Character:", True, BLACK)
        animal_button = font.render("Press A for Animal", True, BLACK)
        human_button = font.render("Press H for Human", True, BLACK)

        screen.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
        screen.blit(animal_button, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
        screen.blit(human_button, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    selected_character = True  # Animal selected
                elif event.key == pygame.K_h:
                    selected_character = False  # Human selected
        
        pygame.display.flip()
        clock.tick(60)

    return selected_character

# Game setup
def setup_game(is_animal):
    player = Player(is_animal=is_animal)  # Create player based on choice
    player_group = pygame.sprite.Group(player)
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    return player, player_group, projectiles, enemies, collectibles

is_animal = character_selection_menu()  # Get player choice
player, player_group, projectiles, enemies, collectibles = setup_game(is_animal)  # Initialize game state

# Main game loop
running = True
game_over = False
while running:
    # Draw background
    screen.blit(background_image, (0, 0))  # Draw background image
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                projectile = Projectile(player.rect.centerx, player.rect.centery)
                projectiles.add(projectile)

            # Restart the game
            if game_over and event.key == pygame.K_r:
                player, player_group, projectiles, enemies, collectibles = setup_game(is_animal)  # Reset player
                game_over = False

            # Return to character selection
            if event.key == pygame.K_ESCAPE:  # Pressing Esc returns to character selection
                is_animal = character_selection_menu()  # Return to character selection menu
                player, player_group, projectiles, enemies, collectibles = setup_game(is_animal)  # Reset game state

    if not game_over:
        # Update all sprites
        player_group.update()
        projectiles.update()
        enemies.update()
        collectibles.update()

        # Collision with enemies
        if pygame.sprite.spritecollideany(player, enemies):
            player.health -= 1
            if player.health <= 0:
                player.lives -= 1
                player.health = 100
            if player.lives == 0:
                game_over = True
                show_game_over()
        
        # Collision with collectibles
        if pygame.sprite.spritecollideany(player, collectibles):
            player.health = min(player.health + 10, 100)
            player.score += 10

        # Draw everything
        player_group.draw(screen)
        projectiles.draw(screen)
        enemies.draw(screen)
        collectibles.draw(screen)

        # Spawn enemies and collectibles randomly
        if random.randint(0, 50) == 0:
            enemy = Enemy()
            enemies.add(enemy)

        if random.randint(0, 100) == 0:
            collectible = Collectible()
            collectibles.add(collectible)

        # Show score and health
        score_text = font.render(f"Score: {player.score}", True, BLACK)
        health_text = font.render(f"Health: {player.health}", True, BLACK)
        lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 40))
        screen.blit(lives_text, (10, 70))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

