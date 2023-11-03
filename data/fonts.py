import pygame

def getFont(font: str = "Assets/Baskic8.otf", size: int = 20) -> pygame.font.Font:
    pygame.font.init()
    pixelFont = pygame.font.Font(font, size)
    return pixelFont