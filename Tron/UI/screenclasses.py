################# Kivy Imports ############################
from kivy.app import App
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior

################ Imports ###################################
import re
import logging
import time
from datetime import datetime
import json
import copy

######## import own modules ############################
from collections import namedtuple
from Backend.Classes.GameClient import GameClient
from Backend.Classes.GameServer import GameServer
from Backend.Core.Vect2D import Vect2D
from Backend.Classes.Game import Game
from Backend.Classes.Arena import Arena
from Backend.Classes.HumanPlayer import HumanPlayer
from Backend.Classes.parser import *
from UI.Widgets.CountdownWidget import CountdownWidget
from UI.Widgets.TrackWidget import TrackWidget
from UI.Widgets.MyKeyboardListener import MyKeyboardListener
from UI.Widgets.PlayerWidget import PlayerWidget
from UI import mainUI

CLIENT: GameClient = GameClient()
datapath = "data.json"

# class GameUI(Widget):
class GameUI(Screen):
	countdown_is_running = BooleanProperty(False)
	game_is_running = BooleanProperty(False)
	playPos = ObjectProperty(Vect2D(10, 0))
	counter_for_running = NumericProperty(0)
	counter_games = NumericProperty(0)
	CLIENT = CLIENT

	def init_onenter(self, **kwargs):
		super(GameUI, self).__init__(**kwargs)
		self.__client = CLIENT
		CLIENT.EMatchEnded += self.on_match_ended
		self.playerList = self.__client.match.players
		self.ids.trackWidget.reset_init()
		# ## creates update function for all uses, ensures synchronized update trigger

		Clock.schedule_interval(self.update, 1 / UPDATES_PER_SECOND)
		logging.info("GameApp ENTERED")


	def update(self, *args):
	## final update function, where I trigger different functuions
		self.ids.trackWidget.update()
		self.ids.playerWidget.printPlayers()

		## functions should only be started after special event is triggered
		if self.countdown_is_running == True:
			## Despite trying to handle the information down, I was forced to create new function,
			## which triggers certain event in subclass
			self.ids.trackWidget.setBooleanCountdown()
			self.ids.trackWidget.increaseOpacity()
			self.ids.trackWidget.getFieldsize(CLIENT.match.arena.sizeX, CLIENT.match.arena.sizeY)

		## functions should only be started after special event is triggered
		if self.game_is_running == True:
			if self.counter_for_running == 0:
				CLIENT.i_am_ready()
				self.counter_for_running = 1
			## Despite trying to handle the information down, I was forced to create new function,
			## which triggers certain event in subclass
			self.ids.trackWidget.setBooleanGame()

		# if self.game_is_running == False:
		# self.game.ids.trackWidget.setBooleanGame_Ended()

	def getPlayerWidgetSize(self):
		## creates the hight for the widget in duty of displaying all players online
		try:
			playerCount = CLIENT.match.feat_players  # NOTE Playercount changed acc. to match
		except:
			playerCount = 0
		return (100, playerCount * 20)

	def do_finished(self):
		## event handler, sets the Booleans for opacity
		def callback(_):
			# Countdown abgelaufen
			# Spiel starten ...
			self.countdown_is_running = False
			self.game_is_running = True

		## after specified time callback function is called anbd game starts
		Clock.schedule_once(callback, 0)

	def updateUpdater(self):
		self.ids.headWidget.update_screen_size(self.size)

	def getControl(self):
		CLIENT.godmode_on()

	def on_match_ended(self, sender, reason):
		self.game_is_running = False
		self.ids.trackWidget.game_ended()
		
		self.exit()

