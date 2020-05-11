import random
import pygame

pygame.font.init()

s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30
score = 0

top_left_x = (s_width - play_width) // 2  # starting points of playing table
top_left_y = s_height - play_height

surface = pygame.display.set_mode((s_width, s_height))

# create lists of shapes

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# make lists of shapes and their corresponding colors
shapes = [T, Z, S, O, L, I, J]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape

# create class for every shape
class Piece(object):
    rows = 20
    columns = 10

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
    '''the first for statement will draw a row of 10 boxes with black color
       and the next for statement will create 20 rows of those 10 box row'''
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            for (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


# create function to draw shape on surface by using normal shapes list
def convert_shape(shape):
    '''the logic behind it:
     if you print i u will get i= index number of each row in one shape's list
      which are equivalent to number of elements like 0th,1st,2nd,3rd row
      while "line" will give you the actual row corresponding to that index number (which is i)
      eg. ['0000.'] for 2nd row having index value 0 in I shape and so on'''
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            '''here j is index number of columns in one shapes list and column will give you each column'''
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  # we subtract 2 and 4 to initialize shape in center
    return positions


# def valid space for every shape
def playing_area(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape(shape)

    for position in formatted:
        if position not in accepted_pos:
            if position[1] > -1:
                return False
    return True


# define function to ove the game once position of shape goes aout of y range
def game_over(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# get shape on playing area
def get_shape():
    return Piece(5, 0, random.choice(shapes))


# make extra function for some labels to make length of code less
def display_text(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - (label.get_width() / 2)))


# define a function to draw lines to separate each block in playing area
def grey_lines(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (50,50,50), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (50,50,50), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


# delete the whole row when the row is completely filled with colors
def clear_rows(grid, locked):
    inc = 0
    global score
    for i in range((len(grid) - 1), -1, -1):
        if (0, 0, 0) not in grid[i]:
            '''when there is no black color in grid list then
            delete the respective list which will eventually delete the whole row'''
            inc += 1
            ind = i
            for j in range(len(grid[i])):
                try:
                    del locked[(j, i)]
                    score += 1
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            '''if the row gets deleted the new row will get added and 
                the row which is above the deleted row will shift below'''
            x, y = key
            if y < ind:
                newkey = (x, y + inc)
                locked[newkey] = locked.pop(key)


# This function is going to display the next falling shape on the right side of the screen.
def next_shape(shape, surface):
    # logic is same as 'convert_shape()' function
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next shape', 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)
    surface.blit(label, (sx + 10, sy - 30))


# function to showcase scoreboard
def scoreboard():
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score', 1, (255, 255, 255))
    label2 = font.render(f'{score}', 1, (255, 255, 255))
    sx = top_left_x + play_width - 450
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx + 10, sy - 30))
    surface.blit(label2, (sx + 30, sy))


# def function to display heading, make red color around playing_area
def playing_screen(surface, grid):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 80,bold=TabError)
    label = font.render('TETRIS', 1, (0, 255, 0))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (0, 255, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    grey_lines(surface, grid)  # call grey_lines to draw grey lines in playing area


# main game loop
def main(surface):
    locked_pos = {}
    grid = create_grid(locked_pos)
    change_piece = False  # assign it to false to avoid more than one shapes to come at a time
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()

        # logic to make shape fall vertically
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1

            # logic to stop shape at bottom and send new pies from top by assigning change_piece to True
            if not (playing_area(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # assign keys for movements
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not playing_area(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not playing_area(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not playing_area(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not playing_area(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape(current_piece)  # shape_pos=position of current shape (x,y)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_pos)

        playing_screen(surface, grid)
        scoreboard()
        next_shape(next_piece, surface)
        pygame.display.update()
        if game_over(locked_pos):
            display_text('Game Over', 80, (255, 255, 255), surface)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
    pygame.display.quit()


# function for main menu
def main_menu(surface):
    run = True
    while run:
        surface.fill((0, 0, 0))
        display_text('Press Enter to play.', 80, (255, 255, 255), surface)
        font = pygame.font.SysFont('comicsans', 200, bold=True)
        label = font.render("TETRIS", 1, (0, 255, 0))
        surface.blit(label, (
            top_left_x + play_width / 2 - (label.get_width() / 2), s_height // 3))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main(surface)
        pygame.display.update()

main_menu(surface)  # start game
