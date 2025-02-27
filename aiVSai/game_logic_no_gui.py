import copy
import math
import random

class MancalaBoard:
    def __init__(self):
        # Initialize the board with 4 seeds in each pit
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,  # Player 1's pits
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,  # Player 2's pits
            1: 0,  # Player 1's store
            2: 0   # Player 2's store
        }
        
        # Player 1's pits
        self.player1_pits = ['A', 'B', 'C', 'D', 'E', 'F']
        
        # Player 2's pits
        self.player2_pits = ['G', 'H', 'I', 'J', 'K', 'L']
        
        # Opposite pits for capturing the component seeds
        self.opposite_pits = {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }
        
        # Next pit sequence (counterclockwise)
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 1,
            1: 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L', 
            'L': 2, 2: 'A'
        }
        
    def possibleMoves(self, player_pits):
        # Return pits with seeds for the given player
        return [pit for pit in player_pits if self.board[pit] > 0]
    
    def doMove(self, player_pits, pit):
        # Collect seeds from the chosen pit & empty the pit
        seeds = self.board[pit]
        self.board[pit] = 0
        
        # Distribute seeds counterclockwise
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
        
        # Check for capturing seeds
        if str(current_pit) in player_pits and self.board[current_pit] == 1:
            opposite_pit = self.opposite_pits[current_pit]
            if self.board[opposite_pit] > 0:
                # Capture seeds in the current pit and opposite pit
                store = 1 if player_pits == self.player1_pits else 2
                self.board[store] += self.board[current_pit] + self.board[opposite_pit]
                self.board[current_pit] = 0
                self.board[opposite_pit] = 0
        
        # Return whether the last seed landed in the player's store (extra turn)
        return isinstance(current_pit, int) and current_pit == (1 if player_pits == self.player1_pits else 2)

    def copy(self):
        """Create a deep copy of the board state"""
        new_board = MancalaBoard()
        new_board.board = self.board.copy()
        return new_board

class Game:
    def __init__(self, human_side='G', computer_side='A'):
        self.state = MancalaBoard()
        self.playerSide = {
            1: computer_side,   
            -1: human_side      
        }
    
    def gameOver(self):
        # Check if either player has no seeds in their pits
        player1_empty = all(self.state.board[pit] == 0 for pit in self.state.player1_pits)
        player2_empty = all(self.state.board[pit] == 0 for pit in self.state.player2_pits)
        
        if player1_empty or player2_empty:
            # Collect remaining seeds
            remaining_pits = self.state.player2_pits if player1_empty else self.state.player1_pits
            store = 2 if player1_empty else 1
            
            for pit in remaining_pits:
                self.state.board[store] += self.state.board[pit]
                self.state.board[pit] = 0
            
            return True
        return False
    
    def findWinner(self):
        player1_score = self.state.board[1]
        player2_score = self.state.board[2]
        
        if player1_score > player2_score:
            return 'Player 1', player1_score
        elif player2_score > player1_score:
            return 'Player 2', player2_score
        else:
            return 'Tie', player1_score
    
    def evaluate_ai1(self):
        return self.state.board[1] - self.state.board[2]

        
    def evaluate_ai2(self):
        # Advanced heuristic: Consider store, pit distribution, and potential moves
        store_diff = self.state.board[1] - self.state.board[2]
        
        # Bonus for more potential moves
        player1_moves = len(self.state.possibleMoves(self.state.player1_pits))
        player2_moves = len(self.state.possibleMoves(self.state.player2_pits))
        moves_diff = player1_moves - player2_moves
        
        # Bonus for pit distribution (encourage spreading seeds)
        player1_total_seeds = sum(self.state.board[pit] for pit in self.state.player1_pits)
        player2_total_seeds = sum(self.state.board[pit] for pit in self.state.player2_pits)
        distribution_bonus = player1_total_seeds - player2_total_seeds
        
        return store_diff + 0.5 * moves_diff + 0.3 * distribution_bonus

