import pygame
import socket
import pickle
from threading import Thread

def game_blue():
    pygame.init()

    screen_width, screen_height = 960, 540
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Screen - BLUE")

    background = pygame.image.load("game_background.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    player_image = pygame.image.load("blue_player(standing).png")
    player_width, player_height = 70, 160
    player_image = pygame.transform.scale(player_image, (player_width, player_height))

    player_image_red = pygame.image.load("Red_player-removebg-preview.png")
    player_width_red, player_height_red = 110, 150
    player_image_red = pygame.transform.scale(player_image_red, (player_width_red, player_height_red))

    ground_height = 50
    ground_color = (159, 164, 73)

    player_x, player_y = 80, screen_height - ground_height - player_height
    player_speed = 0.5
    velocity_y = 0
    gravity = 0.15
    jump_power = -6.5
    on_ground = True

    player_x_red, player_y_red = 680, screen_height - ground_height - player_height_red

    server_address = ('localhost', 1729)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.01)  # Avoid blocking the main loop

    # Identify as BLUE
    my_id = "blue"
    client_socket.sendto(f"PLAYER_ID:{my_id}".encode(), server_address)

    platforms = [
        pygame.Rect(300, 350, 200, 15),
        pygame.Rect(600, 280, 150, 15),
        pygame.Rect(100, 220, 180, 15)
    ]

    platform_color = (0, 0, 0)

    running = True
    frame_count = 0

    # Position receiving in a separate thread
    def receive_positions():
        nonlocal player_x_red, player_y_red
        while True:
            try:
                message, _ = client_socket.recvfrom(8192)
                if message.startswith(b"POSITIONS:"):
                    positions = pickle.loads(message.split(b":", 1)[1])
                    if "red" in positions:
                        player_x_red = positions["red"]["x"]
                        player_y_red = positions["red"]["y"]
            except:
                continue

    Thread(target=receive_positions, daemon=True).start()

    while running:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, ground_color, (0, screen_height - ground_height, screen_width, ground_height))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_w] and on_ground:
            velocity_y = jump_power
            on_ground = False

        velocity_y += gravity
        player_y += velocity_y

        if player_y >= screen_height - ground_height - player_height:
            player_y = screen_height - ground_height - player_height
            velocity_y = 0
            on_ground = True

        future_y = player_y + velocity_y
        future_rect = pygame.Rect(player_x, future_y, player_width, player_height)
        for platform in platforms:
            if future_rect.colliderect(platform) and velocity_y >= 0:
                player_y = platform.top - player_height
                velocity_y = 0
                on_ground = True
                break

        frame_count += 1
        if frame_count % 2 == 0:  # Send update every 2 frames
            position_message = f"POSITION:{player_x},{player_y}"
            client_socket.sendto(position_message.encode(), server_address)

        screen.blit(player_image, (player_x, player_y))
        screen.blit(player_image_red, (player_x_red, player_y_red))

        for platform in platforms:
            pygame.draw.rect(screen, platform_color, platform)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    game_blue()
