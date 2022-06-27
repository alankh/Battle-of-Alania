# List off all the obstacles and unique tiles
waters = [[11, 0], [11, 1], [11, 3], [11, 4], [12, 4], [12, 6], 
        [13, 6], [13, 7], [13, 8], [13, 9], [14, 8], [14, 9], 
        [12, 9], [11, 9], [10, 9]]

bridges = [[11, 2], [12, 5]]

walls = [[0, 0], [0, 1], [2, 0], [2, 1], [3, 0], [3, 1], 
        [4, 0], [4, 1]]

forests = [[5, 0], [3, 2], [6, 2], [10, 2], [0, 3], [2, 4], 
        [5, 4], [7, 4], [3, 5], [8, 5], [0, 6], [2, 6], [3, 6], 
        [6, 6], [8, 6], [9, 6], [0, 7], [3, 7], [6, 7], [9, 7], 
        [3, 8], [5, 8], [6, 8], [5, 9], [5, 10], [1, 9], [6, 9], [8, 9]]

# Create the grid system
class Grid:

    def __init__(self):
        self.rows = 10
        self.cols = 15
        self.coords = []
        
    def createGrid(self):
        for i in range(self.rows):
            self.coords.append([])
            for j in range(self.cols):
                self.coords[i].append([j, i])

        return self.coords