import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
from skimage.draw import disk
from skimage.util import random_noise
from skimage.filters import gaussian

def gen_syn_img(height, width, num_cells, fluore_level, cell_size, shape, noise_level, cell_location):
    fluore_img = np.zeros((height, width), dtype=np.uint16) # create 16-bit fluorescene image
    label_img = np.zeros((height, width), dtype=np.uint8) # create 8-bit labeled image
    
    cell_labels = 1
    
    for i in range(num_cells):
        radius = cell_size[i] // 2 # calculate radius of the cell
        cell_x = cell_location[i][0] # get x coordinate of the cell
        cell_y = cell_location[i][1] # get y coordinate of the cell
        
        # generate coordinates of the cell and make sure they are within the image
        rr, cc = disk((cell_y, cell_x), radius, shape=(height, width))
        
        fluore_intensity = np.clip(np.random.normal(fluore_level, 0.2), 0.5, 1.5) # generate random fluorescence intensity
        
        fluore_img[rr, cc] = (fluore_intensity * 30000).astype(np.uint16) # set the fluorescence level of the cell
        label_img[rr, cc] = cell_labels # set the label of the cell
        
        cell_labels += 1 # increment the cell label
        if cell_labels > 255: 
            break
    
    # add gaussian filter and noise
    fluore_img = gaussian(fluore_img, sigma=1)
    fluore_img = random_noise(fluore_img, mode='gaussian', var=noise_level)
    fluore_img = (fluore_img * 65535).astype(np.uint16) # convert to 16-bit image
    
    return Image.fromarray(fluore_img), Image.fromarray(label_img)

# generate synthetic image
height = 128
width = 128
num_cells = 9
fluore_level = 1.
cell_size = [5, 5, 6, 7.5, 8, 8.5, 9, 4.5, 5]
shape = 'circle'
noise_level = 0.0001
cell_location = [(2, 20), (40, 4), (6, 60), (80, 8), (100, 100), (30, 80), (50, 100), (70, 120), (90, 40)]

fluore_img, label_img = gen_syn_img(height, width, num_cells, fluore_level, cell_size, shape, noise_level, cell_location)

fig, (ax1, ax2) = plt.subplots(1, 2)
im1 = ax1.imshow(fluore_img, cmap='copper')
ax1.set_title('Synthetic Fluorescence Image')


im2 = ax2.imshow(label_img, cmap='viridis')
ax2.set_title('Synthetic Labeled Image')
fig.colorbar(im1, ax=ax1, orientation='horizontal')
fig.colorbar(im2, ax=ax2, orientation='horizontal')
plt.show()

        
        
        
        
            
    