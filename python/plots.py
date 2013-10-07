import matplotlib.pyplot as plt

x = linspace( 0, pi, 100)
y = sin( x )

fig = plt.figure()
fig.show()
ax = fig.add_axes()
ax=fig.add_subplot(1,1,1) # (nrows, ncols, axnum)
fig.tight_layout()

ax.clear()
ax.set_xlabel("time")
ax.set_ylim(auto=True)
ax.set_title("temporal plot")
for p in sol.transpose():
    ax.plot(tspan, p)
fig.canvas.draw()
fig.show()

ax.clear()
ax.set_xlabel("state variables")
ax.set_ylim(auto=True)
ax.set_xlim(auto=True)
ax.set_title("steady state")
ax.bar(range(50), sol[-1])
fig.canvas.draw()
fig.show()

clear
ax.clear()
ax.set_xlabel("time")
ax.set_ylim(auto=True)
ax.set_title("ode info")
ax.plot( info['nst'] )
fig.canvas.draw()
fig.show()








plt.get_current_fig_manager().window.activateWindow()
plt.get_current_fig_manager().window.raise_()

