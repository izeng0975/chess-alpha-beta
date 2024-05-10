from TreeNode import TreeNode
import chess


class AlphaBetaChessTree:
    def __init__(self, fen):
        """
        Initializes an AlphaBetaChessTree object with a board state.
        The board state is represented in FEN (Forsyth-Edwards Notation) format.
        :param fen: A string representing the chess board in FEN format.
        """
        board = chess.Board(fen)
        turn = 'white' if board.turn == chess.WHITE else 'black'
        self._root = TreeNode(board, turn)

    @staticmethod
    def get_supported_evaluations():
        """
        Static method that returns a list of supported evaluation methods.
        :return: A list of strings containing supported evaluation methods.
        """
        pass

    def _apply_move(self, move, node, notation="SAN"):
        """
        Applies a chess move to a given game state (node).
        :param move: The move to be applied.
        :param node: The game state to which the move is applied.
        :param notation: The notation system used for the move (default: "SAN" - Standard Algebraic Notation).
        """
        # move = chess.Move.from_uci(move) if notation == "UCI" else node._board.parse_san(move)
        # node._board.push(move)
        # node._turn = 'white' if node._board.turn else 'black'
        # new_node = TreeNode(node._board.copy(), node._turn)
        # self._root.add_child(new_node)
        new_board = node._board.copy()  # Make a copy of the current board
        if notation == "SAN":
            new_board.push_san(move)
            # return self._root, move  # Return the move in SAN notation
        else:
            new_board.push_uci(move)
            # return self._root, move.uci()  # Return the move in UCI notation
        new_node = TreeNode(new_board, "black" if node._turn == "white" else "white")
        node.add_child(new_node)
        return new_node
    
    def _create_node_from_fen(self, fen):
        """
        Creates a new TreeNode object from a given FEN string.
        :param fen: The FEN string representing the game state.
        :return: A TreeNode object representing the game state.
        """
        board = chess.Board(fen)
        turn = 'white' if board.turn == chess.WHITE else 'black'
        return TreeNode(board, turn)

    def _get_legal_moves(self, node, notation="SAN"):
        """
        Returns a list of all legal moves from the given game state (node).
        :param node: The game state from which to get legal moves.
        :param notation: The notation system used for the moves (default: "SAN").
        :return: A list of strings representing all legal moves for a given node.
        """
        legal_moves = []
        for move in node._board.legal_moves:
            if notation == "SAN":
                legal_moves.append(node._board.san(move))
            else:
                legal_moves.append(move.uci())
        return legal_moves

    def get_best_next_move(self, node, depth, notation="SAN"):
        """
        Determines the best next move for the current player using the Alpha-Beta pruning algorithm.
        :param node: The current game state.
        :param depth: The depth of the search tree to explore.
        :param notation: The notation system for the move (default: "SAN").
        :return: The best next move in the format defined by the variable notation.
        """
        node = self._create_node_from_fen(node)  # Convert FEN string to TreeNode object
        best_move = None
        best_score = float('-inf') if node._turn == 'white' else float('inf')
        legal_moves = self._get_legal_moves(node, notation)

        for move in legal_moves:
            child_node  = self._apply_move(move, node, notation)
            score = self._alpha_beta(child_node, depth - 1, float('-inf'), float('inf'), False if node._turn == 'white' else True)
            if node._turn == 'white':
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        self.get_board_visualization(node._board)
        return best_move

    def _alpha_beta(self, node, depth, alpha, beta, maximizing_player):
        """
        The Alpha-Beta pruning algorithm implementation. This method is used to evaluate game positions.
        :param node: The current node (game state).
        :param depth: The depth of the tree to explore.
        :param alpha: The alpha value for the Alpha-Beta pruning.
        :param beta: The beta value for the Alpha-Beta pruning.
        :param maximizing_player: Boolean indicating if the current player is maximizing or minimizing the score.
        :return: The best score for the current player.
        """
        if depth == 0 or node._board.is_game_over():
            return self._evaluate_position(node, depth)

        if maximizing_player:
            max_score = float('-inf')
            for move in self._get_legal_moves(node):
                child_node = self._apply_move(move, node)
                score = self._alpha_beta(child_node, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break  # Beta cutoff
            return max_score
        else:
            min_score = float('inf')
            for move in self._get_legal_moves(node):
                child_node = self._apply_move(move, node)
                score = self._alpha_beta(child_node, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_score

    def _evaluate_position(self, node, depth):
        """
        Evaluates the position at a given node, taking into account the depth of the node in the decision tree.
        :param node: The game state to evaluate.
        :param depth: The depth of the node in the game tree.
        :return: An evaluation score for the position.
        """
        base_score = self._evaluate_board(node._board)
        depth_adjusted_score = base_score / (depth + 1)  # Adjust the score based on the depth
        return depth_adjusted_score

    def _evaluate_board(self, board):
        """
        Evaluates a provided board and assigns a score.
        :param board: The board to evaluate.
        :return: An evaluation score for the board.
        """
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}  # Assign values to each piece type
        score = 0

        # Iterate over all squares on the board
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                # Add or subtract the value of the piece from the score
                score += piece_values[piece.symbol().upper()] if piece.color == chess.WHITE else -piece_values[piece.symbol().upper()]

        return score

    def get_board_visualization(self, board):
        """
        Generates a visual representation of the board.
        :param board: The board to visualize.
        :return: A visual representation of the board.
        """
        print(board)

    def visualize_decision_process(self, depth, move, notation="SAN"):
        """
        Visualizes the decision-making process for a particular move up to a certain depth.
        :param depth: The depth of the analysis.
        :param move: The move being analyzed.
        :param notation: The notation system for the move (default: "SAN").
        """
        node = self._root
        print("Initial board state:")
        self.get_board_visualization(node._board)

        for _ in range(depth):
            node, san_move = self._apply_move(move, node, notation)
            print(f"\nBoard state after move {san_move}:")
            self.get_board_visualization(node._board)
            if node._board.is_game_over():
                print("\nGame over.")
                break
            move = self.get_best_next_move(node, depth, notation)

    def export_analysis(self):
        """
        Exports the analysis performed by the AlphaBetaChessTree.
        """
        pass
