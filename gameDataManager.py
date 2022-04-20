from HumanPlayer import HumanPlayer
from ComputerPlayer import ComputerPlayer
from MoveQueueManager import MoveQueueManager
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.uix.image import Image,CoreImage
from kivy.uix.button import Button
from GameUnit import GameUnit,StartButton
from GameUnit import Tank
from GameUnit import RocketLauncher
from Building import Building
from Uran import Uran
from UranMiner import UranMiner
from BulletManager import BulletManager
from InteractiveMapManager import InteractiveMapManager
from AutoObjectsManager import AutoObjectsManager
from MapMatrixManager import MapMatrixManager
import os

import gc
import io

class Game_state_reset():
    def __init__(self,root):
        self.root = root
        self.root.scrollEnabled = True
        self.root.clickOnMapEnabled = True

    def set_game_data(self):
        """Setting main variables to begin state"""
        self.root.miniMap = None
        self.root.gameDataObject = Game_state_reset(self.root)
        self.root.humanPlayer = HumanPlayer(self.root)
        self.root.computerPlayer = ComputerPlayer(self.root)
        self.root.computerPlayerEnabled = False
        self.root.moveQueueManager = MoveQueueManager(self.root)
        self.root.bulletManager = BulletManager(self.root)
        self.root.interactiveMapManager = InteractiveMapManager(self.root)
        self.root.autoObjectsManager = AutoObjectsManager(self.root)
        self.root.mapMatrixManager = MapMatrixManager(self.root)

        self.root.building_add_index = 1
        self.root.obj_add_index = 1
        self.root.positionX = Window.size[0] * 0.1
        self.root.positionY = 0
        self.root.shiftX = 0
        self.root.shiftY = 0
        self.root.scrollEnabled = True
        self.root.clickOnMapEnabled = True
        self.root.counter = 0
        self.root.miniMapCounter = 0

        self.root.gameMapMatrix = []
        self.root.numpyMapMatrix = []
        self.root.move_queue = []
        self.root.orders_destinations = []
        self.root.path_compute_threads = []

        self.root.buildingToAdd = []
        self.root.miniMapObject = None
        self.root.miniMapUnits = {}
        self.root.humanPlayerUnits = []
        self.root.computerPlayerUnits = []
        self.root.combatTeamsCounterHuman = 0
        self.root.combatTeamsCounterComp = 0

        self.root.selectedUnits = False
        self.root.onMapObjectsToShift = []
        self.root.movableObjects = []
        self.root.buildings = []
        self.root.bullets = []
        self.root.autoUnits = []
        self.root.urans = []
        self.root.ids["MainMapPicture"].shiftXCounter = 0
        self.root.ids["MainMapPicture"].shiftYCounter = 0
        self.root.ids["MainMapPicture"].x = 0
        self.root.ids["MainMapPicture"].y = 0
        self.root.ids["MapView"].root = self.root
        self.root.ids["MainMapPicture"].root = self.root
        self.root.ids["MapView"].scroll_timeout = 1  # Zsisablować multitouch
        self.root.ids["MapView"].scroll_distance = 100000000
        self.root.ids["MainMapPicture"].scroll_timeout = 1
        self.root.ids["MainMapPicture"].scroll_distance = 100000000

        # Selection box
        self.root.selectBoxSizes = []
        self.root.selectBoxesObjects = []

        # Buttons status
        self.root.ids["MenuButton_BuildMainBase"].disabled = True
        self.root.ids["MenuButton_BuildRafinery"].disabled = True
        self.root.ids["MenuButton_BuildPowerPlant"].disabled = True
        self.root.ids["MenuButton_BuildWarFactory"].disabled = True
        self.root.ids["MenuButton_BuildDefenceTower"].disabled = True

        # Clean counter
        self.root.clean_counter = 0


    def start_game(self,*args):
        """Creates main game"""
        if self.root.restart == 0:
            self.root.remove_widget(self.root.ids["StartButton"])
        self.root.create_map_matrix()
        self.root.convertMapNumpy()
        self.root.ids["MenuButton_BuildMainBase"].disabled = False
        self.root.positionX = Window.size[0] * 0.1
        self.root.create_minimap()
        self.root.add_uran()
        self.root.update_money()
        self.root.computerPlayerEnabled = True
        self.root.computerPlayer.execute_build_plan()
        self.root.restart += 1

    def reset_game_objects(self,winner):
        """Clears all widgets ( except two needed ), creates start button"""
        widgetKivy = self.root.children.pop(0)
        mapView    = self.root.children.pop(-1)
        self.root.clear_widgets()
        self.root.children = [widgetKivy,mapView]
        startButton = StartButton(self.root)
        startButton.id = "StartButton"
        startButton.text = winner
        self.root.add_widget(startButton)


    def load_models_animations_to_memory(self):
        """Function loads all animations of game objects to RAM"""
        self.root.tank_friend_animation = {}
        self.root.tank_enemy_animation  = {}

        self.root.rocketLauncher_friend_animation = {}
        self.root.rocketLauncher_enemy_animation = {}

        self.root.main_base_friend_animation = {}
        self.root.main_base_enemy_animation = {}

        self.root.war_factory_friend_animation = {}
        self.root.war_factory_enemy_animation = {}

        self.root.rafinery_friend_animation = {}
        self.root.rafinery_enemy_animation = {}

        self.root.power_plant_friend_animation = {}
        self.root.power_plant_enemy_animation = {}

        self.root.defence_friend = {}
        self.root.defence_enemy = {}

        self.root.uran_miner_friend = {}
        self.root.uran_miner_enemy = {}

        self.root.uran_source = {}
        self.root.bullet_friend_source = {}
        self.root.bullet_enemy_source = {}

        # Iterate lists
        objectNames = ["Tank_friend/","Tank_enemy/","Rocket_friend/","Rocket_enemy/","Main_base_friend/","Main_base_enemy/",
                       "War_factory_friend/","War_factory_enemy/","Rafinery_friend/","Rafinery_enemy/",
                       "Power_plant_friend/","Power_plant_enemy/","Defence_friend/","Defence_enemy/",
                       "Uran_miner_friend/","Uran_miner_enemy/","Uran_source/","Bullet_friend/","Bullet_enemy/"]
        imagesDicts = [self.root.tank_friend_animation,self.root.tank_enemy_animation,
                       self.root.rocketLauncher_friend_animation,self.root.rocketLauncher_enemy_animation,
                       self.root.main_base_friend_animation,self.root.main_base_enemy_animation,
                       self.root.war_factory_friend_animation,self.root.war_factory_enemy_animation,
                       self.root.rafinery_friend_animation,self.root.rafinery_enemy_animation,
                       self.root.power_plant_friend_animation,self.root.power_plant_enemy_animation,
                       self.root.defence_friend,self.root.defence_enemy,self.root.uran_miner_friend,self.root.uran_miner_enemy,
                       self.root.uran_source,self.root.bullet_friend_source,self.root.bullet_enemy_source]
        directory = "Models/Models_textures/"

        # Load images to memory
        for name,dictionary in zip(objectNames,imagesDicts):
            print("Loading unit animation to memory:",name[:-1])
            currentPath = directory + name
            for file in os.listdir(currentPath):
                if file.endswith("png"):
                    image = open(currentPath+file,"rb")
                    binaryImage = image.read()
                    dataImage = io.BytesIO(binaryImage)
                    textureImage = CoreImage(dataImage,ext="png").texture
                    dictName = file[:-4]
                    dictionary[dictName] = textureImage

    def check_game_state(self):
        winner = None
        if self.root.humanPlayer.money < 650 * 5 and self.root.humanPlayer.units == []:
            winner = """Computer player has won the game ! you got no units and no money to build!

                                            Click here to play again, Esc to exit."""
        elif self.root.computerPlayer.money < 650 * 5 and self.root.computerPlayer.units == []:
            winner = """You have won the game ! computer got no units and no money to build!

                                            Click here to play again, Esc to exit."""

        elif self.root.computerPlayer.MainBase == "Destroyed":
            winner = """You have won the game ! you destroyed computer`s main base!

                                                        Click here to play again, Esc to exit."""

        elif self.root.humanPlayer.MainBase == "Destroyed":
            winner = """Computer player has won the game ! you lost your main base!

                                                        Click here to play again, Esc to exit."""

        if winner != None:
            self.root.time = 0.5
            self.root.gameDataObject.reset_game_objects(winner)
            self.root.gameDataObject.set_game_data()


