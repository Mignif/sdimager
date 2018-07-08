import time
from time import sleep
import os
from subprocess import PIPE
import subprocess
from threading import Thread
from itertools import islice
import sys
from multiprocessing import Process
try:
	from queue import Queue, Empty
	import tkinter
	from tkinter import Tk, RIGHT, BOTH, RAISED, Listbox, StringVar, END, messagebox
	from tkinter.ttk import Frame, Button, Style
except ImportError:
	sys.exit('Initialisation failed: \n   Please use Python 3 and make sure all required packages are installed.')
import tkinter
print('Imported required dependencies...')


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
		self.frame = tkinter.Frame(self, relief=RAISED, borderwidth=1)
		self.frame.pack(fill=BOTH, expand=True)
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
			self.okButton.pack_forget()
			self.carrier.pack_forget()
			self.closeButton.pack_forget()
			self.label.pack_forget()
			self.sourceLabel.pack_forget()
			self.frame.pack_forget()
			self.output = tkinter.Text(self)
			self.output.pack()
			self.update_idletasks()
			messagebox.showinfo("Information", "The software will now begin the imaging process. The program may seem to freeze while the process runs. Current activity can be viewed in the console.")
			self.instr.set("Imaging...")
			for i in self.cmdVarList:
				print('Wiping disks...')
				print("Executing command: dd if=/dev/zero of=" + i + " bs=512 count=1")
				os.system("dd if=/dev/zero of=" + i + " bs=512 count=1")
				print('Spawning subprocesses...')
				self.command = "sudo dd if=" + self.sourceDB + " | pv | dd of=" + i
				self.processes = set()
				self.max_processes = 3
				self.processes.add(subprocess.Popen([self.command], stdout=subprocess.PIPE, shell=True))
				print('Beginning checks for maximum...')
				while len(self.processes) >= self.max_processes:
					time.sleep(5)
					self.processes.difference_update([
						p for p in processes if p.poll() is not None])
				print('System continuing...')
				self.output.pack_forget()
				print('Beginning check for process end...')
			for p in self.processes:
				p.wait()
			self.instr.set("Imaging done!")
			self.label.config(font=(None,245))
			self.frame.pack(fill=BOTH, expand=True)
			self.closeButton.pack(side=RIGHT, padx=2, pady=2)
			messagebox.showinfo("Done!", "The software will now exit.")
			sys.exit("System exited successfully.")
				
def main():
	root = Tk()
	ex = SDFormat()
	root.geometry("350x250+300+300")
	root.mainloop()
	diskListS = subprocess.Popen("lsblk -dpno name", stdout=PIPE, stderr=PIPE, shell=True)
	diskListL = diskListS.communicate()[0].split()


if __name__ == '__main__':
	main()
