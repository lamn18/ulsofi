import scipy.fft as sfft
import numpy as np  # for arrays
import pyaudio
import time
import matplotlib
matplotlib.use('GTK3Agg')
from matplotlib import pyplot as plt

blit = True

# Main runtime
if __name__ == '__main__':
    print('Starting UlSoFi-Py')

    pyaud = pyaudio.PyAudio()
    stream = pyaud.open( format = pyaudio.paInt16, channels = 1, rate = 44100, input_device_index = 2, input = True, frames_per_buffer=4096)
    

    plt.ion()
    X = np.linspace(0,22050,52)
    y = np.cos(X)

    fig, ax2 = plt.subplots(figsize=(8,6))
    line1, = ax2.plot(X, y)

    ax2.set_ylim([0,1000])
    text=ax2.text(0.8,0.5, "")

    plt.title("Dynamic Plot of mic input",fontsize=25)
    plt.xlabel("Frequency (Hz)",fontsize=18)
    plt.ylabel("Intensity",fontsize=18)

    fig.canvas.draw()

    # If blit, set up some blits
    if blit:
        ax2background = fig.canvas.copy_from_bbox(ax2.bbox)

    plt.show(block=False)

    t_start = time.time()
    j = 0
    while True: 
        # Read raw microphone data 
        rawsamps = stream.read(1024, exception_on_overflow = False) 
        # Convert raw data to NumPy array 
        samps = np.fromstring(rawsamps, dtype=np.int16) 
        # Calculate the FFT
        pfft = sfft.rfft(samps)

        # Parse the FFT
        ydata = [0]*int(len(pfft)/10 + 1)
        for i in range(len(pfft)):
            ydata[int(i/10)] += pfft[i]

        # FPS Text
        tx = 'Main Frame Rate:\n {fps:.3f}FPS'.format(fps= ((j+1) / (time.time() - t_start))) 
        text.set_text(tx)
        j += 1

        # DEBUG Space
        #print("Length of all: ", len(rawsamps), len(ydata), len(pfft))
        
        line1.set_xdata(X)
        line1.set_ydata(ydata)

        if blit:
            fig.canvas.restore_region(ax2background)
            ax2.draw_artist(line1)
            #ax2.draw_artist(text)
            # Fill in the axes
            fig.canvas.blit(ax2.bbox)
        else:
            fig.canvas.draw()

        fig.canvas.flush_events()

        


