from data_extraction import extract_data
from PIL import Image
import requests
from io import BytesIO
import os 
import pathlib 
import zipfile
import random
#
#def open_random_images(path):
#    # Get a list of all files in the folder
#    all_files = os.listdir(path)
#    random.shuffle(all_files)
#    image_names = all_files[:4]
#    image_paths = []
#    for i in range(4):
#        image_path = os.path.join(path, image_names[i])
#        image_paths.append(image_path)
#    return image_paths
#    
#
#def visualise_image():
#    url = extract_data()
#    url_response = requests.get(url)
#    with zipfile.ZipFile(BytesIO(url_response.content)) as z:
#        z.extractall('.')
#    images = open_random_images(os.path.join(os.getcwd(),"BraTS2020_TrainingData/MICCAI_BraTS2020_TrainingData/"))
#    for i in range(4):
#        image = Image.open(images[i])
#        image = image.convert('RGB')
#        image.save('sample'+str(i)+'.jpg')
#    #meningioma_tumor_image.save('meningioma_tumor.jpg')
#    return url
#
#visualise_image()


from data_extraction import extract_data
from PIL import Image
import nibabel as nib
import numpy as np
import requests
from io import BytesIO
import os
import random
import plotly.express as px

def open_random_folder(path):
    # Get a list of all folders in the path
    all_folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    random_folder = random.choice(all_folders)
    folder_path = os.path.join(path, random_folder)
    return folder_path

def save_nii_as_jpg(nii_file, output_path):
    # Load the NIfTI file
    nii_img = nib.load(nii_file)
    img_data = nii_img.get_fdata()

    # Select the middle slice for visualization
    slice_index = img_data.shape[2] // 2
    slice_img = img_data[:, :, slice_index]

    # Normalize the image to the range 0-255 and convert to uint8
    slice_img = np.interp(slice_img, (slice_img.min(), slice_img.max()), (0, 255)).astype(np.uint8)

    # Convert to RGB image
    img = Image.fromarray(slice_img)
    img = img.convert('RGB')
    img.save(output_path)

def visualise_image():
    url = extract_data()
    url_response = requests.get(url)
    with zipfile.ZipFile(BytesIO(url_response.content)) as z:
        z.extractall('.')
    old_filename = "BraTS2020_TrainingData/MICCAI_BraTS2020_TrainingData/BraTS20_Training_355/W39_1998.09.19_Segm.nii"
    new_filename = "BraTS2020_TrainingData/MICCAI_BraTS2020_TrainingData/BraTS20_Training_355/BraTS20_Training_355_seg.nii"
    
    # Rename the file
    os.rename(old_filename, new_filename)
    
    print(f"File renamed to: {new_filename}")
    base_path = os.path.join(os.getcwd(), "BraTS2020_TrainingData/MICCAI_BraTS2020_TrainingData/")
    random_folder = open_random_folder(base_path)

    # Process all .nii files in the random folder
    nii_files = [f for f in os.listdir(random_folder) if f.endswith('.nii') and '_seg' not in f]
    for i, nii_file in enumerate(nii_files):
        nii_file_path = os.path.join(random_folder, nii_file)
        output_path = f'sample_{i}.jpg'
        save_nii_as_jpg(nii_file_path, output_path)

    return url

visualise_image()
