import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path
import os
import glob
from astropy.io import fits

path  = Path(r"C:\Users\Optics_Lab_010\Desktop\Project\NanoPiezo\Anjelie img\EvWaCo_Angelie\Mask Pressure Tool Images\Mask_images (copy)")
fname = ''
col_lst = ['r', 'm', 'g', 'b', 'c', 'k']
def gentr_fn(alist):
    while 1:
        for j in alist:
            yield j
col_ele = gentr_fn(col_lst)
#exit()

#mask_image[0,:]     # horizontal line   (x)
#mask_image[:, 0]    # vertical line     (y)

# add figure and par    
#plt.style.use('fivethirtyeight')

def animate(i):
    global fname
    files = list(filter(os.path.isfile, glob.glob(str(path/'*'))))
    files.sort(key=lambda x: os.path.getctime(x))
    
    if fname == files[-1]:
        pass
    else:
        mask_image = fits.open(path / files[-1])[0].data
        y = mask_image[95,:] 
        x = [index for index in range(len(y))]
        diff = mask_image[95,:].max() - mask_image[95,:].min()
        plt.cla()

        plt.plot(x, y, color = next(col_ele), linestyle = 'dashed',
                           marker = 'o', label= 'Horizontal line({})'.format(diff))
        plt.title(files[-1].split('\\')[-1])
        plt.xlabel("pixel")
        plt.ylabel("light intensity")
        plt.legend(loc='lower left')
        #plt.legend()
        plt.tight_layout()
        fname = files[-1]

ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()
    
    























