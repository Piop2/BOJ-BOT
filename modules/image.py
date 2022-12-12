import pygame.draw
import pygame.font
import pygame.image
import pygame.transform
from pygame import Surface

from boj.problem import Problem

SAVE_PATH = "temp/problem_thumbnail.png"

pygame.font.init()


def make_problem_thumbnail(problem: Problem):
    surf = Surface((1280, 720))
    surf.fill((255, 255, 255))
    rank_image = pygame.transform.scale(
        pygame.image.load("resource/rank/0.png"),
        (200, 256)
    )
    id_font = pygame.font.SysFont(name="malgungothic", size=60, bold=True)
    id_text = id_font.render(str(problem.id), True, (0, 0, 0))
    title_font = pygame.font.SysFont(name="malgungothic", size=210, bold=True)
    title_text = title_font.render(problem.title, True, (0, 0, 0))

    surf.blit(rank_image, (50, 170))
    surf.blit(id_text, (150 - (id_text.get_width() / 2), 90))
    surf.blit(title_text, (300, 298 - (title_text.get_height() / 2)))
    pygame.draw.line(surf, (0, 0, 0), (50, 450), (1230, 450), 5)
    pygame.image.save(surf, SAVE_PATH)
    return surf


# if __name__ == '__main__':
#     make_problem_thumbnail(problem=Problem(10000, "TITLE", True, True, 0, 0, 0, []))
