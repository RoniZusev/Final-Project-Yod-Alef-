import socket
import pygame
from threading import Thread

# Client configurations
server_ip = '127.0.0.1'
server_port = 1729


def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print('Connection to server lost')
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, server_port))
        print(f'Connected to server at {server_ip}:{server_port}')

        # Start thread to receive messages from server
        Thread(target=receive_messages, args=(client,)).start()

        # Pygame interface
        pygame.init()
        info = pygame.display.Info()
        screen_width = info.current_w  # Screen width
        screen_height = info.current_h  # Screen height
        screen = pygame.display.set_mode((screen_width/2, screen_height/2))
        pygame.display.set_caption("Final Game")

        # Load and scale the background image
        background_image = pygame.image.load("background.jpg")
        background_image = pygame.transform.scale(background_image, (screen_width/2, screen_height/2))

        # Font for welcome message
        font = pygame.font.SysFont("Arial", 30)
        text = font.render("Press Enter to start", True, (144, 238, 144))  # White text

        # Main game loop
        running = True
        while running:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Blit the background image onto the screen
            screen.blit(background_image, (0, 0))

            # Draw the text at the center of the screen
            text_rect = text.get_rect(center=(screen_width / 4, screen_height / 4 + 190))  # Center text
            screen.blit(text, text_rect)

            # Update the display
            pygame.display.update()

            # Limit to 30 frames per second
            pygame.time.Clock().tick(30)

    except Exception as e:
        print(f'Error: {e}')
    finally:
        client.close()
        pygame.quit()
        print('Client disconnected')


if __name__ == '__main__':
    start_client()
