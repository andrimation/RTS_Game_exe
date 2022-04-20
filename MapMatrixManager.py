import numpy
from GameUnit import GameUnit
from Building import Building

class MapMatrixManager():
    def __init__(self,root):
        self.root = root

    def create_main_matrix(self):
        imageX, imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size
        matrixX = int(imageX / 60)
        matrixY = int(imageY / 60)

        for y in range(matrixY):
            self.root.gameMapMatrix.append([])
            imageY -= 60
            for x in range(matrixX):
                self.root.gameMapMatrix[-1].append([x * 60, imageY])

    def convert_matrix_to_numpy_array(self):
        convertedMap = []
        for line in self.root.gameMapMatrix:
            newLine = []
            for point in line:
                newLine.append(0)
            convertedMap.append(newLine)
        self.root.numpyMapMatrix = numpy.array(convertedMap, dtype=object)

    def force_update_game_matrix(self):
        positions = []
        for object in self.root.children:
            if isinstance(object, GameUnit):
                positions.append(object.matrixPosition)
            elif isinstance(object, Building):
                for smallPos in object.fullMatrixPosition:
                    positions.append(smallPos)

        for x in range(len(self.root.gameMapMatrix) - 1):
            for y in range(len(self.root.gameMapMatrix[0]) - 1):
                if [x, y] in positions:
                    self.root.numpyMapMatrix[x][y] = 1
                else:
                    self.root.numpyMapMatrix[x][y] = 0