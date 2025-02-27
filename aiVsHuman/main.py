import pygame
import sys
import copy
import math
import random
#this is the best version
# Colors
BACKGROUND_COLOR = (247, 236, 216)  # Warm beige
BOARD_COLOR = (139, 69, 19)  # Dark brown
PIT_COLOR = (205, 133, 63)  # Lighter brown
SEED_COLORS = [
    (139, 69, 19),   # Dark Brown
    (165, 42, 42),   # Brown
    (210, 105, 30),  # Chocolate
    (160, 82, 45)    # Sienna
]
TEXT_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 215, 0)  # Gold for highlighting
BUTTON_COLOR = (160, 82, 45)  # Sienna
BUTTON_HOVER_COLOR = (205, 133, 63)  # Lighter brown

class MancalaBoard:
    def __init__(self):
        # Board initialization
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,
            1: 0, 2: 0
        }
        
        self.player1_pits = ['A', 'B', 'C', 'D', 'E', 'F']
        self.player2_pits = ['G', 'H', 'I', 'J', 'K', 'L']
        
        self.opposite_pits = {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }
        
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 1,
            1: 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L', 
            'L': 2, 2: 'A'
        }

    def possibleMoves(self, player_pits):
        return [pit for pit in player_pits if self.board[pit] > 0]
    
    def doMove(self, player_pits, pit):
        seeds = self.board[pit]
        self.board[pit] = 0
        
        current_pit = pit
        while seeds > 0: 
            current_pit = self.next_pit[current_pit]
            
            # Skip opponent's store
            if (isinstance(current_pit, int) and 
                ((player_pits == self.player1_pits and current_pit == 2) or 
                 (player_pits == self.player2_pits and current_pit == 1))):
                continue
            
            # Drop a seed
            self.board[current_pit] += 1
            seeds -= 1
        
        # Capturing seeds logic
        if str(current_pit) in player_pits and self.board[current_pit] == 1:
            opposite_pit = self.opposite_pits[current_pit]
            if self.board[opposite_pit] > 0:
                store = 1 if player_pits == self.player1_pits else 2
                self.board[store] += self.board[current_pit] + self.board[opposite_pit]
                self.board[current_pit] = 0
                self.board[opposite_pit] = 0

