import math
import pygame
import src.resources
import src.sprites.basicsprite
import src.util
import base_sensor

from sonar import Sonar


class FixedTransformDistanceSensor(base_sensor.Sensor):
    def __init__(self, surface: pygame.Surface, parent_robot, sensor_map, offset_x, offset_y, sensor_rot, min_range, max_range, beam_angle):
        self.surface = surface
        self.parent_robot = parent_robot
        self.sensor = Sonar(sensor_map, min_range, max_range, beam_angle)
        self.sensor_offset_x = offset_x
        self.sensor_offset_y = offset_y
        self.sensor_rotation = sensor_rot
        self.sensor_range = 0
        self.sensor_x = 0
        self.sensor_y = 0

    def update_sensor(self):
        """ Calculates the XY position of the sensor origin based on the current position of the robot
            and then takes a reading """
        angle_radians = -math.radians(self.parent_robot.rotation)
        beam_angle = angle_radians + self.sensor_rotation
        beam_angle = src.util.wrap_angle(beam_angle)
        self.sensor_x = self.parent_robot.x + (
            self.sensor_offset_x * math.cos(angle_radians) - (self.sensor_offset_y * math.sin(angle_radians)))
        self.sensor_y = self.parent_robot.y + (
            self.sensor_offset_x * math.sin(angle_radians) + (self.sensor_offset_y * math.cos(angle_radians)))
        self.sensor_range = self.sensor.update_sonar(self.sensor_x, self.sensor_y, beam_angle)

    def get_distance(self):
        """ Returns the last reading taken by this sensor """
        return self.sensor_range

    def get_fixed_triggered(self, trigger_distance):
        """ Returns true is the last reading is less than or equal to trigger_distance """
        if self.sensor_range < trigger_distance:
            return True
        else:
            return False

    #def draw_sensor_position(self):
    #    """ Draws a circle at the origin of the sensor """
    #    src.util.circle(self.sensor_x, self.sensor_y, 5)

    def render(self):
        pygame.draw.circle(
            self.surface,
            (0, 255, 0),
            (int(self.sensor_x), int(self.sensor_y)),
            5,
            width=1
        )


class PanningDistanceSensor(src.sprites.basicsprite.BasicSprite):
    def __init__(self, *args, **kwargs):  # todo - fix this mess
        batch = kwargs.pop('batch')
        robot = kwargs.pop('robot')
        sonar_map = kwargs.pop('sonar_map')
        offset_x = kwargs.pop('offset_x')
        offset_y = kwargs.pop('offset_y')
        min_range = kwargs.pop('min_range')
        max_range = kwargs.pop('max_range')
        beam_angle = kwargs.pop('beam_angle')

        self.parent_robot = robot

        # x offset from ???? of actual sensor point
        self.sonar_offset_x = offset_x
        self.sonar_offset_y = offset_y
        
        self.sonar_angle_max = 90
        self.sonar_angle_min = -90
        self.sonar_angle = 0
        self.sonar_angle_target = 0
        self.sonar_sensor = Sonar(sonar_map, min_range, max_range, beam_angle)

        # centre point of sensor image sprite
        self.sensor_offset_x = self.width - 8
        self.sensor_offset_y = offset_y
        self.sonar_range = 0.0
        
        # ????
        self.sensor_x = 0
        self.sensor_y = 0

    def set_target(self, target):
        """Set the target angle for the panning sonar."""
        if target >= self.sonar_angle_max:
            self.sonar_angle_target = self.sonar_angle_max

        elif target <= self.sonar_angle_min:
            self.sonar_angle_target = self.sonar_angle_min

        else:
            self.sonar_angle_target = target

    def update_sensor(self):
        """Calculates the XY position of the sensor origin based on the current position of the robot and
            then takes a reading."""  
        angle_radians = -math.radians(self.rotation)
        self.sensor_x = self.parent_robot.x + (
            self.sonar_offset_x * math.cos(angle_radians) - (self.sonar_offset_y * math.sin(angle_radians)))
        self.sensor_y = self.parent_robot.y + (
            self.sonar_offset_x * math.sin(angle_radians) + (self.sonar_offset_y * math.cos(angle_radians)))

        self.sonar_range = self.sonar_sensor.update_sonar(self.sensor_x, self.sensor_y, angle_radians)

    def get_distance(self):
        """ Returns the last reading taken by this sensor """
        return self.sonar_range

    def update(self, dt):
        """ Updates the position of the sprite representing the panning servo head """
        angle_radians = -math.radians(self.parent_robot.rotation)
        self.sensor_x = self.parent_robot.x + (self.sensor_offset_x * math.cos(angle_radians))
        self.sensor_y = self.parent_robot.y + (self.sensor_offset_x * math.sin(angle_radians))
        self.x = self.sensor_x
        self.y = self.sensor_y

        # if (self.sonar_angle_target - self.sonar_angle) > 0:
        #     self.sonar_angle += 5
        # elif (self.sonar_angle_target - self.sonar_angle) < 0:
        #     self.sonar_angle -= 5
        if (self.sonar_angle_target - self.sonar_angle) > 0:
            if (self.sonar_angle_target - self.sonar_angle) > 5:
                self.sonar_angle += 5
            else:
                self.sonar_angle = self.sonar_angle_target
        elif (self.sonar_angle_target - self.sonar_angle) < 0:
            if (self.sonar_angle_target - self.sonar_angle) < -5:
                self.sonar_angle -= 5
            else:
                self.sonar_angle = self.sonar_angle_target
        self.rotation = self.parent_robot.rotation - self.sonar_angle
        self.update_sensor()


    def draw_sensor_position(self):
        """Draws a circle at the origin of the sensor."""
        src.util.circle(self.sensor_x, self.sensor_y, 5)
        
    def make_circle(self):
        verts = []
        for i in range(100):
            angle = math.radians(float(i)/100 * 360.0)
            x = 5*math.cos(angle) + self.sensor_x
            y = 5*math.sin(angle) + self.sensor_y
            verts += [x,y]
        outline_rep = self.parent_robot.batch.add(int(len(verts)/2), pyglet.gl.GL_POINTS, None,
        ('v2f', verts),
        ('c4B', (255, 255, 255, 255)*int(len(verts)/2)))
        """ return verts """
