import matplotlib.pyplot as plt
import pandas as pd
from math import sin
import numpy as np
data = pd.read_csv("E:/College/2023/DSP/Task 2/attempt_1/signals/emg.csv")
signal_name = data.columns[1]
yaxis_values = data.iloc[:, 1] # gets second column
xaxis_timestamps = data.iloc[:, 0]
interval = xaxis_timestamps[4]- xaxis_timestamps[3]


fmax = 1000

timestamps = xaxis_timestamps
amplitude = yaxis_values
T = 1/ fmax
T_o = 0.00025
steps_no = int(T / T_o)
print('interval',interval,'steps no ',steps_no,'T',T,'T_o',T_o)
x_sampled = list(timestamps)[0:1000:steps_no]
y_sampled = list(amplitude)[0:1000:steps_no]
#plt.plot(x_sampled,y_sampled,marker=r'$\clubsuit$',)
#plt.show() 


reconstructed_data=[]
#fmax*np.sinc(fmax*)

from scipy.fft import fft, fftfreq
# Number of sample points
#N = int(1000*fmax)
N = int(len(x_sampled))
# sample spacing
T = 1.0 / 1000.0
x = np.linspace(0.0, N*T, N, endpoint=False)
#y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
#x= x_sampled
y = y_sampled
yf = fft(y)
xf = fftfreq(N, T)[:N//2]
#import matplotlib.pyplot as plt
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.grid()
plt.show()
plt.figure()
poly = np.polyfit( xf ,2.0/N * np.abs(yf[0:N//2]),5)
poly_y = np.poly1d(poly)(xf)
plt.plot(xf,poly_y)
plt.plot(xf,2.0/N * np.abs(yf[0:N//2]))
plt.show()

#scipy.ifft()
# s = np.fft.ifft(yf)
# plt.plot(x_sampled, s.real,'g^',x_sampled,y_sampled,'b-')
# plt.show()
'''

T = (1 / fmax) *1000
T_o = self.interval 
steps_no = int(T / T_o)
num_of_samples = int(1000/T)
self.y_samples = []
self.x_samples = []
for counter in range(num_of_samples):
self.y_samples.append(amplitude[np.round(T*counter)])
self.x_samples.append(np.round(T*counter))
'''