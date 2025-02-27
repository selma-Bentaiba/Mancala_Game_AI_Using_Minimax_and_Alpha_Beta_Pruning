import pygame
import sys
import time
from mancala_game import Play 
#works pretty well
class MancalaGUI:
    def __init__(self):
        pygame.init()

        # Screen dimensions and setup
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mancala AI vs AI")

        # Colors
        self.bg_color = (139, 69, 19)  # Wood-like background
        self.text_color = (255, 255, 255)
        self.pit_color = (85, 42, 10)  # Darker wood color for pits
        self.store_color = (50, 25, 5)  # Even darker color for stores

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Load wood texture
        try:
            self.wood_texture = pygame.image.load("wood_texture.jpeg")
            self.wood_texture = pygame.transform.scale(self.wood_texture, (self.screen_width, self.screen_height))
        except:
            # Fallback if image loading fails
            self.wood_texture = None

        # Initialize Mancala game logic
        self.game = Play()
        self.running = True
        self.history = []  # To store the history of game states
        self.current_index = -1
        self.last_move = None  # Track the last move made

        # Pit positioning
        self.pit_positions = {
            # AI 1's pits (bottom row)
            'A': (200, 500), 'B': (300, 500), 'C': (400, 500), 
            'D': (500, 500), 'E': (600, 500), 'F': (700, 500),
            
            # AI 2's pits (top row)
            'G': (700, 200), 'H': (600, 200), 'I': (500, 200), 
            'J': (400, 200), 'K': (300, 200), 'L': (200, 200),
            
            # Stores
            1: (800, 350),   # AI 1's store (right)
            2: (100, 350)    # AI 2's store (left)
        }

    def draw_board(self):
        # Draw background texture or fallback to color
        if self.wood_texture:
            self.screen.blit(self.wood_texture, (0, 0))
        else:
            self.screen.fill(self.bg_color)

        # Draw board outline
        pygame.draw.rect(self.screen, (70, 40, 20), 
                         (50, 150, self.screen_width - 100, 400), 4)

        # Draw pits and stores
        board = self.history[self.current_index] if self.history else self.game.game_ai1.state.board
        
        for pit, pos in self.pit_positions.items():
            # Determine pit color and size
            if isinstance(pit, int):
                # Stores are slightly larger
                color = self.store_color
                radius = 50
            else:
                color = self.pit_color
                radius = 40

            # Draw pit
            pygame.draw.circle(self.screen, color, pos, radius)
            pygame.draw.circle(self.screen, (120, 80, 50), pos, radius, 3)  # Border

            # Draw seed count
            seeds = board.get(pit, 0)
            text_surface = self.font.render(str(seeds), True, self.text_color)
            text_rect = text_surface.get_rect(center=pos)
            self.screen.blit(text_surface, text_rect)

        # Draw pit labels
        labels = {
            'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F',
            'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L',
            1: 'AI 1 Store', 2: 'AI 2 Store'
        }

        for pit, pos in self.pit_positions.items():
            label_surface = self.small_font.render(labels[pit], True, self.text_color)
            label_rect = label_surface.get_rect(center=(pos[0], pos[1] + 60 if pit in [1,2] else pos[1] + 50))
            self.screen.blit(label_surface, label_rect)

        # Highlight the last move if exists
        if self.last_move:
            if self.last_move in self.pit_positions:
                pygame.draw.circle(self.screen, (255,0,0), self.pit_positions[self.last_move], 55, 4)

    def draw_message(self, message):
        text_surface = self.font.render(message, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(text_surface, text_rect)

    def ai_turn(self, ai_function, ai_name):
        """Handles an AI's turn and updates the board."""
        # Clear previous messages
        self.screen.fill(self.bg_color if not self.wood_texture else (0,0,0), 
                         (0, 50, self.screen_width, 100))
        
        self.draw_message(f"{ai_name} is thinking...")
        pygame.display.flip()
        time.sleep(0.5)  # Slight pause for visibility
        # Store the last chosen move
        if ai_name == "AI 1":
            # Save the move before executing
            self.last_move = self._get_best_move(self.game.MinimaxAlphaBetaPruning, 
                                                 self.game.game_ai1, 
                                                 'ai1')
            # Execute AI's move
            ai_function()
        else:
            # Save the move before executing
            self.last_move = self._get_best_move(self.game.MinimaxAlphaBetaPruning, 
                                                 self.game.game_ai2, 
                                                 'ai2')
            # Execute AI's move
            ai_function()
    

        self.history.append(self.game.game_ai1.state.board.copy())  # Save state after move
        self.current_index += 1

        # Update the display with the new state
        self.update_display()
        time.sleep(0.5)  # Pause after move for clarity

    def _get_best_move(self, minimax_func, game, ai_type):
        """Helper method to get the best move without executing it."""
        _, best_move = minimax_func(
            game, 1, depth=6, alpha=-float('inf'), beta=float('inf'), ai_type=ai_type
        )
        return best_move

    def update_display(self):
        if self.wood_texture:
            self.screen.blit(self.wood_texture, (0, 0))
        else:
            self.screen.fill(self.bg_color)
        
        self.draw_board()
        pygame.display.flip()

    def handle_navigation(self, event):
        if event.key == pygame.K_LEFT:  # Backward
            if self.current_index > 0:
                self.current_index -= 1
                self.update_display()
        elif event.key == pygame.K_RIGHT:  # Forward
            if self.current_index < len(self.history) - 1:
                self.current_index += 1
                self.update_display()

    def display_winner_screen(self, winner, score):
        """Display a dedicated winner screen"""
        while True:
            self.screen.fill((50, 50, 50))  # Dark background
            
            # Winner text
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("Game Over!", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 200))
            self.screen.blit(title_text, title_rect)

            # Winner details
            winner_font = pygame.font.Font(None, 48)
            winner_text = winner_font.render(f"{winner} wins with {score} seeds!", True, (255, 255, 255))
            winner_rect = winner_text.get_rect(center=(self.screen_width // 2, 300))
            self.screen.blit(winner_text, winner_rect)

            # Instructions
            instruction_font = pygame.font.Font(None, 32)
            instruction_text = instruction_font.render("Press SPACE to view final board or ESC to quit", True, (200, 200, 200))
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, 500))
            self.screen.blit(instruction_text, instruction_rect)

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        return  # Return to show final board

    def main_loop(self):
        # Initialize game state history
        self.history.append(self.game.game_ai1.state.board.copy())
        self.current_index = 0
        self.update_display()
        ai_turn = 1

        winner_announced = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        self.handle_navigation(event)

            if not winner_announced and not self.game.game_ai1.gameOver():
                if ai_turn == 1:
                    self.ai_turn(self.game.ai1_turn, "AI 1")
                    ai_turn = -1
                else:
                    self.ai_turn(self.game.ai2_turn, "AI 2")
                    ai_turn = 1
            elif not winner_announced:
                # Game is over, determine winner
                winner, score = self.game.game_ai1.findWinner()
                
                # Display winner screen
                self.display_winner_screen(winner, score)
                
                winner_announced = True

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = MancalaGUI()
    gui.main_loop()