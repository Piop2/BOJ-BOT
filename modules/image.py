import pygame.draw
import pygame.font
import pygame.image
import pygame.transform
from pygame import Surface

from boj.problem import Problem

SAVE_PATH = "temp/problem_thumbnail.png"
IMAGE_SIZE = (1280, 720)  # 720p
RANK_IMG_PATH = "resource/rank/{}.png"
FONT_FILE = "resource/font/BMJUA.ttf"

pygame.font.init()


def _get_rank_image(level):
    rank_image = pygame.image.load(RANK_IMG_PATH.format(level))
    scaled_image = pygame.transform.scale(rank_image, (200, 256))
    return scaled_image


def _get_id_image(problem_id):
    id_font = pygame.font.Font(FONT_FILE, 60)
    id_image = id_font.render(str(problem_id), True, (0, 0, 0))
    return id_image


def _get_title_image(problem_title):
    title_font = pygame.font.Font(FONT_FILE, 150)
    if title_font.size(problem_title)[0] > 930:
        title_font = pygame.font.Font(FONT_FILE, 100)

    title_image = title_font.render(problem_title, True, (0, 0, 0))
    return title_image


def _get_tag_image(problem_tags):
    tag_font = pygame.font.Font(FONT_FILE, 40)
    text = ""
    for i in range(1, len(problem_tags) + 1):
        text = " ".join([f"#{i}" for i in problem_tags[:i]])
        if tag_font.size(text)[0] > 930:
            text = f'{" ".join([f"#{i}" for i in problem_tags[:i - 1]])} ...'
            return tag_font.render(text, True, (100, 100, 100))
    return tag_font.render(text, True, (100, 100, 100))


def make_problem_thumbnail(problem: Problem):
    surf = Surface(IMAGE_SIZE)
    surf.fill((255, 255, 255))

    rank_image = _get_rank_image(level=problem.level)
    id_image = _get_id_image(problem_id=problem.id)
    title_image = _get_title_image(problem_title=problem.title)
    tag_image = _get_tag_image(problem_tags=problem.shorts)

    surf.blit(rank_image, (50, 170))
    surf.blit(id_image, (150 - (id_image.get_width() / 2), 90))
    surf.blit(title_image, (290, 258 - (title_image.get_height() / 2)))
    surf.blit(tag_image, (290, 470 - tag_image.get_height()))
    pygame.draw.line(surf, (0, 0, 0), (50, 480), (1230, 480), 5)
    pygame.image.save(surf, SAVE_PATH)
    return surf
