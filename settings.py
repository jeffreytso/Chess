import pygame
import visuals as vs
import sys
"""Contains the settings class."""

class Settings():
    """A class to store all settings for Chess."""
    def __init__(self):
        """Initializes the various settings for Chess."""

        # Size of a single square.
        self.SQUARE = 100

        # Creates a group to store all the pieces in play.
        self.pieces = pygame.sprite.Group()

        # Groups that stores images.
        self.dots = pygame.sprite.Group()
        self.square_backgrounds = pygame.sprite.Group()
        self.previous_move_bg = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        # Keeps track of the currently selected piece.
        self.selected_piece = None

        self.fenPosition = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.gameHistory = []

        for x in range(0, self.SQUARE * 8, self.SQUARE):
            for y in range(0, self.SQUARE * 8, self.SQUARE):
                self.square_backgrounds.add(vs.loadBackgroundSquare((x, y)))
                self.borders.add(vs.loadBorder((x, y)))

        
    def loadPosition(self, position):
        fullPos = position.split(' ')
        pos = fullPos[0]
        rows = pos.split('/')
        for i in range(8):
            ind = 1
            while ind <= 8:
                if rows[i][ind] == 



    def draw_screen(self, board, screen):
        """Draws and displays the board, images, and pieces."""
        screen.blit(board, board.get_rect())
        self.dots.draw(screen)
        self.square_backgrounds.draw(screen)
        self.previous_move_bg.draw(screen)
        self.borders.draw(screen)
        self.pieces.draw(screen)
        pygame.display.flip()

        

    def game_over(self, game_result, screen):
        """Prompts the user to either play again or quit."""
        background = pygame.Surface((self.SQUARE * 4, self.SQUARE * 4))
        background.fill((0, 128, 0))
        play_again = vs.Image("images/play_again.bmp")
        play_again.rect.center = (self.SQUARE * 4, self.SQUARE * 4.7)
        yes = vs.Image("images/yes.bmp")
        yes.rect.center = (self.SQUARE * 3.5, self.SQUARE * 5.5)
        no = vs.Image("images/no.bmp")
        no.rect.center = (self.SQUARE * 4.5, self.SQUARE * 5.5)

        IMG1_POS = (self.SQUARE * 4, self.SQUARE * 2.7)
        IMG2_POS = (self.SQUARE * 4, self.SQUARE * 3.7)

        if game_result == "Checkmate":
            img2 = vs.Image("images/by_checkmate.bmp")
            if self.p1s_turn:
                img1 = vs.Image("images/p2_wins.bmp")
            else:
                img1 = vs.Image("images/p1_wins.bmp")
        else:
            img1 = vs.Image("images/draw.bmp")
            if game_result == "Stalemate":
                img2 = vs.Image("images/stalemate.bmp")
            else:
                img2 = vs.Image("images/repetition.bmp")
        img1.rect.center = IMG1_POS
        img2.rect.center = IMG2_POS

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_r:
                        game_over = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if yes.rect.collidepoint(event.pos):
                        game_over = False
                    elif no.rect.collidepoint(event.pos):
                        sys.exit()
            screen.blit(background, (self.SQUARE * 2, self.SQUARE * 2))
            screen.blit(img1.image, img1.rect)
            screen.blit(img2.image, img2.rect)
            screen.blit(play_again.image, play_again.rect)
            screen.blit(yes.image, yes.rect)
            screen.blit(no.image, no.rect)
            pygame.display.flip()