import tkinter as tk
import tkinter.ttk as ttk
import tksheet
from PIL import Image, ImageTk
from datetime import datetime 


"""
card dict data structure

the card dict=																					
	{"card name":																						|list, of card per room ["knife", "Rope", ect....]
		{"own": owener if known or ""},																	|str,  "player(character)"
		{"shown to": list of player you have show the card to},											|list, ["player(character)", "player(character)", ect....]
		{"posibly own": list player that could have shown the card or caller if no one shows card}		|list, ["player(character)", "player(character)", ect....]
				self.dicNotebook[card].update({"does not own": []})	                                    |list, ["player(character)", "player(character)", ect....] 
		{"called": 
			{"var form player list": # time called for card}											|int, 0, +=1 for every time they call the card   
			}																							
	}
}

"""



suspects = [
	'Colonel Mustard',
	'Miss Scarlet',
	'Mr. Green',
	'Mrs. Peacock',
	'Mrs. White',
	'Professor Plum'
	]

rooms =  [
	'Ballroom',
	'Billiard Room',
	'Conservatory',
	'Dining',
	'Hall',
	'Kitchen',
	'Library',
	'Lounge',
	'Study'
	]

weapons = [
	'Candlestick',
	'Knife',
	'Lead Pipe',
	'Revolver',
	'Rope',
	'Wrench'
	]



cardTypes = [
	'suspects',
	'rooms',
	'weapons'
	]

playersName = ''


