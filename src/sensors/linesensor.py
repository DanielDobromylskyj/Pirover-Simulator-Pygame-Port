import math

import pygame
import src.util
import src.sensors.base_sensor as base_sensor


class LineMapData:
    def __init__(self, line_map_sprite, position, rotation):
        self.x, self.y = position
        self.rotation = rotation
        self.image = line_map_sprite


class LineSensorMap:
    def __init__(self, line_map_sprite: LineMapData):
        self.pixel_cache = {}

        self.line_map_sprite = None
        self.line_data = None
        self.x_offset = 0
        self.y_offset = 0

        self.set_line_map(line_map_sprite)

    def set_line_map(self, line_map_sprite):
        """Update the line sensor map with a new image."""
        self.pixel_cache = {}
        if line_map_sprite is None:
            self.line_map_sprite = None
            self.line_data = None
            self.x_offset = 0
            self.y_offset = 0
        else:
            self.line_map_sprite = line_map_sprite
            self.x_offset = self.line_map_sprite.x - int(self.line_map_sprite.image.get_width() / 2.0)
            self.y_offset = self.line_map_sprite.y - int(self.line_map_sprite.image.get_height() / 2.0)
            self.line_data = self.line_map_sprite.image

    def check_triggered(self, x, y):
        """Takes as input the current xy position of the line sensor in screen coordinates, this function will then
        translate those to the coordinate system of the image (which may be arbitrarily positioned/rotated) so the
        correct image coordiates can be checked. Returns true if the average intensity of the pixel is greater than
        zero."""
        if self.line_data is not None:
            theta = -math.radians(self.line_map_sprite.rotation)

            px, py = src.util.rotate_around_og((self.line_map_sprite.x, self.line_map_sprite.y), (x, y), -theta)

            px -= self.x_offset
            py -= self.y_offset

            if px < 0 or px > self.line_map_sprite.image.get_width():
                return False

            if py < 0 or py > self.line_map_sprite.image.get_height():
                return False

            if (int(px), int(py)) in self.pixel_cache:
                a = int(self.pixel_cache[(int(px), int(py))])
                return a > 0
            else:
                pix = self.line_data.get_at((int(px), int(py)))
                self.pixel_cache[(int(px), int(py))] = 1

                if len(pix) > 3:
                    r = int(pix[0])
                    g = int(pix[1])
                    b = int(pix[2])
                    a = int(pix[3])

                    self.pixel_cache[(int(px), int(py))] = a

                    return a > 0
                else:
                    return False
        else:
            return False


class FixedLineSensor(base_sensor.Sensor):
    def __init__(self, surface: pygame.Surface, parent_robot, sensor_map, offset_x, offset_y):
        self.surface = surface
        self.parent_robot = parent_robot
        self.sensor_map = sensor_map
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.line_sensor_triggered = False
        self.sensor_x = 0
        self.sensor_y = 0

    def get_triggered(self):
        """Returns the last reading taken from the sensor."""
        return self.line_sensor_triggered

    def update_sensor(self):
        """Computes the xy position of the line sensor based on the position of the robot and queries the
        line sensor map."""
        angle_radians = -math.radians(self.parent_robot.rotation)

        self.set_xvalue(self.parent_robot.x + (
            self.offset_x * math.cos(angle_radians) - (self.offset_y * math.sin(angle_radians))))

        self.set_yvalue(self.parent_robot.y + (
            self.offset_x * math.sin(angle_radians) + (self.offset_y * math.cos(angle_radians))))

        self.line_sensor_triggered = self.sensor_map.check_triggered(int(self.sensor_x), int(self.sensor_y))

    def set_xvalue(self, xvalue):
        self.x = self.sensor_x = (xvalue + self.parent_robot.image.get_width() // 2)

    def set_yvalue(self, yvalue):
        self.y = self.sensor_y = (yvalue + self.parent_robot.image.get_height() // 2)

    def render(self):
        pygame.draw.circle(
            self.surface,
            (0, 255, 0),
            (int(self.sensor_x), int(self.sensor_y)),
            5,
            width=1
        )

    #def draw_sensor_position(self):  # todo - unsure if needed
    #    """Draws a circle at the origin of the sensor."""
    #    src.util.circle(self.sensor_x, self.sensor_y, 5)