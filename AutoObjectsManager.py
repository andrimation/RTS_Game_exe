from Uran import Uran
import random
from kivy.core.window import Window

class AutoObjectsManager():
    def __init__(self,root):
        self.root = root

    def create_uran_fields(self):
        uranOrigins = [[random.randint(0, len(self.root.gameMapMatrix) - 1), random.randint(0, len(self.root.gameMapMatrix[0]) - 1)]
                       for x in range(10)]
        for position in uranOrigins:
            count = random.randint(5, 15)
            for nugget in range(count):
                uranOnMap = Uran()
                y = random.randint(-5, 5)
                while position[0] + y > len(self.root.gameMapMatrix) - 1 or position[0] + y < 0:
                    y = random.randint(-5, 5)
                x = random.randint(-5, 5)
                while position[1] + x > len(self.root.gameMapMatrix[0]) - 1 or position[0] + y < 0:
                    x = random.randint(-5, 5)
                if self.root.numpyMapMatrix[position[0] + y][position[1] + x] == 0:
                    uranOnMap.root = self.root
                    uranOnMap.matrixPosition = [position[0] + y, position[0] + x]
                    uranOnMap.pos = [
                        self.root.gameMapMatrix[uranOnMap.matrixPosition[0]][uranOnMap.matrixPosition[1]][0] + Window.size[
                            0] * 0.1, self.root.gameMapMatrix[uranOnMap.matrixPosition[0]][uranOnMap.matrixPosition[1]][1]]
                    uranOnMap.add_on_minimap()
                    self.root.urans.append(uranOnMap)
                    self.root.onMapObjectsToShift.append(uranOnMap)
                    self.root.add_widget(uranOnMap, canvas="before", index=self.root.ids["SidePanelWidget"].index + 1)

    def auto_units_actions(self):
        for object in self.root.autoUnits:
            object.mineUran()

        for object in self.root.movableObjects:
            object.auto_attack()

        for building in self.root.buildings:
            building.animate_building()
            building.auto_attack()