loaded =False
class TheMeat():
	"""docstring for TheMeat"""
	def __init__(self, rootParent, hasCard):

		self.playersName = ''

		super(TheMeat, self).__init__()
		now = datetime.now()
		timeVar = now.strftime('%I:%M:%S') 



		#building a list of player names and their characters for  drop down list  |self.playerDropdownlist = ["playerName(character)", "playerName(character)", "playerName(character)", .... ect]
		self.LoadScreenPlayed = False
		self.done = False
		self.curBlinking = True
		self.hasCard = hasCard
		self.widthPDL = 0
		self.rootParent = rootParent
		self.playerDropdownList = ["None",]
		self.calledList = ["Who called"]
		self.showerList = ['Person showing']
		self.playerList = rootParent.playerList
		for player in self.playerList:
			tempName = ""
			i = 0 
			for name in player:
				if i == 0:
					tempName = name
					i += 1
					if self.playersName == '':
						self.playersName = name
				else:
					tempName = tempName + '(' + name + ')'
			if len(tempName) > self.widthPDL:
				self.widthPDL = len(tempName)
			self.playerDropdownList.append(tempName)
			self.calledList.append(tempName)
			self.showerList.append(tempName)			
		self.tempShowerList = []


		self.suspectsList = ['Suspects',]
		for suspect in suspects:
			self.suspectsList.append(suspect)

		self.roomList = ['Rooms',]
		for room in rooms:
			self.roomList.append(room)
	

		self.weaponList = ['Weapons',]
		for weapon in weapons:
			self.weaponList.append(weapon)

		#building the dict to hold card call info
		def buildDB():
			self.dicNotebook = {}
			for each in cardTypes:
				match each:
					case "rooms":
						cardType = rooms
					case "suspects":
						cardType = suspects
					case "weapons":
						cardType = weapons
				for card in cardType:

					if card in self.hasCard:
						own = self.playerDropdownList[1]
					else:
						own = ""
					called ={}
					for i in range (1, len(self.playerDropdownList)):
						called.update({self.playerDropdownList[i]:0})
					self.dicNotebook.update({card : {}})
					self.dicNotebook[card].update({'own': own})       	#player(character) in hand or if shown load here
					self.dicNotebook[card].update({'shown to': []})   	# if you have shown to someone thier name added to the list
					self.dicNotebook[card].update({"posibly own": []})	#load otherPlayer if other player called and no one showed or the shower's tag if someone showed them ##superuser update when does not own 
					self.dicNotebook[card].update({"does not own": []})	#load player if someone called and the play could not show a card	#super user
					self.dicNotebook[card].update({'called':called})    #inc anytime the card is called #called dict of players followed by the number of type they have ask to see the card 
		



		#function for builing a name/character drop down list
		def nameDL():
			one = ttk.Combobox(self.rootParent, values = self.playerDropdownList, state = 'readonly', width = self.widthPDL+2)
			return one



		def resize(event):
			self.pWidth = event.width -30
			if self.pWidth <= 0:
				self.pWidth = 30
			self.pHeight = int(self.pWidth//self.width_ratio)
			self.resize_image = self.photo.resize((self.pWidth, self.pHeight))
			self.tkPhoto =ImageTk.PhotoImage(self.resize_image)
			self.header.itemconfig(bg_pic, image= self.tkPhoto)
			self.header['width'] = self.pWidth 
			self.header['height'] = self.pHeight


		

		
		
		
		self.photo = Image.open("./img/notebook.png")
		self.pWidth, self.pHeight = self.photo.size
		self.width_ratio = self.pWidth/self.pHeight
		self.pWidth = self.rootParent.winfo_width()
		self.wHeight = self.rootParent.winfo_height() 
		self.pWidth -=50
		self.pHeight = int(self.pWidth//self.width_ratio)
		self.resize_image = self.photo.resize((self.pWidth, self.pHeight))
		self.tkPhoto = ImageTk.PhotoImage(self.resize_image)
		self.detectiveNotebook = ttk.Notebook(self.rootParent, style = "DickBook.TNotebook")
		self.detectiveNotebook.pack(fill = 'both', expand = True , ipadx = 0, ipady = 0, pady = 0, padx = 0)
		self.startTab = tk.Frame(self.detectiveNotebook, bg = '#d8bd7c', bd = 0)
		self.startTab.pack(fill = 'both', expand = True, ipadx = 0, ipady = 0, pady = 0, padx = 0)
		self.caseStamp = Image.open("./img/case_file_stamp.png")
		self.stamp = ImageTk.PhotoImage(self.caseStamp)
		self.stampHolder = tk.Label(self.startTab, image = self.stamp, bd =0)
		self.stampHolder.pack(fill = 'none', expand = True, ipadx = 0, ipady = 0, pady = 0, padx = 0)
		self.detectiveNotebook.add(self.startTab, text = 'The case file.')
		self.manualTab = tk.Frame(self.detectiveNotebook, bg = '#d8bd7c', bd = 0, highlightthickness=0)
		self.manualTab.pack(fill = 'both', expand = True, ipadx = 0, ipady = 0, pady = 0, padx = 0)
		self.detectiveNotebook.add(self.manualTab, text = "Manually add info")
		self.leftSide =tk.Canvas(self.manualTab, width = 15, bg = '#d8bd7c', bd = -2, highlightthickness =0)
		self.leftSide.pack(side = "left", fill = tk.Y, expand = True, ipadx = 0, padx = 0, ipady = 0, pady = 0)
		self.rightSide = tk.Canvas(self.manualTab, width = 15, bg = '#d8bd7c', bd = -2, highlightthickness = 0)
		self.rightSide.pack(side = "right", fill = tk.Y, expand = True, ipadx = 0, padx = 0, ipady = 0, pady = 0)
		self.header = tk.Canvas(self.manualTab, width= self.pWidth , height= self.pHeight, bg= '#d8bd7c', bd = -2, selectborderwidth = 0)
		self.header.pack( anchor = tk.NW,  ipadx = 0, padx = 0, ipady = 0, pady = 0)
		self.body = tk.Canvas(self.manualTab,  bg= '#f0f1f5', bd = -2, highlightthickness=0)
		self.body.pack(fill = 'both', expand = True, ipadx = 0, padx = 0, ipady = 0, pady = 0)
		bg_pic = self.header.create_image(0, 3, image = self.tkPhoto, anchor = 'nw')
		self.detectiveNotebook.bind('<Configure>', resize)		
		self.headSpace = tk.Frame(self.body, height= 20)
		self.headSpace['borderwidth'] =5
		self.headSpace.pack(fill = tk.X, anchor = 'n')
		self.holder = tk.Label(self.headSpace, text = "WHO, WHAT and WHERE.",  bg = '#f0f1f5')
		self.holder.pack(expand = True)
		self.headSpaceLine = ttk.Separator(self.body, orient = tk.HORIZONTAL)
		self.headSpaceLine.pack(fill = tk.X, expand = False, anchor = 'n')
		self.bodyMain = tk.Canvas(self.body,  bg= '#f0f1f5', bd = -2, highlightthickness=0)
		self.bodyMain.pack(fill = 'both', expand = True)
		self.leftBM = tk.Canvas(self.bodyMain, bd = 3,  bg = '#f0f1f5', width = 500, highlightthickness=0)
		self.leftBM.pack(side = 'left', fill = 'both', expand = True)
		self.leftBM.pack_propagate(0)
		self.rightBM = tk.Canvas(self.bodyMain, bd = 3, bg = '#f0f1f5', width = 500, highlightthickness=0)
		self.rightBM.pack(side = 'right', fill = 'both', expand = True,)
		self.suspectframe = tk.Frame(self.leftBM, bg = 'black')
		self.suspectframe.grid(row = 0, column = 0, columnspan = 3, sticky =  tk.E+tk.W, padx = 7, pady = 7 )
		self.suspectHeader = tk.Label(self.suspectframe, bg = 'black', fg = 'white', font = ('Times', '16'), text = "Suspects")
		self.suspectHeader.pack(fill = tk.Y, expand = False)
		self.suspectSpacer = tk.Frame(self.leftBM, bg = '#f0f1f5', bd = 3, width = 20, relief = 'groove', padx =7)
		self.suspectSpacer.grid(row =1, column = 0, rowspan = 6, sticky = tk.E+tk.W)
		self.mustardLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = 'Colonel Mustard ')
		self.mustardLabel.grid(row = 1, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.mustardEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50, selectborderwidth = 0)
		self.mustardEntry.grid(row = 1, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.scarlettLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = "Miss Scarlett ")
		self.scarlettLabel.grid(row = 2, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.scarlettEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.scarlettEntry.grid(row = 2, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.greenLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = 'Mr. Green ')
		self.greenLabel.grid(row = 3, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.greenEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.greenEntry.grid(row = 3, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.peacockLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = 'Mrs. Peacock ')
		self.peacockLabel.grid(row = 4, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.peacockEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.peacockEntry.grid(row = 4, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.whiteLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = 'Mrs. White ')
		self.whiteLabel.grid(row = 5, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.whiteEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.whiteEntry.grid(row = 5, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.plumLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = ' Professor Plum ')
		self.plumLabel.grid(row = 6, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.plumEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.plumEntry.grid(row = 6, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.weaponframe = tk.Frame(self.leftBM, bg = 'black')
		self.weaponframe.grid(row = 7, column = 0, columnspan = 3, sticky =  tk.E+tk.W, padx = 7, pady = 7 )
		self.weaponHeader = tk.Label(self.weaponframe, bg = 'black', fg = 'white', font = ('Times', '16'), text = "Suspects")
		self.weaponHeader.pack(fill = tk.Y, expand = False)
		self.weaponSpacer = tk.Frame(self.leftBM, bg = '#f0f1f5', bd = 3, width = 20, relief = 'groove', padx =7)
		self.weaponSpacer.grid(row =8, column = 0, rowspan = 6, sticky = tk.E+tk.W)
		self.candlestickLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = ' Candlestick ')
		self.candlestickLabel.grid(row = 8, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.candlestickEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.candlestickEntry.grid(row = 8, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.knifeLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = " Knife ")
		self.knifeLabel.grid(row = 9, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.knifeEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.knifeEntry.grid(row = 9, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.pipeLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = ' Lead Pipe ')
		self.pipeLabel.grid(row = 10, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.pipeEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.pipeEntry.grid(row = 10, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.revolverLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = 'Revolver ')
		self.revolverLabel.grid(row = 11, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.revolverEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.revolverEntry.grid(row = 11, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.ropeLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = ' Rope ')
		self.ropeLabel.grid(row = 12, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.ropeEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.ropeEntry.grid(row = 12, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.wrenchLabel = tk.Label(self.leftBM, bg = '#f0f1f5', bd = 3,  text = ' Wrench ')
		self.wrenchLabel.grid(row = 13, column = 1, sticky = tk.N+tk.E+tk.S+tk.W)
		self.wrenchEntry = tk.Entry(self.leftBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.wrenchEntry.grid(row = 13, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.roomframe = tk.Frame(self.rightBM, bg = 'black')
		self.roomframe.grid(row = 0, column = 0, columnspan = 3, sticky =  tk.E+tk.W, padx = 7, pady = 7 )
		self.roomHeader = tk.Label(self.roomframe, bg = 'black', fg = 'white', font = ('Times', '16'), text = "Rooms")
		self.roomHeader.pack(fill = tk.Y, expand = False)
		self.roomSpacer = tk.Frame(self.rightBM, bg = '#f0f1f5', bd = 3, width = 20, relief = 'groove', padx =7)
		self.roomSpacer.grid(row =1, column = 0, rowspan = 9, sticky = tk.E+tk.W)
		self.ballroomLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = 'Ballroom ')
		self.ballroomLabel.grid(row = 1, column = 1, sticky = tk.E+tk.S+tk.W)
		self.ballroomEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.ballroomEntry.grid(row = 1, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.billiardLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = " Billiard Room ")
		self.billiardLabel.grid(row = 2, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.billiardEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.billiardEntry.grid(row = 2, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.conservatoryLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = 'Conservatory ')
		self.conservatoryLabel.grid(row = 3, column = 1, sticky = tk.E+tk.S+tk.W)
		self.conservatoryEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.conservatoryEntry.grid(row = 3, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.diningLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = 'Dining')
		self.diningLabel.grid(row = 4, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.diningEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.diningEntry.grid(row = 4, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.hallLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = ' Hall ')
		self.hallLabel.grid(row = 5, column = 1, sticky = tk.E+tk.S+tk.W, pady = 1)
		self.hallEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.hallEntry.grid(row = 5, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.kitchenLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = ' Kitchen ')
		self.kitchenLabel.grid(row = 6, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.kitchenEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.kitchenEntry.grid(row = 6, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.libraryLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = ' Library ')
		self.libraryLabel.grid(row = 7, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.libraryEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.libraryEntry.grid(row = 7, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.loungeLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = ' Lounge ' )
		self.loungeLabel.grid(row = 8, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.loungeEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.loungeEntry.grid(row = 8, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.studyLabel = tk.Label(self.rightBM, bg = '#f0f1f5', bd = 3,  text = ' Study ')
		self.studyLabel.grid(row = 9, column = 1, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)
		self.studyEntry = tk.Entry(self.rightBM, bg = '#fafbff', relief = 'flat', bd = 3, width = 50)
		self.studyEntry.grid(row = 9, column = 2, sticky = tk.N+tk.E+tk.S+tk.W, pady = 1)



		# now starts the interactive part. OH LORD WHAT HAVE I GOT MYSELF INTO!!!!!!
		def updateTime():
			now = datetime.now()
			timeVar = now.strftime('%H:%M:%S') 
			self.timeNow.set(timeVar)
			rootParent.after(100, updateTime)

		def cur_blink():
			if self.curBlinking == True:
			    self.playGame['text'] = self.playGame['text'][0:-1] + "Ш" if self.playGame['text'][-1] == ' ' else self.playGame['text'][0:-1] + ' '
			    rootParent.after(375, cur_blink)
	
		self.messageList = []
		self.messageList.append(f'Hello and good day, {self.playersName}.')
		if self.playersName == 'Your name here.':
			self.messageList.append('What a funny name, I will call you meat bag #5428.')
			self.playerDropdownList[1] = self.playerDropdownList[1].replace('Your name here.', 'meat bag #5428')
			self.calledList[1] = self.calledList[1].replace('Your name here.', 'meat bag #5428')
			self.showerList[1] = self.showerList[1].replace('Your name here.', 'meat bag #5428')
		buildDB()
		self.messageList.append("I am C.A.L. 9000, it's a pleasure to meet you.")
		self.messageList.append('I will assist you in your detective endeavors.')
		self.messageList.append('(press any key to continue.)')

		def typemessage(*args):
			if args == ():        
				if self.messageInc <= 0 and self.messageInc2 > 0: #
					if self.messageList != []:
						typemessage(self.messageList[0])
						return
					else:
						self.done = True
						return 
			else:
				self.message = args[0]
				self.messageList.pop(0)
				self.messageInc = len(self.message)
				self.messageInc2 = self.messageInc + 10 #
			if self.messageInc2 > self.messageInc and self.messageInc > 0:
				self.messageInc2 -=1
				self.messageInc +=1
			elif self.messageInc > 0:
				self.messageInc2 -= 1
				self.playGame['text'] = self.playGame['text'][0:-1] + self.message[-self.messageInc] + self.playGame['text'][-1]
			else:
				if self.playGame['text'][-4: -1] != '>>>':
					self.playGame['text'] = self.playGame['text'][0:-1] + '\n>>>' + self.playGame['text'][-1]
				self.messageInc -=1
				self.messageInc2 +=1
			self.messageInc -= 1
			rootParent.after(100, typemessage)

		def messageStart(event):
			tabOpened = event.widget.select()
			tabName = event.widget.tab(tabOpened, "text")
			if tabName == 'Interactive add info' and self.done == False:
				typemessage(self.messageList[0])

		def killCAL(event):
			if self.done == True:
				self.curBlinking = False
				self.playGame.destroy()
				self.entryFrame.pack(fill = tk.X, pady = 10, ipady = 5)
				self.entryFrame.pack_propagate(0)
				self.entryFrame2.pack(fill = tk.X, pady = 0, ipady = 5)
				self.entryFrame2.pack_propagate(0)
				self.dictFrame.pack(fill = 'both', expand = True)

		def gridShowenlist(event):
			self.tempShowerList = []
			caller = event.widget.get()
			if caller != 'Who called':
				for name in self.showerList:
					self.tempShowerList.append(name)
				self.tempShowerList.remove(caller)
			else:
				self.showerCB.destroy()
				self.showerCB = ttk.Combobox(self.entryFrame2, values = ['Who called'], width = self.widthPDL+1 , state = 'readonly', style = 'CAL.TCombobox')
				self.updateBtn.destroy()
				self.updateBtn = tk.Button(self.entryFrame2)
				return
			self.showerCB.destroy()
			self.showerCB = ttk.Combobox(self.entryFrame2, values = self.tempShowerList, width = self.widthPDL+1 , state = 'readonly', style = 'CAL.TCombobox')
			self.showerCB.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -foreground #03bc3a -background #031a03'  % self.showerCB)
			self.showerCB.current(0)
			self.showerCB.grid(row = 0, column = 0, sticky = tk.N+tk.W+tk.E+tk.S )
			self.showerCB.bind('<<ComboboxSelected>>' , dispalyUpdateBTN)
			self.updateBtn.destroy()
			self.updateBtn = tk.Button(self.entryFrame2)


		def buildShownCardList(event):
			self.tempCardlist = [' ','Unknown cards', 'Could not show']
			sus = self.callSus.get()
			if sus != 'Suspects':
				self.tempCardlist.append(sus)
			else:
				self.shownCardCB.destroy()
				self.shownCardCB = ttk.Combobox(self.entryFrame2)
				self.updateBtn.destroy()
				self.updateBtn = tk.Button(self.entryFrame2)
				return
			room = self.callroom.get()
			if room != 'Rooms':
				self.tempCardlist.append(room)
			else:
				self.shownCardCB.destroy()
				self.shownCardCB = ttk.Combobox(self.entryFrame2)
				self.updateBtn.destroy()
				self.updateBtn = tk.Button(self.entryFrame2)
				return
			weap = self.callweapon.get()
			if weap != 'Weapons':
				self.tempCardlist.append(weap)
				self.shownCardCB.destroy()
				self.shownCardCB = ttk.Combobox(self.entryFrame2, values = self.tempCardlist, width = 17 , state = 'readonly', style = 'CAL.TCombobox')
				self.shownCardCB.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -foreground #03bc3a -background #031a03'  % self.shownCardCB)
				self.shownCardCB.current(0)
				self.shownCardCB.grid(row = 0, column = 1, sticky = tk.N+tk.W+tk.E+tk.S )
				self.shownCardCB.bind('<<ComboboxSelected>>' , dispalyUpdateBTN)
				self.updateBtn.destroy()
				self.updateBtn = tk.Button(self.entryFrame2)
			else:
				self.shownCardCB.destroy()
				self.shownCardCB = ttk.Combobox(self.entryFrame2)
				self.updateBtn.destroy()
				self.updateBtn = tk.Button(self.entryFrame2)
				return

		def dispalyUpdateBTN(event):
			shower = self.showerCB.get()
			showCard = self.shownCardCB.get()
			if shower != 'Person showing' and showCard != ' ':
				self.updateBtn.destroy()
				self.updateBtn = tk.Button(self.entryFrame2,
					text = 'Update C.A.L',
					bg = '#031a03',
					fg = '#03bc3a',
					activebackground = '#03bc3a',
					activeforeground = '#031a03',
					font =('Glass TTY VT220', '11'),
					anchor = tk.E,
					command = updateDB
					)
				self.updateBtn.grid(row = 0, column = 2, sticky = tk.N+tk.S+tk.E, padx = 20)
			else:
				self.updateBtn.destroy()
				self.updateBtn = tk.Button(self.entryFrame2)

		def buildSheetTabel():
			row_num = 0
			rowHeight = 1
			rowHeightList = []
			self.table = []
			for each in cardTypes:
				match each:
					case "rooms":
						cardType = rooms
					case "suspects":
						cardType = suspects
					case "weapons":
						cardType = weapons
				row = [each, '','', '','','']
				self.table.append(row)
				row_num += 1
				for card in cardType:
					has = 	self.dicNotebook[card]['own']
					if has != '':
						endOfName = has.index('(')
						has = has[0:endOfName]
					shown = self.dicNotebook[card]['shown to']
					if len(shown) >= rowHeight:
						rowHeight = len(shown)
					if shown == []:
						shown = ''
					else:
						i = 0
						for player in shown:
							if i == 0:
								endOfName = player.index('(')
								player = player[0:endOfName]
								shown = player
								i = 1
							else:
								endOfName = player.index('(')
								player = player[0:endOfName]
								shown = shown + '\n' + player
					pHas =  self.dicNotebook[card]['posibly own']
					if pHas == []:
						pHas = '' 
					else:
						i = 0
						for player in pHas:
							if i == 0:
								endOfName = player.index('(')
								player = player[0:endOfName]
								pHas = player
								i = 1
							else:
								endOfName = player.index('(')
								player = player[0:endOfName]
								pHas = pHas + '\n' + player
					notHas = self.dicNotebook[card]["does not own"]
					if notHas == []: 
						notHas = ''
					else:
						i = 0
						for player in notHas:
							if i == 0:
								endOfName = player.index('(')
								player = player[0:endOfName]
								notHas = player
								i = 1
							else:
								endOfName = player.index('(')
								player = player[0:endOfName]
								notHas = notHas + '\n' + player
					row = ['', card, has, shown, notHas, pHas ]
					self.table.append(row)
					rowHeightList.append([row_num, rowHeight])
					row_num += 1
					rowHeight = 1
			
			self.sheet.enable_bindings('row_height_resize')
			self.sheet.set_sheet_data(self.table, redraw = True)
			for rowHeights in rowHeightList:
				tempRow = int(rowHeights[0])
				self.sheet.row_height(row = tempRow, height = 'text', only_set_if_too_small = True, redraw = False)
			self.sheet.column_width(column = 0, width = 0)

		def updateDB():
			player = self.showerCB.get()
			card = self.shownCardCB.get()
			calledSus = self.callSus.get()
			calleRoom = self.callroom.get()
			calledWeap = self.callweapon.get()
			caller = self.caller.get()
			if card != 'Unknown cards' and card != ' ' and card != 'Could not show':
				if player != self.playerDropdownList[1]:
					if player != self.dicNotebook[card]['own']:
						self.dicNotebook[card]['own'] = player
						self.dicNotebook[card]['posibly own'] = ''
						self.dicNotebook[card]['does not own'] = ''
				else:
					if caller not in self.dicNotebook[card]['shown to']:
						self.dicNotebook[card]['shown to'].append(caller)
			elif card == 'Unknown cards':
				if player not in self.dicNotebook[calledSus]['does not own'] and player not in self.dicNotebook[calledSus]['own']:
					if player not in self.dicNotebook[calledSus]['posibly own']:
						self.dicNotebook[calledSus]['posibly own'].append(player)
				if player not in self.dicNotebook[calleRoom]['does not own'] and player not in self.dicNotebook[calleRoom]['own']:
					if player not in self.dicNotebook[calleRoom]['posibly own']:
						self.dicNotebook[calleRoom]['posibly own'].append(player)
				if player not in self.dicNotebook[calledWeap]['does not own'] and player not in self.dicNotebook[calledWeap]['own']:
					if player not in self.dicNotebook[calledWeap]['posibly own']:
						self.dicNotebook[calledWeap]['posibly own'].append(player)
			elif card == 'Could not show':
				if player not in self.dicNotebook[calledSus]['does not own']:
					self.dicNotebook[calledSus]['does not own'].append(player)
				if player in self.dicNotebook[calledSus]['posibly own'] and len(self.dicNotebook[calledSus]['posibly own']) > 0:
					self.dicNotebook[calledSus]['posibly own'].remove(player)
				else:
					self.dicNotebook[calledSus]['posibly own'] = []
				if player not in self.dicNotebook[calleRoom]['does not own']:
					self.dicNotebook[calleRoom]['does not own'].append(player)
				if player in self.dicNotebook[calleRoom]['posibly own'] and len(self.dicNotebook[calleRoom]['posibly own']) > 0:
					self.dicNotebook[calleRoom]['posibly own'].remove(player)
				else:
					self.dicNotebook[calleRoom]['posibly own'] = []
				if player not in self.dicNotebook[calledWeap]['does not own']:
					self.dicNotebook[calledWeap]['does not own'].append(player)
				if player in self.dicNotebook[calledWeap]['posibly own'] and len(self.dicNotebook[calledWeap]['posibly own']) > 0:
					self.dicNotebook[calledWeap]['posibly own'].remove(player)
				else:
					self.dicNotebook[calledWeap]['posibly own'] =[]
			buildSheetTabel()





		self.interactiveTab = tk.Frame(self.detectiveNotebook, bg = '#d8bd7c', bd = -2)
		self.interactiveTab.pack(fill = 'both', expand = True, ipadx = 0, ipady = 0, pady = 0, padx = 0)
		self.detectiveNotebook.add(self.interactiveTab, text = "Interactive add info")
		self.screen = tk.Canvas(self.interactiveTab, bg = '#031a03', bd = -2, highlightbackground = '#d8bd7c', highlightthickness=0)#031a03
		self.screen.pack(fill = 'both', expand = True, ipadx = 0, ipady = 0, pady = 20, padx = 20)
		self.tlScreenCorn = tk.Canvas(self.screen, bg = '#d8bd7c', bd = -2, height = 18, width = 18, highlightbackground = '#d8bd7c',highlightthickness=0)
		self.tlScreenCorn.pack(fill = 'none', expand = False)
		self.tlScreenCorn.place(anchor =  tk.NW, relx = 0, rely = 0)
		self.tlPatch = self.tlScreenCorn.create_arc(0,0,30,30, fill = '#031a03', start = 90, extent = 90, width = 0)
		self.trScreenCorn = tk.Canvas(self.screen, bg = '#d8bd7c', bd = -2, height = 20, width = 20, highlightbackground = '#d8bd7c',highlightthickness=0)
		self.trScreenCorn.pack(fill = 'none', expand = False)
		self.trScreenCorn.place(anchor = tk.NE, relx = 1, rely = 0)
		self.trPatch = self.trScreenCorn.create_arc(-20,0,15,31, fill = '#031a03', start = 0, extent = 90, width = 0)
		self.mainScreen = tk.Canvas(self.screen, bg = '#031a03', bd = -2, highlightbackground = '#08bd7c',highlightthickness=0)#widget color #03bc3a   
		self.mainScreen.pack(fill = 'both', expand = True, ipadx = 0, ipady = 0, pady = 15, padx = 15)
		self.blScreenCorn = tk.Canvas(self.screen, bg = '#d8bd7c', bd = -2, height = 20, width = 20, highlightbackground = '#d8bd7c',highlightthickness=0)
		self.blScreenCorn.pack(fill = 'none', expand = False)
		self.blScreenCorn.place(anchor =  tk.SW, relx = 0, rely = 1)
		self.blPatch = self.blScreenCorn.create_arc(0,-17,30,15, fill = '#031a03', start = 180, extent = 270, width = 0)
		self.brScreenCorn = tk.Canvas(self.screen, bg = '#d8bd7c', bd = -2, height = 20, width = 20,highlightthickness=0)
		self.brScreenCorn.pack(fill = 'none', expand = False)
		self.brScreenCorn.place(anchor = tk.SE, relx = 1, rely = 1)
		self.brPatch = self.brScreenCorn.create_arc(-17,-15,15,15, fill = '#031a03', start = 270, extent = 359, width = 0)#widget color #03bc3a font =('Glass TTY VT220', '12')
		self.title = tk.Label(self.screen,fg = '#03bc3a', bg ='#031a03',  text ='Clue Assisting Logic 9000', font =('Glass TTY VT220', '12'))
		self.title.pack(fill = 'none', expand = True)
		self.title.place(anchor = tk.NW, relx = .05, rely = 0)
		self.timeNow = tk.StringVar()
		self.timeBar = tk.Label(self.screen,fg = '#03bc3a', bg ='#031a03',  textvariable = self.timeNow, font =('Glass TTY VT220', '12'))
		self.timeBar.pack(fill = 'none', expand = True)
		self.timeBar.place(anchor = tk.NE, relx = .95, rely = 0)
		updateTime()
		self.playGame = tk.Label(self.mainScreen, fg = '#03bc3a', bg ='#031a03',  text ='>>> ', font =('Glass TTY VT220', '15'), justify = 'left', anchor = 'sw')
		self.playGame.pack(fill = 'both', expand = True, side = 'left')
		cur_blink()
		self.detectiveNotebook.bind('<<NotebookTabChanged>>', messageStart)
		self.detectiveNotebook.bind('<Any-KeyPress>', killCAL)
		self.entryFrame = tk.LabelFrame(self.mainScreen, text = 'Called:', labelanchor = 'nw', font =('Glass TTY VT220', '12'), height = 70, fg = '#03bc3a', bg ='#031a03', highlightbackground = '#d8bd7c',highlightthickness=0)
		self.entryFrame2 = tk.LabelFrame(self.mainScreen, text = 'Showen:', labelanchor = 'ne', font =('Glass TTY VT220', '12'), height = 20, fg = '#03bc3a', bg ='#031a03', highlightbackground = '#d8bd7c',highlightthickness=0)
		self.dictFrame = tk.Frame(self.mainScreen, bg = '#031a03', highlightbackground = '#d8bd7c',highlightthickness=0, bd = -2)
		self.caller = ttk.Combobox(self.entryFrame, values = self.calledList, width = self.widthPDL+1 , state = 'readonly', style = 'CAL.TCombobox')
		self.caller.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -foreground #03bc3a -background #031a03'  % self.caller)
		self.caller.current(0)
		self.caller.grid(row = 0, column = 0, sticky = tk.N+tk.W+tk.E )
		self.callSus = ttk.Combobox(self.entryFrame, values = self.suspectsList, width = 17 , state = 'readonly', style = 'CAL.TCombobox')
		self.callSus.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -foreground #03bc3a -background #031a03'  % self.callSus)
		self.callSus.current(0)
		self.callSus.grid(row = 0, column = 1, sticky = tk.N+tk.W+tk.E )
		self.callroom = ttk.Combobox(self.entryFrame, values = self.roomList, width = 14 , state = 'readonly', style = 'CAL.TCombobox')
		self.callroom.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -foreground #03bc3a -background #031a03'  % self.callroom)
		self.callroom.current(0)
		self.callroom.grid(row = 0, column = 2, sticky = tk.N+tk.W+tk.E )
		self.callweapon = ttk.Combobox(self.entryFrame, values = self.weaponList, width = 14 , state = 'readonly', style = 'CAL.TCombobox')
		self.callweapon.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -foreground #03bc3a -background #031a03'  % self.callroom)
		self.callweapon.current(0)
		self.callweapon.grid(row = 0, column = 3, sticky = tk.N+tk.W+tk.E )
		self.callSus.bind('<<ComboboxSelected>>' , buildShownCardList)
		self.callroom.bind('<<ComboboxSelected>>' , buildShownCardList)
		self.callweapon.bind('<<ComboboxSelected>>' , buildShownCardList)
		self.caller.bind('<<ComboboxSelected>>' , gridShowenlist)
		self.showerCB = ttk.Combobox(self.entryFrame2)
		self.shownCardCB = ttk.Combobox(self.entryFrame2)
		self.updateBtn = tk.Button(self.entryFrame2)

		cbgc = '#031a03'
		cfgc = '#03bc3a'
		self.sheet = tksheet.Sheet(self.dictFrame,
			column_width = 150,
			show_x_scrollbar = False,
			header_align = 'center',
			align = 'center',
			show_row_index = True,
			row_index = 0,
			row_height = "1",
			enable_edit_cell_auto_resize = True,
			auto_resize_default_row_index = True,
			popup_menu_fg                      = cfgc,
			popup_menu_bg                      = cbgc,
			popup_menu_highlight_bg            = cfgc,
			popup_menu_highlight_fg            = cbgc,
			frame_bg                           = cbgc,
			table_grid_fg                      = cfgc,
			table_bg                           = cbgc,
			table_fg                           = cfgc, 
			table_selected_cells_border_fg     = cfgc,
			table_selected_cells_bg            = cfgc,
			table_selected_cells_fg            = cbgc,
			table_selected_rows_border_fg      = cfgc,
			table_selected_rows_bg             = cfgc,
			table_selected_rows_fg             = cbgc,
			table_selected_columns_border_fg   = cfgc,
			table_selected_columns_bg          = cfgc,
			table_selected_columns_fg          = cbgc,
			resizing_line_fg                   = cfgc,
			drag_and_drop_bg                   = cbgc,
			index_bg                           = cbgc,
			index_border_fg                    = cfgc,
			index_grid_fg                      = cfgc,
			index_fg                           = cfgc,
			index_selected_cells_bg            = cfgc,
			index_selected_cells_fg            = cbgc,
			index_selected_rows_bg             = cfgc,
			index_selected_rows_fg             = cbgc,
			index_hidden_rows_expander_bg      = cbgc,
			header_bg                          = cbgc,
			header_border_fg                   = cfgc,
			header_grid_fg                     = cfgc,
			header_fg                          = cfgc,
			header_selected_cells_bg           = cfgc,
			header_selected_cells_fg           = cbgc,
			header_selected_columns_bg         = cfgc,
			header_selected_columns_fg         = cbgc,
			header_hidden_columns_expander_bg  = cbgc,
			top_left_bg                        = cbgc,
			top_left_fg                        = cfgc,
			top_left_fg_highlight              = cfgc
			)
		self.sheet.pack(fill = 'both', expand = True)
		headers = ["card type", 'Card', 'Player has', 'Shown to' , "Doesn't have", 'Might have' ]
		self.sheet.headers(headers)
		buildSheetTabel()


		numberOcolumns = (len(self.playerDropdownList) +1)*2

		xInc = 0
		yInc = 0
		for column in range(numberOcolumns):
			pass

