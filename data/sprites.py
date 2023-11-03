import pygame

class TilePiece(pygame.sprite.Sprite):
    
    def __init__(self, sprites: list, pos_x: float, pos_y: float, scale: int) -> None:
        super().__init__()
        self.is_animating = True
        self.sprites = self.scaleSprites(sprites, scale)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self) -> None:
        if self.is_animating:
            
            self.current_sprite += 0.5

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = len(self.sprites) - 1
                self.is_animating = False
            
            self.image = self.sprites[int(self.current_sprite)]

    def scaleSprites(self, objsToScale: list, scaleAmount: int) -> list:
        scaledObjs = []
        for obj in objsToScale:
            obj = pygame.transform.scale(obj, (obj.get_width() * scaleAmount, obj.get_height() * scaleAmount))
            scaledObjs.append(obj)
        return scaledObjs


class PopUp(TilePiece):
    
    def __init__(self, sprites: list, pos_x: float, pos_y: float, scale: int) -> None:
        super().__init__(sprites, pos_x, pos_y, scale)

    def update(self) -> None:
        return super().update()
    
    def scaleSprites(self, objsToScale: list, scaleAmount: int) -> list:
        return super().scaleSprites(objsToScale, scaleAmount)
    
class Button(TilePiece):

    def __init__(self, sprites: list, pos_x: float, pos_y: float, scale: int) -> None:
        super().__init__(sprites, pos_x, pos_y, scale)
        self.is_animating = False

    def update(self) -> None:
        if self.is_animating:
            
            self.current_sprite += 1

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            
            self.image = self.sprites[int(self.current_sprite)]

    def scaleSprites(self, objsToScale: list, scaleAmount: int) -> list:
        return super().scaleSprites(objsToScale, scaleAmount)
    
class Cursor(pygame.sprite.Sprite):
    def __init__(self, sprites: list, scale: int) -> None:
        super().__init__()
        self.sprites = self.scaleSprites(sprites, scale)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        pos_x, pos_y = pygame.mouse.get_pos()
        self.rect.topleft = [pos_x, pos_y]

    def update(self, events) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.current_sprite = 1
            if event.type == pygame.MOUSEBUTTONUP:
                self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        pos_x, pos_y = pygame.mouse.get_pos()
        self.rect.topleft = [pos_x, pos_y]

    def scaleSprites(self, objsToScale: list, scaleAmount: int) -> list:
        scaledObjs = []
        for obj in objsToScale:
            obj = pygame.transform.scale(obj, (obj.get_width() * scaleAmount, obj.get_height() * scaleAmount))
            scaledObjs.append(obj)
        return scaledObjs