class SettingsMenu(Screen):
	def loadplayerdata(self) -> None:
		"""
		Load the Player Name from data.json
		Load the Player Color from data.json

		Args: -
		Return: -
		"""
		filef = open(datapath)
		data = json.load(filef)
		playername = data[0]
		color = data[1]
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.nameTextInput.hint_text=("Current Playername: %s" % playername)
		self.ids.colordisplayLabel.background_color=playercolor
		
	def savechanges(self, playername: str, color: tuple) -> None:
		"""
		Saves the Player Name to backend and data.json
		Saves the Player Color to backend and data.json 

		Args:
			playername (str): new playername / old playername from data.json
			color (tuple): new color / old color from data.json
		Return: -
		"""
		# sends playername and color to backend, but if it wasnt changed, it sends the data of data.json to backend
		filef = open(datapath)
		loaddata = json.load(filef)
		if playername == "":
			playername = loaddata[0]
			CLIENT.me.setName(playername)
			print("Playername stayed: %s" % playername)
		else:
			CLIENT.me.setName(playername)
			print("Playername changed to: %s" % playername)

		r,g, b = color
		color = (int(r), int(g), int(b))

		if color == (0, 0, 0):
			playercolor = loaddata[1]
			color = (int(playercolor[0]), int(playercolor[1]), int(playercolor[2]))
			CLIENT.me.setColor(color)
			print("Color stayed: %s" % str(color))
		else:
			CLIENT.me.setColor(color)
			print("Color changed to: %s" % str(color))

		#saves the current playername and color in the json file data.json
		savedata = (playername, color, loaddata[2], loaddata[3])
		with open(datapath, 'w', encoding='utf-8') as outfile:
			json.dump(savedata, outfile)

	def validateInput(self, inpt: str) -> None:
		"""
		Validates the input of the playername text field

		Args: input (str): the playername
		Return: -
		"""
		self.inpt = inpt
		try:
			lastcharacter = self.inpt[-1:]
			x = re.findall("[a-zA-Z0-9_]", lastcharacter)
			if len(x) == 1:
				self.ids.nameTextInput.text = inpt
			else:
				rightstring = self.inpt[:-1]
				self.ids.nameTextInput.text = rightstring

		except Exception as e:
			logging.warning(str(e))

class SearchForLobbiesMenu(Screen):

	lobby = 0
	lobbies = []
	lobbiesdummy = [
    '198.168.0.1 - Lobby 1: 54001',
    '198.168.0.1 - Lobby 2: 54002',
    '198.168.0.1 - Lobby 3: 54003',
    '198.168.0.1 - Lobby 4: 54004',
    '198.168.0.1 - Lobby 5: 54005']

	def getPlayerdata(self):

		outputname = CLIENT.me.getName()
		if outputname == '':
			pass
		elif outputname == 'Enter_Name':
			pass
		else:
			self.ids.explainmenuLabel.text = ('Here you can Enter the Lobby as %s' % outputname)

		color = CLIENT.me.getColor()
		playercolor = (color[0]*255, color[1]*255, color[2]*255, 1)
		self.ids.explainmenuLabel.background_color = playercolor

	def getavailableLobbies(self):
		"""
		Get the Lobbies which are available

		Args:
			Lobbies (list): IP & Port
		Return:
			-
		"""
		CLIENT.discover_lobby()
		listlobbies = CLIENT.lobbies
		count_lobbies = listlobbies.__len__()
		lasthost = '0.0.0.0'
		k = 0
		for i in range(0,count_lobbies):
			indexlobby = listlobbies[i]
			currenthost = indexlobby.host
			self.lobbies.append('%s - Lobby %d: %s' % (indexlobby.host, i+1, indexlobby.port))

		return self.lobbies

	def update_list(self):
		self.ids.lobby_port.data = [{'text' : str(x)} for x in self.lobbies]

	def clear_list(self):
		self.lobbies.clear()

	def updatechosenLobby(self, currentlobby):
		"""
		Sets variable for choosen Lobby

		Args:
			Lobby (int):
		Return:
			Lobby (int)
		"""
		self.currentlobby = currentlobby
		self.lobby = int(self.currentlobby)
		logging.info('UI Search for Lobby Menu: Lobby %d has been clicked by player.' % (self.lobby+1))
		SearchForLobbiesMenu.lobby = self.lobby

	def enterLobby(self):
		"""
		Sends Lobby to Server

		Args:
			-
		Return:
			-
		"""
		logging.info('UI Search for Lobbies Menu: Player enters Lobby %s with Index %s' % (self.lobby+1, self.lobby))
		CLIENT.enter_lobby(self.lobby)

