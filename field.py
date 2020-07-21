from tkinter import Tk, Canvas
import time

class Field:

    def __init__(self):
        self.lines_color = "#fff"
        self.field_color = "#0b0"
        self.goal_color = "#dd0"

        self.red_color = "#f00"
        self.blue_color = "#0cf"
        self.ball_color = "#000"

        self.lines_width = 2

        self.x_margin = 30
        self.y_margin = 30

        # measurements in yards, scaled to pixels by factor 10, might adjust later for variable factor
        # IMPORTANT: width is x-axis on screen, height is y-axis
        self.field_width = 1200
        self.field_height = 750
        self.center_radius = 100
        self.corner_radius = 10
        self.penalty_area_width = 180
        self.penalty_area_height = 440
        self.penalty_arc_radius = 120
        self.penalty_arc_center = 120
        self.goal_area_width = 60
        self.goal_area_height = 120
        self.goal_height = 80
        self.goal_width = min(self.x_margin-10, 20)
        self.player_radius = 4
        self.ball_radius = 4

        # player positions
        self.red_pos = [(i, i) for i in range(10, 120, 10)]
        self.blue_pos = [(i, i) for i in range(130, 240, 10)]
        self.ball_pos = (self.x_margin+self.field_width//2, self.y_margin+self.field_height//2)

        # player canvas objects
        self.TEAM_SIZE = 2
        self.red_players = [None]*self.TEAM_SIZE
        self.blue_players = [None]*self.TEAM_SIZE
        self.ball = None
        self.root = Tk()
        self.canvas = Canvas()

    def windowDims(self):
        w = self.field_width + self.x_margin*2
        h = self.field_height + self.y_margin*2
        return "{}x{}".format(w, h)


    def drawField(self):
        # draw the background and boundary
        self.canvas.create_rectangle(self.x_margin, self.y_margin, self.x_margin+self.field_width, self.y_margin+self.field_height, outline=self.lines_color, fill=self.field_color, width=self.lines_width)
        
        # draw the half line
        self.canvas.create_line(self.x_margin+self.field_width//2, self.y_margin, self.x_margin+self.field_width//2, self.y_margin+self.field_height, fill=self.lines_color, width=self.lines_width)
        
        # draw the centre circle
        self.canvas.create_oval(self.x_margin+self.field_width//2-self.center_radius, self.y_margin+self.field_height//2-self.center_radius, self.x_margin+self.field_width//2+self.center_radius, self.y_margin+self.field_height//2+self.center_radius, outline = self.lines_color, width = self.lines_width)
        
        # draw the corner arcs, top left, top right, bottom left, bottom right
        self.canvas.create_arc(self.x_margin-self.corner_radius, self.y_margin-self.corner_radius, self.x_margin+self.corner_radius, self.y_margin+self.corner_radius, start=270, extent=90, outline=self.lines_color, width=self.lines_width, style='arc')
        self.canvas.create_arc(self.x_margin+self.field_width-self.corner_radius, self.y_margin-self.corner_radius, self.x_margin+self.field_width+self.corner_radius, self.y_margin+self.corner_radius, start=180, extent=90, outline=self.lines_color, width=self.lines_width, style='arc')
        self.canvas.create_arc(self.x_margin-self.corner_radius, self.y_margin+self.field_height-self.corner_radius, self.x_margin+self.corner_radius, self.y_margin+self.field_height+self.corner_radius, start=0, extent=90, outline=self.lines_color, width=self.lines_width, style='arc')
        self.canvas.create_arc(self.x_margin+self.field_width-self.corner_radius, self.y_margin+self.field_height-self.corner_radius, self.x_margin+self.field_width+self.corner_radius, self.y_margin+self.field_height+self.corner_radius, start=90, extent=90, outline=self.lines_color, width=self.lines_width, style='arc')
        
        # draw the penalty arcs, left side, right side
        self.canvas.create_arc(self.x_margin+self.penalty_arc_center-self.penalty_arc_radius, self.y_margin+self.field_height//2-self.penalty_arc_radius, self.x_margin+self.penalty_arc_center+self.penalty_arc_radius, self.y_margin+self.field_height//2+self.penalty_arc_radius, start=270, extent=180, outline=self.lines_color, width=self.lines_width, style='arc')
        self.canvas.create_arc(self.x_margin+self.field_width-self.penalty_arc_center-self.penalty_arc_radius, self.y_margin+self.field_height//2-self.penalty_arc_radius, self.x_margin+self.field_width-self.penalty_arc_center+self.penalty_arc_radius, self.y_margin+self.field_height//2+self.penalty_arc_radius, start=90, extent=180, outline=self.lines_color, width=self.lines_width, style='arc')
        
        # draw the penalty areas, left side, right side
        self.canvas.create_rectangle(self.x_margin, self.y_margin+self.field_height//2-self.penalty_area_height//2, self.x_margin+self.penalty_area_width, self.y_margin+self.field_height//2+self.penalty_area_height//2, fill=self.field_color, outline=self.lines_color, width=self.lines_width)
        self.canvas.create_rectangle(self.x_margin+self.field_width-self.penalty_area_width, self.y_margin+self.field_height//2-self.penalty_area_height//2, self.x_margin+self.field_width, self.y_margin+self.field_height//2+self.penalty_area_height//2, fill=self.field_color, outline=self.lines_color, width=self.lines_width)
        
        #draw the goal areas, left side, right side
        self.canvas.create_rectangle(self.x_margin, self.y_margin+self.field_height//2-self.goal_area_height//2, self.x_margin+self.goal_area_width, self.y_margin+self.field_height//2+self.goal_area_height//2, outline=self.lines_color, width=self.lines_width)
        self.canvas.create_rectangle(self.x_margin+self.field_width-self.goal_area_width, self.y_margin+self.field_height//2-self.goal_area_height//2, self.x_margin+self.field_width, self.y_margin+self.field_height//2+self.goal_area_height//2, outline=self.lines_color, width=self.lines_width)
        
        #draw the goals, left side, right side
        self.canvas.create_rectangle(self.x_margin-self.goal_width, self.y_margin+self.field_height//2-self.goal_height//2, self.x_margin, self.y_margin+self.field_height//2+self.goal_height//2, fill=self.goal_color, outline=self.lines_color, width=self.lines_width)
        self.canvas.create_rectangle(self.x_margin+self.field_width, self.y_margin+self.field_height//2-self.goal_height//2, self.x_margin+self.field_width+self.goal_width, self.y_margin+self.field_height//2+self.goal_height//2, fill=self.goal_color, outline=self.lines_color, width=self.lines_width)
        
        self.canvas.pack(fill="both", expand=True)


    def initialize_players(self):
        for i in range(self.TEAM_SIZE):
            px, py = self.red_pos[i]
            self.red_players[i] = self.canvas.create_oval(self.x_margin+px-self.player_radius, self.y_margin+py-self.player_radius, self.x_margin+px+self.player_radius, self.y_margin+py+self.player_radius, fill=self.red_color)
        for i in range(self.TEAM_SIZE):
            px, py = self.blue_pos[i]
            self.blue_players[i] = self.canvas.create_oval(self.x_margin+px-self.player_radius, self.y_margin+py-self.player_radius, self.x_margin+px+self.player_radius, self.y_margin+py+self.player_radius, fill=self.blue_color)
        self.ball = self.canvas.create_oval(self.ball_pos[0]-self.ball_radius, self.ball_pos[1]-self.ball_radius, self.ball_pos[0]+self.ball_radius, self.ball_pos[1]+self.ball_radius, fill=self.ball_color)

    '''
    def update_positions():
        global red_players, red_pos, blue_players, blue_pos, ball, ball_pos, canvas
        for i in range(11):
            canvas.move(red_players[i], 2, 0)
            red_pos[i] = (red_pos[i][0]+2, red_pos[i][1])
        for i in range(11):
            canvas.move(blue_players[i], 0, 2)
            blue_pos[i] = (blue_pos[i][0], blue_pos[i][1]+2)
        canvas.move(ball, 2, 2)
        ball_pos = (ball_pos[0]+2, ball_pos[1]+2)
    '''

    def update_positions(self, team_red, team_blue, new_ball_pos): #list of agent objects
        
        for i in range(self.TEAM_SIZE):
            old_x, old_y = self.red_pos[i]
            new_x, new_y = team_red[i]
            diff_x, diff_y = new_x-old_x, new_y-old_y
            self.canvas.move(self.red_players[i], diff_x, diff_y)
            self.red_pos[i] = (new_x, new_y)
        
        for i in range(self.TEAM_SIZE):
            old_x, old_y = self.blue_pos[i]
            new_x, new_y = team_blue[i]
            diff_x, diff_y = new_x-old_x, new_y-old_y
            self.canvas.move(self.blue_players[i], diff_x, diff_y)
            self.blue_pos[i] = (new_x, new_y)
        
        new_x, new_y = new_ball_pos
        old_x, old_y = ball_pos
        diff_x, diff_y = new_x-old_x, new_y-old_y
        self.canvas.move(self.ball, diff_x, diff_y)
        self.ball_pos = new_ball_pos

    def main(self):
        # root = Tk()
        self.root.geometry(self.windowDims())
        self.root.title("Robocup Simulation")
        self.canvas = Canvas()
        self.drawField()
        self.initialize_players()
        self.root.mainloop()
        print("Window closed")

# f = Field()
# f.main()