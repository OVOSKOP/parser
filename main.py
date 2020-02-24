import tkinter as gui
from py import *

class Main(gui.Frame):
	def __init__(self, root):
		super().__init__(root)
		self.init_main()

	def init_main(self):
		toolbar = gui.Frame(bg="#000000", bd=2)
		toolbar.pack(side=gui.TOP, fill=gui.X)
		self.t = gui.Text(toolbar, height=1,width=113,bd=2)
		self.t.pack(side=gui.LEFT)
		self.text = gui.Text(root, height=70,width=150,bd=2)
		self.text.pack()

		btn_open_str = gui.Button(toolbar, width=10, height=1, text="Open", command=self.pars, bg="#ffffff", bd=0, compound=gui.TOP)
		btn_open_str.place(x=915,y=0)
		# btn_open_str.pack()
	def pars(self):
		self.text.delete('1.0', gui.END)
		filename = self.t.get('1.0', gui.END)
		res = parserHTML(filename.replace('\n', ''))
		self.text.insert(1.0, str(res))

if __name__ == '__main__':
	root = gui.Tk()
	app = Main(root)
	app.pack()

	root.geometry("1000x800+400+300")
	root.title("Parser")

    # l = gui.Text(root)
    # l.insert(1.0, str(document))
    # l.pack()
	root.mainloop()