class MainMenu(Screen):

	def loadplayerdata(self) -> None:
		"""
		Load the Player Name from data.json
		Load the Player Color from data.json

		Args: -
		Return: -
		"""
		try:
			filef = open(datapath)
			data = json.load(filef)
			playername = data[0]
			color = data[1]
			wincount = data[2]
			lostcount = data[3]
			playercolor = (color[0], color[1], color[2])
			CLIENT.me.setName(playername)
			CLIENT.me.setColor(playercolor)
		except:
			savedata = ("Enter_Name", (0,0,0), 0, 0)
			with open(datapath, 'w', encoding='utf-8') as outfile:
				json.dump(savedata,outfile)


	def quit(self) -> None:
		#CreateServerMenuFloat.statusServer(self, False, 0)
		#self.server.Stop()
		#self.client.Stop()
		try:
			CLIENT.close()
		except:
			pass
		exit()

class LobbyMenu(Screen):

	match = 0
	matchlist = []
	sentmatch = 0
	sentmatches = []

	def getPlayerdata(self):
		"""
		Get the Playerdata from the current Player to display in headerlabel
		"""

		outputname = CLIENT.me.getName()
		if outputname == '':
			pass
		elif outputname == 'Enter_Name':
			pass
		else:
			self.ids.explainmenuLabel.text = ('Here you can join a Match as %s' % outputname)

		color = CLIENT.me.getColor()
		playercolor = (color[0]*255, color[1]*255, color[2]*255, 1)
		self.ids.explainmenuLabel.background_color = playercolor

	def logging(self):
		"""
		Print a LOG, when refresh Button in LobbyMenu is pressed
		"""
		logging.info('UI Lobby Menu: Refresh Button pressed')

	def refresh_matches_list(self):
		"""
		Asks the Server for all current matches in the choosen Lobby
		"""
		CLIENT.lobby.list_matches('Tron')
	
	def on_matches_update(sender, matches):
		"""
		Show the newly updated matches in Lobby Menu
		"""
		## clear the List with matches to avoid multiple listings of the same match
		logging.info('UI Lobby Menu: on_matches_update function was called')
		self.clear_list()

		## Marcell's solution
		## Print out the list of matches for debugging
		# for sentmatch in matches:
		# 	self.sentmatches.append("[%s %s %s]" % (sentmatch.name, sentmatch.game, sentmatch.get_feature_string()))
		# logging.info('UI Lobby Menu: Backend sent: %s' % str(self.sentmatches))
		# self.sentmatches.clear()

		# for match in matches:
		# 	self.matchlist.append("[%s \t %s \t %s]" % (match.name, match.game, match.get_feature_string()))

		## solution from old function
		listmatches = matches
		# time.sleep(2) ## delay for compensating server delay when sending matches
		count_matches = listmatches.__len__() ## getting number of matches for calling single matches
		logging.info('UI Lobby Menu: Var: count_matches = %d' % count_matches)

		## Debugging: what is Backend sending
		for i in range(0,count_matches):
			sentmatch = listmatches[i]
			self.sentmatches.append("[%s %s %s]" % (sentmatch.name, sentmatch.game, sentmatch.get_feature_string()))
		logging.info('UI Lobby Menu: Backend sent: %s' % str(self.sentmatches))
		self.sentmatches.clear()

		## add all content from listmatches into a list with strings for showing in Lobby Menu
		for i in range(0,count_matches):
			match = listmatches[i]
			self.matchlist.append("%s \t %s \t %s" % (match.name, match.game, match.get_feature_string()))
		
		self.update_shown_list()

	def get_matchlist_from_server(self):
		"""
		Get the Information of the available Lobbies

		Args:
			Lobbies (list): name; game; features
		Return:
			-
		"""
		self.clear_list()
		logging.info('UI Lobby Menu: Getting current list of Matches from Server')
		CLIENT.lobby.list_matches('Tron')
		listmatches = CLIENT.lobby.matches
		time.sleep(2) ## delay for compensating server delay when sending matches
		count_matches = listmatches.__len__() ## getting number of matches for calling single matches
		logging.info('UI Lobby Menu: Var: count_matches = %d' % count_matches)

		## Debugging: what is Backend sending
		for i in range(0,count_matches):
			sentmatch = listmatches[i]
			self.sentmatches.append("[%s %s %s]" % (sentmatch.name, sentmatch.game, sentmatch.get_feature_string()))
		logging.info('UI Lobby Menu: Backend sent: %s' % str(self.sentmatches))
		self.sentmatches.clear()

		## add all content from listmatches into a list with strings for showing in Lobby Menu
		for i in range(0,count_matches):
			match = listmatches[i]
			self.matchlist.append("%s       %s       %s" % (match.name, match.game, match.get_feature_string()))
			# if self.matches.count('%s       %s       %s' % (match.name, match.game, match.get_feature_string())) == 0: ## was ment to prevent several listings of the same match --> no always clearing whole list
			# 	self.matches.append("%s       %s       %s" % (match.name, match.game, match.get_feature_string()))
			# else:
			# 	pass
		
		self.update_shown_list()

	def update_shown_list(self):
		"""
		Show the in getLobbyinformation created List in the Lobby Menu
		"""
		logging.info('UI Lobby Menu: Update shown List in the Menu')
		self.ids.lobby_match.data = [{'text' : str(x)} for x in self.matchlist]

	def clear_list(self):
		"""
		Clear the list with matches for preventing multiple listing of the same match
		"""
		logging.info('UI Lobby Menu: List cleared')
		self.matchlist.clear()

	def updatechosenMatch(self, currentmatch=0):
		"""
		Sets variable for choosen Lobby

		Args:
			Lobby (int):
		Return:
			Lobby (int)
		"""
		self.currentmatch = currentmatch

		self.match = int(self.currentmatch)

		logging.info('UI Lobby Menu: Match %d has been clicked by player.' % (self.match+1))
		LobbyMenu.match = self.match

	def joinMatch(self):
		"""
		Join the Match
		"""
		logging.info('UI Lobby Menu: Player joins Match %s with Index %s' % (self.match+1, self.match))
		CLIENT.join_match(self.match)

	def leaveMatch(self):
		"""
		Leave the Match
		"""
		logging.info('UI Lobby Menu: Player leaves Match %s with Index %s' % (self.match+1, self.match))
		CLIENT.leave_match()

