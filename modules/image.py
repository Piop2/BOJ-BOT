import pygame.draw
import pygame.font
import pygame.image
import pygame.transform
from pygame import Surface

from boj.problem import Problem

SAVE_PATH = "temp/problem_thumbnail.png"

pygame.font.init()


def make_problem_thumbnail():
    surf = Surface((1280, 720))
    surf.fill((255, 255, 255))
    rank_image = pygame.transform.scale(
        pygame.image.load("resource/rank/0.png"),
        (200, 256)
    )
    font = pygame.font.SysFont(name="arial", size=200, bold=True)
    text = font.render("ID. TITLE", True, (0, 0, 0))
    pygame.draw.rect(surface=surf, color=(0, 0, 0), rect=(0, 0, *surf.get_size()), width=1)
    surf.blit(rank_image, (50, 100))
    surf.blit(text, (280, 228 - (text.get_height() / 2)))
    pygame.image.save(surf, SAVE_PATH)
    return surf


if __name__ == '__main__':
    make_problem_thumbnail()
