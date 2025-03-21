import pygame


def game_blue():
    pygame.init()

    # Screen setup
    screen_width, screen_height = 960, 540
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Screen")

    # Load images
    background = pygame.image.load("game_background.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    player_image = pygame.image.load("Red_player-removebg-preview.png")
    player_width, player_height = 130, 140
    player_image = pygame.transform.scale(player_image, (player_width, player_height))

    # Ground setup
    ground_height = 50
    ground_color = (57, 46, 46)

    # Player setup
    player_x, player_y = 80, screen_height - ground_height - player_height
    player_speed = 1
    velocity_y = 0  # Vertical velocity
    gravity = 0.5  # Gravity strength
    jump_power = -5  # Jump strength
    on_ground = True  # Track if player is on the ground

    running = True
    while running:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, ground_color, (0, screen_height - ground_height, screen_width, ground_height))

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and on_ground:  # Jump only if on the ground
            velocity_y = jump_power
            on_ground = False

        # Apply gravity
        velocity_y += gravity
        player_y += velocity_y

        # Check if player hits the ground
        if player_y >= screen_height - ground_height - player_height:
            player_y = screen_height - ground_height - player_height
            velocity_y = 0
            on_ground = True

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    game_blue()
