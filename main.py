# Author: Dianna Pham
# GitHub username: dianna-SE
# Date: 6/21/2023
# Description: Create a program that mimics the Reversi game (text-based Reversi) using
#               several classes and several methods to recreate two players playing the game.
import sys
import pygame


class Player:
    """
    Represents a Player class that is an implementation of the player name
    and the player’s color piece. This class will be used in coordination with the
    Reversi class.
    """

    def __init__(self, player, color):
        """
        Represents an init method or a constructor that initializes private data members
        player name and the color of the pieces. The player’s name along with the player’s
        color piece are initialized as private data members.
        """
        self._player = player
        self._color = color

    def get_player(self):
        """
        Represents a get method that takes no parameters and is used in
        conjunction with the Othello class to retrieve the current player name.

        Returns – current value of the player name
        """
        return self._player

    def get_color(self):
        """
        Represents a get method that takes no parameters and is used in
        conjunction with the Othello class to retrieve the current player color
        piece.

        Returns – current value of the color
        """
        return self._color


class Reversi:
    """
    Represents the Reversi class that is an implementation of the Reversi game
    that will track the progress of the game being played.

    Moves will be validated on whether it can capture the opposing player’s piece, and
    any move that can be made is considered part of the available positions.

    The game ends when no capturing move can be made on the board and the winner is
    the player that has the most pieces on the board.
    """
    def __init__(self):
        """
        Represents an init method or a constructor that takes no parameters
        and initializes all assets for a functional Reversi game. 

        This includes the pygame window, buttons, grid, colors, state of players,
        flags, and player counts.
        """
        pygame.init()

        self.window_width = 900
        self.window_height = 900
        self.state = "intro"  # Initial game state is "intro"

        # Initialize buttons for intro and grid
        self.intro_start_button = pygame.Rect(self.window_width // 2 - 25, self.window_height // 2 + 100, 50, 50)
        self.grid_back_button = pygame.Rect(25, 25, 40, 40)
        self.grid_help_button = pygame.Rect(self.window_width // 2 - 25, self.window_height // 2 + 250, 50, 50)

        # Colors
        self.purple = (216, 219, 255)  # DBDBFFh
        self.beige = (255, 246, 239)  # FFF6EFh
        self.rose = (255, 217, 228)  # ebd3cb
        self.grid_color = (245, 231, 221)  # Color of the grid cells
        self.background_color = (245, 231, 221)  # Background color
        self.button_color = self.purple  # Color of the buttons

        # Grid dimensions
        self.grid_size = 10
        self.cell_size = 55
        self.padding = 10  # Decreased padding value of grid cells
        self.radius = (self.cell_size - 2 * self.padding) // 2
        self.cell_padding = 8
        self.outer_padding = 20
        self.corner_radius = 20

        # Set cell state
        self.cell_rect = None
        self.cells = []
        self.cell_clicked = False
        self.clicked_cell = None
        self.clicked_list = []
        self.piece_position = (0, 0)
        self.flipped = False

        # Initialize players
        self.player1 = Player("purple", "purple")  # X
        self.player2 = Player("rose", "rose")  # O
        self.current_player = self.player1
        self.player1_positions = True
        self.player2_positions = True
        self.player1_count = 0
        self.player2_count = 0
        self.grid_updated = False

        # Initialize the board
        self._board = []
        self.check_both_player_positions = 0

        for row in range(10):
            this_list = []
            for column in range(10):
                if row != 0 and row != 9 and column != 0 and column != 9:
                    this_list.append(".")
                else:
                    this_list.append("*")
            self._board.append(this_list)

        self._board[4][5] = "X"
        self._board[5][5] = "O"
        self._board[5][4] = "X"
        self._board[4][4] = "O"

        # Message handling
        self.out_of_bounds_error = False
        self.message = "Welcome to Othello!"

        # Load the cursor images
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("o t h e l l o")

    def draw_intro(self):
        """
        Represents.....
        """

        self.window.fill(self.grid_color)

        # Draw intro-specific elements here, including the circles and button
        pygame.draw.circle(self.window, self.beige, (self.window_width // 2 - 60, self.window_height // 2 - 100), 50)
        pygame.draw.circle(self.window, self.purple, (self.window_width // 2 + 60, self.window_height // 2 - 100), 50)
        pygame.draw.circle(self.window, self.purple, (self.window_width // 2 - 60, self.window_height // 2 + 20), 50)
        pygame.draw.circle(self.window, self.beige, (self.window_width // 2 + 60, self.window_height // 2 + 20), 50)

        # Draw start button
        intro_start_button_rect = pygame.Rect(self.window_width // 2 - 25, self.window_height // 2 + 100, 50, 50)
        pygame.draw.rect(self.window, self.button_color, intro_start_button_rect, border_radius=16)

        intro_start_button_image = pygame.image.load("images/right-arrow.png")
        intro_start_button_image = pygame.transform.scale(intro_start_button_image, (30, 30))

        intro_start_button_x = intro_start_button_rect.x + intro_start_button_rect.width // 2 - intro_start_button_image.get_width() // 2
        intro_start_button_y = intro_start_button_rect.y + intro_start_button_rect.height // 2 - intro_start_button_image.get_height() // 2

        self.window.blit(intro_start_button_image, (intro_start_button_x, intro_start_button_y))

        pygame.display.flip()

    def draw_grid(self):
        """
        Represents a method that draws initializes state of the entire board.
        """
        self.window.fill(self.background_color)

        # Draw the back button
        self.back_button()

        # Draw the help button
        grid_help_button_rect = pygame.Rect(self.window_width // 2 - 25, self.window_height // 2 + 250, 40, 40)
        pygame.draw.rect(self.window, self.button_color, grid_help_button_rect, border_radius=16)
        grid_help_button_image = pygame.image.load("images/help.png")
        grid_help_button_image = pygame.transform.scale(grid_help_button_image, (20, 20))
        grid_help_button_x = grid_help_button_rect.x + grid_help_button_rect.width // 2 - grid_help_button_image.get_width() // 2
        grid_help_button_y = grid_help_button_rect.y + grid_help_button_rect.height // 2 - grid_help_button_image.get_height() // 2
        self.window.blit(grid_help_button_image, (grid_help_button_x, grid_help_button_y))

        # Text
        metropolis_font = "fonts/Metropolis-Medium.otf"  # Replace with the actual path to your font file
        font = pygame.font.Font(metropolis_font, 25)  # Customize the font and size

        # Draw the player's turns (TOP IMAGE)
        if self.current_player == self.player1:
            text = font.render("player 1", True, (255, 255, 255))  # Customize the text and color
            text_rect = text.get_rect(center=(self.window_width // 2, 180))  # Customize the position of the text
            self.window.blit(text, text_rect)

            # Create a circle on top of the text
            circle_radius = 25
            circle_center = (text_rect.centerx, text_rect.centery - 50)  # Customize the position of the circle
            pygame.draw.circle(self.window, self.purple, circle_center, circle_radius)

        else:
            text = font.render("player 2", True, (255, 255, 255))  # Customize the text and color
            text_rect = text.get_rect(center=(self.window_width // 2, 180))  # Customize the position of the text
            self.window.blit(text, text_rect)

            # Create a circle on top of the text
            circle_radius = 25
            circle_center = (text_rect.centerx, text_rect.centery - 50)  # Customize the position of the circle
            pygame.draw.circle(self.window, self.rose, circle_center, circle_radius)

        self.play_game()

        # Draw message box and text (bottom)
        font = pygame.font.Font(metropolis_font, 19)
        text_surface = font.render(self.message, True, (160, 160, 160))  # Customize the text and color
        text_rect = text_surface.get_rect()
        text_rect.center = ((self.window_width - 500) // 2 + 250, self.window_height - 110)
        pygame.draw.rect(self.window, self.beige, ((self.window_width - 500) // 2, self.window_height - 140, 500, 60),
                         border_radius=20)
        self.window.blit(text_surface, text_rect)

        # Draw the label and instructions (right of grid)
        box_width = 150
        box_height = 200
        box_x = self.window_width - box_width
        box_y = (self.window_height - box_height) // 2

        # player 1 label
        font = pygame.font.Font(metropolis_font, 15)
        text_surface = font.render("player 1", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (box_x + 40, box_y + 49)
        self.window.blit(text_surface, text_rect)
        pygame.draw.circle(self.window, self.purple, (box_x - 15, box_y + 48), 10)
        self.window.blit(text_surface, text_rect)

        # player 2 label
        font = pygame.font.Font(metropolis_font, 15)
        text_surface = font.render("player 2", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (box_x + 40, box_y + 81)
        self.window.blit(text_surface, text_rect)
        pygame.draw.circle(self.window, self.rose, (box_x - 15, box_y + 80), 10)
        self.window.blit(text_surface, text_rect)

        # available positions label
        font = pygame.font.Font(metropolis_font, 15)
        text_surface = font.render("moves", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (box_x + 36, box_y + 111)
        self.window.blit(text_surface, text_rect)
        pygame.draw.circle(self.window, (255, 255, 255), (box_x - 15, box_y + 112), 10)
        self.window.blit(text_surface, text_rect)

        # player 1 COUNT
        font = pygame.font.Font(metropolis_font, 15)
        text_surface = font.render(str(self.player1_count), True, (160, 160, 160))
        text_rect = text_surface.get_rect()
        text_rect.center = (box_x - 660, box_y + 80)
        self.window.blit(text_surface, text_rect)
        pygame.draw.circle(self.window, self.purple, (box_x - 660, box_y + 48), 13)
        self.window.blit(text_surface, text_rect)

        # player 2 COUNT
        font = pygame.font.Font(metropolis_font, 15)
        text_surface = font.render(str(self.player2_count), True, (160, 160, 160))
        text_rect = text_surface.get_rect()
        text_rect.center = (box_x - 620, box_y + 80)
        self.window.blit(text_surface, text_rect)
        pygame.draw.circle(self.window, self.rose, (box_x - 620, box_y + 48), 13)
        self.window.blit(text_surface, text_rect)

        pygame.display.flip()

    def draw_help(self):
        """
        Represents a method......
        """
        self.window.fill(self.background_color)
        self.back_button()

    def switch_players(self, player):
        """
        Represents a method that simply updates player turns.

        Returns -- nothing, but sets certain flags to handle cell clicks.
        """
        if player.get_player() == "purple":
            self.current_player = self.player2

        elif player.get_player() == "rose":
            self.current_player = self.player1

        self.clicked_cell = None
        self.cell_clicked = False
        self.grid_updated = False

    def display_board(self):
        """
        Represents a method that takes no parameters and displays the
        current progress of the board and boundaries. It returns the layout of
        the board for the Reversi game to be played. Cells are centered based
        on the window layout of pygame.
        """
        # Calculate the total grid size with padding
        total_grid_size = self.grid_size * (2 * self.radius + self.cell_padding) - self.cell_padding
        total_size = total_grid_size + 2 * self.outer_padding
        start_x = (self.window_width - total_size) // 2
        start_y = (self.window_height - total_size) // 2

        # Draw the padding around the grid with rounded corners
        pygame.draw.rect(self.window, self.beige, (start_x, start_y, total_size, total_size), border_radius=self.corner_radius)

        # Initialize the starting pieces of the board based on self._board
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                cell_value = self._board[row][col]
                # Calculate the center point of each grid cell
                center_x = start_x + self.outer_padding + self.radius + col * (2 * self.radius + self.cell_padding)
                center_y = start_y + self.outer_padding + self.radius + row * (2 * self.radius + self.cell_padding)

                # Create a rectangle around the grid cell
                self.cell_rect = pygame.Rect(
                    center_x - self.radius,
                    center_y - self.radius,
                    2 * self.radius,
                    2 * self.radius
                )
                self.cells.append(self.cell_rect)

                # Update the game board state based on cell interactions
                self.handle_cell_interactions(row, col, self.cell_rect)

                if cell_value == 'O':
                    pygame.draw.circle(self.window, self.rose, (center_x, center_y), self.radius)
                elif cell_value == 'X':
                    pygame.draw.circle(self.window, self.purple, (center_x, center_y), self.radius)

                # !!! ADDING THESE WILL DISABLE THE HOVER COLOR FOR PLAYER1 AND PLAYER2 !!!! #
                elif cell_value == '.':
                    pygame.draw.circle(self.window, self.grid_color, (center_x, center_y), self.radius)
                else:
                    pygame.draw.circle(self.window, self.beige, (center_x, center_y), self.radius)

                    # this kind works but is lowkey brute force
                    if self.cell_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def play_game(self):
        """Represents a method that plays the game and calls several methods to assist in it."""
        self.display_board()
        self.return_available_positions(self.current_player)

        if self.grid_updated:
            self.switch_players(self.current_player)

    def return_winner(self):
        """
        Represents a method that takes no parameters and returns the
        results that includes the winner’s name, the winner’s piece count and the
        opposing piece count. The results are tallied by a count (variables purple
        and rose) that increments by one every time a specified color piece is
        identified in the board.
        """
        # get the sum of purple and rose counts
        purple = 0
        rose = 0

        # traverse through each row
        for row in self._board:

            # traverse through each index in row
            for column in row:
                if column == "X":
                    purple += 1

                if column == "O":
                    rose += 1

        if purple > rose:
            self.message = "Game ended. Player 1 wins!"
            print("Winner is player 1")

        elif rose > purple:
            self.message = "Game ended. Player 2 wins!"
            print("Winner is player 2")

        else:
            self.message = "Game ended. It's a tie!"
            print("It's a tie")

    def back_button(self):
        """
        Represents the back button of a page.
        :return:
        """
        # Draw the back button
        grid_back_button_rect = pygame.Rect(25, 25, 40, 40)
        pygame.draw.rect(self.window, self.button_color, grid_back_button_rect, border_radius=16)
        grid_back_button_image = pygame.image.load("images/left-arrow.png")
        grid_back_button_image = pygame.transform.scale(grid_back_button_image, (20, 20))
        grid_back_button_x = grid_back_button_rect.x + grid_back_button_rect.width // 2 - grid_back_button_image.get_width() // 2
        grid_back_button_y = grid_back_button_rect.y + grid_back_button_rect.height // 2 - grid_back_button_image.get_height() // 2
        self.window.blit(grid_back_button_image, (grid_back_button_x, grid_back_button_y))

    def handle_cell_interactions(self, row, col, cell_rect):
        """
        Represents a method that handles cell state between each player in the game.
        :param row: The row index of the cell.
        :param col: The column index of the cell.
        :param cell_rect: The rectangle representing the cell.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.count_grid()

        metropolis_font = "fonts/Metropolis-Medium.otf"  # Replace with the actual path to your font file
        font = pygame.font.Font(metropolis_font, 25)  # Customize the font and size

        # handle player1
        if self.cell_clicked and cell_rect.collidepoint(mouse_pos) and self.current_player == self.player1:
            # check for boundaries
            if self.check_boundaries(self.current_player, (row, col)):
                self.make_move(self.current_player.get_color(), (row, col))
                self.grid_updated = True
                self.message = "Player 1 has made a move."
            else:
                self.out_of_bounds_error = True
                self.message = "Invalid move. Please try again."
                return

        # handle player2
        if self.cell_clicked and cell_rect.collidepoint(mouse_pos) and self.current_player == self.player2:
            if self.check_boundaries(self.current_player, (row, col)):
                self.make_move(self.current_player.get_color(), (row, col))  # Update the board state
                self.grid_updated = True
                self.message = "Player 2 has made a move."
            else:
                self.out_of_bounds_error = True
                self.message = "Invalid move. Please try again."
                return

        # Draw the grid cell with the default color
        if self._board[row][col] == 'X':
            pygame.draw.circle(self.window, self.purple, cell_rect.center, self.radius)
            self.player1_count += 1
        elif self._board[row][col] == 'O':
            pygame.draw.circle(self.window, self.rose, cell_rect.center, self.radius)
        else:
            pygame.draw.circle(self.window, self.grid_color, cell_rect.center, self.radius)

        # Check if the mouse is hovering over the current cell for player 1
        if cell_rect.collidepoint(mouse_pos) and self.current_player == self.player1:
            pygame.draw.circle(self.window, self.purple, cell_rect.center, self.radius)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Check if the mouse is hovering over the current cell for player 2
        elif cell_rect.collidepoint(mouse_pos) and self.current_player == self.player2:
            pygame.draw.circle(self.window, self.rose, cell_rect.center, self.radius)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    def check_boundaries(self, player, check_position):
        """
        Represents......
        """
        row, col = check_position
        this_move = self._board[row][col]

        available_positions = self.return_available_positions(player)

        # check if piece_position is part of the captured positions
        if check_position in available_positions:

            # position out of bounds
            if this_move == "*" or this_move == "O" or this_move == "X":
                print("Out of bounds. Valid moves for", self.current_player.get_color(), ":", available_positions)
                self.cell_clicked = False
                return False

            # position is valid, call make_move
            elif this_move == ".":
                self.piece_position = row, col

        # piece_position is not in available_positions
        else:
            print("Unable to capture. Valid moves for", self.current_player.get_color(), ":", available_positions)
            self.cell_clicked = False
            return False

        return True

    def return_available_positions(self, player):
        """
        Represents a method that takes in one parameter, the player’s color
        piece and calculates the available spots for a player to travel to for a
        capturing move based on which player it is.

        An additional recursive method called “rec_validate_move” takes in four
        parameters, the row, column, and x and y directions to validate possible
        moves to capture within the board’s boundaries.
        """

        available_positions = []
        row_length = len(self._board)
        column_length = len(self._board[0])

        if player.get_color() == "rose":
            color_piece = "O"
            opposing_piece = "X"
        else:
            color_piece = "X"
            opposing_piece = "O"

        # Find the positions of the player's pieces on the board
        existing_positions = []
        for row in range(row_length):
            for column in range(column_length):

                if self._board[row][column] == color_piece:
                    existing_positions.append((row, column))

        # iterate through the player's positions to calculate available capturing moves
        def rec_validate_move(this_row, this_column, move_x, move_y):
            """
            Represents a recursive function......
            """
            # increment move directions to current position
            x, y = this_row + move_x, this_column + move_y

            # check if next position is within boundary
            if row_length > x >= 0 and column_length > y >= 0:

                check_position = self._board[x][y]

                # check if move can be captured
                if check_position == opposing_piece:
                    capture_position = self._board[x + move_x][y + move_y]

                    if capture_position == ".":
                        available_positions.append((x + move_x, y + move_y))

                    # check multiple pieces that can be captured
                    elif capture_position == opposing_piece:

                        # update the position and make a recursive call
                        check_x, check_y = x + move_x, y + move_y

                        # check that this position is in bounds and has more opponents to capture
                        while row_length > check_x >= 0 and column_length > check_y >= 0 and \
                                self._board[check_x][check_y] == opposing_piece:

                            # increment neighboring directions to current position
                            check_x += move_x
                            check_y += move_y

                            # check that there is an empty slot on the other side to capture
                            if row_length > check_x >= 0 and column_length > check_y >= 0 and \
                                    self._board[check_x][check_y] == ".":
                                # append validated move into list
                                validated_x, validated_y = check_x, check_y
                                available_positions.append((validated_x, validated_y))

                                # increment direction and make recursive call to check again
                                rec_validate_move(validated_x, validated_y, move_x, move_y)

        # check for capturing moves within current pieces in board
        for position in existing_positions:
            row, column = position

            moves = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]

            # call validate_move for each direction (right, left, up, down, diagonal)
            for x_direction, y_direction in moves:
                rec_validate_move(row, column, x_direction, y_direction)

        # skip a turn if no available positions are available for a player
        if not list(set(available_positions)):

            if player.get_color() == "purple":
                print("no positions for purple")
                self.message = "No moves for player 1. Player 2's turn"
                self.player1_positions = False

            if player.get_color() == "rose":
                print("no positions for rose")
                self.message = "No moves for player 2. Player 1's turn"
                self.player2_positions = False

            if not self.player1_positions and not self.player2_positions:
                print("no positions for BOTH players, ending the game.")
                self.return_winner()

            else:
                print("only one player has no positions available. switching players.")
                self.switch_players(self.current_player)

            return

        # Calculate the total grid size with padding
        total_grid_size = self.grid_size * (2 * self.radius + self.cell_padding) - self.cell_padding
        total_size = total_grid_size + 2 * self.outer_padding
        start_x = (self.window_width - total_size) // 2
        start_y = (self.window_height - total_size) // 2

        # Initialize the starting pieces of the board based on self._board
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):

                # Draw circles on available positions
                for position in available_positions:
                    row, column = position

                    # Calculate the center coordinates of the cell within the grid
                    center_x = start_x + self.outer_padding + self.radius + column * (
                                2 * self.radius + self.cell_padding)
                    center_y = start_y + self.outer_padding + self.radius + row * (2 * self.radius + self.cell_padding)

                    # Create a rectangle around the cell
                    cell_rect = pygame.Rect(
                        center_x - self.radius,
                        center_y - self.radius,
                        2 * self.radius,
                        2 * self.radius
                    )

                    pygame.draw.circle(self.window, (255, 255, 255), cell_rect.center, self.radius)

        # checks if there are still positions for either player
        if player.get_color() == "purple":
            self.player1_positions = True

        if player.get_color() == "rose":
            self.player2_positions = True

        sort_positions = sorted(available_positions)

        return sort_positions

    def flip_piece(self, color, piece_position):
        """
        Represents a method that takes in the position of the player piece
        and will flip the piece at neighboring positions to the player piece and
        updates the progress of the board.
        """
        row, column = piece_position

        if color.get_color() == "rose":
            player = "O"
            opponent = "X"
            player_color = self.rose
        else:
            player = "X"
            opponent = "O"
            player_color = self.purple

        moves = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]

        for x_direction, y_direction in moves:

            # traverse to neighboring areas with piece_position
            x, y = row + x_direction, column + y_direction

            flip_pieces = []
            while self._board[x][y] == opponent:
                # add captured pieces to the list
                flip_pieces.append((x, y))

                # iterate while loop to move again to flip multiple pieces
                x += x_direction
                y += y_direction

            # if loop ends with a player's piece on other end
            if self._board[x][y] == player:

                # flip the captured pieces
                for flip_piece in flip_pieces:
                    flip_row, flip_column = flip_piece
                    self._board[flip_row][flip_column] = player
                    pygame.draw.circle(self.window, player_color, self.cell_rect.center, self.radius)

    def make_move(self, color, piece_position):
        """
        Represents a method that takes in the position of the player piece.

        The piece at that position for that color is placed and the board
        is updated to the current status. Pieces are also flipped accordingly.
        """
        row, col = piece_position

        # if parameter passed in is black, piece is X
        if color == "purple":
            player = "X"
        else:
            player = "O"

        # place current piece onto the board
        self._board[row][col] = player

        # call this method to flip opposing pieces to player pieces
        self.flip_piece(self.current_player, (row, col))

        return row, col

    def count_grid(self):
        """
        Represents a method.......
        """
        # Initialize counts
        self.player1_count = 0
        self.player2_count = 0

        for row in self._board:
            for column in row:
                if column == "X":
                    self.player1_count += 1

                if column == "O":
                    self.player2_count += 1

    def run(self):
        """
        Represents a method that handles the state of the game Reversi.
        :return:
        """

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Detect any event when clicked
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.state == "intro":
                            if self.intro_start_button.collidepoint(event.pos):
                                self.state = "grid"

                        elif self.state == "grid":
                            if self.grid_back_button.collidepoint(event.pos):
                                self.state = "intro"

                            if self.grid_help_button.collidepoint(event.pos):
                                self.state = "help"

                            for cell in self.cells:
                                if cell.collidepoint(event.pos):
                                    self.cell_clicked = True

                        elif self.state == "help":
                            if self.grid_back_button.collidepoint(event.pos):
                                self.state = "grid"

                # Detect any motion for hover state
                elif event.type == pygame.MOUSEMOTION:
                    if self.state == "intro":
                        if self.intro_start_button.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                    if self.state == "grid":
                        if self.grid_back_button.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        elif self.grid_help_button.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                    if self.state == "help":
                        if self.grid_back_button.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.state == "intro":
                self.draw_intro()

            elif self.state == "grid":
                self.draw_grid()

            elif self.state == "help":
                self.draw_help()

            pygame.display.update()


game = Reversi()
game.run()
