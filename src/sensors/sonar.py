import pygame
from math import pi, cos, sin
import numpy as np

import src.sensors.base_sensor as base_sensor

SONAR_BEAM_STEP = pi / 25.0

MAP_FILL_COLOUR = (255, 255, 255)
MAP_BLANK_COLOUR = (0, 0, 0)


class Map:
    def __init__(self, surface: pygame.Surface, cell_size):
        self.origin_x = 0
        self.origin_y = 0
        self.resolution = cell_size
        self.surface = surface
        self.height = int(self.surface.get_height() / cell_size)
        self.width = int(self.surface.get_width() / cell_size)
        self.grid = np.zeros((self.height, self.width))

    def clear_map(self):
        """ Removes all obstacles from the Grid Map """
        self.grid = np.zeros((self.height, self.width))

    def insert_rectangle(self, ctr_x, ctr_y, size_x, size_y, cell_value=1):
        """ Insert a rectangle into the Grid Map at position defined by (ctr_x, ctr_y) and
            size (size_x, size_y). The optional cell value allows this function to be used to
            delete a rectangle."""
        ctr_x_cells = int(ctr_x / self.resolution)
        ctr_y_cells = int(ctr_y / self.resolution)

        size_x_cells = int(size_x / self.resolution / 2)
        size_y_cells = int(size_y / self.resolution / 2)
        for x in range(ctr_x_cells - size_x_cells, ctr_x_cells + size_x_cells + 1):
            for y in range(ctr_y_cells - size_y_cells, ctr_y_cells + size_y_cells + 1):
                self.set_cell(int(x), int(y), cell_value)

    def delete_rectangle(self, ctr_x, ctr_y, size_x, size_y):
        """Delete a rectangle into the Grid Map at position defined by (ctr_x, ctr_y) and
            size (size_x, size_y). Uses the code from the insert_rectangle function to
            avoid duplication."""
        self.insert_rectangle(ctr_x, ctr_y, size_x, size_y, 0)

    def set_cell(self, x, y, val):
        """Set the value of a grid cell (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = val

    def update(self, delta_time):
        pass

    def render(self):
        self.draw()

    def draw(self):  # NOTE - if this doesn't change, we dont need to re-render it - todo
        """Draw the Grid Map."""
        self.surface.fill(MAP_BLANK_COLOUR)

        cell_size = self.resolution
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x]:
                    square_coords = (x * cell_size, y * cell_size,
                                     x * cell_size, y * cell_size + cell_size,
                                     x * cell_size + cell_size, y * cell_size,
                                     x * cell_size + cell_size, y * cell_size + cell_size)

                    pygame.draw.rect(self.surface, MAP_FILL_COLOUR, square_coords)


class Sonar(base_sensor.Sensor):
    def __init__(self, sensor_map, min_range, max_range, cone_angle):
        self.min_range = min_range
        self.max_range = max_range
        self.cone_angle = cone_angle
        self.sensor_map = sensor_map
        self.current_range = -1.0

    def update_sonar(self, x, y, theta):
        """ Returns the distance to the nearest obstacle for a sensor at position (x, y) and at angle theta."""
        self.current_range = self.max_range

        # create a bundle of rays to replicate a sonar beam
        sweep = np.arange(-self.cone_angle / 2.0, self.cone_angle / 2.0, SONAR_BEAM_STEP)

        # cast each ray until it hits an obstacle or the end of the map
        for angle in sweep:
            distance = 1
            while distance <= (self.max_range / self.sensor_map.resolution):
                x_map = x / self.sensor_map.resolution
                x_map += distance * cos(angle + theta)
                x_map = int(x_map)

                y_map = y / self.sensor_map.resolution
                y_map += distance * sin(angle + theta)
                y_map = int(y_map)

                if y_map > self.sensor_map.height - 1 or x_map > self.sensor_map.width - 1:
                    break

                if y_map < 1 or x_map < 1:
                    break

                if self.sensor_map.grid[y_map][x_map]:
                    break

                distance += 1

            sensor_range = distance * self.sensor_map.resolution
            if sensor_range < self.max_range and sensor_range < self.current_range:
                self.current_range = sensor_range

        # cap the distance to the min and max values of the sensors
        self.current_range = max(self.min_range, self.current_range)
        self.current_range = min(self.max_range, self.current_range)

        return self.current_range
