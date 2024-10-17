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
pygame.display.set_caption("Desert Dash")

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

    def take_damage(self):
        """Decreases player's health and lives if hit by an enemy."""
        print(f"Player hit! Health before: {self.health}, Lives before: {self.lives}")
        self.health -= 20
        
        if self.health <= 0:
            self.lives -= 1
            self.health = 100  # Reset health after losing a life
            print(f"Lives remaining: {self.lives}")
        
        if self.lives <= 0:
            print("Game Over!")
            return True  # Indicate game over
        
        return False

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (20, 20), 20)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 100)
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.x -= self.speed
        
        if self.rect.right < 0:
            self.kill()

# Game Over Screen
def show_game_over():
    screen.fill(BLACK)
    text = font.render("Game Over - Press R to Restart or ESC to Quit", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    pygame.display.flip()

# Character selection menu with background restoration
def character_selection_menu():
    selected_character = None
    
    while selected_character is None:
        screen.blit(background_image, (0, 0)) # Restore background on menu
        
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
                    selected_character = True
                elif event.key == pygame.K_h:
                    selected_character = False
        
        pygame.display.flip()
        clock.tick(60)

    return selected_character

# Game setup with score initialization
def setup_game(is_animal):
    player = Player(is_animal=is_animal)
    player_group = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    score = 0   # Initialize score here.
    
    return player, player_group, enemies, score

# Initialize game state variables.
is_animal = character_selection_menu()
player, player_group, enemies, score = setup_game(is_animal)

# Main game loop
running = True
game_over = False

while running:
    # Draw background 
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
         # Restart the game or go back to menu with ESC key.
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player, player_group, enemies, score = setup_game(is_animal)
                game_over = False
            elif event.key == pygame.K_ESCAPE:
                is_animal = character_selection_menu() # Return to character selection menu.
                player, player_group, enemies, score = setup_game(is_animal) 
                game_over = False 

    if not game_over:
        # Update all sprites 
        player_group.update()
        enemies.update()

        # Collision with enemies 
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = player.take_damage() 

        # Draw everything 
        player_group.draw(screen)
        enemies.draw(screen)

        # Spawn enemies randomly 
        if random.randint(0, 100) == 0:  # Increase the range to increase the distance between enemies
            enemy = Enemy()
            enemies.add(enemy)

        # Draw HUD 
        lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
        health_text = font.render(f"Health: {player.health}", True, BLACK)
        score_text= font.render(f"Score: {score}", True , BLACK)   # Display score on HUD.

        screen.blit(lives_text,(20 ,20))
        screen.blit(health_text,(20 ,60))
        screen.blit(score_text,(20 ,100))   # Position for score display.

    # Show game over screen if game is over 
    if game_over:
        show_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
