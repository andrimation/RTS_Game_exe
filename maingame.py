# Kivy
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from MainMapPicture import MainMapPicture
from MapView import MapView
from GameUnit import GameUnit,Bullet
from Building import Building
from MenuButton import MenuButton

from kivy.config import Config
from Uran import Uran
from SelectBox import SelectBox
from kivy.config import Config
from MoveQueueManager import MoveQueueManager
from UranMiner import UranMiner
from miniMap import miniMap
from gameDataManager import Game_state_reset
from BulletManager import BulletManager

# Others
import threading
import PIL
import random
import pyautogui
import math
import MarsPathfinder_setup
import numpy
import gc
import copy



# Fullscreen
Window.fullscreen = 'auto'    # To nam włacza fullscreen
# Mouse
Config.set("input","mouse","mouse,disable_multitouch")


class MainWindow(FloatLayout):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.restart = 0
        self.gameDataObject = Game_state_reset(self)
        self.gameDataObject.load_models_animations_to_memory()
        self.gameDataObject.set_game_data()
        Window.fullscreen = 'auto'

    def start(self,*args):
        self.gameDataObject.start_game(*args)

    def create_minimap(self):
        miniMapInit  = miniMap(self)
        miniMapInit.create_minimap()
        self.miniMap = miniMapInit

    # Create select box
    def on_touch_move(self, touch):
        self.interactiveMapManager.create_selection_box(touch)

    # Remove selection box
    def on_touch_up(self, touch):
        self.interactiveMapManager.remove_selection_box(touch)

    def deselect_all_objects_on_map(self):
        self.interactiveMapManager.deselect_all_objects_on_map()

    def scroll_game_map(self):
        self.interactiveMapManager.scroll_and_shift_objects()

    def create_map_matrix(self):
        self.mapMatrixManager.create_main_matrix()

    def convertMapNumpy(self):
        self.mapMatrixManager.convert_matrix_to_numpy_array()

    def add_uran(self):
        self.autoObjectsManager.create_uran_fields()

    def build_HumanPlayerUnit(self,unitType,side):
        self.humanPlayer.build_unit(unitType,side)

    def build_queue_execute(self):
        self.humanPlayer.execute_build_queue()

    def make_bullet(self, startObject, endPos):
        self.bulletManager.add_new_bullet(startObject,endPos)

    def add_building(self,*args):
        self.deselect_all_objects_on_map()
        buildingAdd = Building(self,args[1],self.humanPlayer,args[0])
        buildingAdd.add_to_game()

    def move_building_on_map(self):
        if self.buildingToAdd:
            currentBuilding = self.buildingToAdd[0]
            currentBuilding.move_building_widget_along_cursor()

    def update_money(self):
        self.ids["Money_label"].text = str(self.humanPlayer.money)

    def bullet_shot_execute(self):
        self.bulletManager.bullet_move()

    def move_queue_execute(self):
        self.moveQueueManager.execute_units_movement()

    def make_attack(self):
        self.moveQueueManager.attack()

    def compute_mouse_position(self,*args):
        return self.interactiveMapManager.mouse_position_on_map(args)

    def click_on_map(self,*args):
        self.interactiveMapManager.click_on_map_event(args)

    def compute_orders_paths(self):
        self.moveQueueManager.pathThreads_creator()

    def recomupute_all_orders(self):
        self.moveQueueManager.force_recompute_orders()

    def update_positionX(self):
        self.positionX = Window.size[0] * 0.1

    def updateGameMatrix(self):
        self.mapMatrixManager.force_update_game_matrix()

    def manage_auto_units(self):
        self.autoObjectsManager.auto_units_actions()

    def order_and_units_cleaner(self):
        self.moveQueueManager.force_units_and_orders_clean()

    def check_if_loose(self):
        self.gameDataObject.check_game_state()

###########################################################################

    def next_frame(self,*args):

        # Check mouse position, and move map.
        self.scroll_game_map()

        # Compute paths
        self.compute_orders_paths()

        # Attack
        self.make_attack()

        # Bulet shot
        self.bullet_shot_execute()

        # Move units on map
        self.move_queue_execute()

        # Adding buildings
        self.move_building_on_map()

        # Auto units behave
        self.manage_auto_units()

        # execute build queue
        self.build_queue_execute()

        # Clean orders  - not sure if necessary
        # self.clean_counter += 1
        # if self.clean_counter == 500:
        #     self.order_and_units_cleaner()
        #     self.clean_counter = 0

        # Make sure panel inex is 0
        self.ids["SidePanelWidget"].index = 0

        # Computer Player
        if self.computerPlayerEnabled:
            self.computerPlayer.execute_Computer_Play()

        self.check_if_loose()

        self.ids["MainMapPicture"].clear_explosions()

    pass

class MainGameApp(App):

    def build(self):
        mainwindow = MainWindow()
        Clock.schedule_interval(mainwindow.next_frame,0.01)
        return mainwindow

if __name__ == "__main__":
    MainGameApp().run()