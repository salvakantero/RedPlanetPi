
#===============================================================================
# MarqueeText class
#===============================================================================

import constants
from font import Font

class MarqueeText():
    def __init__(self, surface, x, y, speed, text):
        # attributes
        self.surface = surface    
        self.font = Font('images/fonts/small_font.png', constants.PALETTE['YELLOW'], True)
        self.x = x
        self.y = y  
        self.speed = speed
        self.text = text

    # update the xy position
    def update(self):
        self.x -= self.speed
        self.font.render(self.text, self.surface, (self.x, self.y))

# # marquee
# def marquee_text(mtext):
#     # Define el texto y la fuente
#     font = pygame.font.Font(None, 32)
#     text = font.render(mtext, True, (255, 255, 255))
#     # Calcula la posición inicial del texto
#     text_rect = text.get_rect(center=(720, 400))
#     # Bucle principal del juego
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         # Actualiza la posición del texto
#         text_rect.left -= 1
#         if text_rect.left < -text_rect.width:
#             text_rect.left = 720
#         # Dibuja el texto en la pantalla
#         screen.fill((0, 0, 0))
#         screen.blit(text, text_rect)
#         pygame.display.update()