'''
========================================================
| Title:  time domain and frequenct domain(fft) figure |
| Author: Yang Hang Wu                                 |
| Date:   22 Nov 2019                                  |
========================================================
'''


import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
import glob, os

import seaborn
from scipy.fftpack import fft,ifft

def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)


interval=1                      # interval of plotting data
time=0.5                          # update time of plotting rate
fig_w=10                        # fig width
fig_h=5                         # fig hight
fig_x=130                       # fig upper left x 
fig_y=80                       # fig upper left y
color=['go-','ro-','bo-','co-'] # colors of time domain subplot
f_color=['g-','r-','b-','c-']   # colors of frequenct domain subplot
Fs = 1000.0;                    # sampling rate (Hz)
T = 0.4;                        # sampling time (s)

path = os.getcwd()
os.chdir(path)
print(path)
fig, axs = plt.subplots(4, 2,figsize = (fig_w, fig_h))
move_figure(fig, fig_x, fig_y)
index=0
while(True):
    '''get files in dirctory'''
    file_list=[]
    while(True):
        for file in glob.glob("*.lvm"):
            file_list.append(file)
        break
    try:
        latest_file_name = file_list[len(file_list)-1]
    except:
        print("no file")
        continue
    if(index<len(file_list)):
        index = index +1
        print(index)

    else:
        print("no new file")
        continue
    
    if(index%interval==0):
        '''read file'''
        file_path = os.path.join(path, "exhibition_"+str(index)+".lvm" )
        print(file_path)
        channels=[[],[],[],[]]
        fp = open(file_path, "r")
        channel_num=0
        for line in iter(fp):
            components=line.split("	")
            channel_num=len(components)-1
            for k in range(channel_num):                
                channels[k].append(float(components[k+1]))
        fp.close()

        ''' fft'''
        freq_channels=[[],[],[],[]]
        for i in range(channel_num):
            freq_channels[i]=abs(fft(channels[i]))
            freq_channels[i]=freq_channels[i][range(int(Fs*T/2))]
        xf = np.arange(len(freq_channels[channel_num-1]))
        xf = xf[range(int(Fs*T/2))] #half interval

        '''plotting'''
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=1)
        fig.suptitle("exhibition_"+str(index)+".lvm", fontsize=16)
        mngr = plt.get_current_fig_manager()       
        for n in range(channel_num):
            axs[n, 0].clear()          
            axs[n, 0].plot(np.arange(0,T,1/Fs),channels[n], color[n])
            axs[n, 0].set_title('channel '+str(n+1)+' time domain')
        for n in range(channel_num):
            axs[n, 1].clear()          
            axs[n, 1].plot(xf,freq_channels[n], f_color[n])
            axs[n, 1].set_title('channel '+str(n+1)+' frequency domain')
        try:
            plt.pause(time)
        except:
            fig, axs = plt.subplots(4, 2,figsize = (fig_w, fig_h))
            move_figure(fig, fig_x, fig_y)


