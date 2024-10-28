import math
import pygame
import src.util

import base_sensor

LED_RADIUS = 4
LED_NUMPOINTS_CIRCLE = 100
MAX_VALUE = 4095


class FixedLED(base_sensor.Sensor):
    def __init__(self, surface: pygame.Surface, parent_robot, offset_x, offset_y, name="UnNamed"):
        self.surface = surface
        self.parent_robot = parent_robot
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.x = self.sensor_x = 0.0
        self.y = self.sensor_y = 0.0
        self.name = name
        self.red_value = 0
        self.green_value = 0
        self.blue_value = 0
        self.LED_on = False
        self.outline_rep = None
        self.fill_rep = None

    def update_position(self):
        """ Computes the xy position of the LED based on the position of the robot """
        angle_radians = -math.radians(self.parent_robot.rotation)

        self.set_xvalue(self.parent_robot.x + (
                self.offset_x * math.cos(angle_radians) - (self.offset_y * math.sin(angle_radians))))

        self.set_yvalue(self.parent_robot.y + (
                self.offset_x * math.sin(angle_radians) + (self.offset_y * math.cos(angle_radians))))

    def set_colour(self, red, green, blue):
        """ Accepts RGB value and sets the colour of this LED """
        self.red_value = red
        self.green_value = green
        self.blue_value = blue

    def get_colour(self):
        """ Returns the RGB colour value of this LED """
        return self.red_value, self.green_value, self.blue_value

    def turn_off(self):
        """ Turns off the LED by setting its colour value to black """
        self.set_colour(0, 0, 0)
        self.LED_on = False

    def set_xvalue(self, xvalue):
        self.x = self.sensor_x = xvalue

    def set_yvalue(self, yvalue):
        self.y = self.sensor_y = yvalue

    def draw_sensor_position(self):
        """Draws a circle at the origin of the sensor """
        src.util.circle(self.sensor_x, self.sensor_y, 20)

    def shine(self):
        """ lights up the LED at its position with its colour value """
        self.update_position()
        self.LED_on = True

    def render(self):
        pygame.draw.circle(
            self.surface,
            (255, 0, 0),
            (self.x, self.y),
            LED_RADIUS,
            width=1
        )

        if self.LED_on:
            pygame.draw.circle(
                self.surface,
                (self.red_value, self.green_value, self.blue_value),
                (self.x, self.y),
                LED_RADIUS - 1
            )
