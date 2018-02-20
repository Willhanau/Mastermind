#Author: William Hanau
#Date: 12-3-16
#Updated Version(v2.0) of my MasterMind python game

from graphics import *
import random

G_WINDOW_WIDTH = 360
G_WINDOW_HEIGHT = 700
LEFTMOST_X = 50
CIRCLE_RADIUS = 20
CIRCLE_DIAMETER = CIRCLE_RADIUS * 2
H_CIRCLE_SPACING = 5
V_CIRCLE_SPACING = 10
PALETTE_X = LEFTMOST_X + CIRCLE_RADIUS
PALETTE_Y = G_WINDOW_HEIGHT - 50
PALETTE_COLORS = ['green', 'orange', 'darkblue', 'yellow', 'darkred', 'lightblue']
BLANK_COLORS = ['white', 'white', 'white', 'white']
EXIT_X = 30
EXIT_Y = 30
STATE_X = G_WINDOW_WIDTH - CIRCLE_RADIUS
STATE_Y = EXIT_Y
GUESS_X = LEFTMOST_X + CIRCLE_RADIUS + H_CIRCLE_SPACING
GUESS_Y = PALETTE_Y - 100
H_FEEDBACK_SPACING = 20
V_FEEDBACK_SPACING = 20
SECRET_CODE_X = GUESS_X + CIRCLE_DIAMETER
SECRET_CODE_Y = 65
SKEL_X = GUESS_X + CIRCLE_DIAMETER
SKEL_Y = GUESS_Y
FEEDBACK_CIRCLE_RADIUS = 5
FEEDBACK_X = SKEL_X + LEFTMOST_X + FEEDBACK_CIRCLE_RADIUS + CIRCLE_DIAMETER*3
FEEDBACK_Y = GUESS_Y + V_CIRCLE_SPACING
FINAL_TEXT_X = 185
FINAL_TEXT_Y = 25
GAME_WON_TEXT = 'YOU WIN! :)'
GAME_LOSE_TEXT = 'YOU LOSE :('
WIN = GraphWin("MasterMind" , G_WINDOW_WIDTH , G_WINDOW_HEIGHT)
SECRET_CODE_ARRAY = []
PALETTE_CIRCLE_ARRAY = []
MAIN_GAME_CIRCLE_ARRAY = []
EXIT_CIRCLE = []
HINT_CIRCLE = []
COVER_ARRAY = []
STATE_CIRCLE = 0
STATE_COLOR = 'white'

class Cell: #acts like C-style struct
    def __init__(self):
        self.text = None
        self.rectangle = None

def exit_Game():
    WIN.close()

def uncover_Hint(num):
    if(num < len(COVER_ARRAY)):
        COVER_ARRAY[num].text.undraw()
        COVER_ARRAY[num].rectangle.undraw()

def uncover_All_Hints():
    for i in range(len(COVER_ARRAY)):
        uncover_Hint(i)

def create_Circle_Text(circle, text, text_size,text_color):
    text_to_display = Text(circle.getCenter(), text)
    text_to_display.setSize(text_size)
    text_to_display.setTextColor(text_color)
    text_to_display.draw(WIN)

def create_Circle(x, y, color):
    center_Point = Point(x, y)
    circle = Circle(center_Point, CIRCLE_RADIUS)
    circle.setFill(color)
    circle.draw(WIN)
    return circle

def create_Circle_Row(x, y, color, num_circles):
    circle_array = []
    for i in range(num_circles):
        circle = create_Circle(x, y, color[i])
        circle_array.append(circle)
        x += CIRCLE_DIAMETER + H_CIRCLE_SPACING
    return circle_array

def contained_In_Array(array, item):
    for i in range(len(array)):
        if array[i] == item:
            return True, i
    return False, None

def create_FeedBack_Circles(x, y):
    tmp_secret_code = []
    for i in range(len(SECRET_CODE_ARRAY)):
        tmp_secret_code.append(SECRET_CODE_ARRAY[i])
    num_right = 0
    num_in = 0
    feedBack_colors = []
    for i in range(len(tmp_secret_code)):
        feedBack_colors.append('')
        if tmp_secret_code[i] == BLANK_COLORS[i]:
            feedBack_colors[num_right] = 'red'
            tmp_secret_code[i] = 0
            BLANK_COLORS[i] = 1
            num_right += 1
    for i in range(len(BLANK_COLORS)):
        is_found, idx = contained_In_Array(BLANK_COLORS, tmp_secret_code[i])
        if is_found:
            feedBack_colors[num_right + num_in] = 'white'
            BLANK_COLORS[idx] = 1
            num_in += 1
    x_2 = x
    y_2 = y - V_FEEDBACK_SPACING
    for i in range(len(BLANK_COLORS)):
        if i == 2:
            y_2 += V_FEEDBACK_SPACING
            x_2 = x
        feedback_point = Point(x_2, y_2)
        feedback_circle = Circle(feedback_point, FEEDBACK_CIRCLE_RADIUS)
        feedback_circle.setFill(feedBack_colors[i])
        if feedBack_colors[i] != '':
            feedback_circle.draw(WIN)
        x_2 += H_FEEDBACK_SPACING
    return num_right == len(SECRET_CODE_ARRAY)

def create_Secret_Code_Colors():
    secret_code_array = []
    num_palette_colors = len(PALETTE_COLORS)
    for i in range(4):
        idx = int(round(random.random() * (num_palette_colors - 1)))
        secret_code_array.append(PALETTE_COLORS[idx])
    return secret_code_array

