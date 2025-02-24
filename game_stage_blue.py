import pygame
import socket

def game_blue():
    pygame.init()

    # Get screen information and set screen size
    screen_width, screen_height = 960, 540
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Screen")

    # Load background image
    background = pygame.image.load("game_background.jpg")  # Change to your image file
    background = pygame.transform.scale(background, (screen_width, screen_height))  # Resize to fit screen

    # Load font and text
    font = pygame.font.SysFont("Times New Roman", 60, bold= True)
    text = font.render("GAME", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, 50))

    ground_height = 50  # Height of the ground
    ground_color =  (0, 0, 0)  # Brown color for the ground (like dirt)

    # Blue Player settings
    player_width, player_height = 50, 50  # Player size
    player_x, player_y = screen_width // 2, screen_height // 2  # Start at center
    player_speed = 1  # Movement speed

    running = True
    while running:
        screen.blit(background, (0, 0))  # Draw background
        screen.blit(text, text_rect)  # Draw "GAME" text

        pygame.draw.rect(screen, ground_color, (0, screen_height - ground_height, screen_width, ground_height))

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - ground_height:
            player_y += player_speed

        # Draw blue player
        pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_width, player_height))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    game_blue()
