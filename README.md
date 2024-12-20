> ⚠️ **Warning: Incomplete Repository**
>
> This repository is currently under development and is actively being updated. Please be aware that it may not load or function as expected at this time.
>
> We appreciate your patience as we work on making this project fully functional.

## About [Pirover-Simulator-Pygame-Port](https://github.com/DanielDobromylskyj/Pirover-Simulator-Pygame-Port)

This repository is a **port** of the original [pirover_simulator](https://github.com/legorovers/pirover_simulator) project. The main change is that this version uses **Pygame** for graphical rendering instead of **Pyglet**. All other functionality and features are intended to closely match the original project, with the added compatibility for Pygame. Do not expect everything to be cross-compatable, although it is our aim - so please make issues with any inconsistencies you find.

For details on the original project, please check out the original repository [here](https://github.com/legorovers/pirover_simulator).

> **Note:**
> This repository and the original project are **not officially affiliated**;
> this port is maintained independently.


## Used Libaries (Modules)
- Pygame
- Numpy
- Tkinter
- Math
- XML
- Threading
- Socket

## Requirements
- Python 3.10+ (Made on 3.12)
- Pip Installs (Non-Built-in):
  + Pygame
  + Numpy


> ## Todo:
> + src
>   + robots
>     + base robot
>       - Add rotational "reaction" force on collision. (Added, just requires more testing and 'work')
>       - Add Slight "bounce" to colliding on walls.
>     + pi2go
>       - Complete Tests
>   + sensors
>     - Ensure all sensors render correctly
