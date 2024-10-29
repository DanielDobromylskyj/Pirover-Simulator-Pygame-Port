import pygame

from src.robots.initio import Initio
from src.world import World, get_window_size

pygame.init()


class Simulator:
    def __init__(self, world_file="default.xml", selected_robot="Initio", window_size=None, target_fps=60):
        if window_size is None:
            window_size = get_window_size(world_file)

        self.window = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()

        self.running = False
        self.target_fps = target_fps

        self.world = World(self.window, world_file)
        self.robot = self.load_robot(selected_robot)

    def load_robot(self, selected):
        match selected:
            case "Initio":
                return Initio(
                    self.window,
                    self.world.sonar_map,
                    self.world.line_map_sprite,
                    self.world.static_objects,
                    self.window.get_width(),
                    self.window.get_height()
                )

            case "Pi2Go":
                raise NotImplementedError("Pi2Go is not implemented yet")

            case _:
                raise NameError(f"No Robot With Name '{selected}'")

    def render(self):
        self.world.render()
        self.robot.render()

    def update(self, delta_time):
        self.robot.update(delta_time, self)

    def run(self):
        self.running = True
        self.clock.tick(self.target_fps)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.robot.on_mouse_press(event.pos[0], event.pos[1], event.button, None)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.robot.on_mouse_release(event.pos[0], event.pos[1], event.button, None)

                elif event.type == pygame.MOUSEMOTION:
                    self.robot.on_mouse_drag(event.pos[0], event.pos[1], event.rel[0], event.rel[1], event.buttons, None)



            self.update(self.clock.get_time() * 1000)
            self.render()
            pygame.display.flip()
            self.clock.tick(self.target_fps)

        self.close()

    def close(self):
        pygame.quit()
