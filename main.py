import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
from pathlib import Path
import os
import glob
from astropy.io import fits
import json
import time
import matplotlib
matplotlib.use('TkAgg')

'''
mask_image[0,:]     # horizontal line   (x)
mask_image[:, 0]    # vertical line     (y)
'''

def sample():
    files = list(filter(os.path.isfile, glob.glob(str(path/'*'))))
    files.sort(key=lambda x: os.path.getctime(x))
    return files

def gen_iterate(alist):
    while 1:
        for j in alist:
            yield j

def on_click(event):
    global h_select, v_select, fname
    '''
    if event.inaxes is not None:
        if event.inaxes == ax[0]:
            h_select = int(event.ydata)
        elif event.inaxes == ax[2]:
            v_select = int(event.ydata)
    '''
    if event.inaxes == ax[1]:
        v_select = int(event.xdata)
        h_select = int(event.ydata)
        #print(f'Clicked at x = {v_select}, y = {h_select}')
        fname = ''
    # print(event)
    
            
# Open log file
with open('../log.txt') as json_file:
    data = json_file.read()
js = json.loads(data)

# Path assign
path  = Path(js['Path'])
if js['Path'] == "":
    os.chdir(os.path.dirname(__file__) + '/../sample')

# Initialize variables 
try:
    h_select = js['Hline']
    v_select = js['Vline']
except:
    h_select = 100
    v_select = 100
fname = ''

# Color Iterate
col_lst = ['r', 'g', 'b', 'c', 'm', 'k']
col_ele = gen_iterate(col_lst)

# add Subplot and on click handler 
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
fig.canvas.mpl_connect('button_press_event', on_click)
#plt.style.use('fivethirtyeight')
#exit()


def animate(i):
    global fname
    files = list(filter(os.path.isfile, glob.glob(str(path/'*.fits'))))
    files.sort(key=lambda x: os.path.getctime(x))
    try:
        if fname == files[-1]:
            pass
        else:
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
                               marker = '.', label= 'Horizontal line = {}'.format(h_select))
            ax[0].set_title('Horizontal line@{} ({})'.format(h_select, diffh))
            ax[0].set_xlabel("pixel")
            ax[0].set_ylabel("light intensity")
            #ax[0].legend(loc='lower left')
            ax[2].plot(xv, yv, color = next(col_ele), linestyle = 'dashed',
                               marker = '.', label= 'Vertical line = {}'.format(v_select))
            ax[2].set_title('Vertical line@{} ({})'.format(v_select, diffv))
            ax[2].set_xlabel("pixel")
            ax[2].set_ylabel("light intensity")
            #ax[2].legend(loc='lower left')
            ax[1].imshow(mask_image_copy, cmap='gray') # cm.get_cmap('Spectral')
            ax[1].set_title(files[-1].split('\\')[-1])
            #fig.tight_layout()
            fig.savefig('../_Dump/'+ ''.join(str(i) for i in time.localtime()[:6]) +'.png')
            
            fname = files[-1]
    except Exception as e:
        print('.', end='')

ani = FuncAnimation(plt.gcf(), animate, interval=100)
##plt.tight_layout()
plt.show()
    























