import xml.etree.ElementTree as ET
import pygame
import math

from src.sensors.sonar import Map
from src.sensors.linesensor import LineMapData

NUM_LINE_MAPS = 10
NUM_BACKGROUNDS = 4


def load_image_grid(path, rows, columns):
    image = pygame.image.load(path)
    return [
        image.subsurface((
            math.floor(x * (image.get_width() / columns)),
            math.floor(y * (image.get_height() / rows)),
            image.get_width() // columns,
            image.get_height() // rows
        )).copy() for x in range(columns) for y in range(rows)
    ]


image_grid = load_image_grid("resources/static_objects/boxesv2.png", 1, 9)

# todo - Make the line maps and backgrounds load from os.listdir()
line_maps = [
    pygame.image.load("resources/line_maps/map" + str(i) + ".png")
    for i in range(NUM_LINE_MAPS)
]

# Load all available backgrounds
backgrounds = [
    pygame.image.load("resources/backgrounds/bg" + str(i) + ".png")
    for i in range(NUM_BACKGROUNDS)
]


def get_window_size(world_file):
    root = ET.parse(f"worlds/{world_file}").getroot()

    background_image_idx = int(root.attrib['background_index'])
    if 0 <= background_image_idx < len(backgrounds):
        return int(root.attrib['width']), int(root.attrib['height'])

    return pygame.display.get_desktop_sizes()[0]  # last resort


class WorldObject:
    def __init__(self, image, x, y, object_type, index):
        self.image = image
        self.x = x
        self.y = y
        self.object_type = object_type
        self.index = index


class World:
    def __init__(self, surface, world_file):
        self.root = ET.parse(f"worlds/{world_file}").getroot()
        self.surface = surface

        self.sonar_resolution = int(self.root.attrib['sonar_resolution'])
        self.sonar_map = Map(self.surface, self.sonar_resolution)

        self.line_map_position = [0, 0]
        self.line_map_sprite = None

        self.static_objects = []

        background_image_idx = int(self.root.attrib['background_index'])
        if 0 <= background_image_idx < len(backgrounds):
            self.background_image = backgrounds[background_image_idx]

        for child in self.root:
            if child.tag == "robot":  # Load Position And Rotation Of Robot
                self.robot_position = [int(child.attrib["position_x"]), int(child.attrib["position_y"])]
                self.robot_rotation = int(child.attrib["rotation"])
            elif child.tag == "line_map":  # Load Line Map
                line_map_index = int(child.attrib['index'])
                if 0 <= line_map_index < len(line_maps):
                    self.line_map_position = [int(child.attrib['position_x']), int(child.attrib['position_y'])]
                    self.line_map_sprite = LineMapData(line_maps[line_map_index], self.line_map_position, 0)
            elif child.tag == "static_object":  # Load Static Object (And Sonar Map)
                index = int(child.attrib['index'])
                if 0 <= index < len(image_grid):
                    x = int(child.attrib['position_x'])
                    y = int(child.attrib['position_y'])
                    self.sonar_map.insert_rectangle(x, y, image_grid[index].get_width(), image_grid[index].get_height())

                    self.static_objects.append(
                        WorldObject(image_grid[index], x, y, "object", index)
                    )

    def render(self):
        self.surface.blit(self.background_image, (0, 0))

        for static_object in self.static_objects:
            self.surface.blit(static_object.image, (static_object.x, static_object.y))
