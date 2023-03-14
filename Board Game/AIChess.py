class ChessGame:
    def __init__(self):
        self.board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                      [' ', '.', ' ', '.', ' ', '.', ' ', '.'],
                      ['.', ' ', '.', ' ', '.', ' ', '.', ' '],
                      [' ', '.', ' ', '.', ' ', '.', ' ', '.'],
                      ['.', ' ', '.', ' ', '.', ' ', '.', ' '],
                      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                      ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
        self.current_player = 'white'
        self.piece_values = {'K': 10, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}

    def print_board(self):
        for row in self.board:
            print(' '.join(str(col) for col in row))

    def get_heuristic(self):
        heuristic = 0
        for row in self.board:
            for piece in row:
                if piece.isupper() and self.current_player == 'white':
                    heuristic += self.piece_values[piece]
                elif piece.islower() and self.current_player == 'black':
                    heuristic += self.piece_values[piece.upper()]
        return heuristic

    def play_game(self):
        while True:
            print('\n' + self.current_player + '\'s turn')
            self.print_board()
            print('Heuristic:', self.get_heuristic())

            # Get user input for move
            move = input('Enter move (e.g. "a2 a3"): ')

            # Check if move is valid
            # ...

            # Make move
            # ...

            # Switch to next player
            if self.current_player == 'white':
                self.current_player = 'black'
            else:
                self.current_player = 'white'

if __name__ == '__main__':
    game = ChessGame()
    game.play_game()

