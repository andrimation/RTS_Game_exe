from kivy.core.window import Window
from SelectBox import SelectBox
from UranMiner import UranMiner
import pyautogui
import math

class InteractiveMapManager():
    def __init__(self,root):
        self.root = root

    def create_selection_box(self, touch):
        """Function creates selection box"""
        if not self.root.selectedUnits:
            self.root.clickOnMapEnabled = False
            self.root.scrollEnabled = False
            if touch.pos[0] >= Window.size[0]*0.1:
                self.root.selectBoxSizes.append(touch.pos)
                boxStartPos = self.root.selectBoxSizes[0]
                selectBox = SelectBox()
                selectBox.pos = boxStartPos
                selectBox.size_hint = (None,None)
                selectBox.width = touch.pos[0]-boxStartPos[0]
                selectBox.height = touch.pos[1]-boxStartPos[1]
                self.root.add_widget(selectBox,index=self.root.ids["SidePanelWidget"].index+1)
                self.root.selectBoxesObjects.append(selectBox)
                if len(self.root.selectBoxesObjects) >= 2:
                    boxToRemove = self.root.selectBoxesObjects.pop(-2)
                    self.root.remove_widget(boxToRemove)
                self.root.ids["SidePanelWidget"].index = 0

    def remove_selection_box(self, touch):
        """Function removes all selection box widgets when mouse button up"""
        if self.root.selectBoxesObjects:

            selectBoxOrigin = self.root.selectBoxSizes[0]
            boxToRemove = self.root.selectBoxesObjects.pop()
            rangeXStart = int(selectBoxOrigin[0])
            rangeXEnd   = int(selectBoxOrigin[0] + boxToRemove.width)
            rangeYStart = int(selectBoxOrigin[1])
            rangeYEnd   = int(selectBoxOrigin[1] + boxToRemove.height)

            if rangeXStart > rangeXEnd:
                rangeXStart,rangeXEnd = rangeXEnd,rangeXStart

            if rangeYStart > rangeYEnd:
                rangeYStart,rangeYEnd = rangeYEnd,rangeYStart

            for object in self.root.movableObjects:
                if object.pos[0] in range(rangeXStart,rangeXEnd) and object.pos[1] in range(rangeYStart,rangeYEnd) and object.player == self.root.humanPlayer:
                    object.selected = True
                    if not isinstance(object,UranMiner):
                        for unit in self.root.movableObjects:
                            if unit.combatTeam == object.combatTeam and unit.side == object.side:
                                unit.selected = object.selected
                    self.root.selectedUnits = True

            self.root.remove_widget(boxToRemove)
            self.root.selectBoxSizes = []

        self.root.scrollEnabled = True
        self.root.ids["SidePanelWidget"].index = 0

    def deselect_all_objects_on_map(self):
        for object in self.root.movableObjects:
                object.selected = False
        self.root.selectedUnits = False

    def scroll_and_shift_objects(self):
        """Shifting objects on map while scrolling, so they remain on place"""
        if self.root.scrollEnabled:
            self.root.ids["MainMapPicture"].older = self.root
            mouseX,mouseY = pyautogui.position()
            width,height = pyautogui.size()
            mouseY = abs(mouseY-height)  #
            self.root.shiftX = self.root.ids["MainMapPicture"].moveX(mouseX,width)
            self.root.shiftY = self.root.ids["MainMapPicture"].moveY(mouseY,height)

            # Shift value for mouse position
            try:
                self.root.positionX += self.root.shiftX
            except:
                pass
            try:
                self.root.positionY += self.root.shiftY
            except:
                pass

            # Move minimap
            if self.root.miniMap != None:
                self.root.miniMap.update_view_position(self.root.shiftX,self.root.shiftY)

            # Shift all objects on map
            for element in self.root.onMapObjectsToShift:
                try:
                    element.x += self.root.shiftX
                except:
                    pass
                try:
                    element.y += self.root.shiftY
                except:
                    pass

            for element in self.root.bullets:
                try:
                    element.x += self.root.shiftX
                except:
                    pass
                try:
                    element.y += self.root.shiftY
                except:
                    pass

    def mouse_position_on_map(self,args):
        """Function computes mouse XY to XY in game matrix and returns XY and matrix YX"""
        if args[-1] == "building":
            imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size[1]
            x, y = args[0],args[1]
            bigMatrixY = math.floor(abs((abs(self.root.positionY) + y) - imageY) // 60)
            bigMatrixX = math.floor(x + abs(self.root.positionX - Window.size[0] * 0.1)) // 60
            return bigMatrixY,bigMatrixX
        # Convert kivy X,Y coords, to matrix coords
        imageY = self.root.ids["MainMapPicture"].ids["main_map_image"].size[1]
        x, y = args[1].pos

        # Actual cursor position in window.
        pos_X = (x // 60) * 60 + (Window.size[0] * 0.1)
        pos_Y = (y // 60) * 60

        # Cursor position in whole game matrix
        bigMatrixY = math.floor(abs((abs(self.root.positionY) + y) - imageY)//60)
        bigMatrixX = math.floor(x + abs(self.root.positionX-Window.size[0]*0.1))//60
        return pos_X, pos_Y, bigMatrixY, bigMatrixX

    def click_on_map_event(self,args):
        # self.root.updateGameMatrix()
        try:
            if args[1].button == "right":
                return self.root.deselect_all_objects_on_map()
        except:
            pass
        if args[0] != "Attack":
            # Deselect
            if args[1].button == "right":
                self.root.deselect_all_objects_on_map()

            # Move objects
            elif self.root.ids["MenuButton_AddSelect"].selected == False:
                pos_X, pos_Y, matrixX, matrixY = self.mouse_position_on_map(args)
            else:
                self.root.buildingToAdd = []

        # Add object,coords to orders compute
        elif args[0] == "Attack":
            matrixX, matrixY = args[1].matrixPosition

        elif args[0] == "Uran":
            matrixX, matrixY = args[1].matrixPosition

        selectedObjectsList = []
        for object in self.root.movableObjects:
            if object.selected == True:  # and object.side == "Friend":
                selectedObjectsList.append(object)
        # usedCoords = []
        if args[0] == "Attack":
            move = "Attack"
            target = args[1]
            # usedCoords.append([matrixX,matrixY])
        else:
            move = "Move"
            target = None
        if selectedObjectsList:
            for object in selectedObjectsList:
                if move == "Move":
                    self.root.orders_destinations.append([object, [matrixX, matrixY], move, target, None])
                    continue
                elif move == "Attack" and isinstance(object, UranMiner):
                    move = "Move"
                    self.root.orders_destinations.append(
                        [object, [matrixX, matrixY], move, target, list(target.matrixPosition.copy())])
                    continue
                elif move == "Attack":
                    self.root.orders_destinations.append(
                        [object, [matrixX, matrixY], move, target, list(target.matrixPosition.copy())])
                    continue