class CreateServerMenu(Screen):

	def statusServer(self, statusswitch, numberlobbies, fieldsize_x, fieldsize_y):
		"""
		Call open server function and sends number of lobbies

		Args:
			statusswitch(boolean)
			numberlobbies (int)
			fieldsize_x (int)
			fieldsize_y (int)
		Return:
			-
		"""
		self.statusswitch = statusswitch
		self.numberlobbies = numberlobbies
		self.fieldsize_x = fieldsize_x
		self.fieldsize_y = fieldsize_y

		if self.statusswitch:
			logging.info('UI Create Server Menu: Create Server with %d Lobbies, Width %d and Height %d' % (self.numberlobbies, self.fieldsize_x, self.fieldsize_y))
			self.server = GameServer(self.numberlobbies, (self.fieldsize_x, self.fieldsize_y))
			# self.server = GameServer(self.numberlobbies, self.fieldsize_x, self.fieldsize_y) ## use when implemented in server
			self.server.Start()
			
		else:
			logging.info('Stopping Server...')
			self.server.Stop()

class CreateMatchMenu(Screen):

	i = 1

	def createMatch(self, numberplayer, numberlifes, matchname='DefaultGame'):

		self.numberplayer = numberplayer
		self.numberlifes = numberlifes
		self.matchname = matchname
		i = self.i
		# give Default Game name, if no Input was given
		if self.matchname == '':
			self.matchname = 'DefaultGame%d' % i
			self.numberplayer = 1
			self.i += 1

		logging.info('UI Create Match Menu: Create Match with %d players, %d lifes and name %s' % (self.numberplayer, self.numberlifes, self.matchname))
		settings = {
			'Players' : self.numberplayer,
			'Lifes' : self.numberlifes
		}
		CLIENT.lobby.create_match('Tron', self.matchname, settings)

	def validateInput(self, inpt):

		self.inpt = inpt

		try:
			lastcharacter = self.inpt[-1:]
			x = re.findall("[a-zA-Z0-9_]", lastcharacter)
			if len(x) == 1:
			#if len(parsspace) == 1:
				self.ids.gamenameTextInput.text = inpt

			else:
				#self.openBubble(lastcharacter)
				rightstring = self.inpt[:-1]
				self.ids.gamenameTextInput.text = rightstring

		except Exception as e:
			logging.warning(str(e))

