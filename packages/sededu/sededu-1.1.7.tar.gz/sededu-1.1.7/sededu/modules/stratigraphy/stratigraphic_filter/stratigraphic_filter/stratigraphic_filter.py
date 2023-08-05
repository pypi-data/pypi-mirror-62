# interactive stratigraphic filter toy model


# IMPORT LIBLARIES
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget
from mpl_toolkits.axes_grid1 import make_axes_locatable

if __name__ == '__main__':
    import utils
    import functions as funcs
else:
    from . import utils
    from . import functions as funcs

# SET PARAMETERS
time = 50
T = time
timestep = 1
dt = int(timestep)
t = np.linspace(0, T, T+1//dt)

muInit = 0
mu = muInit
muMax = 1
muMin = -muMax

sigmaInit = 1
sigma = sigmaInit
sigmaMax = 2
sigmaMin = 0

yView = 30



def make_column(strat):
    '''
    calculate the column to plot on the right
    as bed contacts, and plot it
    '''
    diff = strat[1:] - strat[:-1]
    bedelevs = strat[np.nonzero(diff)]
    
    ax_strat.clear()
    if len(bedelevs) <= 1:
        bedelev = strat.min()
        ax_strat.axhline(linewidth=1, color='k', y=bedelev)
    else:
        for b in bedelevs:
            ax_strat.axhline(linewidth=1, color='k', y=b)


def run_model(event):
    '''
    the core model run method
        - can be triggered by multiple events or event wrappers
    '''
    # read values from the sliders/statics
    themu = slide_mu.val
    thesigma = slide_sigma.val
    T = time
    dt = timestep

    # compute one run
    t = np.linspace(0, T, T+1//dt)
    elev = funcs.generate_elevation(t, themu, thesigma)
    strat = funcs.generate_stratigraphy(t, elev)
    stats = funcs.compute_statistics(T, elev, strat)
    summ_stats = np.tile(np.nan, (len(stats), 1))

    # if summary stats is checked, compute more runs
    if chk_conn.get_status()[0]:
        nRun = 500
        summ_stats = stats
        for i in np.arange(1, nRun+1):
            ielev = funcs.generate_elevation(t, themu, thesigma)
            istrat = funcs.generate_stratigraphy(t, ielev)
            istats = funcs.compute_statistics(T, ielev, istrat) 
            summ_stats = (summ_stats*(i-1) + istats) / i

    # update the plot and the table
    zero_line.set_ydata(np.zeros(len(t)))
    elev_line.set_data(t, elev)
    strat_line.set_data(t, strat)
    make_column(strat)
    for tab_row in np.arange(1, np.size(tabData,0)+1):
        statsTable._cells[(tab_row, 0)]._text.set_text(utils.format_table_number(stats[tab_row-1]))
        statsTable._cells[(tab_row, 1)]._text.set_text(utils.format_table_number(summ_stats[tab_row-1]))

    # redraw the canvas
    new_yView = np.absolute(elev).max() * 1.2
    if new_yView > yView:
        ax_filter.set_ylim(-new_yView, new_yView)
    else:
        ax_filter.set_ylim(-yView, yView)
    fig.canvas.draw_idle()


def slider_wrapper(event):
    # this is a wrapper for the sliders to only run model if connected
    if chk_conn.get_status()[1]:
        run_model(event)


def reset(event):
    # reset button
    needs_run = False
    if any((slide_mu.val != slide_mu.valinit, 
            slide_sigma.val != slide_sigma.valinit)):
        needs_run = True
    slide_mu.reset()
    slide_sigma.reset()
    for cb in [i for i, x in enumerate(chk_conn.get_status()) if x]:
        chk_conn.set_active(cb)
    if needs_run:
        run_model(event)

    fig.canvas.draw_idle()


# run the program once with the initial values
elev = funcs.generate_elevation(t, muInit, sigmaInit)
strat = funcs.generate_stratigraphy(t, elev)
stats = funcs.compute_statistics(T, elev, strat)
summ_stats = np.tile(np.nan, (len(stats), 1)) # fill nans for init


# setup the figure
plt.rcParams['toolbar'] = 'None'
plt.rcParams['figure.figsize'] = 11, 7
fig, ax_filter = plt.subplots()
fig.canvas.set_window_title('SedEdu -- The Stratigraphic Filter')
plt.subplots_adjust(left=0.075, bottom=0.1, top=0.95, right=0.525)
background_color = 'white'
ax_filter.set_xlabel("time")
ax_filter.set_ylabel("elevation")
plt.ylim(-yView, yView)


# add second axes for strat column
divider = make_axes_locatable(ax_filter)
ax_strat = divider.append_axes("right", 0.5, pad=0.1, sharey=ax_filter)
ax_strat.yaxis.tick_right()
ax_strat.xaxis.set_visible(False)


# add plot elements
zero_line, = ax_filter.step(t, np.zeros(len(t)), linestyle=":", lw=1.5, color='black')
strat_line, = ax_filter.step(t, strat, lw=2, color='red')
elev_line, = ax_filter.step(t, elev, lw=1.5, color='grey')
make_column(strat)


# add slider
widget_color = 'lightgoldenrodyellow'

ax_mu = plt.axes([0.625, 0.85, 0.3, 0.05], facecolor=widget_color)
slide_mu = utils.MinMaxSlider(ax_mu, 'mean of elevation change ($\mu$)', muMin, muMax, 
    valinit=muInit, valstep=0.05, valfmt='%g', transform=ax_filter.transAxes)

ax_sigma = plt.axes([0.625, 0.725, 0.3, 0.05], facecolor=widget_color)
slide_sigma = utils.MinMaxSlider(ax_sigma, 'std. dev. of change ($\sigma$)', sigmaMin, sigmaMax, 
    valinit=sigmaInit, valstep=0.1, transform=ax_filter.transAxes)


# add table
statsNames = ['Final elevation', 'Frac. time preserved', 'Mean bed thickness']
columnNames = ['this run', 'of 500 runs']
ax_statsTable = plt.axes([0.6, 0.325, 0.5, 0.1], frameon=False, xticks=[], yticks=[])
tabData = np.tile(['0', '0'], (len(statsNames), 1))
statsTable = plt.table(cellText=tabData, rowLabels=statsNames,
                       colLabels=columnNames, colWidths=[0.2, 0.2],
                       loc="center")
statsTable.scale(1, 1.5) # xscale, yscale of cells
for tab_row in np.arange(1, np.size(tabData,0)+1):
    statsTable._cells[(tab_row, 0)]._text.set_text(utils.format_table_number(stats[tab_row-1]))
    statsTable._cells[(tab_row, 1)]._text.set_text(utils.format_table_number(summ_stats[tab_row-1]))


# add gui buttons
chk_conn_ax = plt.axes([0.59, 0.5, 0.175, 0.15], facecolor=background_color)
chk_conn_list = ['500-run statistics', 'run w/ slider']
chk_conn = widget.CheckButtons(chk_conn_ax,
                               chk_conn_list,
                               [False, True])

btn_run_ax = plt.axes([0.82, 0.575, 0.125, 0.075])
btn_run = widget.Button(btn_run_ax, 'Run', color='lightskyblue', hovercolor='0.975')

btn_reset_ax = plt.axes([0.82, 0.5, 0.1, 0.04])
btn_reset = widget.Button(btn_reset_ax, 'Reset', color=widget_color, hovercolor='0.975')


# connect widgets
slide_mu.on_changed(slider_wrapper)
slide_sigma.on_changed(slider_wrapper)
btn_reset.on_clicked(reset)
btn_run.on_clicked(run_model)


if __name__ == '__main__':
    # show the results
    plt.show()
