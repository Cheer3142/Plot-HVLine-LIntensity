import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
from pathlib import Path
import os
import glob
from astropy.io import fits
import json

def sample():
    files = list(filter(os.path.isfile, glob.glob(str(path/'*'))))
    files.sort(key=lambda x: os.path.getctime(x))
    return files

with open('log.txt') as json_file:
    # Load the JSON data
    data = json_file.read()
js = json.loads(data)
path  = Path(js['Path'])
fname = ''
col_lst = ['r', 'g', 'b', 'c', 'm', 'k']
def gentr_fn(alist):
    while 1:
        for j in alist:
            yield j
col_ele = gentr_fn(col_lst)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
#exit()

#mask_image[0,:]     # horizontal line   (x)
#mask_image[:, 0]    # vertical line     (y)

# add figure and par    
#plt.style.use('fivethirtyeight')

def animate(i):
    global fname
    files = list(filter(os.path.isfile, glob.glob(str(path/'*'))))
    files.sort(key=lambda x: os.path.getctime(x))

    try:
        if fname == files[-1]:
            pass
        else:
            # Read image and draw line
            with open('log.txt') as json_file:
                # Load the JSON data
                data = json_file.read()
            js = json.loads(data)
            h_select = js['Hline']
            v_select = js['Vline']
            
            mask_image = fits.open(path / files[-1])[0].data
            yh = mask_image[h_select, :] 
            xh = [index for index in range(len(yh))]
            yv = mask_image[:, v_select] 
            xv = [index for index in range(len(yv))]

            # Min Max Differential
            diffh = mask_image[h_select, :].max() - mask_image[h_select, :].min()
            diffv = mask_image[:, v_select].max() - mask_image[:, v_select].min()

            # Mark Line
            mask_image_copy = mask_image.copy()
            mask_image_copy[h_select, :] = 0
            mask_image_copy[:, v_select] = 0
            
            # Clear plot
            ax[0].cla()
            ax[1].cla()
            ax[2].cla()

            ### Plotting ###
            ax[0].plot(xh, yh, color = next(col_ele), linestyle = 'dashed',
                                label= 'Horizontal line = {}'.format(h_select))
            ax[0].set_title('Horizontal line ({})'.format(diffh))
            ax[0].set_xlabel("pixel")
            ax[0].set_ylabel("light intensity")
            #ax[0].legend(loc='lower left')
            #plt.legend()
            ax[1].imshow(mask_image_copy, cmap='gray')
            # cm.get_cmap('Spectral')
            ax[1].set_title(files[-1].split('\\')[-1])
            ax[2].plot(xv, yv, color = next(col_ele), linestyle = 'dashed',
                                label= 'Vertical line = {}'.format(v_select))
            ax[2].set_title('Vertical line ({})'.format(diffv))
            ax[2].set_xlabel("pixel")
            ax[2].set_ylabel("light intensity")
            #ax[2].legend(loc='lower left')
            
            #fig.tight_layout()
            fname = files[-1]
    except Exception as e:
        print(e)

ani = FuncAnimation(plt.gcf(), animate, interval=1000)
##plt.tight_layout()
plt.show()
    
    























