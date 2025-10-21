import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from math import radians, sin, cos

ser = serial.Serial('COM3', 9600)
plt.ion()
fig = plt.figure(figsize=(10,5))
ax_graph = fig.add_subplot(121)
ax_3d = fig.add_subplot(122, projection='3d')

cube = np.array([[1,1,1],[-1,1,1],[-1,-1,1],[1,-1,1],
                 [1,1,-1],[-1,1,-1],[-1,-1,-1],[1,-1,-1]])
faces = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[0,3,7,4],[1,2,6,5]]
pitch_data, roll_data = [], []

def rotation_matrix(pitch, roll):
    p, r = radians(pitch), radians(roll)
    Rx = np.array([[1,0,0],[0,cos(r),-sin(r)],[0,sin(r),cos(r)]])
    Ry = np.array([[cos(p),0,sin(p)],[0,1,0],[-sin(p),0,cos(p)]])
    return Ry @ Rx

while True:
    try:
        data = ser.readline().decode().strip().split(',')
        pitch, roll = float(data[0]), float(data[1])
        pitch_data.append(pitch)
        roll_data.append(roll)
        if len(pitch_data)>100: pitch_data.pop(0); roll_data.pop(0)
        ax_graph.clear()
        ax_graph.plot(pitch_data, label='Pitch')
        ax_graph.plot(roll_data, label='Roll')
        ax_graph.set_ylim(-90,90)
        ax_graph.legend()
        R = rotation_matrix(pitch, roll)
        rotated_cube = cube @ R.T
        ax_3d.clear()
        for f in faces:
            ax_3d.add_collection3d(Poly3DCollection([rotated_cube[f]], facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
        ax_3d.set_xlim(-2,2)
        ax_3d.set_ylim(-2,2)
        ax_3d.set_zlim(-2,2)
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        pass
