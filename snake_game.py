import pygame
import random
import os
import json
from enum import Enum
from collections import deque


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Difficulty(Enum):
    EASY = 5
    MEDIUM = 10
    HARD = 15


class GameState(Enum):
    MENU = 1
    DIFFICULTY_SELECT = 2
    PLAYING = 3
    GAME_OVER = 4


class SnakeGame:
    GRID_SIZE = 20
    CELL_SIZE = 30
    WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
    WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE
    FPS = 60
    HIGH_SCORE_FILE = "highscore.json"

    COLORS = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "dark_green": (0, 180, 0),
        "yellow": (255, 255, 0),
        "gray": (128, 128, 128),
        "light_gray": (200, 200, 200),
    }

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.state = GameState.MENU
        self.difficulty = Difficulty.MEDIUM
        self.high_score = self.load_high_score()
        self.reset_game()

    def reset_game(self):
        """Initialize or reset game variables."""
        self.snake = deque()
        start_x = self.GRID_SIZE // 2
        start_y = self.GRID_SIZE // 2

        self.snake.append((start_x, start_y))
        self.snake.append((start_x - 1, start_y))
        self.snake.append((start_x - 2, start_y))

        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.food_pos = self.spawn_food()
        self.move_counter = 0

    def spawn_food(self):
        """Spawn food at a random location not occupied by snake."""
        while True:
            x = random.randint(0, self.GRID_SIZE - 1)
            y = random.randint(0, self.GRID_SIZE - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def load_high_score(self):
        """Load high score from file."""
        if os.path.exists(self.HIGH_SCORE_FILE):
            try:
                with open(self.HIGH_SCORE_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            except Exception:
                return 0
        return 0

    def save_high_score(self):
        """Save high score to file."""
        with open(self.HIGH_SCORE_FILE, "w") as f:
            json.dump({"high_score": self.high_score}, f)

    def handle_input(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_s:
                        self.state = GameState.DIFFICULTY_SELECT
                    elif event.key == pygame.K_q:
                        return False

                elif self.state == GameState.DIFFICULTY_SELECT:
                    if event.key == pygame.K_1:
                        self.difficulty = Difficulty.EASY
                        self.start_game()
                    elif event.key == pygame.K_2:
                        self.difficulty = Difficulty.MEDIUM
                        self.start_game()
                    elif event.key == pygame.K_3:
                        self.difficulty = Difficulty.HARD
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.direction != Direction.DOWN:
                            self.next_direction = Direction.UP
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.direction != Direction.UP:
                            self.next_direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.direction != Direction.RIGHT:
                            self.next_direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.direction != Direction.LEFT:
                            self.next_direction = Direction.RIGHT

                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.state = GameState.DIFFICULTY_SELECT
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

        return True

    def start_game(self):
        """Start the game."""
        self.reset_game()
        self.state = GameState.PLAYING

    def update(self):
        """Update game logic."""
        if self.state != GameState.PLAYING:
            return

        self.move_counter += 1
        moves_per_frame = self.difficulty.value

        if self.move_counter >= (self.FPS // moves_per_frame):
            self.move_counter = 0
            self.direction = self.next_direction

            head_x, head_y = self.snake[0]
            dx, dy = self.direction.value
            new_head = (head_x + dx, head_y + dy)

            if self.check_collision(new_head):
                self.end_game()
                return

            self.snake.appendleft(new_head)

            if new_head == self.food_pos:
                self.score += 1
                self.food_pos = self.spawn_food()

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
            else:
                self.snake.pop()

    def check_collision(self, pos):
        """Check if position collides with walls or snake body."""
        x, y = pos

        if x < 0 or x >= self.GRID_SIZE or y < 0 or y >= self.GRID_SIZE:
            return True

        if pos in self.snake:
            return True

        return False

    def end_game(self):
        """End the game and go to game over screen."""
        self.state = GameState.GAME_OVER

    def draw(self):
        """Draw the current game state."""
        self.screen.fill(self.COLORS["black"])

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.DIFFICULTY_SELECT:
            self.draw_difficulty_select()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        """Draw the main menu."""
        title = self.font_large.render("SNAKE", True, self.COLORS["green"])
        title_rect = title.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 100)
        )
        self.screen.blit(title, title_rect)

        start_text = self.font_small.render("Press S to Start", True, self.COLORS["white"])
        start_rect = start_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        )
        self.screen.blit(start_text, start_rect)

        quit_text = self.font_small.render("Press Q to Quit", True, self.COLORS["white"])
        quit_rect = quit_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 80)
        )
        self.screen.blit(quit_text, quit_rect)

        high_score_text = self.font_small.render(
            f"High Score: {self.high_score}", True, self.COLORS["yellow"]
        )
        high_score_rect = high_score_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT - 50)
        )
        self.screen.blit(high_score_text, high_score_rect)

    def draw_difficulty_select(self):
        """Draw the difficulty selection screen."""
        title = self.font_large.render("SELECT DIFFICULTY", True, self.COLORS["green"])
        title_rect = title.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 120)
        )
        self.screen.blit(title, title_rect)

        easy_text = self.font_small.render("1 - Easy", True, self.COLORS["white"])
        easy_rect = easy_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 20)
        )
        self.screen.blit(easy_text, easy_rect)

        medium_text = self.font_small.render("2 - Medium", True, self.COLORS["white"])
        medium_rect = medium_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 40)
        )
        self.screen.blit(medium_text, medium_rect)

        hard_text = self.font_small.render("3 - Hard", True, self.COLORS["white"])
        hard_rect = hard_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 100)
        )
        self.screen.blit(hard_text, hard_rect)

        esc_text = self.font_small.render("ESC - Back to Menu", True, self.COLORS["gray"])
        esc_rect = esc_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT - 50)
        )
        self.screen.blit(esc_text, esc_rect)

    def draw_game(self):
        """Draw the game board, snake, and food."""
        self.draw_grid()
        self.draw_snake()
        self.draw_food()
        self.draw_score()

    def draw_grid(self):
        """Draw the game grid."""
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                rect = pygame.Rect(
                    x * self.CELL_SIZE,
                    y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                )
                pygame.draw.rect(self.screen, self.COLORS["gray"], rect, 1)

    def draw_snake(self):
        """Draw the snake."""
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(
                x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE
            )
            if i == 0:
                pygame.draw.rect(self.screen, self.COLORS["green"], rect)
            else:
                pygame.draw.rect(self.screen, self.COLORS["dark_green"], rect)
            pygame.draw.rect(self.screen, self.COLORS["white"], rect, 2)

    def draw_food(self):
        """Draw the food."""
        x, y = self.food_pos
        rect = pygame.Rect(
            x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE
        )
        pygame.draw.rect(self.screen, self.COLORS["red"], rect)
        pygame.draw.rect(self.screen, self.COLORS["yellow"], rect, 2)

    def draw_score(self):
        """Draw the current score on the game board."""
        score_text = self.font_small.render(
            f"Score: {self.score}", True, self.COLORS["white"]
        )
        score_rect = score_text.get_rect(topleft=(10, 10))
        self.screen.blit(score_text, score_rect)

        high_score_text = self.font_small.render(
            f"High Score: {self.high_score}", True, self.COLORS["yellow"]
        )
        high_score_rect = high_score_text.get_rect(
            topright=(self.WINDOW_WIDTH - 10, 10)
        )
        self.screen.blit(high_score_text, high_score_rect)

    def draw_game_over(self):
        """Draw the game over screen."""
        self.draw_game()

        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(self.COLORS["black"])
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font_large.render("GAME OVER", True, self.COLORS["red"])
        game_over_rect = game_over_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 80)
        )
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = self.font_medium.render(
            f"Score: {self.score}", True, self.COLORS["white"]
        )
        final_score_rect = final_score_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
        )
        self.screen.blit(final_score_text, final_score_rect)

        high_score_display = self.font_medium.render(
            f"High Score: {self.high_score}", True, self.COLORS["yellow"]
        )
        high_score_display_rect = high_score_display.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 60)
        )
        self.screen.blit(high_score_display, high_score_display_rect)

        restart_text = self.font_small.render("Press R to Restart", True, self.COLORS["white"])
        restart_rect = restart_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 140)
        )
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font_small.render("Press Q or ESC to Quit", True, self.COLORS["white"])
        quit_rect = quit_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 190)
        )
        self.screen.blit(quit_text, quit_rect)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

        pygame.quit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