class MancalaPygame:
    def __init__(self):
        pygame.init()
        
        # Screen setup
        self.WIDTH, self.HEIGHT = 1200, 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Elegant Mancala')
        
        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 50)
        self.text_font = pygame.font.Font(None, 36)
        
        # Game state
        self.board = MancalaBoard()
        self.current_player = None
        self.game_over = False
        
        # Pit and seed rendering
        self.pit_positions = self.calculate_pit_positions()
        
    def draw_button(self, text, x, y, width, height, hover=False):
        """Draw a button with optional hover effect"""
        button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
        
        # Render text
        text_surface = self.text_font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
    
    def start_screen(self):
        """Display start screen to choose first player"""
        while True:
            self.screen.fill(BACKGROUND_COLOR)
            
            # Title
            title = self.title_font.render('Mancala', True, TEXT_COLOR)
            title_rect = title.get_rect(center=(self.WIDTH//2, 100))
            self.screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = self.subtitle_font.render('Choose Who Starts', True, TEXT_COLOR)
            subtitle_rect = subtitle.get_rect(center=(self.WIDTH//2, 200))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Get mouse position for hover effects
            mouse_pos = pygame.mouse.get_pos()
            
            # Player buttons
            you_button = self.draw_button(
                'You Start', 
                self.WIDTH//2 - 200, 
                300, 
                200, 
                75, 
                pygame.Rect(self.WIDTH//2 - 200, 300, 200, 75).collidepoint(mouse_pos)
            )
            
            computer_button = self.draw_button(
                'Computer Starts', 
                self.WIDTH//2 + 50, 
                300, 
                200, 
                75, 
                pygame.Rect(self.WIDTH//2 + 50, 300, 200, 75).collidepoint(mouse_pos)
            )
            
            # Instruction text
            instruction = self.text_font.render('Click to select who goes first', True, TEXT_COLOR)
            instruction_rect = instruction.get_rect(center=(self.WIDTH//2, 500))
            self.screen.blit(instruction, instruction_rect)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if you_button.collidepoint(event.pos):
                        self.current_player = -1  # Human starts
                        return
                    elif computer_button.collidepoint(event.pos):
                        self.current_player = 1  # Computer starts
                        return
            
            pygame.display.flip()
    
    def calculate_pit_positions(self):
        positions = {}
        
        # Stores
        positions[1] = (200, self.HEIGHT // 2 - 200, 100, 400)  # Left store (Player 2)
        positions[2] = (self.WIDTH - 200, self.HEIGHT // 2 - 200, 100, 400)  # Right store (Player 1)
        
        # Player 2 pits (top row)
        pit_labels = ['G', 'H', 'I', 'J', 'K', 'L']
        for i, label in enumerate(pit_labels):
            x = 350 + i * 120
            positions[label] = (x, 100, 100, 150)
        
        # Player 1 pits (bottom row)
        pit_labels = ['A', 'B', 'C', 'D', 'E', 'F']
        for i, label in enumerate(pit_labels):
            x = 350 + i * 120
            positions[label] = (x, self.HEIGHT - 250, 100, 150)
        
        return positions
    
    def draw_elegant_seeds(self, x, y, width, height, seed_count):
        """
        Render seeds in a more elegant and structured manner
        """
        seed_radius = 8  # Slightly smaller seeds
        max_seeds_per_row = 5  # Maximum seeds per row/grid
        
        # Seed positioning grid
        seed_spacing = seed_radius * 2.5
        
        for i in range(seed_count):
            # Calculate grid position
            row = i // max_seeds_per_row
            col = i % max_seeds_per_row
            
            # Center the seed grid within the pit
            grid_width = min(seed_count, max_seeds_per_row) * seed_spacing
            grid_height = (seed_count // max_seeds_per_row + 1) * seed_spacing
            
            start_x = x + width/2 - grid_width/2 + col * seed_spacing
            start_y = y + height/2 - grid_height/2 + row * seed_spacing
            
            # Slight randomness in seed position
            jitter_x = random.uniform(-seed_radius/2, seed_radius/2)
            jitter_y = random.uniform(-seed_radius/2, seed_radius/2)
            
            # Choose seed color with variation
            seed_color = SEED_COLORS[i % len(SEED_COLORS)]
            
            # Draw seed with subtle depth
            pygame.draw.circle(self.screen, seed_color, 
                               (int(start_x + jitter_x), int(start_y + jitter_y)), 
                               seed_radius)
            
            # Add subtle highlight for depth
            highlight_color = tuple(min(255, c + 30) for c in seed_color)
            pygame.draw.circle(self.screen, highlight_color, 
                               (int(start_x + jitter_x), int(start_y + jitter_y)), 
                               seed_radius // 2)
    
    def draw_board(self):
        # Background with subtle gradient
        for i in range(self.HEIGHT):
            r = int(247 * (1 - i/self.HEIGHT) + 220 * (i/self.HEIGHT))
            g = int(236 * (1 - i/self.HEIGHT) + 220 * (i/self.HEIGHT))
            b = int(216 * (1 - i/self.HEIGHT) + 200 * (i/self.HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, i), (self.WIDTH, i))
        
        # Game board with subtle shadow
        board_rect = pygame.Rect(300, 50, 600, 600)
        board_shadow = board_rect.inflate(10, 10)
        pygame.draw.rect(self.screen, (100, 100, 100, 50), board_shadow, border_radius=40)
        pygame.draw.rect(self.screen, BOARD_COLOR, board_rect, border_radius=30)
        
        # Draw pits and stores
        for pit, (x, y, width, height) in self.pit_positions.items():
            color = PIT_COLOR
            
            # Soft shadow for pits
            shadow_offset = 3
            shadow_color = tuple(max(0, c - 30) for c in color)
            
            # Draw pit shadow
            if isinstance(pit, int):
                pygame.draw.rect(self.screen, shadow_color, 
                                 (x + shadow_offset, y + shadow_offset, width, height), 
                                 border_radius=20)
                pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=20)
            else:
                pygame.draw.ellipse(self.screen, shadow_color, 
                                    (x + shadow_offset, y + shadow_offset, width, height))
                pygame.draw.ellipse(self.screen, color, (x, y, width, height))
            
            # Draw seeds in each pit
            seed_count = self.board.board[pit]
            self.draw_elegant_seeds(x, y, width, height, seed_count)
            
            # Seed count text with soft shadow
            seed_text = self.text_font.render(str(seed_count), True, TEXT_COLOR)
            shadow_text = self.text_font.render(str(seed_count), True, (200, 200, 200))
            
            text_rect = seed_text.get_rect(center=(x + width//2, y + height + 25))
            shadow_rect = shadow_text.get_rect(center=(x + width//2 + 2, y + height + 27))
            
            self.screen.blit(shadow_text, shadow_rect)  # Shadow first
            self.screen.blit(seed_text, text_rect)
        
        # Refined title with shadow
        title = self.title_font.render('Mancala', True, TEXT_COLOR)
        shadow_title = self.title_font.render('Mancala', True, (200, 200, 200))
        
        self.screen.blit(shadow_title, (self.WIDTH//2 - title.get_width()//2 + 2, 12))
        self.screen.blit(title, (self.WIDTH//2 - title.get_width()//2, 10))
        
        # Player indicators with improved styling
        player_text = 'Your Turn' if self.current_player == -1 else 'Computer Turn'
        player_color = (50, 150, 50) if self.current_player == -1 else (200, 50, 50)
        player_render = self.subtitle_font.render(player_text, True, player_color)
        
        self.screen.blit(player_render, (self.WIDTH//2 - player_render.get_width()//2, self.HEIGHT - 50))
    
    def handle_click(self, mouse_pos):
        for pit, (x, y, width, height) in self.pit_positions.items():
            if isinstance(pit, int):  # Skip stores
                continue
            
            # Check if click is within pit area
            pit_rect = pygame.Rect(x, y, width, height)
            if pit_rect.collidepoint(mouse_pos):
                # Check if it's a valid move for the human player
                if pit in self.board.possibleMoves(self.board.player1_pits):
                    self.board.doMove(self.board.player1_pits, pit)
                    self.current_player *= -1
                break
    
    def computer_turn(self):
        """Computer's turn using simple strategy"""
        # Get possible moves for computer (player 2 pits)
        possible_moves = self.board.possibleMoves(self.board.player2_pits)
        
        if possible_moves:
            # Randomly choose a pit with seeds
            chosen_pit = random.choice(possible_moves)
            
            # Make the move
            self.board.doMove(self.board.player2_pits, chosen_pit)
            
            # Switch player
            self.current_player *= -1
    
    def check_game_over(self):
        """Check if the game is over"""
        player1_empty = all(self.board.board[pit] == 0 for pit in self.board.player1_pits)
        player2_empty = all(self.board.board[pit] == 0 for pit in self.board.player2_pits)
        
        if player1_empty or player2_empty:
            # Collect remaining seeds
            remaining_pits = self.board.player2_pits if player1_empty else self.board.player1_pits
            store = 2 if player1_empty else 1
            
            for pit in remaining_pits:
                self.board.board[store] += self.board.board[pit]
                self.board.board[pit] = 0
            
            self.game_over = True
    
    def run(self):
        # Start with the start screen to choose first player
        self.start_screen()
        
        clock = pygame.time.Clock()
        
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.current_player == -1:
                    self.handle_click(event.pos)
            
            if self.current_player == 1:
                self.computer_turn()
            
            self.check_game_over()
            
            self.draw_board()
            pygame.display.flip()
            clock.tick(30)
        
        # Game over screen
        self.screen.fill(BACKGROUND_COLOR)
        winner_text = 'You Win!' if self.board.board[2] < self.board.board[1] else 'Computer Wins!'
        final_score = f'Final Score: You {self.board.board[1]} - {self.board.board[2]} Computer'
        
        winner = self.title_font.render(winner_text, True, TEXT_COLOR)
        score = self.subtitle_font.render(final_score, True, TEXT_COLOR)
        restart = self.text_font.render('Press R to Restart', True, TEXT_COLOR)
        
        self.screen.blit(winner, (self.WIDTH//2 - winner.get_width()//2, self.HEIGHT//2 - 100))
        self.screen.blit(score, (self.WIDTH//2 - score.get_width()//2, self.HEIGHT//2))
        self.screen.blit(restart, (self.WIDTH//2 - restart.get_width()//2, self.HEIGHT//2 + 100))
        
        pygame.display.flip()
        
        # Wait for restart
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.__init__()
                    self.run()
                    waiting = False

if __name__ == "__main__":
    game = MancalaPygame()
    game.run()
    pygame.quit()
    sys.exit()
