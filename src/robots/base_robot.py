import pygame
import numpy as np


class Robot:
    def __init__(self, x, y, rotation, image_path):
        self.position = [x, y]
        self.x = x
        self.y = y

        self.image = pygame.image.load(image_path)
        self.static_objects = []

        self.rotation = rotation

        self.mouse_move_state = False
        self.min_rad_sq = (0.5 * min(self.image.get_width(), self.image.get_height())) ** 2
        self.in_collision = False
        self.prev_x = x
        self.prev_y = y
        self.mouse_target_x = x
        self.mouse_target_y = y
        self.is_rotating = False
        self.receiving_light_focus = False

    def set_position(self, x=None, y=None):
        if x is not None:
            self.x = x
            self.position[0] = x

        if y is not None:
            self.y = y
            self.position[1] = y

    def on_mouse_press(self, x, y, button, modifiers):
        """Uses a radius check to see if the sprite has been clicked, then sets the mouse move state to True so the
        sprite can be moved using the mouse."""

        if button == 1:
            if 0 < (x - self.x) < self.image.get_width():
                if 0 < (y - self.y) < self.image.get_height():
                    self.mouse_move_state = True

    def on_mouse_release(self, x, y, button, modifiers):
        """Sets the mouse move state to false once the mouse button is released."""
        self.mouse_move_state = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Sets target x,y position for the sprite based on the mouse pointer."""
        if self.mouse_move_state:
            self.mouse_target_x = x
            self.mouse_target_y = y

    def __robot_collides_with_object(self, x, y, rotation, static_object):
        return self.check_overlap(
            (x, y, self.image.get_width(), self.image.get_height(), rotation),
            (static_object.x, static_object.y, static_object.image.get_width(), static_object.image.get_height(),
             static_object.rotation),
        )

    def robot_collides_with_object(self, x, y, rotation):  # todo - make it only check "close" static objects
        for static_object in self.static_objects:
            if self.__robot_collides_with_object(x, y, rotation, static_object):
                return True
        return False

    def update_position(self, dt):  # todo - Maybe make it so it "bounces" of walls slightly (or rotate)
        target_pos = float(self.position[0]) + (self.velocity_x * dt), float(self.position[1]) + (self.velocity_y * dt)

        if not self.robot_collides_with_object(target_pos[0], target_pos[1], self.rotation):
            self.set_position(target_pos[0], target_pos[1])

        else:  # if target position is NOT available, try to move each axis individually
            if not self.robot_collides_with_object(target_pos[0], self.y, self.rotation):
                self.set_position(x=target_pos[0])
            else:
                self.velocity_x = 0

            if not self.robot_collides_with_object(self.x, target_pos[1], self.rotation):
                self.set_position(y=target_pos[1])
            else:
                self.velocity_y = 0

    def update_rotation(self, dt):  # todo - maybe add a sorta "reaction" force if it is colliding with a object?
        target_rotation = float(self.rotation) - (self.vth * dt)

        if not self.robot_collides_with_object(self.x, self.y, target_rotation):
            self.rotation = target_rotation

    @staticmethod
    def get_corners(x, y, width, height, angle):
        cx, cy = x + width / 2, y + height / 2

        corners = [
            (-width / 2, -height / 2),
            (width / 2, -height / 2),
            (width / 2, height / 2),
            (-width / 2, height / 2)
        ]

        # Rotation matrix
        rad = np.deg2rad(angle)
        rotation_matrix = np.array([
            [np.cos(rad), -np.sin(rad)],
            [np.sin(rad), np.cos(rad)]
        ])

        rotated_corners = []
        for corner in corners:
            rotated = rotation_matrix @ np.array(corner)  # Rotate point
            rotated_corners.append((rotated[0] + cx, rotated[1] + cy))  # Translate to actual position

        return rotated_corners

    @staticmethod
    def project(corners, axis):
        projections = [np.dot(corner, axis) for corner in corners]
        return min(projections), max(projections)

    def overlap_on_axis(self, corners1, corners2, axis):
        min1, max1 = self.project(corners1, axis)
        min2, max2 = self.project(corners2, axis)
        return max1 >= min2 and max2 >= min1

    def check_overlap(self, box1, box2):
        x1, y1, w1, h1, angle1 = box1
        x2, y2, w2, h2, angle2 = box2

        # Get corners of both rectangles
        corners1 = self.get_corners(x1, y1, w1, h1, angle1)
        corners2 = self.get_corners(x2, y2, w2, h2, angle2)

        edges = []
        for i in range(4):
            edge1 = np.subtract(corners1[i], corners1[(i + 1) % 4])
            edge2 = np.subtract(corners2[i], corners2[(i + 1) % 4])
            edges.append(np.array([-edge1[1], edge1[0]]))
            edges.append(np.array([-edge2[1], edge2[0]]))

        for axis in edges:
            axis = axis / np.linalg.norm(axis)  # Normalize the axis
            if not self.overlap_on_axis(corners1, corners2, axis):
                return False

        return True
