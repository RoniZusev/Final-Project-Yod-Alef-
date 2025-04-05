import game_stage_red
import socket
import pygame
import cv2
from threading import Thread
import sqlite3

import game_stage_red

# Client configurations
server_ip = '127.0.0.1'
server_port = 1729

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive_messages():
    """Receives messages from the server and prints them."""
    while True:
        try:
            message, _ = client.recvfrom(1024)  # UDP does not use connections
            message = message.decode().strip()
            print(f"Server: {message}")

            if message == "!ENTER_PRESSED":
                print("Server acknowledged ENTER key press. Switching screen...")
                return Login_To_Game()  # Call Login_To_Game properly

            if message == "success":
                print("success")
                if __name__ == '__main__':
                    game_stage_red.game_red()

            if message == "failed":
                print("failed")
                return Login_To_Game()

        except Exception as e:
            print(f'⚠ Connection error: {e}')
            break

def start_background():
    try:
        print(f'✅ Client ready to communicate with {server_ip}:{server_port}')

        # Start thread to receive messages
        Thread(target=receive_messages, daemon=True).start()

        # Initialize Pygame
        pygame.init()
        info = pygame.display.Info()
        screen_width, screen_height = info.current_w // 2, info.current_h // 2
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Final Game")

        # Load video
        video = cv2.VideoCapture("background.mp4")
        if not video.isOpened():
            print("Error: Could not open video file!")
            return  # Stop execution if video cannot be loaded

        # Load text
        font = pygame.font.SysFont("Times New Roman", 45)
        text = font.render("Press Enter to start", True, (0, 0, 0))

        font2 = font = pygame.font.SysFont("Times New Roman", 20, bold= True)
        text_by = font.render("Roni Zusev", True, (0, 0, 0), )

        clock = pygame.time.Clock()
        running = True
        print("🎬 Starting video playback...")

        while running:
            ret, frame = video.read()

            if not ret:
                print("🔄 Restarting video...")
                video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
                continue  # Skip frame processing

            if frame is None:
                print("⚠ Error: Empty frame received, skipping...")
                continue

            # Convert BGR to RGB and resize
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (screen_width, screen_height))
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # Draw video frame as background
            screen.blit(frame, (0, 0))

            # Create a rectangle for the text box effect
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + 190))
            box_padding = 5  # Padding inside the box
            box_width = text_rect.width + 2 * box_padding  # Adjust box width to fit text
            box_height = text_rect.height + 2 * box_padding  # Adjust box height to fit text

            # Draw the background box (light gray background)
            pygame.draw.rect(screen, (200, 200, 200),
                             (text_rect.x - box_padding, text_rect.y - box_padding, box_width, box_height))
            # Draw the border of the box
            pygame.draw.rect(screen, (0, 0, 0),
                             (text_rect.x - box_padding, text_rect.y - box_padding, box_width, box_height), 3)

            # Draw text on top of the box
            screen.blit(text, text_rect)

            # Draw the "By" text
            text_by_rect = text_by.get_rect(center=(screen_width // 2 - 330, screen_height // 2 - 240))
            screen.blit(text_by, text_by_rect)

            pygame.display.update()
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("🛑 Quit event detected. Exiting...")
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    print("⏩ Enter key pressed! Sending to server...")
                    client.sendto("ENTER_PRESSED".encode(), (server_ip, server_port))  # UDP send
                    running = False  # Stop loop
                    video.release()
                    pygame.quit()
                    receive_messages()

        print("🚪 Closing video...")
        video.release()
        print("📴 Closing Pygame window...")
        pygame.quit()

    except Exception as e:
        print(f'⚠ Error: {e}')
    finally:
        client.close()
        print('🔌 Client disconnected')


import pygame
import pygame.freetype  # For font rendering and text input

def Login_To_Game():
    """Transition to the game screen while keeping Pygame running."""
    print("🔄 Switching to game login screen...")

    pygame.quit()  # Quit previous session
    pygame.init()  # Restart Pygame

    # Get screen information and set screen size
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w // 2, info.current_h // 2
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Login Screen")

    # Set up the background color and font
    screen.fill((0, 0, 0))  # Black background
    font = pygame.font.SysFont("Times New Roman", 40)
    text = font.render("Game Screen - Login", True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(screen_width // 2, screen_height / 4 + 35))
    screen.blit(text, text_rect)

    # Input box and button positioning
    input_box_width = 300
    input_box_height = 40
    input_y_start = screen_height // 2 - 60  # Offset for the input fields
    button_y_start = screen_height // 2 + 40  # Offset for buttons

    # Username input box
    username_box = pygame.Rect(screen_width / 2 - input_box_width / 2, input_y_start, input_box_width, input_box_height)
    password_box = pygame.Rect(screen_width / 2 - input_box_width / 2, input_y_start + 50, input_box_width, input_box_height)

    # Connect button
    connect_button = pygame.Rect(screen_width / 2 - input_box_width / 2, button_y_start, input_box_width, 40)

    active_input = None
    username = ""
    password = ""
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("🛑 Closing game screen...")
                running = False

            if event.type == pygame.KEYDOWN:
                if active_input == 'username':
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:  # <-- Correct indentation here
                        username += event.unicode

                elif active_input == 'password':
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is clicked inside the input boxes or button
                if username_box.collidepoint(event.pos):
                    active_input = 'username'
                elif password_box.collidepoint(event.pos):
                    active_input = 'password'
                elif connect_button.collidepoint(event.pos):
                    print(f"Attempting to connect with username: {username} and password: {password}")
                    client.sendto(f"ATTEMPT: {username} , {password}".encode(), (server_ip, server_port))  # UDP send
                    receive_messages()

        # Redraw the screen
        screen.fill((0, 0, 0))  # Clear screen

        # Display the title text
        screen.blit(text, text_rect)

        # Draw the input fields and buttons
        pygame.draw.rect(screen, (255, 255, 255), username_box, 2)  # White border for input box
        pygame.draw.rect(screen, (255, 255, 255), password_box, 2)  # White border for password box
        pygame.draw.rect(screen, (255, 255, 255), connect_button)  # White border for connect button

        small_font = pygame.font.SysFont("Times New Roman", 25)
        username_text = small_font.render(username, True, (255, 255, 255))  # White text
        password_text = font.render('*' * len(password), True, (255, 255, 255))  # Mask password with asterisks

        # Display text in the input boxes
        screen.blit(username_text, (username_box.x + 5, username_box.y + 2))
        screen.blit(password_text, (password_box.x + 5, password_box.y + 5))

        # Render "Connect" text on the button
        connect_text = font.render("Connect", True, (0, 0, 0))  # Black text for button
        screen.blit(connect_text, (connect_button.x + (connect_button.width - connect_text.get_width()) // 2,
                                   connect_button.y + (connect_button.height - connect_text.get_height()) // 2))

        pygame.display.update()
    pygame.quit()



if __name__ == '__main__':

    start_background()
