import socket
import pygame
from threading import Thread

# Client configurations
server_ip = '127.0.0.1'
server_port = 1729


def receive_messages(client):
    """Receives messages from the server and prints them."""
    while True:
        try:
            message = client.recv(1024).decode().strip()
            print(f"Server: {message}")

            if message == "the answer is hello: ENTER_PRESSED":
                print("Server acknowledged ENTER key press. Switching screen...")
                return Login_To_Game(client)  # Call Login_To_Game properly

        except Exception as e:
            print(f'Connection to server lost: {e}')
            break


def start_client():
    """Starts the client, connects to the server, and initializes the Pygame interface."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, server_port))
        print(f'Connected to server at {server_ip}:{server_port}')

        # Start thread to receive messages from server
        Thread(target=receive_messages, args=(client,), daemon=True).start()

        # Pygame initialization
        pygame.init()
        info = pygame.display.Info()
        screen_width = int(info.current_w / 2)
        screen_height = int(info.current_h / 2)
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Final Game")

        # Load and scale the background image
        background_image = pygame.image.load("background.jpg")
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

        # Font for welcome message
        font = pygame.font.SysFont("Arial", 30)  # Keeping your original font size
        text = font.render("Press Enter to start", True, (144, 238, 144))  # Keeping your text color

        clock = pygame.time.Clock()
        running = True

        while running:
            screen.blit(background_image, (0, 0))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + 190))  # Keeping text placement
            screen.blit(text, text_rect)

            pygame.display.update()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    print("Enter key pressed! Sending to server...")
                    client.send("ENTER_PRESSED".encode())  # Send message to server
                    running = False  # Stop the loop to transition screens

        # Do not quit pygame, just close the window
        pygame.display.quit()
        print("Pygame window closed.")

        # Move to the login screen
        Login_To_Game(client)

    except Exception as e:
        print(f'Error: {e}')
    finally:
        client.close()
        print('Client disconnected')


def Login_To_Game(client):
    """Transition to the game screen while keeping Pygame running."""
    print("Switching to game login screen...")
    pygame.init()  # Ensure Pygame is reinitialized
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w // 2, info.current_h // 2
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Login Screen")

    screen.fill((0, 0, 128))  # Dark blue background
    font = pygame.font.SysFont("Arial", 50)  # Keeping original font for login screen
    text = font.render("Game Screen - Login", True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    screen.blit(text, text_rect)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    print("Game screen closed.")


if __name__ == '__main__':
    start_client()
