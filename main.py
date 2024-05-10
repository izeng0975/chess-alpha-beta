from AlphaBetaChessTree import AlphaBetaChessTree


def main():
    #fen = "4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1"
    fen = "rnbqkb1r/1p3ppp/p2ppn2/8/3NP3/2N5/PPP2PPP/R1BQKB1R b KQkq - 1 6"
    #fen = ""
    chess_tree = AlphaBetaChessTree(fen)
    best = chess_tree.get_best_next_move(fen, 3)

    print("Best move:", best)

    # Please implement your own main function to test the AlphaBetaChessTree class.
    # Try various FEN strings and different depths to see how your algorithm performs.
    # You can also implement your own evaluation functions to test the algorithm with different strategies.
    # For example, you could implement a simple evaluation function that counts the material value of the pieces.
    # (optional) It is recommended to implement methods to visualize your board state and moves.
    # chess_tree.visualize_tree()
    # chess_tree.visualize_decision_process(chess_tree._board, 2, best_move, "SAN")

    # (optional) It is recommended to support the export of tree statistics to understand tree pruning.

    # Feel free to add additional FEN strings and test cases to further evaluate your algorithms below.


if __name__ == "__main__":
    main()
