#Imports
import math
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import cv2
import numpy as np
def plot_visualization(imgs,segts,outputs,check): # Write the required arguments
  #applying masks on images
  original=[]#this will store original images
  copy_=[]#this will store segmented image
  ans=[]#this willl store bounding box imga
  for i in range(len(imgs)):
    original.append(imgs[i])#original image
    copy_.append(imgs[i])
    # rgb=[0,0,0]
    # index=0
    # rgb[index]=1
    for j in segts[i][1][0:3]:#applying segmentation masks    
      copy_[i]=copy_[i]*((j<0.5).astype(int))+np.rollaxis(((np.transpose(j,(1,2,0)))*[0,1,0.5]),2,0)+copy_[i]*(j>=0.5).astype(int)*0.35
      # copy_[i]=copy_[i]*((j<0.5).astype(int))
      # copy_[i]=copy_[i]+ np.rollaxis(( ( np.transpose ( j , ( 1 , 2 , 0 ) ) ) * [ 0 , 1 , 0.5 ] ),2,0)
      # copy_[i]=copy_[i]*((j<0.5).astype(int))+(j>=0.5).astype(int)*tuple(rgb)+copy_[i]*(j>=0.5).astype(int)*0.35 
    # changing axis of images
    imgs[i]=Image.fromarray((np.rollaxis(imgs[i],0,3)*255).astype(np.uint8))  #hw3 <--- 3hw 
    copy_[i]=Image.fromarray((np.rollaxis(copy_[i],0,3)*255).astype(np.uint8))  #hw3 <--- 3hw 
    original[i]=Image.fromarray((np.rollaxis(original[i],0,3)*255).astype(np.uint8))  #hw3 <--- 3hw 
    
    #making bounding boxes
    #drawing rectangles on images
    cnt=0
    outline_colr=["red","green","yellow"]#using different colors for different shapes
    for j in segts[i][0][0:3]:
      img1=ImageDraw.Draw(imgs[i])
      img1.rectangle(j,outline=outline_colr[cnt])
      cnt+=1
    
    #converting images to array
    imgs[i]=np.array(imgs[i])
    copy_[i]=np.array(copy_[i])
    original[i]=np.array(original[i])
    
    #putting text on images
    cnt=0
    text_colr=[(0, 0, 255),(231, 84, 128),(0,255, 0)]
    for j in range(0,min(3,len(segts[i][2]))):
      cal=segts[i][2][j]#name
      prob=segts[i][3][j]#probability
      text=cal+'\n'+str("%.4f" % (prob))
      cv2.putText(img=imgs[i], text=text, org=tuple(map(int,segts[i][0][j][0])), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.4, color=text_colr[cnt],thickness=1)
      cnt+=1

    #converting from array to image and saving image
    imgs[i]=Image.fromarray(imgs[i])
    copy_[i]=Image.fromarray(copy_[i])
    original[i]=Image.fromarray(original[i])

    original[i].save(outputs+'/'+'original'+'.jpg')
    #appending image to ans for returning
    ans.append(original[i])
    ans.append(imgs[i])
    ans.append(copy_[i])
    if (check=='1'):#if normal image without transformation#check is for naming the file
      imgs[i].save(outputs+'/'+'Segmentation'+'.jpg')
      copy_[i].save(outputs+'/'+'BoundingBox'+'.jpg')
    else:#if any transformation is used# check will contain its name(transformation)
      imgs[i].save(outputs+'/'+check+'Segmentation'+'.jpg')
      copy_[i].save(outputs+'/'+check+'BoundingBox'+'.jpg')

  return ans
      
    

      
  # The function should plot the predicted segmentation maps and the bounding boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
  
