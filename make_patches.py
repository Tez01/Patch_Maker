import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

parser=argparse.ArgumentParser()
def path1(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)
def path2(string):
    if os.path.isdir(string):
        return string
    else:
        os.mkdir(string)
        return string

parser.add_argument('--txt_path',type=path1,dest='path_to_txt',help='Path to text file')
parser.add_argument('--img_path',type=path1,dest='path_to_img_folder',help='Path to text file')
parser.add_argument('--save_path',type=path2,dest='save_path',help='Path to text file')
args=parser.parse_args()
path_to_txt=args.path_to_txt
path_to_img_folder=args.path_to_img_folder
save_path=args.save_path

def main():
    '''Provide complete paths'''
    data=pd.read_csv(path_to_txt,names=['Frame number','Identity number','Bounding box left','Bounding box top','Bounding box width','Bounding box height','Confidence score','Class','Visibility'])
    data.drop('Confidence score',axis=1,inplace=True)
    id_=1
    count=0 # For skipping frames
    for index,row in data.iterrows():
        if row['Class']==1 or row['Class']==2 or row["Class"]==7  : # Check for pedestrian class
            if row['Identity number']==id_:                         # Check if same pedestrian
                if count==0:                                        # Apply crop for count=0 and skip next two frames
                    id_=row['Identity number']
                    print(row)
                    # Making file_name
                    l=len(str(int(row['Frame number'])))
                    file_name='0'*(6-l) + str(int(row['Frame number']))
                    # Grab image
                    img=plt.imread(path_to_img_folder+file_name+'.jpg')
                    # Cropping
                    left=int(row['Bounding box left'])
                    top=int(row['Bounding box top'])
                    width=int(row['Bounding box width'])
                    height=int(row['Bounding box height'])
                    img_crop=img[top:top+height,left:left+width,:]
                    # Saving
                    if not os.path.isdir(save_path):
                        os.mkdir(save_path)
                    plt.imsave(save_path+file_name+'.jpg',img_crop)
                    count+=1
                elif count==1:
                    count+=1
                    continue
                elif count==2:
                    count=0
                    continue

if __name__=='__main__':
    main()
