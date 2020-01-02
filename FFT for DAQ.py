'''
========================================================
| Title:  time domain and frequenct domain(fft) figure |
| Author: Yang Hang Wu                                 |
| Date:   25 Nov 2019                                  |
========================================================
'''


import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt
import glob, os
import threading
import seaborn
from scipy.fftpack import fft,ifft
# 子執行緒的工作函數

def plot_job():
    for n in range(channel_num):
        axs[n, 0].clear()          
        axs[n, 0].plot(np.arange(0,0.4,1/1000),channels[n], color[n])
        axs[n, 0].set_title('channel '+str(n+1)+' time domain')
    print("thread finished")
    



Fs = 25600.0;                   # sampling rate (Hz)
T = 1;                          # sampling time (s)
interval=1                      # interval of plotting data
pause_time=0.5                  # update time of plotting rate
fig_w=10                        # fig width
fig_h=5                         # fig hight
fig_x=130                       # fig upper left x 
fig_y=80                        # fig upper left y
color=['g-','r-','b-','c-']     # colors of time domain subplot
f_color=['g-','r-','b-','c-']   # colors of frequenct domain subplot


path = os.getcwd()
os.chdir(path)
print(path)
index=0
tStart = time.time()#計時開始
fig, axs = plt.subplots(4, 3,figsize = (fig_w, fig_h))

tEnd = time.time()#計時結束
print ("create fig cost %f sec" % (tEnd - tStart))
'''
file_thread = threading.Thread(target = create_fig)
file_thread.start()
plot_thread_pool=[]
for i in range(8):
    plot_thread_pool.append(threading.Thread(target = plot_job))
'''
file_num=0
max_freq_channels=[[],[],[],[]]
while(True):
    '''get files in dirctory'''
    tStart = time.time()#計時開始
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
        #print("no new file")
        continue
    
    if(index%interval==0):
        '''read file'''
        file_num+=1
        channels=[[],[],[],[]]
        file_path = os.path.join(path, "exhibition_"+str(index)+".lvm" )
        print(file_path)
        fp = open(file_path, "r")
        global channel_num
        for line in iter(fp):
            components=line.split("	")
            channel_num=len(components)-1
            for k in range(channel_num):                
                channels[k].append(float(components[k+1]))
        fp.close()
        tEnd = time.time()#計時結束
        print ("readfile cost %f sec" % (tEnd - tStart))
        filename= os.path.join(path, "exhibition_peak_"+str(index)+".txt" )
        fp = open(filename, "w")
        for i in range(4):
            fp.write(str(max(channels[i]))+"\n")
        fp.close()
        ''' fft'''
        tStart = time.time()#計時開始
        freq_channels=[[],[],[],[]]
        filename= os.path.join(path, "exhibition_fft_"+str(index)+".txt" )
        fp = open(filename, "w")
        for i in range(channel_num):
            freq_channels[i]=abs(fft(channels[i]))
            freq_channels[i][:] = [x / Fs for x in freq_channels[i]]
            freq_channels[i]=freq_channels[i][range(int(Fs*T/2))]
            max_freq_channels[i].append(list(freq_channels[i]).index(max(freq_channels[i])))
            fp.write(str(max_freq_channels[i][-1])+"\n")
            print(max_freq_channels[i])
        fp.close()

        xf = np.arange(len(freq_channels[channel_num-1]))
        xf = xf[range(int(Fs*T/2))] #half interval
        tEnd = time.time()#計時結束
        print ("fft cost %f sec" % (tEnd - tStart))

        '''plotting'''
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                wspace=None, hspace=1)
        fig.suptitle("exhibition_"+str(index)+".lvm", fontsize=16)
        mngr = plt.get_current_fig_manager()  
        #plot_t=threading.Thread(target = plot_job)
        tStart = time.time()#計時開始
        #plot_t.start()
        
        for n in range(channel_num):
            axs[n, 0].clear()          
            axs[n, 0].plot(np.arange(0,T,1/Fs),channels[n], color[n])
            axs[n, 0].set_title('channel '+str(n+1)+' time domain')
        
        #tEnd = time.time()#計時結束
        #print ("plot time cost %f sec" % (tEnd - tStart))
        #tStart = time.time()#計時開始 
        for n in range(channel_num):
            axs[n, 1].clear()          

            axs[n, 1].plot(xf[:1000],freq_channels[n][:1000], f_color[n])
            axs[n, 1].set_title('channel '+str(n+1)+' frequency domain')
        for n in range(channel_num):
            axs[n, 2].clear()          
            axs[n, 2].scatter(range(file_num),max_freq_channels[n])
            axs[n, 2].set_title('channel '+str(n+1)+' max frequency')
        #plot_t.join()
        tEnd = time.time()#計時結束
        print ("plot freq cost %f sec" % (tEnd - tStart))
        try:
            plt.pause(pause_time)
        except:
            fig, axs = plt.subplots(4, 2,figsize = (fig_w, fig_h))
            move_figure(fig, fig_x, fig_y)