def cover_Secret_Code():
    cell_Array = []
    rect_x = SECRET_CODE_X - 20
    rect_y = SECRET_CODE_Y - 20
    text_x = SECRET_CODE_X
    text_y = SECRET_CODE_Y
    for i in range(len(SECRET_CODE_ARRAY)):
        c = Cell()
        point1 = Point(rect_x, rect_y)
        point2 = Point(rect_x + 40, rect_y + 40)
        rect = Rectangle(point1, point2)
        rect.setFill('grey')
        rect.draw(WIN)
        c.rectangle = rect
        center_of_text = Point(text_x, text_y)
        text_to_display = Text(center_of_text, '?')
        text_to_display.setSize(25)
        text_to_display.setTextColor('gold')
        text_to_display.draw(WIN)
        c.text = text_to_display
        cell_Array.append(c)
        rect_x += 45
        text_x += 45
    return cell_Array

def find_Clicked_Circle(click_point, object_Array):
    for i in range(len(object_Array)):
        for j in range(len(object_Array[i])):
            c_center = object_Array[i][j].getCenter()
            dist = (c_center.getX() - click_point.getX()) ** 2 + (c_center.getY() - click_point.getY()) ** 2
            if dist < CIRCLE_RADIUS**2:
                return j, i
    return None, None

def check_If_Game_Circles_Filled():
    sum = 0
    for i in BLANK_COLORS:
        if i != 'white':
            sum += 1
    return sum == len(BLANK_COLORS)

def clone_And_Move_Circles_Up(circles, dy):
    for i in range(len(circles)):
        clone_circle = circles[i].clone()
        clone_circle.draw(WIN)
        circles[i].move( 0 , dy)
        circles[i].setFill('white')

def show_Final_Text(text_to_use, color):
    center_of_text = Point(FINAL_TEXT_X , FINAL_TEXT_Y)
    text_to_display = Text(center_of_text , text_to_use )
    text_to_display.setSize(30)
    text_to_display.setTextColor(color)
    text_to_display.draw(WIN)

def start():
    global SECRET_CODE_ARRAY
    global PALETTE_CIRCLE_ARRAY
    global MAIN_GAME_CIRCLE_ARRAY
    global COVER_ARRAY
    global EXIT_CIRCLE
    global STATE_CIRCLE
    global HINT_CIRCLE
    EXIT_CIRCLE.append(create_Circle(EXIT_X, EXIT_Y, 'red'))
    create_Circle_Text(EXIT_CIRCLE[0], 'Exit', 15, 'black')
    STATE_CIRCLE = create_Circle(STATE_X, STATE_Y, 'white')
    SECRET_CODE_ARRAY = create_Secret_Code_Colors()
    create_Circle_Row(SECRET_CODE_X, SECRET_CODE_Y, SECRET_CODE_ARRAY, len(SECRET_CODE_ARRAY))
    COVER_ARRAY = cover_Secret_Code()
    HINT_CIRCLE.append(create_Circle(EXIT_X, EXIT_Y + 45, 'grey'))
    create_Circle_Text(HINT_CIRCLE[0], 'Hint', 15, 'gold')
    PALETTE_CIRCLE_ARRAY = create_Circle_Row(PALETTE_X, PALETTE_Y, PALETTE_COLORS, len(PALETTE_COLORS))
    MAIN_GAME_CIRCLE_ARRAY = create_Circle_Row(SKEL_X, SKEL_Y, BLANK_COLORS, len(BLANK_COLORS))

def update(num_rounds):
    global STATE_COLOR
    global BLANK_COLORS
    global FEEDBACK_Y
    hint_num = 0
    all_circles_filled = False
    window_Object_Array = [PALETTE_CIRCLE_ARRAY, MAIN_GAME_CIRCLE_ARRAY, EXIT_CIRCLE, HINT_CIRCLE]
    for i in range(num_rounds):
        while all_circles_filled != True:
            click_point = WIN.getMouse()
            idx, win_obj_arr_idx = find_Clicked_Circle(click_point, window_Object_Array)
            if win_obj_arr_idx == None:
                STATE_CIRCLE.setFill('white')
                STATE_COLOR = 'white'
            elif win_obj_arr_idx == 0:
                STATE_CIRCLE.setFill(PALETTE_COLORS[idx])
                STATE_COLOR = PALETTE_COLORS[idx]
            elif win_obj_arr_idx == 1:
                if STATE_COLOR != 'white':
                    MAIN_GAME_CIRCLE_ARRAY[idx].setFill(STATE_COLOR)
                    BLANK_COLORS[idx] = STATE_COLOR
                    STATE_CIRCLE.setFill('white')
                    STATE_COLOR = 'white'
            elif win_obj_arr_idx == 2:
                exit_Game()
            elif win_obj_arr_idx == 3:
                uncover_Hint(hint_num)
                hint_num += 1
            all_circles_filled = check_If_Game_Circles_Filled()
        if create_FeedBack_Circles(FEEDBACK_X, FEEDBACK_Y):
            return True
        if i < num_rounds-1:
            clone_And_Move_Circles_Up(MAIN_GAME_CIRCLE_ARRAY, -CIRCLE_DIAMETER - V_CIRCLE_SPACING)
            all_circles_filled = False
            BLANK_COLORS = ['white', 'white', 'white', 'white']
            FEEDBACK_Y -= CIRCLE_DIAMETER + V_CIRCLE_SPACING
    return False

def main():
    start()
    if update(8):
        show_Final_Text(GAME_WON_TEXT, 'blue')
        uncover_All_Hints()
        WIN.getMouse()
        WIN.close()
    else:
        show_Final_Text(GAME_LOSE_TEXT, 'red')
        uncover_All_Hints()
        WIN.getMouse()
        WIN.close()

main()