import os
import random
import ast
import shutil
import ast
import cv2
import numpy as np


def file_name_extract(img_path):
    '''Returned all files in img_path loc'''
    file_list = os.listdir(img_path)
    file_list = [file for file in file_list if not file.startswith('.')]
    file_list = [i.split('.')[0] for i in file_list]
    return(file_list)

def copy_files(src, sink, files,img_type):
    '''Copies files from src to sink of img_type
    
    Params:
    src - valid dir_type string, source loc of the files
    sink - valid dir_type string, final destination of files
    files - list of files to be copied
    img_type - string extention
    
    Outputs:
    NA - helper file to move files
    '''
    for file in files:
        src_file = os.path.join(src,(file + img_type))
        sink_file = os.path.join(sink,(file + img_type))
        shutil.copyfile(src_file,sink_file )
        
def create_mask_files(img_tag_path, dest, files, img_type, file_type, pixel_x = 1280, pixel_y = 1280, rgb = True):
    """ Copies files from src to sink of img_type
    
    Params:
    img_tag_path - valid dir_type string, source loc of tag txt files
    dest - desired destination folder of the mask file
    files - list of files to be converted to mask images
    img_type - string extention of text files
    file_type - string extention of seg files 
    pixel_x - resolution x of tag files, default 1280
    pixel_y - resolution y of tag files, default 1280
    rgb - if true number of channels set to 3 else 1, default value set to 3
    
    Outputs:
    NA - helper file to generate file types
    """
    if rgb :
        channels = 3
    else:
        channels = 1

    
    for file in files:
        seg_img = np.zeros((pixel_x,pixel_y,channels))
        
        src_file = os.path.join(img_tag_path,(file+file_type))
        #print(src_file)
        sink_file = os.path.join(dest,(file+img_type))
        with open(src_file) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = [ast.literal_eval(x) for x in content]
        
        #print(content)
        for i in range(len(content)):
            contour = np.array(content[i])
            #print(contour)
            cv2.fillPoly(seg_img, pts =[contour],color = (0,255,0))

        seg_img = np.array(seg_img, np.uint8)
        cv2.imwrite(sink_file, seg_img)
        
def test_file_names(loc_img, loc_seg):
    '''Unit test to check if same files are there in loc_img, loc_seg
    Params:
    loc_img - location of images
    loc_seg - location of tags
    
    Outputs:
    result: str, 'Pass' or 'Fail' indicating status of test
    
    '''

    file_images = os.listdir(loc_img)
    file_images = [file for file in file_images if not file.startswith('.')]


    file_seg = os.listdir(loc_seg)
    file_seg = [file for file in file_seg if not file.startswith('.')]

    m_set=set(file_images)
    A = all(x in m_set  for x in file_seg)

    m_set=set(file_seg)
    B = all(x in m_set  for x in file_images)
    
    result = A & B
    if result:
        return('Pass')
    else:
        return('Fail')
