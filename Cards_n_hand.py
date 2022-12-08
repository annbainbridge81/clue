import tkinter as tk
import tkinter.ttk as ttk
from dickBook import TheMeat


rooms =  [
	'Kitchen',
	'Ballroom',
	'Conservatory',
	'Billiard Room',
	'Library',
	'Study',
	'Hall',
	'Lounge',
	'Dining'
	]
roomImgs = [
	'kitchen.png',
	'ballroom.png',
	'conservatory.png',
	'billiardroom.png',
	'library.png',
	'study.png',
	'hall.png',
	'lounge.png',
	'diningroom.png']

weapons = [
	"Candlestick",
	"Knife",
	"Lead Pipe",
	"Revolver",
	"Rope",
	"Wrench"
	]
weaponsImgs = [
	"candlestick.png",
	"knife.png",
	"lead-pipe.png",
	"revolver.png",
	"rope.png",
	"wrench.png"
	]

suspects = [
	"Mrs. White",
	"Mrs. Peacock",
	"Professor Plum",
	"Colonel Mustard",
	"Miss Scarlet",
	"Mr. Green"
	]
suspectsImgs = [
	"mrswhite.png",
	"Mrspeacock.png",
	"ProfPlum.png",
	"ColMustard.png",
	"missscarlet.png",
	"mrgreen.png"
	]

#self.hasCard = []
class CNHWidgetBuilder:
	def __init__(self, rootParent, parent):

		self.hasCard = []

		def updateCardList(card, yesNo):
			#global hasCard
			if yesNo == "0":
				self.hasCard.remove(card)
			else:
				self.hasCard.append(card)
				self.hasCard.sort()

		class FuckingShit:
			def __init__(self, parent, cardname, imageLacation, x, y, hideCardCheckBoxs, hasCard):
				self.parent = parent
				self.s = ttk.Style()
				self.imgfile = (f"./img/{imageLacation}")
				self.photoImg= tk.PhotoImage(file = self.imgfile)
				self.styleName = f'{cardname}.TLabel'
				self.s.configure(self.styleName, image = self.photoImg)
				self.s.configure('TCheckbutton', justified = 'center')
				self.photoCnvs = ttk.Label(self.parent,  style = self.styleName)
				self.cardBox =ttk.LabelFrame(
					self.parent,
					labelanchor = 'n',
					labelwidget = self.photoCnvs
					)
				self.cardBox.grid(column = x, row = y, padx = 5, pady =5)
				self.cbVar = tk.StringVar()
				self.checkBox =ttk.Checkbutton(
					self.cardBox,
					text = cardname,
					variable = self.cbVar,
					command = lambda: updateCardList(cardname, self.cbVar.get())
					)
				if cardname in hasCard:
					self.cbVar.set(1)
				else:
					self.cbVar.set(0)
				self.checkBox.pack()	
				#self.checkBox.grid(column = 0, row = 0, padx = 10, pady = 5)
				if hideCardCheckBoxs == True:
					#self.paceholder = ttk.Label(self.cardBox, text = cardname)
					#self.paceholder.grid(column = 0, row = 0, padx = 10, pady = 5)
					#self.checkBox.grid_forget()
					self.paceholder = ttk.Label(self.cardBox, text = cardname)
					self.paceholder.pack()
					self.checkBox.pack_forget()

		def rebuild():
			loadCards("inHand", self.inHandCanvas)
			loadCards("suspects", self.suspectsFrame)
			loadCards("weapons", self.weaponsFrame)
			loadCards("suspects", self.suspectsFrame)

		def reloadInhadFrame(*arg):
			for child in self.inHandCanvas.winfo_children():
				child.destroy()
			rebuild()

		def killCardsNoteook():
			#self.cardsNotebook.pack_forget()
			parent.destroy()
			TheMeat(rootParent, self.hasCard)



		def loadCards(type, parent):
			hideCardCheckBoxs = False
			hasCardImg = []
			match type:
				case "suspects":
					textVar = suspects
					imgVar = suspectsImgs
				case "rooms":
					textVar = rooms
					imgVar = roomImgs
				case "weapons":
					textVar = weapons
					imgVar = weaponsImgs
				case "inHand":
					for card in self.hasCard:
						if card  in weapons:
							cardIndex = weapons.index(card)
							hasCardImg.append(weaponsImgs[cardIndex])
						if card  in rooms:
							cardIndex = rooms.index(card)
							hasCardImg.append(roomImgs[cardIndex])
						if card  in suspects:
							cardIndex = suspects.index(card)
							hasCardImg.append(suspectsImgs[cardIndex])
					textVar = self.hasCard
					imgVar = hasCardImg
					hideCardCheckBoxs = True

			x = 0
			y = 0
			i = 0
			for item in textVar:
				FuckingShit(parent, textVar[i], imgVar[i], x, y, hideCardCheckBoxs, self.hasCard)
				x += 1
				i += 1
				if x > 5:
					x = 0
					y += 1
			if type == "inHand":
				self.buttonFrame = ttk.Frame(parent, width = 120, height = 120, relief = "ridge")
				self.buttonFrame.grid( column= x, row = y,padx=10,pady=20, sticky = tk.N+tk.E+tk.S+tk.W )
				self.playBtn = ttk.Button(
					self.buttonFrame,
					text = "Let's Play.",
					command = killCardsNoteook,
					)
				self.playBtn.grid(column = 0, row = 1, padx = 20, pady = 30, sticky = tk.S)

		
		self.cardsNotebook = ttk.Notebook(parent)
		self.cardsNotebook.pack(fill = 'both', expand = True)
		self.suspectsFrame = ttk.Frame(self.cardsNotebook)
		self.suspectsFrame.pack(fill = 'both', expand = True)
		self.cardsNotebook.add(self.suspectsFrame, text = "suspects")
		loadCards("suspects", self.suspectsFrame)
		self.weaponsFrame = ttk.Frame(self.cardsNotebook)
		self.weaponsFrame.pack(fill = 'both', expand = True)
		self.cardsNotebook.add(self.weaponsFrame, text = "weapons")
		loadCards("weapons", self.weaponsFrame)
		self.roomsFrame = ttk.Frame(self.cardsNotebook)
		self.roomsFrame.pack(fill = 'both', expand = True)
		self.cardsNotebook.add(self.roomsFrame, text = "rooms")
		loadCards("rooms", self.roomsFrame)
		self.inHandFrame = ttk.Frame(self.cardsNotebook)
		self.inHandFrame.pack(fill = 'both', expand = True)
		self.cardsNotebook.add(self.inHandFrame, text = "Card in your hand.")
		self.inHandCanvas = tk.Canvas(self.inHandFrame, bg = '#d9d9d9', bd = 0)
		self.inHandCanvas.pack(fill ='both', expand = True)
		self.cardsNotebook.bind('<<NotebookTabChanged>>', reloadInhadFrame)