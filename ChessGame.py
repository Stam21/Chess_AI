"""
This class stores all the information of the current state about the chess game, as well as 
information about the validity of moves.
"""
import numpy as np

class GameState():
    def __init__(self):
        self.board = [
            np.array(["bR","bN","bB","bQ","bK","bB","bN","bR"]),
            np.array(["bp","bp","bp","bp","bp","bp","bp","bp"]),
            np.array([" "," "," "," "," "," "," "," "]),
            np.array([" "," "," "," "," "," "," "," "]),
            np.array([" "," "," "," "," "," "," "," "]),
            np.array([" "," "," "," "," "," "," "," "]),
            np.array(["wp","wp","wp","wp","wp","wp","wp","wp"]),
            np.array(["wR","wN","wB","wK","wQ","wB","wN","wR"])
        ]
        self.whiteMove = True
        