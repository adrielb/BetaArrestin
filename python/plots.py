import matplotlib.pyplot as plt
from numpy import *

x = linspace( 0, pi, 100)
y = sin( x )

fig = plt.figure()
fig.tight_layout()
fig.show()
ax = fig.add_axes()
ax=fig.add_subplot(1,1,1) # (nrows, ncols, axnum)

ax.clear()
ax.set_ylim(-1,1)
ax.set_title("wave")
ax.plot(x,y)
fig.canvas.draw()
fig.show()

plt.get_current_fig_manager().window.activateWindow()
plt.get_current_fig_manager().window.raise_()

