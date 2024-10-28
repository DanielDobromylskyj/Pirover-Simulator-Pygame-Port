from src.windows.simulator import Simulator
from src.windows.startwindow import StartWindow

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
            simulator.run()

            start_window.quit_callback()
