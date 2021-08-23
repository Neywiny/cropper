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
		x1.set(event.x)
		y1.set(event.y)
	elif state == 1:
		box = (x1.get()*scale, y1.get()*scale, event.x*scale, event.y*scale)
		ic = img.crop(box)
		idx = img_index.get()
		ic.save('done/' + images[idx])
		img_index.set(idx + 1)
		state = -1
		if idx == len(images) - 1:
			root.destroy()
		else:
			global p_img
			img = Image.open('raw/' + images[idx + 1])
			p_img = ImageTk.PhotoImage(img.resize((img.size[0]//scale, img.size[1]//scale)))
			canvas.itemconfigure(c_img, image=p_img)
			resizer(root, img, canvas)
		
		
	state_var.set(state + 1)
	#print(event.x, event.y)

images = os.listdir("raw")
images.sort()

root = Tk()
root.title('cropper')
state_var = IntVar(root)
x1 = IntVar(root)
y1 = IntVar(root)
img_index = IntVar(root)

scale = 9
canvas = Canvas(root, height=100, width=100)
canvas.pack() 

img = Image.open('raw/' + images[img_index.get()])
resizer(root, img, canvas)
p_img = ImageTk.PhotoImage(img.resize((img.size[0]//scale, img.size[1]//scale)))
c_img = canvas.create_image(0, 0, anchor=NW, image=p_img)
canvas.bind("<1>", mouse_down)

root.mainloop()
