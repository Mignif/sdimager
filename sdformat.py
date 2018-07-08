import time
from time import sleep
import os
from subprocess import PIPE
import subprocess
from multiprocessing import Process
import tkinter
from tkinter import Tk, RIGHT, BOTH, RAISED, Listbox, StringVar, END, messagebox
from tkinter.ttk import Frame, Button, Style
print('Imported tkinter for Python3')

class SDFormat(Frame):
	diskListS = subprocess.Popen("lsblk -dpno name", stdout=PIPE, stderr=PIPE, shell=True)
	diskListL = diskListS.communicate()[0].split()

	def __init__(self):
		super().__init__()
		self.initUI()
	def sel():
		print('User selected something')
	def initializeVars(self):
		for item in self.diskListL:
			item = tkinter.IntVar()
	def initUI(self):
		try:
			self.isSourceSelect
		except AttributeError:
			print('Assigned variable isSourceSelect to "1"')
			self.isSourceSelect = 1
		try:
			self.cmdVarList
		except AttributeError:
			print('Assigned variable cmdVarList to "[]"')
			self.cmdVarList = []
		self.master.title("Disk Multi-Imager V1.0.0")
		self.pack(fill=BOTH, expand=1)
		self.style = Style()
		self.style.theme_use("default")
		self.instr = StringVar()
		self.instr.set("Please select a source disk.")
		self.label = tkinter.Label(self, text="Please select a source disk.", textvariable=self.instr)
		self.label.pack()
		self.carrier = tkinter.Listbox(self)
		for i in self.diskListL:
			self.carrier.insert(END, i)
		self.carrier.bind("<<ListboxSelect>>", self.onSelect)
		self.carrier.pack(pady=15)
		self.var = StringVar()
		self.label = tkinter.Label(self, text=0, textvariable=self.var)
		self.label.pack()
		frame = tkinter.Frame(self, relief=RAISED, borderwidth=1)
		frame.pack(fill=BOTH, expand=True)
		self.closeButton = tkinter.Button(self, text="Close", command=self.quit)
		self.closeButton.pack(side=RIGHT, padx=2, pady=2)
		self.okButton = tkinter.Button(self, text="Ok", command=self.selectItem)
		self.okButton.pack(side=RIGHT, padx=2, pady=2)
		self.srclabel = StringVar()
		self.sourceLabel = tkinter.Label(self, textvariable=self.srclabel)
		vars = self.initializeVars()

	def onSelect(self, val):
		if self.isSourceSelect == 1:
			sender = val.widget
			idx = sender.curselection()
			value = sender.get(idx)
			self.sourceDisk = value
			self.var.set(value)
			self.selectedIdx = idx
			print(sender)
			print(idx)
		else:
			sender = val.widget
			idx = sender.curselection()
			self.multiSelect = []
			for i in idx:
				value = sender.get(i)
				self.multiSelect.append(value)
				print(value)
	def selectItem(self):
		if self.isSourceSelect == 1:
			print(self.sourceDisk)
			self.isSourceSelect = 0
			print(self.selectedIdx)
			self.carrier.delete(self.selectedIdx)
			self.instr.set("Please select a destination disk(s).")
			self.carrier.config(selectmode=tkinter.MULTIPLE)
			self.srclabel.set(self.sourceDisk)
			self.sourceDB = self.sourceDisk.decode("utf-8")
		else:
			print(self.multiSelect)
			for i in self.multiSelect:
				print(i)
				self.cmdVar = i.decode("utf-8")
				self.cmdVarList.append(self.cmdVar)
				print(' ')
				print(self.cmdVarList)
				for i in self.cmdVarList:
					os.system("echo " + i + " was echoed by bash")
			self.master.withdraw()
			messagebox.showwarning("Warning!", "Continuing will erase all data on target device(s)")
			self.master.deiconify()
			self.okButton.config(state = tkinter.DISABLED)
			for i in self.cmdVarList:
				i = subprocess.Popen(["sudo dd if=" + self.sourceDB + " | pv | dd of=" + i], stdout=subprocess.PIPE, shell=True)
				i.wait()
			self.okButton.config(state = tkinter.NORMAL)
			self.okButton.pack_forget()
			self.carrier.pack_forget()
			self.closeButton.pack_forget()
			self.label.pack_forget()
			self.sourceLabel.pack_forget()
def main():
	root = Tk()
	ex = SDFormat()
	root.geometry("350x250+300+300")
	root.mainloop()
	diskListS = subprocess.Popen("lsblk -dpno name", stdout=PIPE, stderr=PIPE, shell=True)
	diskListL = diskListS.communicate()[0].split()


if __name__ == '__main__':
	main()
