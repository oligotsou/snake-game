
import pygame
import random
import sys

CELL        = 40
COLS, ROWS  = 30, 30
WIDTH       = COLS * CELL
HEIGHT      = ROWS * CELL + 60
FPS         = 10

BG          = (15,  15,  30)
GRID        = (25,  25,  45)
SNAKE_HEAD  = (0,   230, 118)
SNAKE_BODY  = (0,   180,  80)
FOOD_COL    = (255,  70,  70)
TEXT_COL    = (220, 220, 220)
OVER_COL    = (255,  70,  70)
BORDER      = (40,  40,  70)

def random_food(snake):
    while True:
        pos = [random.randint(0, COLS - 1), random.randint(0, ROWS - 1)]
        if pos not in snake:
            return pos

def draw_cell(surface, col, row, color, shrink=2):
    rect = pygame.Rect(col * CELL + shrink, row * CELL + shrink,
                       CELL - shrink * 2, CELL - shrink * 2)
    pygame.draw.rect(surface, color, rect, border_radius=4)

def main():
    pygame.init()
    screen  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock   = pygame.time.Clock()
    font_lg = pygame.font.SysFont("consolas", 36, bold=True)
    font_sm = pygame.font.SysFont("consolas", 22)

    def reset():
        snake     = [[COLS // 2, ROWS // 2],
                     [COLS // 2 - 1, ROWS // 2],
                     [COLS // 2 - 2, ROWS // 2]]
        direction = [1, 0]
        food      = random_food(snake)
        return snake, direction, food, 0

    snake, direction, food, score = reset()
    high_score = 0
    game_over  = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key in (pygame.K_r, pygame.K_RETURN):
                        snake, direction, food, score = reset()
                        game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                else:
                    if event.key == pygame.K_UP    and direction != [0,  1]: direction = [0, -1]
                    if event.key == pygame.K_DOWN  and direction != [0, -1]: direction = [0,  1]
                    if event.key == pygame.K_LEFT  and direction != [1,  0]: direction = [-1, 0]
                    if event.key == pygame.K_RIGHT and direction != [-1, 0]: direction = [1,  0]
                    if event.key == pygame.K_w and direction != [0,  1]: direction = [0, -1]
                    if event.key == pygame.K_s and direction != [0, -1]: direction = [0,  1]
                    if event.key == pygame.K_a and direction != [1,  0]: direction = [-1, 0]
                    if event.key == pygame.K_d and direction != [-1, 0]: direction = [1,  0]

        if not game_over:
            head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
            if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
                game_over = True
            elif head in snake:
                game_over = True
            else:
                snake.insert(0, head)
                if head == food:
                    score += 1
                    high_score = max(high_score, score)
                    food = random_food(snake)
                else:
                    snake.pop()

        screen.fill(BG)
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(screen, GRID, pygame.Rect(c*CELL, r*CELL, CELL, CELL), 1)
        pygame.draw.rect(screen, BORDER, (0, 0, WIDTH, ROWS * CELL), 2)
        draw_cell(screen, food[0], food[1], FOOD_COL, shrink=3)
        for i, seg in enumerate(snake):
            draw_cell(screen, seg[0], seg[1], SNAKE_HEAD if i == 0 else SNAKE_BODY,
                      shrink=1 if i == 0 else 2)
        bar_y = ROWS * CELL
        pygame.draw.rect(screen, (20, 20, 40), (0, bar_y, WIDTH, 60))
        screen.blit(font_sm.render(f"Score: {score}   Best: {high_score}", True, TEXT_COL), (12, bar_y + 18))
        ctrl = font_sm.render("Arrow Keys / WASD", True, (100, 100, 140))
        screen.blit(ctrl, (WIDTH - ctrl.get_width() - 12, bar_y + 18))

        if game_over:
            overlay = pygame.Surface((WIDTH, ROWS * CELL), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            go = font_lg.render("GAME OVER", True, OVER_COL)
            screen.blit(go, (WIDTH//2 - go.get_width()//2, ROWS*CELL//2 - 50))
            sc = font_sm.render(f"Score: {score}", True, TEXT_COL)
            screen.blit(sc, (WIDTH//2 - sc.get_width()//2, ROWS*CELL//2))
            re = font_sm.render("R / ENTER to restart  |  ESC to quit", True, (160,160,200))
            screen.blit(re, (WIDTH//2 - re.get_width()//2, ROWS*CELL//2 + 40))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
