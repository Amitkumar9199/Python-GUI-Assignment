####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package_new.model import InstanceSegmentationModel
from my_package_new.data.dataset import Dataset
from my_package_new.analysis.visualize import plot_visualization
from PIL import ImageTk
from tkinter import *
from tkinter import filedialog as fd
import os
from functools import partial	
####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor,e):
	####### CODE REQUIRED (START) #######
	#this label is used to display original image # its is global as everytime we click on brwse button old image needs to be deleted
	global panel
	
	#checking if any image is already shown in label , then we need to delete it
	if(e.get()!="Browse the file: "):
		panel.after(1000, panel.destroy())#original
		panel1.after(1000, panel1.destroy())#segmented/boundingbox
	
	# This function should pop-up a dialog for the user to select an input image file.
	path = os.path.join(os.getcwd(), 'data', 'imgs').replace('\\', '/') + '/'
	typesOfFiles=(("jpg files", "*.jpg"), ("all files", "*.*"))
	browsedFile= fd.askopenfilename(initialdir=path,title="Select a File",filetypes=typesOfFiles)
	requiredIndex=int(browsedFile[-5])

	#filling the entry box with the image index which we obtained
	e.delete(0, END)
	e.insert(0, "Image : "+str(requiredIndex))
	# Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
	imgs=[]
	length=dataset.__len__()#this function intialises/reads the json file
	item = dataset.__getitem__(requiredIndex)
	image=item['image']#storing image
	imgs.append(image)
	#predicted imgs
	segts=[]
	segt=segmentor.__call__(imgs[0])
	segts.append(segt)
	
	#Draw the segmentation maps and save them
	outputs='data/output'#place where we will store our output  # helpful in debugging
	global segmented_image#variable to store final segmented image #this is global so as it can be used by process fn
	global boundingbox_image#variable to store final bounding box image #this is global so as it can be used by process fn
	original,boundingbox_image,segmented_image=plot_visualization(imgs,segts,outputs,'1')
	
	####### CODE REQUIRED (END) #######
	
	# showing the original image here itself
	imgi=ImageTk.PhotoImage(original)
	panel=Label(root,image=imgi)
	panel.image_names=imgi
	panel.grid(row=1,column=0)
	# Once the output is computed it should be shown automatically based on choice the dropdown button is at.
	process(clicked,e,1)

# `process` function definition starts from here,will process the output when clicked.
def process(clicked,e,check):
	####### CODE REQUIRED (START) #######
	# Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.
	#since we change the entry boc input to image index once image is selected
	if(e.get()=="Browse the file: "):
		print("Ohh! Dear , select a file first.!!")
		return 
	global panel1#global varaible for label so as it can be deleted when required from fileclick fn
	
	if(check==0):#if process button is called multiple times then to delete previous images this is required
		panel1.after(1000,panel1.destroy())
	
	if clicked.get()=="Segmentation":#showing image according to dropdown choice
		img=ImageTk.PhotoImage(segmented_image)
		panel1=Label(root,image=img)
		panel1.image_names=img
		panel1.grid(row=1,column=8)
	else:
		img=ImageTk.PhotoImage(boundingbox_image)
		panel1=Label(root,image=img)
		panel1.image_names=img
		panel1.grid(row=1,column=8)
	####### CODE REQUIRED (END) #######

# `main` function definition starts from here.
if __name__ == '__main__':
	####### CODE REQUIRED (START) ####### (2 lines)
	# Instantiate the root window.
	root=Tk()
	# Provide a title to the root window.
	root.title("SWLAB | IITKGP | IMAGE VIEWER | AMIT |20CS30003")
	####### CODE REQUIRED (END) #######
	# Setting up the segmentor model.
	annotation_file = './data/annotations.jsonl'
	transforms = []
	segmentor = InstanceSegmentationModel()# Instantiate the segmentor model.
	dataset = Dataset(annotation_file, transforms=transforms)# Instantiate the dataset.
	# Declare the options.
	options = ["Segmentation", "Bounding-box"]
	clicked = StringVar()
	clicked.set(options[0])
	e = Entry(root, width=70)
	e.insert(0,"Browse the file: ")#initial value #will help in fixing bug
	e.grid(row=0, column=0)
	####### CODE REQUIRED (START) #######
	# Declare the file browsing button
	browsebutton = Button(root, text="Browse", command=lambda: fileClick(clicked, dataset, segmentor,e))
	browsebutton.grid(row=0,column=1)
	####### CODE REQUIRED (END) #######
	####### CODE REQUIRED (START) #######
	# Declare the drop-down button
	drop=OptionMenu( root , clicked , *options )
	drop.grid(row=0,column=2)
	####### CODE REQUIRED (END) #######
	# This is a `Process` button, check out the sample video to know about its functionality
	processButton = Button(root, text="Process", command=partial(process, clicked,e,0))
	processButton.grid(row=0, column=3)
	####### CODE REQUIRED (START) ####### (1 line)
	buttton_quit=Button(root,text="Exit",command=root.quit)#button to quit the program
	buttton_quit.grid(row=0,column=4)	
	root.mainloop()# Execute with mainloop()
	####### CODE REQUIRED (END) #######