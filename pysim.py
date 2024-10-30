from src.windows.simulator import Simulator
from src.windows.startwindow import StartWindow

# Test imports
import threading


def _start_test():
    import examples.LineFollower


def start_test():
    threading.Thread(target=_start_test).start()


if __name__ == "__main__":
    selected_file = ""
    selected_robot = ""
    start_window = None

    while (selected_file == "") and (start_window is None):
        # Get inputs from user (GUI)
        if start_window is not None:
            start_window.refresh_world_filelist()
        else:
            start_window = StartWindow()

        selected_file, selected_robot = start_window.start()

        if selected_file == "None":
            selected_file = None

        if selected_file is not None and selected_robot is not None:
            simulator = Simulator(selected_file, selected_robot)
            #simulator.robot.rotation = 15
            start_test()
            simulator.run()

            start_window.quit_callback()

            start_window = None
            selected_file = ""
