import serial
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ser = serial.Serial('COM3', 9600)
plt.ion()
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(5,8))

line, = ax1.plot([], [])
pitch_data = []
ax1.set_xlim(0,100)
ax1.set_ylim(-90,90)
rect = Rectangle((-0.5,-0.5),1,1, fc='cyan', ec='r')
ax2.add_patch(rect)
ax2.set_xlim(-2,2)
ax2.set_ylim(-2,2)

while True:
    try:
        data = ser.readline().decode().strip().split(',')
        pitch = float(data[0])
        pitch_data.append(pitch)
        if len(pitch_data) > 100: pitch_data.pop(0)
        line.set_xdata(range(len(pitch_data)))
        line.set_ydata(pitch_data)
        rect.set_angle(pitch)
        ax1.relim()
        ax1.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        pass
