import pygame
import socket
import pickle
from threading import Thread

def game_red():
    pygame.init()

    screen_width, screen_height = 960, 540
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Screen - RED")

    background = pygame.image.load("game_background.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))

    player_image = pygame.image.load("Red_player-removebg-preview.png")
    player_width, player_height = 110, 150
    player_image = pygame.transform.scale(player_image, (player_width, player_height))

    player_image_blue = pygame.image.load("blue_player(standing).png")
    player_width_blue, player_height_blue = 70, 160
    player_image_blue = pygame.transform.scale(player_image_blue, (player_width_blue, player_height_blue))

    ground_height = 50
    ground_color = (159, 164, 73)

    player_x, player_y = 680, screen_height - ground_height - player_height
    player_speed = 0.5
    velocity_y = 0
    gravity = 0.15
    jump_power = -6.5
    on_ground = True

    player_x_blue, player_y_blue = 80, screen_height - ground_height - player_height_blue

    server_address = ('localhost', 1729)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.01)

    my_id = "red"
    client_socket.sendto(f"PLAYER_ID:{my_id}".encode(), server_address)

    platforms = [
        pygame.Rect(300, 350, 200, 15),
        pygame.Rect(600, 280, 150, 15),
        pygame.Rect(100, 220, 180, 15)
    ]

    platform_color = (0, 0, 0)

    running = True
    frame_count = 0

    def receive_positions():
        nonlocal player_x_blue, player_y_blue
        while True:
            try:
                message, _ = client_socket.recvfrom(8192)
                if message.startswith(b"POSITIONS:"):
                    positions = pickle.loads(message.split(b":", 1)[1])
                    if "blue" in positions:
                        player_x_blue = positions["blue"]["x"]
                        player_y_blue = positions["blue"]["y"]
            except:
                continue

    Thread(target=receive_positions, daemon=True).start()

    while running:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, ground_color, (0, screen_height - ground_height, screen_width, ground_height))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and on_ground:
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
        if frame_count % 2 == 0:
            position_message = f"POSITION:{player_x},{player_y}"
            client_socket.sendto(position_message.encode(), server_address)

        screen.blit(player_image, (player_x, player_y))
        screen.blit(player_image_blue, (player_x_blue, player_y_blue))

        for platform in platforms:
            pygame.draw.rect(screen, platform_color, platform)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    game_red()