class Play:
    def __init__(self, ai1_side='A', ai2_side='G', human_side=None):
        self.game_ai1 = Game(computer_side=ai1_side)
        self.game_ai2 = Game(computer_side=ai2_side)
        self.human_side = human_side
    
    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta, ai_type='ai1'):
        if game.gameOver() or depth == 0:
            evaluation_func = game.evaluate_ai1 if ai_type == 'ai1' else game.evaluate_ai2
            return evaluation_func(), None
  
        if player == 1:  # MAX player (computer)
            best_value = -math.inf
            best_pit = None

            # Determine which pits belong to the computer
            player_pits = (game.state.player1_pits 
                           if game.playerSide[player] in game.state.player1_pits 
                           else game.state.player2_pits)

            for pit in game.state.possibleMoves(player_pits):
                child_game = copy.deepcopy(game)
                is_extra_turn = child_game.state.doMove(game.playerSide[player], pit)
                
                # If extra turn, recursively call with the same player
                next_player = player if is_extra_turn else -player
                value, _ = self.MinimaxAlphaBetaPruning(
                    child_game, next_player, depth-1, alpha, beta, ai_type
                )
                
                if value > best_value:
                    best_value = value
                    best_pit = pit
                
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            
            return best_value, best_pit
        
        else:  # MIN player 
            best_value = math.inf
            best_pit = None
            
            player_pits = (game.state.player1_pits 
                           if game.playerSide[player] in game.state.player1_pits 
                           else game.state.player2_pits)
            
            for pit in game.state.possibleMoves(player_pits):
                child_game = copy.deepcopy(game)
                is_extra_turn = child_game.state.doMove(game.playerSide[player], pit)
                
                # If extra turn, recursively call with the same player
                next_player = player if is_extra_turn else -player
                value, _ = self.MinimaxAlphaBetaPruning(
                    child_game, next_player, depth-1, alpha, beta, ai_type
                )
                
                if value < best_value:
                    best_value = value
                    best_pit = pit
                
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            
            return best_value, best_pit
    
    def ai1_turn(self):
        # Increased depth from 4 to 6 for more strategic look-ahead
        _, best_move = self.MinimaxAlphaBetaPruning(
            self.game_ai1, 1, depth=6, alpha=-math.inf, beta=math.inf, ai_type='ai1'
        )
        
        print(f"\nAI 1 chooses pit: {best_move}")
        self.game_ai1.state.doMove(
            self.game_ai1.state.player1_pits if best_move in self.game_ai1.state.player1_pits 
            else self.game_ai1.state.player2_pits, 
            best_move
        )
    
    def ai2_turn(self):
        # AI 2 using advanced heuristic
        _, best_move = self.MinimaxAlphaBetaPruning(
            self.game_ai2, 1, depth=4, alpha=-math.inf, beta=math.inf, ai_type='ai2'
        )
        
        print(f"\nAI 2 chooses pit: {best_move}")
        self.game_ai2.state.doMove(
            self.game_ai2.state.player1_pits if best_move in self.game_ai2.state.player1_pits 
            else self.game_ai2.state.player2_pits, 
            best_move
        )
    
    def printBoard(self, game):
        board = game.state.board
        print("\n    L  K  J  I  H  G")
        print("    {} {} {} {} {} {}".format(
            board['L'], board['K'], board['J'], board['I'], board['H'], board['G']))
        print("{}                    {}".format(board[2], board[1]))
        print("    {} {} {} {} {} {}".format(
            board['A'], board['B'], board['C'], board['D'], board['E'], board['F']))
        print("    A  B  C  D  E  F")
    
    def play_ai_vs_ai(self):
        print("Welcome to Mancala AI vs AI Game!")
        current_game = self.game_ai1  # Start with AI1's game
        ai_turn = 1  # 1 for AI1, -1 for AI2
        
        while not self.game_ai1.gameOver():
            # Alternate between AI1 and AI2
            if ai_turn == 1:
                self.printBoard(self.game_ai1)
                self.ai1_turn()
                # Check if extra turn for AI1
                extra_turn = any(self.game_ai1.state.board[pit] == 0 for pit in self.game_ai1.state.player1_pits)
                ai_turn = 1 if extra_turn else -1
            else:
                self.printBoard(self.game_ai2)
                self.ai2_turn()
                # Check if extra turn for AI2
                extra_turn = any(self.game_ai2.state.board[pit] == 0 for pit in self.game_ai2.state.player2_pits)
                ai_turn = -1 if extra_turn else 1
        
        # Determine the winner based on AI1's game (psq both games will have same final state)
        winner, score = self.game_ai1.findWinner()
        print(f"\nGame Over! {winner} wins with {score} seeds.")

if __name__ == "__main__":
    game = Play()
    game.play_ai_vs_ai()