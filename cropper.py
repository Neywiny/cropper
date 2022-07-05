from tkinter import *
from PIL import Image, ImageTk
import os
import numpy as np

def resizer(root, img, canvas):
	width, height = img.size
	width //= scale
	height //= scale
	canvas.config(height=height, width=width)
	root.geometry(f"{width}x{height}")
	

def mouse_down(event):
	state = state_var.get()
	#print(state_var.get())
	global img
	if img.width//scale - event.x <= 10:
		event.x = img.width//scale
	elif event.x <= 10:
		event.x = 0
	if img.height//scale - event.y <= 10:
		event.y = img.height//scale
	elif event.y <= 10:
		event.y = 0
	if state == 0:
		x1_var.set(event.x)
		y1_var.set(event.y)
	elif state == 1:
		box = [event.x*scale, event.y*scale, x1_var.get()*scale, y1_var.get()*scale]
		if box[2] - box[0] < 0:
			box[0], box[2] = box[2], box[0]
		if box[3] - box[1] < 0:
			box[1], box[3] = box[3], box[1]
		ic = img.crop(box)
		idx = img_index.get()
		ic.save('done/' + images[idx])
		img_index.set(idx + 1)
		state = -1
		if idx == len(images) - 1:
			root.destroy()
		else:
			canvas.itemconfigure(rect, state=HIDDEN)
			global p_img
			img = Image.open('raw/' + images[idx + 1])
			p_img = ImageTk.PhotoImage(img.resize((img.size[0]//scale, img.size[1]//scale)))
			canvas.itemconfigure(c_img, image=p_img)
			resizer(root, img, canvas)
		
		
	state_var.set(state + 1)
	#print(event.x, event.y)
	
def motion(event):
	if state_var.get() == 1:
		x2, y2 = event.x, event.y
		x1, y1 = x1_var.get(), y1_var.get()
		canvas.coords(rect, x1, y1, x2, y1, x2, y2, x1, y2, x1, y1)
		canvas.itemconfigure(rect, state=NORMAL)
	else:
		canvas.itemconfigure(rect, state=HIDDEN)
def escape(event):
	state_var.set(0)
	canvas.itemconfigure(rect, state=HIDDEN)

images = os.listdir("raw")
images.sort()

root = Tk()
root.title('cropper')
state_var = IntVar(root)
x1_var = IntVar(root)
y1_var = IntVar(root)
img_index = IntVar(root)

scale = 9
canvas = Canvas(root, height=100, width=100)
canvas.pack() 



img = Image.open('raw/' + images[img_index.get()])
resizer(root, img, canvas)
p_img = ImageTk.PhotoImage(img.resize((img.size[0]//scale, img.size[1]//scale)))
c_img = canvas.create_image(0, 0, anchor=NW, image=p_img)
rect = canvas.create_line(0, 0, 0, 0, 0, 0, 0, 0, dash=(10, 10), activewidth=3, disabledwidth=0, state=HIDDEN)
canvas.bind("<1>", mouse_down)
canvas.bind('<Motion>', motion)
root.bind('<Escape>', escape)

root.mainloop()
