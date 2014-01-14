import matplotlib.pyplot as plt

showfigs = False

def displayfig():
    global showfigs
    showfigs = True

def genfig( idx=1 ):
    fig = plt.figure(idx)
    fig.clear()
    ax = fig.gca()
    if showfigs:
        fig.show()
    return fig, ax

def showfig( block=False ):
    #fig = plt.figure( idx )
    fig = plt.gcf()
    fig.canvas.draw()
    #fig.canvas.manager.window.move(1200,(idx-1) * 544)
    #plt.ion()
    #plt.get_current_fig_manager().window.activateWindow()
    plt.get_current_fig_manager().window.raise_()
    if showfigs:
        if block:
            plt.show()
        else:
            fig.show()

