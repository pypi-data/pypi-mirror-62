print("importing: pytest and platform")
import pytest
import platform

print("importing: sys and os")
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

print("importing: numpy")
import numpy as np

print("importing: matplotlib")
import matplotlib



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', remove_text=True)
def test_launch_fig():

    print("in test_launch_fig, importing rain_table.rain_table.GUI")
    from rain_table.rain_table import GUI


    gui = GUI()
    return gui.fig


@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', remove_text=True)
def test_line_into_map_ax():

    from rain_table.rain_table import GUI

    gui = GUI()
    gui.map_ax.plot([-2000, 2000], [-100, 10])
    gui.fig.canvas.draw_idle()

    return gui.fig


@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', remove_text=True)
def test_change_baseflow_slider():

    from rain_table.rain_table import GUI

    gui = GUI()
    gui.sm.slide_baseflow.set_val(gui.config.baseflowmax)
    gui.fig.canvas.draw_idle()

    return gui.fig


@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', remove_text=True)
def test_change_cloud_slider():

    from rain_table.rain_table import GUI

    gui = GUI()
    gui.sm.slide_cloud.set_val(gui.config.cloudmax)
    gui.fig.canvas.draw_idle()

    return gui.fig


@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', remove_text=True)
def test_change_transp_slider():

    from rain_table.rain_table import GUI

    gui = GUI()
    gui.sm.slide_transp.set_val(gui.config.transpmax)
    gui.fig.canvas.draw_idle()

    return gui.fig


@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', remove_text=True)
def test_change_chk():

    from rain_table.rain_table import GUI

    gui = GUI()
    gui.sm.chk_baseflow.set_active(0)
    gui.fig.canvas.draw_idle()

    return gui.fig
