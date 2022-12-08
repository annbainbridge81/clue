import tkinter as tk
import tkinter.ttk as ttk
from Cards_n_hand import CNHWidgetBuilder


with open('./backEnd/gifnoc.wgy') as f:
	xywxh = f.readline()
	f.close


doneBtnVar = 0
playerCount = 0
cardsNhand = 0
characters = [
	"Mrs. White",
	"Mrs. Peacock",
	"Professor Plum",
	"Colonel Mustard",
	"Miss Scarlet",
	"Mr. Green"
	]
suspects = [
	"Mrs. White",
	"Mrs. Peacock",
	"Professor Plum",
	"Colonel Mustard",
	"Miss Scarlet",
	"Mr. Green"
	]
weapons = [
	"Candlestick",
	"Knafe",
	"Lead Pipe",
	"Revolver",
	"Rope",
	"Wrench"
	]

class Root(tk.Tk):
	def __init__(self):
		super().__init__()
		self.playerList = []
		greenBlack = '#031a03'
		greentype = '#03bc3a'
		s = ttk.Style()
		s.theme_use('alt')
		s.configure('DickBook.TNotebook.Tab', background="#c7ad6c")
		s.map("DickBook.TNotebook.Tab", background= [("selected", "#d8bd7c")])
		s.configure('CAL.TCombobox',
			selectbackground = greenBlack,
			background = greenBlack,
			arrowcolor = greentype,
			bordercolor = greentype,
			selectforeground = greentype,
			)
		s.map('CAL.TCombobox',
			background = [('active', greenBlack),
				('!disabled', greenBlack)
				],
			fieldbackground = [('!disabled', greenBlack),
				('active', greenBlack)
				],
			foreground = [('active', greentype), ('!disabled', greentype)]
			)
		s.map('CAL.TCombobox.field',
			feildbackground = [('active', greenBlack),('!disabled', greenBlack)])
		s.configure('TScrollbar', troughcolor = greenBlack, background = greentype, bordercolor = greentype, arrowcolor = greenBlack, foreground = greentype)
		s.map('TScrollbar',
			background = [('active', greentype),
				('!disabled', greentype)
				],
			fieldbackground = [('!disabled', greenBlack),
				('active', greenBlack)
				],
			foreground = [('active', greentype), ('!disabled', greentype)]
			)


		def closing_time():
			if self.state() == "zoomed":
				self.state("normal")
			with open('./backEnd/gifnoc.wgy', 'w') as f:
				f.write(self.geometry())
				f.close()
			print(self.geometry(), self.state())
			self.destroy()

		def nextPlayer(addPlayerBtn, doneBtn, charDropDown, nameEntry):
			global playerCount
			global characters
			self.playerList
			if doneBtn != 0:
				doneBtn.grid_remove()
			addPlayerBtn.grid_remove()
			playerCount +=1
			using = charDropDown.get()
			characters.remove(using)
			self.playerList.append((nameEntry.get(), using))
			nameEntry['state'] = "disabled"
			charDropDown['state'] = 'disabled'
			Character(self.startFrame)

		def doneWithPlayers(charDropDown, nameEntry, startFrame, inHandFrame):
			self.playerList
			using = charDropDown.get()
			characters.remove(using)
			self.playerList.append((nameEntry.get(), using))
			#startFrame.pack_forget()
			startFrame.destroy()
			inHandFrame.pack(fill = 'both', expand = True)


		class Character():
			def __init__(self, parent):


				name = tk.StringVar()
				if playerCount > 0:
					name.set("Enter play's name")
				else:
					name.set("Your name here.")		
				self.nameEntry = tk.Entry(
					parent,
					textvariable = name,
					state=tk.NORMAL
					)
				#self.nameEntry.namefield.set("Your name here")
				self.nameEntry.grid(
					column = 0,
					row = playerCount,
					padx = 10,
					pady = 10,
					sticky = tk.E+tk.W
					)


				self.charDropDown = ttk.Combobox(
					parent,
					values = characters,
					state = 'readonly',
					exportselection =0
					)
				self.charDropDown.current(0)
				self.charDropDown.grid(
					column = 1,
					row = playerCount,
					padx = 10,
					pady = 10,
					sticky = tk.E+tk.W
					)
				self.addPlayerBtn = ttk.Button(
					parent,
					text = "Add another player.",
					command = lambda: nextPlayer(
						self.addPlayerBtn,
						doneBtnVar,
						self.charDropDown, 
						self.nameEntry
						)
					)
				self.addPlayerBtn.grid(
					column = 3,
					row =playerCount,
					padx = 10,
					pady = 10
					)
				if playerCount == 5:
					self.addPlayerBtn.grid_remove()
				if playerCount > 0:
					self.doneBtn = ttk.Button(
						parent,
						text = "This is the last player.",
						command = lambda: doneWithPlayers(
							self.charDropDown,
							self.nameEntry,
							parent, 
							inHandFrame
							)
						)
					self.doneBtn.grid(
						column = 4,
						row = playerCount,
						padx =10,
						pady = 10
						)
					global doneBtnVar
					doneBtnVar = self.doneBtn	
		self.geometry(xywxh)
		self.title("Clue Detective Notebook")
		icon = tk.PhotoImage(file = "./img/icon.png")
		self.iconphoto(False, icon)
		
		self.startFrame = ttk.Frame(
			self,
			width = self.winfo_width(),
			height = self.winfo_height()
			)
		self.startFrame.pack(fill = 'both', expand = True)
		Character(self.startFrame)
		self.inHandFrame = tk.Frame(
			self,
			width = self.winfo_width(),
			height = self.winfo_height()
			)
		self.inHandFrame.pack(fill = 'both', expand = True)
		self.inHandFrame.pack_forget()
		global inHandFrame
		inHandFrame = self.inHandFrame
		CNHWidgetBuilder(self, self.inHandFrame)




		self.protocol("WM_DELETE_WINDOW", closing_time)


if __name__ == "__main__":
  app = Root()
  app.mainloop()