class StatisticsMenu(Screen):
	def loadplayerdata(self) -> None:
		"""
		Load the Player Name from data.json
		Load the Player Color from data.json
		Load Wincount
		Load Lostcount

		Args: -
		Return: -
		"""
		filef = open(datapath)
		data = json.load(filef)
		playername = data[0]
		color = data[1]
		wincount = data[2]
		lostcount = data[3]

		outputname = "Player Name: %s" % playername
		self.ids.nameLabel.text = outputname

		sol = "Color: %s" % str(color)
		playercolor = (color[0], color[1], color[2], 1)
		self.ids.colorLabel.text = sol
		self.ids.showcolorLabel.background_color = playercolor

		outputwincount = "Wincount: %s" % str(wincount)
		self.ids.wincountLabel.text = outputwincount

		outputlostcount = "Lostcount: %s" % str(lostcount)
		self.ids.lostcountLabel.text = outputlostcount

	def reset_statistics(self) -> None:
		"""
		sets wincount and lostcount to 0 and saves it to data,json
		"""
		filef = open(datapath)
		data = json.load(filef)
		wincount = 0
		lostcount = 0

		outputwincount = "Wincount: %s" % str(wincount)
		self.ids.wincountLabel.text = outputwincount

		outputlostcount = "Lostcount: %s" % str(lostcount)
		self.ids.lostcountLabel.text = outputlostcount

		savedata = (data[0], data[1], wincount, lostcount)
		with open(datapath, 'w', encoding='utf-8') as outfile:
			json.dump(savedata,outfile)

class AboutMenu(Screen):
    pass

######## Define KV file classes ############################
class BackToMenuButton(Screen):
	
	def changeScreen(self):
		mainUI.screen_manager.current = 'mainmenu'

class ListLabel(Screen):
	pass

class WindowManager(ScreenManager):
	pass

class SelectableLabel(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.index = index
		return super(SelectableLabel, self).refresh_view_attrs(
			rv, index, data)

	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if super(SelectableLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		''' Respond to the selection of items in the view. '''
		self.selected = is_selected
		self.index = index
		if is_selected:
			SearchForLobbiesMenu().updatechosenLobby(index)
		else:
			pass

class SelectableLabelMatch(RecycleDataViewBehavior, Label):
	''' Add selection support to the Label '''
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		''' Catch and handle the view changes '''
		self.index = index
		return super(SelectableLabelMatch, self).refresh_view_attrs(rv, index, data)

	def on_touch_down(self, touch):
		''' Add selection on touch down '''
		if super(SelectableLabelMatch, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		''' Respond to the selection of items in the view. '''
		self.selected = is_selected
		self.index = index
		if is_selected:
			LobbyMenu().updatechosenMatch(index)
		else:
			pass

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''
	pass