import pygame.draw
import pygame.font
import pygame.image
import pygame.transform
from pygame import Surface

from boj.problem import Problem

SAVE_PATH = "temp/problem_thumbnail.png"
RANK_IMG_PATH = "resource/rank/{}.png"
FONT_FILE = "resource/font/BMJUA.ttf"

pygame.font.init()


def make_problem_thumbnail(problem: Problem):
    surf = Surface((1280, 720))
    surf.fill((255, 255, 255))
    rank_image = pygame.transform.scale(
        pygame.image.load(RANK_IMG_PATH.format(problem.level)),
        (200, 256)
    )
    id_font = pygame.font.Font(FONT_FILE, 60)
    id_text = id_font.render(str(problem.id), True, (0, 0, 0))

    title_font = pygame.font.Font(FONT_FILE, 150)
    title_text = title_font.render(problem.title, True, (0, 0, 0))

    tag_font = pygame.font.Font(FONT_FILE, 40)
    if len(problem.shorts) > 4:
        tag_str = f"{' '.join([f'#{i}' for i in problem.shorts[:4]])} ..."
    else:
        tag_str = " ".join([f'#{i}' for i in problem.shorts])
    tag_text = tag_font.render(tag_str, True, (100, 100, 100))

    surf.blit(rank_image, (50, 170))
    surf.blit(id_text, (150 - (id_text.get_width() / 2), 90))
    surf.blit(title_text, (290, 258 - (title_text.get_height() / 2)))
    surf.blit(tag_text, (290, 470 - tag_text.get_height()))
    pygame.draw.line(surf, (0, 0, 0), (50, 480), (1230, 480), 5)
    pygame.image.save(surf, SAVE_PATH)
    return surf

# if __name__ == '__main__':
#     make_problem_thumbnail(problem=Problem(10000, "TITLE", True, True, 0, 0, 0, []))
