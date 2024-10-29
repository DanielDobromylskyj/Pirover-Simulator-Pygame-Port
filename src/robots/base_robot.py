import pygame


class Robot:
    def __init__(self, x, y, rotation, image_path):
        self.position = [x, y]
        self.x = x
        self.y = y

        self.image = pygame.image.load(image_path)

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

    def set_position(self, x, y):
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
            dsq = (self.x - x) ** 2 + (self.y - y) ** 2
            # print dsq
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

    def collides_with(self, other_object, use_mouse=False):
        """Simple axis aligned bounding box collision detections to check if this sprite collides with another."""
        # AABB collision detection
        if use_mouse:
            if self.mouse_target_x < other_object.x + other_object.width and \
                    self.mouse_target_x + self.image.get_width() > other_object.x and \
                    self.mouse_target_y < other_object.y + other_object.height and \
                    self.image.get_height() + self.mouse_target_y > other_object.y:
                return True
        else:
            if self.x < other_object.x + other_object.width and \
                    self.x + self.image.get_width() > other_object.x and \
                    self.y < other_object.y + other_object.height and \
                    self.image.get_height() + self.y > other_object.y:
                return True
        return False
