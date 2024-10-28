import pygame

pygame.init()


class Simulator:
    def __init__(self, world_file="default.xml", selected_robot="Initio", window_size=None):
        if window_size is None:
            window_size = pygame.display.get_surface().get_size()

        self.window = pygame.display.set_mode(window_size)
        self.running = False

    def render(self):
        pass

    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        self.close()

    def close(self):
        pygame.quit()
