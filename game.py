from board import Board
from engine import Engine
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

grid_size: int
board: Board

clock = time.Clock()
WIN = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Minesweeper")

def choose_option() -> (int, bool):
    is_checkbox_selected = False
    run = True

    while run:
        clock.tick(FPS)

        buttons, checkbox = draw_screen_and_get_buttons(is_checkbox_selected)

        for event in pygame_event.get():
            if (event_type := event.type) == EVENT_QUIT:
                return -1 # Represents a quit signal instead of grid size
            
            if event_type == EVENT_MOUSEBUTTONUP:
                mouse_pos = mouse.get_pos()

                for button in buttons:
                    if button.collidepoint(mouse_pos):
                        run = False
                        break
                
                if checkbox.collidepoint(mouse_pos):
                    is_checkbox_selected = not is_checkbox_selected
            
        display.update()

    return (
        buttons.index(button) + 9, # index+9 because the index would be in range [0, 2] but the sizes mentioned are [9, 11]
        is_checkbox_selected
    )


def draw_board(board: Board, tile_size: int):
    board_state = board.playable_board

    for i in range(board.size ** 2):
        tile = board_state[i]
        x = i % board.size
        y = i // board.size

        if tile == EMPTY:
            color = LIGHT_GRAY
        elif tile == FLAG:
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


def game_over(has_won: bool):
    text_boldfont = font.SysFont("Corbel", 40, bold=True)
    text_surface1 = text_boldfont.render("Exit the game now.", True, WHITE)

    if has_won:
        text_surface2 = text_boldfont.render("CONGRATS! YOU'VE WON.", True, WHITE)
    else:
        text_surface2 = text_boldfont.render("YOU'VE LOST SUCKER!", True, WHITE)

    WIN.blit(text_surface2, (WIDTH//5, HEIGHT//5))
    WIN.blit(text_surface1, (WIDTH//4, HEIGHT//4+20))

    Beep(500, 500)
    display.update()

    run = True

    while run:
        for event in pygame_event.get():
            if event.type == EVENT_QUIT:
                run = False
    
    pygame_quit()
        

def draw_screen_and_get_buttons(is_checkbox_selected) -> (tuple[Rect, Rect, Rect], Rect):
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
    checkbox = Rect((210, 320), (30, 30))
    checkbox_selected_box = Rect((215, 325), (20, 20))

    draw.rect(WIN, WHITE, button_1, border_radius=10)
    draw.rect(WIN, WHITE, button_2, border_radius=10)
    draw.rect(WIN, WHITE, button_3, border_radius=10)
    draw.rect(WIN, WHITE, checkbox, border_radius=5)
    draw.rect(WIN, BEIGE if is_checkbox_selected else WHITE, checkbox_selected_box, border_radius=5)

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
    ai_solver_text = "AI Player"

    button_text_surface_1 = text_font_bold.render(button_text_1, True, BLACK)
    button_text_surface_2 = text_font_bold.render(button_text_2, True, BLACK)
    button_text_surface_3 = text_font_bold.render(button_text_3, True, BLACK)
    ai_solver_button = text_font.render(ai_solver_text, True, WHITE)

    # Don't ask about the hard-coded button positions. Font is really annoying to work with.
    WIN.blit(button_text_surface_1, (275, 115))
    WIN.blit(button_text_surface_2, (260, 187))
    WIN.blit(button_text_surface_3, (260, 257))
    WIN.blit(ai_solver_button, (260, 318))

    return (button_1, button_2, button_3), checkbox


def handle_click(mouse_pos: tuple[int, int], button: int, board: Board, tile_size: int):
    x, y = int(mouse_pos[0] // tile_size), int(mouse_pos[1] // tile_size)
    pos = x + y*board.size

    match button:
        case 1:
            if not board.move(pos):
                Beep(5000, 150)
        case 3:
            if not board.move(pos, True):
                Beep(5000, 150)
        case _:
            return


def run_game(game_board: Board|None, use_engine: bool = False):
    if game_board is None:
        pygame_quit()
        return
    
    engine = Engine(game_board.playable_board, game_board.flags_remaining) if use_engine else None
    
    WIN.fill(BLACK)

    run = True
    tile_size = WIDTH//game_board.size

    while run:
        draw_board(game_board, tile_size)
        display.update()

        if engine is not None:
            move, is_flag = engine.best_move()

            game_board.move(move, is_flag)
            time.wait(100)
        else:
            clock.tick(FPS)
        
        for event in pygame_event.get():
            if (event_type := event.type) == EVENT_QUIT:
                run = False
                break
            elif event_type == EVENT_MOUSEBUTTONUP and engine is None:
                mouse_pos = mouse.get_pos()
                handle_click(mouse_pos, event.button, game_board, tile_size)

        if game_board.is_gameover():
            draw_board(game_board, tile_size)
            display.update()

            game_over(game_board.has_won())
            return
        
        if engine is not None:
            engine.update_board(game_board.playable_board, game_board.has_lost())
            engine.update_evaluation()

    pygame_quit()