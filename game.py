from board import Board
from pygame import (
    display,
    draw,
    event as pygame_event,
    font,
    init as pygame_init,
    mouse,
    MOUSEBUTTONUP as EVENT_MOUSEBUTTONUP,
    quit as pygame_quit,
    QUIT as EVENT_QUIT,
    Rect,
    time,
)
from utils import *
from winsound import Beep

pygame_init()

clock = time.Clock()
WIN = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Minesweeper")

def choose_option() -> int:
    run = True

    while run:
        clock.tick(FPS)

        buttons = get_buttons_from_drawn_homescreen()

        for event in pygame_event.get():
            if (event_type := event.type) == EVENT_QUIT:
                return -1 # Represents a quit signal instead of grid size
            
            if event_type == EVENT_MOUSEBUTTONUP:
                mouse_pos = mouse.get_pos()
                for button in buttons:
                    if button.collidepoint(mouse_pos):
                        run = False
                        break
            
        display.update()

    return buttons.index(button)


def draw_board(board: Board, tile_size: int):
    board_state = board.get_playable_board()

    for x in range(board.size):
        for y in range(board.size):
            tile = board_state[x][y]
            if tile == EMPTY:
                color = LIGHT_GRAY
            elif tile == MARKED:
                color = BEIGE
            elif tile == MINE:
                color = RED
            elif tile == POP:
                color = YELLOW
            elif tile == SAFE:
                color = DARK_GRAY
            else:
                text_font = font.SysFont("Sans Serif", tile_size)
                text_surface = text_font.render(str(tile), True, BLUE)

                WIN.blit(text_surface, (x*tile_size+tile_size//4, y*tile_size+tile_size//4))
                continue
            
            draw.rect(WIN, color, (x*tile_size, y*tile_size, tile_size-1, tile_size-1))


def game_over(board: Board):
    text_boldfont = font.SysFont("Corbel", 40, bold=True)

    if board.has_won():
        text_surface = text_boldfont.render("YOU'VE WON (you cheater).", True, WHITE)
    else:
        text_surface = text_boldfont.render("YOU'VE LOST SUCKER!", True, WHITE)
    text_surface2 = text_boldfont.render("Exit the game now.", True, WHITE)

    WIN.blit(text_surface, (WIDTH//5, HEIGHT//5))
    WIN.blit(text_surface2, (WIDTH//4, HEIGHT//4+20))

    Beep(500, 500)
    display.update()

    run = True

    while run:
        for event in pygame_event.get():
            if event.type == EVENT_QUIT:
                run = False
    
    pygame_quit()
        

def get_buttons_from_drawn_homescreen() -> tuple[Rect, Rect, Rect]:
    WIN.fill(DARK_GRAY)

    text_font = font.SysFont("Corbel", 35)
    text_font_bold = font.SysFont("Corbel", 35, bold=True)

    text = "Choose your settings"
    text_surface = text_font.render(text, True, WHITE)
    WIN.blit(text_surface, (150, 50)) # (150, 50) is the text position

    # Hard coded button positions are vertical with a padding of 20. i.e., button_width + 20
    button_1 = Rect((200, 110), HOMESCREEN_BUTTONS_SIZE)
    button_2 = Rect((200, 180), HOMESCREEN_BUTTONS_SIZE)
    button_3 = Rect((200, 250), HOMESCREEN_BUTTONS_SIZE)

    draw.rect(WIN, WHITE, button_1, border_radius=10)
    draw.rect(WIN, WHITE, button_2, border_radius=10)
    draw.rect(WIN, WHITE, button_3, border_radius=10)

    # Hover effect
    mouse_pos = mouse.get_pos()
    for button in [button_1, button_2, button_3]:
        if button.collidepoint(mouse_pos):
            button_color = (211, 211, 211)
            # Change the button color if the mouse is hovering over it
            draw.rect(WIN, button_color, button, border_radius=10)

    button_text_1 = "9x9"
    button_text_2 = "10x10"
    button_text_3 = "11x11"

    button_text_surface_1 = text_font_bold.render(button_text_1, True, BLACK)
    button_text_surface_2 = text_font_bold.render(button_text_2, True, BLACK)
    button_text_surface_3 = text_font_bold.render(button_text_3, True, BLACK)

    # Don't ask about the hard-coded button positions. Font is really annoying to work with.
    WIN.blit(button_text_surface_1, (275, 115))
    WIN.blit(button_text_surface_2, (260, 187))
    WIN.blit(button_text_surface_3, (260, 257))

    return (button_1, button_2, button_3)


def handle_click(mouse_pos: tuple[int, int], button: int, board: Board, tile_size: int):
    mouse_pos = mouse_pos[::-1]
    x, y = int(mouse_pos[0] // tile_size), int(mouse_pos[1] // tile_size)

    match button:
        case 1:
            if not board.move(x, y):
                Beep(5000, 150)
        case 3:
            if not board.move(x, y, True):
                Beep(5000, 150)
        case _:
            return


def run_game(grid_size:int):
    if grid_size == -1:
        pygame_quit()
        return
    
    WIN.fill(BLACK)

    grid_size += 9 # Index returns 0, 1 or 2 so +9 would make it better.
    game_board = Board(size=grid_size)
    tile_size = WIDTH//game_board.size

    run = True

    while run:
        clock.tick(FPS)

        #===============DONT EVEN ACCIDENTALLY DELETE==============
        # if game_board.is_gameover():
        #     game_over(game_board)
        #     return

        for event in pygame_event.get():
            if (event_type := event.type) == EVENT_QUIT:
                run = False
            if event_type == EVENT_MOUSEBUTTONUP:
                mouse_pos = mouse.get_pos()
                handle_click(mouse_pos, event.button, game_board, tile_size)
        
        draw_board(game_board, tile_size)
        display.update()
    
    pygame_quit()


if __name__ == "__main__":
    grid_size = choose_option()
    run_game(grid_size)
