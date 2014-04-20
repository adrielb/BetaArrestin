import matplotlib.pyplot as plt

# global plot colors {{{
# medialab iwanthue 'pimp, but lighter' color scheme
mycolors = {
    'yellow' : '#CADB44',
    'purple' : '#D4A2E1',
    'blue'   : '#51DECF',
    'orange' : '#F0B13C',
    'green'  : '#74E166',
}
color_native='red'
color_oe='blue'

# }}}

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

