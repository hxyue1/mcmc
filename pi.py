import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.animation as animation
from matplotlib.text import Text

import numpy as np

batch_size = 50

fig, ax = plt.subplots(figsize=(24,16))
ax.set_xlim(-0.6,2)
ax.set_ylim(-0.6,0.6)
square = Rectangle((-0.5,-0.5), 1, 1, fc='None', ec='Black')
circle = Circle((0,0),0.5, fc='None', ec='Black')

blue_count_text = Text(x=0.6, y=0.4, text='1', fontsize=40, color='Blue')
red_count_text = Text(x=0.6, y=0.25, text='1', fontsize=40, color='Red')
calc_text = Text(x=0.6, y=0.1, text= '4xBlue/(Red+Blue)', fontsize=40)
pi_text = Text(x=0.6, y=-0.05, text = '= 3.141592', fontsize=40)

ax.add_patch(square)
ax.add_patch(circle)
ax.add_artist(blue_count_text)
ax.add_artist(red_count_text)
ax.add_artist(calc_text)
ax.add_artist(pi_text)
ax.axis('off')

dots = np.random.uniform(-0.5,0.5, size=(10000000,2))
blue_count = np.sum(dots[:,0]**2 + dots[:,1]**2 < 0.5**2)    
red_count = np.sum(dots[:,0]**2 + dots[:,1]**2 > 0.5**2)
pi = 4*blue_count/(blue_count+red_count)

def animate(frame):
    minibatch = dots[frame*batch_size:frame*batch_size+batch_size]
    
    blue_count = np.sum(dots[:frame*batch_size,0]**2 + dots[:frame*batch_size,1]**2 < 0.5**2)    
    red_count = np.sum(dots[:frame*batch_size,0]**2 + dots[:frame*batch_size,1]**2 > 0.5**2)
    
    for xy in minibatch:
        if xy[0]**2+xy[1]**2 <0.5**2:
            xy_marker = Circle(xy, radius=0.01, fc='None', ec='Blue')        
        else:
            xy_marker = Circle(xy, radius=0.01, fc='None', ec='Red')
        ax.add_patch(xy_marker)
        
    #Updating axes
    
    blue_count_text.set_text(str(blue_count))
    red_count_text.set_text(str(red_count))
    
    calc_text.set_text('4x'+str(blue_count)+'/('+str(blue_count)+'+'+str(red_count)+')')
    pi_text.set_text('= '+str(np.round(4*blue_count/(blue_count+red_count),8)))
    print(frame)
    return[]

anim = animation.FuncAnimation(fig, animate,frames=100, blit=True)
Writer = animation.writers['ffmpeg']
writer = Writer(metadata=dict(artist='Me'), bitrate=1800, fps=4)
anim.save('pi_calc.mp4', writer=writer)