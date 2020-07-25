from tkinter import Tk, Canvas
import time
import math

import config_values

TEAM_SIZE = config_values.TEAM_SIZE

lines_color = "#fff"
field_color = "#0b0"
goal_color = "#dd0"

red_color = "#f00"
blue_color = "#0cf"
ball_color = "#000"

lines_width = 2

x_margin = 30
y_margin = 30

# measurements in yards, scaled to pixels by factor 10, might adjust later for variable factor
# IMPORTANT: width is x-axis on screen, height is y-axis
field_width = 1200
field_height = 750
center_radius = 100
corner_radius = 10
penalty_area_width = 180
penalty_area_height = 440
penalty_arc_radius = 120
penalty_arc_center = 120
goal_area_width = 60
goal_area_height = 120
goal_height = 80
goal_width = min(x_margin-10, 20)
player_radius = 10
ball_radius = 6

# player positions
red_pos = [(i, i) for i in range(10, 120, 10)]
blue_pos = [(i, i) for i in range(130, 240, 10)]
ball_pos = (x_margin+field_width//2, y_margin+field_height//2)

# player canvas objects
red_players = [None]*TEAM_SIZE
blue_players = [None]*TEAM_SIZE
ball = None


def windowDims():
    w = field_width + x_margin*2
    h = field_height + y_margin*2
    return "{}x{}".format(w, h)


def drawField(canvas):
    # draw the background and boundary
    canvas.create_rectangle(x_margin, y_margin, x_margin+field_width, y_margin+field_height, outline=lines_color, fill=field_color, width=lines_width)
    
    # draw the half line
    canvas.create_line(x_margin+field_width//2, y_margin, x_margin+field_width//2, y_margin+field_height, fill=lines_color, width=lines_width)
    
    # draw the centre circle
    canvas.create_oval(x_margin+field_width//2-center_radius, y_margin+field_height//2-center_radius, x_margin+field_width//2+center_radius, y_margin+field_height//2+center_radius, outline = lines_color, width = lines_width)
    
    # draw the corner arcs, top left, top right, bottom left, bottom right
    canvas.create_arc(x_margin-corner_radius, y_margin-corner_radius, x_margin+corner_radius, y_margin+corner_radius, start=270, extent=90, outline=lines_color, width=lines_width, style='arc')
    canvas.create_arc(x_margin+field_width-corner_radius, y_margin-corner_radius, x_margin+field_width+corner_radius, y_margin+corner_radius, start=180, extent=90, outline=lines_color, width=lines_width, style='arc')
    canvas.create_arc(x_margin-corner_radius, y_margin+field_height-corner_radius, x_margin+corner_radius, y_margin+field_height+corner_radius, start=0, extent=90, outline=lines_color, width=lines_width, style='arc')
    canvas.create_arc(x_margin+field_width-corner_radius, y_margin+field_height-corner_radius, x_margin+field_width+corner_radius, y_margin+field_height+corner_radius, start=90, extent=90, outline=lines_color, width=lines_width, style='arc')
    
    # draw the penalty arcs, left side, right side
    canvas.create_arc(x_margin+penalty_arc_center-penalty_arc_radius, y_margin+field_height//2-penalty_arc_radius, x_margin+penalty_arc_center+penalty_arc_radius, y_margin+field_height//2+penalty_arc_radius, start=270, extent=180, outline=lines_color, width=lines_width, style='arc')
    canvas.create_arc(x_margin+field_width-penalty_arc_center-penalty_arc_radius, y_margin+field_height//2-penalty_arc_radius, x_margin+field_width-penalty_arc_center+penalty_arc_radius, y_margin+field_height//2+penalty_arc_radius, start=90, extent=180, outline=lines_color, width=lines_width, style='arc')
    
    # draw the penalty areas, left side, right side
    canvas.create_rectangle(x_margin, y_margin+field_height//2-penalty_area_height//2, x_margin+penalty_area_width, y_margin+field_height//2+penalty_area_height//2, fill=field_color, outline=lines_color, width=lines_width)
    canvas.create_rectangle(x_margin+field_width-penalty_area_width, y_margin+field_height//2-penalty_area_height//2, x_margin+field_width, y_margin+field_height//2+penalty_area_height//2, fill=field_color, outline=lines_color, width=lines_width)
    
    #draw the goal areas, left side, right side
    canvas.create_rectangle(x_margin, y_margin+field_height//2-goal_area_height//2, x_margin+goal_area_width, y_margin+field_height//2+goal_area_height//2, outline=lines_color, width=lines_width)
    canvas.create_rectangle(x_margin+field_width-goal_area_width, y_margin+field_height//2-goal_area_height//2, x_margin+field_width, y_margin+field_height//2+goal_area_height//2, outline=lines_color, width=lines_width)
    
    #draw the goals, left side, right side
    canvas.create_rectangle(x_margin-goal_width, y_margin+field_height//2-goal_height//2, x_margin, y_margin+field_height//2+goal_height//2, fill=goal_color, outline=lines_color, width=lines_width)
    canvas.create_rectangle(x_margin+field_width, y_margin+field_height//2-goal_height//2, x_margin+field_width+goal_width, y_margin+field_height//2+goal_height//2, fill=goal_color, outline=lines_color, width=lines_width)
    
    canvas.pack(fill="both", expand=True)


def initialize_players(canvas):
    global red_players, blue_players, ball
    for i in range(TEAM_SIZE):
        px, py = red_pos[i]
        red_players[i] = canvas.create_oval(x_margin+px-player_radius, y_margin+py-player_radius, x_margin+px+player_radius, y_margin+py+player_radius, fill=red_color)
    for i in range(TEAM_SIZE):
        px, py = blue_pos[i]
        blue_players[i] = canvas.create_oval(x_margin+px-player_radius, y_margin+py-player_radius, x_margin+px+player_radius, y_margin+py+player_radius, fill=blue_color)
    ball = canvas.create_oval(ball_pos[0]-ball_radius, ball_pos[1]-ball_radius, ball_pos[0]+ball_radius, ball_pos[1]+ball_radius, fill=ball_color)

def update_positions(team_red, team_blue, new_ball_pos, canvas): #list of agent objects
    global red_players, red_pos, blue_players, blue_pos, ball, ball_pos
    
    for i in range(TEAM_SIZE):
        old_x, old_y = red_pos[i]
        new_x, new_y = team_red[i]
        diff_x, diff_y = new_x-old_x, new_y-old_y
        canvas.move(red_players[i], diff_x, diff_y)
        red_pos[i] = (new_x, new_y)
    
    for i in range(TEAM_SIZE):
        old_x, old_y = blue_pos[i]
        new_x, new_y = team_blue[i]
        diff_x, diff_y = new_x-old_x, new_y-old_y
        canvas.move(blue_players[i], diff_x, diff_y)
        blue_pos[i] = (new_x, new_y)
    
    old_x, old_y = ball_pos
    new_x, new_y = new_ball_pos
    new_x, new_y = new_x+x_margin, new_y+y_margin
    diff_x, diff_y = new_x-old_x, new_y-old_y
    step = max(diff_x, diff_y)

    mod = math.sqrt(diff_x*diff_x + diff_y*diff_y)
    c_x, c_y = old_x, old_y
    speed = 10
    while ((c_x != new_x) or (c_y != new_y)):
        unit_vec = (diff_x / mod, diff_y / mod)
        step_x = unit_vec[0] * speed
        step_y = unit_vec[1] * speed
        if c_x == new_x:
            step_x = 0
        if c_y == new_y:
            step_y = 0
        if ((c_x>new_x) and (c_x+step_x < new_x)) or ((c_x < new_x) and (c_x + step_x) > new_x):
            step_x = new_x - c_x
            c_x = new_x
        else:
            c_x = c_x + step_x
        if ((c_y>new_y) and (c_y+step_y < new_y)) or ((c_y < new_y) and (c_y + step_y) > new_y):
            step_y = new_y - c_y
            c_y = new_y
        else:
            c_y = c_y + step_y
        ball_pos = (c_x, c_y)
        canvas.move(ball, step_x, step_y)
        canvas.update()
        time.sleep(0.01)

