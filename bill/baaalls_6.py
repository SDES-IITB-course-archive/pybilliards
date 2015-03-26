#!/usr/bin/python
#
# How to use it ??
# Ball is placed on screen, click left button of mouse to have a stick on screen
# You can feel the streching of stick if you take the mouse pointer away from the stick end point
# Press right button of mouse to hit the stick :D
# Ball will move in appropriate direction :D
# 
# Working billiards game, 
# Balls will disappear after being pocketed :D
# 6 pockets are added :D
# After all balls are pocketed, then game will stop, you can quit or continue the game :D
# ----------------------------------------------------------------------------------------------------------
import pygame

# import time
import random
from math import *
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
GREEN = (0,140,0)
FPS = 40
dispHeight = 500
dispWidth = 800
font = pygame.font.SysFont(None, 25)

# gameDisplay = pygame.display.set_mode((dispHeight,dispWidth))
gameDisplay = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption('pyBilliard')
clock = pygame.time.Clock()

pygame.display.update()
# pygame.display.flip()

class Balls:
    def __init__(self, (x,y), size, thickness=0, color=(0,0,255)):
        self.x = x
        self.y = y
        self.size = size
        self.thickness = thickness # Default :D
        self.color = color
        self.speed = 1
        self.angle = 0 # This is in radian :D
        self.pocketed = self.is_pocketed()

    def disp(self):
        pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), self.size, self.thickness)
        pygame.display.update()

    def boundary(self):
        if self.x > dispWidth - self.size:
            self.x = 2*(dispWidth - self.size) - self.x
            self.angle = - self.angle

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        if self.y > dispHeight - self.size:
            self.y = 2*(dispHeight - self.size) - self.y
            self.angle = pi - self.angle

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = pi - self.angle


    def move(self, dist, angle, speed, smear=False):
        self.angle = angle
        self.speed = speed

        # Adding boundary function :D
        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)
        while dist > 0:
            # s = "current distance of movement is " + str(dist)
            # msg2screen(s,self.x - 100, self.y + 200)
            if not smear:
                gameDisplay.fill(GREEN)

            self.x += int(round(sin(self.angle) * self.speed))
            self.y -= int(round(cos(self.angle) * self.speed))

            #---------
            self.boundary()
            #---------

            # if (self.x + self.size) > dispWidth or (self.x - self.size) < 0 or (self.y + self.size) > dispHeight or (self.y - self.size)< 0:
            #     s = "I am breaking it bad .... :( " + str(dist)
            #     msg2screen(s,self.x - 100, self.y + 200)
            #     pygame.display.update()
            #     break
            # else:
            #     s = "I am doing it good .... :) " + str(dist)
            #     msg2screen(s,self.x - 100, self.y + 200)
            #     pygame.display.update()

            self.disp()
            # pygame.display.update()
            dist -= 1 # Movement of these units only :D
        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)
    def move_with_collision_correction(self,dist=None, angle = None, speed=3, list_of_ball_objects = []):
        
        if dist != None:
            self.dist = dist

        if angle != None:
            self.angle = angle

        if list_of_ball_objects == []:
            list_of_ball_objects.append(self)
        
        self.speed = speed

        # Adding boundary function :D

        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)
        while self.dist > 0:
            # s = "current distance of movement is " + str(dist)
            # msg2screen(s,self.x - 100, self.y + 200)
            gameDisplay.fill(GREEN)

            self.x += int(round(sin(self.angle) * self.speed))
            self.y -= int(round(cos(self.angle) * self.speed))

            #---------
            self.collision(list_of_ball_objects, self.dist)
            self.is_pocketed()
            self.boundary()
            #---------
            self.disp()
            # pygame.display.update()
            self.dist -= 1 # Movement of these units only :D

    def is_clicked(self, a, b):
        if hypot(self.x-a, self.y-b) <= self.size:
            return 1                                # If the point (a,b) is inside the ball then return 1 :D
        else:
            return 0                                # Else return 0 :D

    def collision(self, all_balls, dist):
        all_other_except_me = [my_ball for my_ball in all_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = my_ball.x - self.x
            dy = my_ball.y - self.y

            dist_of_separation = hypot(dx,dy)

            if dist_of_separation < (self.size + my_ball.size):             # Collision happened :D
                print "Bang Bang !!"
                
                tangent = atan2(dy, dx)
                self.angle      = 2*tangent - self.angle
                self.dist       = self.dist/2

                my_ball.angle   = 2*tangent - my_ball.angle
                my_ball.dist    = self.dist             # This is modified distance, which 1/2 of the previous :D

                # list_for_my_ball = [temp_ball for temp_ball in all_balls if temp_ball != my_ball]

                my_ball.move_with_collision_correction(list_of_ball_objects = all_balls)

    def is_pocketed(self):
        x_limits = (0, dispWidth/2, dispWidth)
        y_limits = (0, dispHeight)

        for i in x_limits:
            for j in y_limits:
                ball_dist = hypot(self.x - i, self.y -j)
                if ball_dist < 3*self.size:
                    self.pocketed = 1
                    self.dist = 0           # So that the ball will not move any further :D
                    return 1
        return 0

def create_rand_Ball(size):
    x = random.randint(size, dispWidth-size)
    y = random.randint(size, dispHeight-size)
    return Balls((x,y), size)

def msg2screen(msg, x_loc=dispWidth/4, y_loc=dispHeight/2, color=black):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x_loc,  y_loc])

def show_pockets(pocket_size):
    a = (0, dispWidth/2, dispWidth)
    b = (0, dispHeight)

    for i in a:
        for j in b:
            pygame.draw.circle(gameDisplay, (0, 0, 0), (i, j), pocket_size, 0)
            pygame.display.update()
            
def stick(block_size, stickList): # This will print our stick of finite length :D
    for each in stickList:
        pygame.draw.rect(gameDisplay, blue, [each[0], each[1], block_size, block_size])

def get_points(x1, y1, x2, y2, curr_dist, m, choice):
    # choice = 0 for start point , 
    #        = 1 for end point :D

    # In logic, (x1,y1) is start point, and (x2,y2) is end point
    # What I am finding out it another point on the line at distance "curr_dist" in direction of movement :D

    # if (y2 >= y1) ^ choice:
    # # y2 = y2-1
    #     y = y1 - curr_dist
    # else:
    # # y2 = y2+1
    #     y = y1 + curr_dist

    # x = x2 + round(m*(y - y2))  # From (x2,y2) and y selected, x will be found out :D
    # a = dispWidth/4
    # b = 3*dispHeight/4

    if abs(y2-y1) >= abs(x2-x1):
        if (y2 >= y1) ^ choice:
        # y2 = y2-1
            y = y1 - curr_dist
        else:
        # y2 = y2+1
            y = y1 + curr_dist

        x = x2 + round(m*(y - y2))  # From (x2,y2) and y selected, x will be found out :D
        # s = "<<--------Inside y------->>  " + str(m)
    else:
        if (x2 >= x1) ^ choice:
            x = x1 - curr_dist
        else:
            x = x1 + curr_dist

        y = y2 + round(m*(x - x2))  # From (x2,y2) and y selected, x will be found out :D
        # s = "<<--------Inside x------->>  " + str(m)

    # msg2screen(s,a,b)
    return (x, y)

def new_get_slope(x1,y1,x2,y2):
    # p = dispWidth/4
    # q = 3*dispHeight/4
    # s = "x1, y1, x2, y2: " + str(x1) + ":" + str(x1) + ":" + str(y1) + ":" + str(x2) + ":" + str(y2)

    if (y2-y1)!=0:
        m = float(x2-x1)/(y2-y1)
    else:
        m = abs(x2-x1)*10**2   # I am returing a high value, equivalent to infinity :D
        # if y1 > y2:
        #     m = m * -1
        if x2 > x1:
            m = m * -1
    return m

def get_slope(x1,y1,x2,y2):
    # p = dispWidth/4
    # q = 3*dispHeight/4
    # s = "x1, y1, x2, y2: " + str(x1) + ":" + str(x1) + ":" + str(y1) + ":" + str(x2) + ":" + str(y2)
    # # if (x2-x1)!=0:
    #                                 #          (y2-y1)
    #                 #                (y-y1) =  ------- * (x-x1)                                      
    #                            #               (x2-x1) 
    #     m1 = float(y2-y1)/(x2-x1)
    #     m = m1
    #     s = "you are is m111111111"
    #     # return m1

    # elif (y2-y1)!=0:
    #                                 #          (x2-x1)
    #                 #                (x-x1) =  ------- * (y-y1)                                      
    #                            #               (y2-y1)                     
    #     m2 = float(x2-x1)/(y2-y1)
    #     m = m2
    #     s = "you are is m222222222"
    #     # return m2
    # # msg2screen(s,p,q)
    y_diff = (y2-y1)
    x_diff = (x2-x1)

    m = tan(atan2(y_diff,x_diff))
    return m

def get_angle(point_loc, Ball_obj):
    temp1 = point_loc[0] - Ball_obj.x
    temp2 = -1* (point_loc[1] - Ball_obj.y) # This -ve sign is to incorporate the inverted y-axis :D

    # if temp2 == 0:
    #     move_angle = (pi/2) * (temp1/abs(temp1)) # This is for the sign of than angle also :D
    # else:
    #     move_angle = atan(float(temp1)/temp2)

    move_angle = atan2(temp1, temp2)

    return move_angle

def ball_got_hit(start_point, Ball_obj):
    hamming_dist = sqrt((start_point[0]- Ball_obj.x)**2 + (start_point[1]- Ball_obj.y)**2)

    if hamming_dist < Ball_obj.size:
        return 1
    else:
        return 0
def trace_the_shot(start_point, end_point, m, mouse_pos):
    # This only projects a line from the stick with some finite distnace :D
    # Ball touch is not included here :D

    move_dist = sqrt((end_point[0] - mouse_pos[0])**2 + (end_point[1] - mouse_pos[1])**2)
    # get_points(x1,y1,x2,y2,curr_dist,m,choice):
    a,b = start_point[0], start_point[1], 
    c,d = end_point[0], end_point[1]

    # m = get_slope(a,b,c,d)
    trace_point = get_points(a, b, c, d, move_dist, m, 0)  # Here choice = 0, Since I want to find the trace point :D

    point_to_draw = []
    point_to_draw.append(start_point)       # Line will start from here
    # Now I am checking for any boundary reflection of that trace line :D

    temp_dist = 1
    # points_on_line = []

    while temp_dist <= move_dist:
        # m = get_slope(a,b,c,d)
        # if abs(m)>1:
        #     m = 1/m

        temp_point = get_points(a, b, c, d, temp_dist, m, 0)  # Here choice = 0, Since I want to find the trace point :D
        temp_dist += 1
        # points_on_line.append(temp_point)

        x,y = temp_point
        # if x < 0 or y < 0 or x > (dispWidth ) or y > (dispHeight ):  
        # # Here the condition is written in special way, so that point to added has positive cooradinates :D
        #     last_point = points_on_line[-2]   
        #     # I want to add the second last point which was added
        #     # The last point which was added is the out of boundary point :D
        #     point_to_draw.append(last_point)

        #     # Modifying the "get_points" function call, so that line will be traced even after the boundary was crossed :D

        #     # Checking which boundary was crossed
        #     # 
        #     #                                 this is boundary no. 1   (x---->--->)
        #     #                               --------------------------
        #     #                               |                        |
        #     #                               |                        |
        #     #     this is boundary no. 4    |                        |  this is boundary no. 2
        #     #                               |                        |
        #     #                               |                        |
        #     #                               --------------------------
        #     #                                   this is boundary no. 3

        #     if x < 0 or x > (dispWidth ):
        #         x = dispWidth - (x % dispWidth)

        #     if y < 0 or y > (dispHeight ):
        #         y = dispHeight - (y % dispHeight)

        #     # Now after solving boundary problem, we need to modify the start and end points so that the line is traced correct
        #     # Hence, "new end point" is the boundary point that added
        #     # and "new start point" will be the out of boundary point which has been corrected as above :D
        #     c,d = last_point        # new end point
        #     a,b = x,y               # new start point :D
    
        k = 0 
        # This is special unit :D

        if x < k or y < k or x > (dispWidth -k) or y > (dispHeight -k):  
            
            # Here the condition is written in special way, so that point to added has positive cooradinates :D
            
            # Modifying the "get_points" function call, so that line will be traced even after the boundary was crossed :D

            # Checking which boundary was crossed
            # 
            #                                 this is boundary no. 1   (x---->--->)
            #                               --------------------------
            #                               |                        |
            #                               |                        |
            #     this is boundary no. 4    |                        |  this is boundary no. 2
            #                               |                        |
            #                               |                        |
            #                               --------------------------
            #                                   this is boundary no. 3
            
            

            if x < k or x > (dispWidth - k):
                x = dispWidth - (x % dispWidth)
                if x < k:
                    x_cordi = 0

                    c = c
                    d = -d 
                    
                else:
                    x_cordi = dispWidth

                    c = c
                    d = 2*dispHeight - d

                y_cordi = m*x_cordi + (b - m*a)  

            if y < k or y > (dispHeight -k):
                y = dispHeight - (y % dispHeight)
                if y < k:
                    y_cordi = 0

                    c = -c
                    d = d 

                else:
                    y_cordi = dispHeight

                    c = 2*dispWidth - c
                    d = d

                x_cordi = (1/m)*y_cordi + (a - (1/m)*b)  # You can replace y2 by y2 , and x2 by x1 also :D

            last_point = (x_cordi, y_cordi)
            point_to_draw.append(last_point)

            # Now after solving boundary problem, we need to modify the start and end points so that the line is traced correct
            # Hence, "new start point" is the boundary point that added
            # and "new end point" will be calculated as below (I have reflected previous end point to get this new one :D)
            a,b = last_point        # new start point
                                    # new start point :D already modified
         # After finishing the while loop, I must add the last point which got traced, to list of "point_to_draw"       

        m = tan(pi - atan(m))  # AFter coming out of the loop for correcting x,y change the slop of the line :D
        if abs(m)>1:
            m = 1/m


    point_to_draw.append(temp_point)

     # I will now draw lines in between the point in my list "point_to_draw"
     # i.e. line between 1st and 2nd, then between 2nd and 3rd, and so on
     # Why/when "point_to_draw" will have more than 2 points??
     # If there is reflection due to surface then only more than 2
     # If no reflection at all then only 2 point in the list "point_to_draw" :D
    print point_to_draw
    for i in xrange(len(point_to_draw) - 1):  
     # Ques: Why    len(point_to_draw) -1    ? 
     # Ans : Because to no pair for the last point :D
        # pygame.draw.aaline(gameDisplay, (0, 255, 0), point_to_draw[i], point_to_draw[i+1])
        # pygame.draw.line(gameDisplay, (255, 0, 0), point_to_draw[i], point_to_draw[i+1],20)
        pygame.display.update()
    aa,bb = trace_point
    # aa = aa % dispWidth
    # bb = bb % dispHeight
    new = aa,bb
    pygame.draw.line(gameDisplay, (255, 0, 0), point_to_draw[0], new,2)
    pygame.display.update()
    # p = dispWidth/4 - 100
    # q = 3*dispHeight/4 + 100
    # s = "tracing the shot.... No of lines to be drawn is : "+ str(len(point_to_draw) -1) +"::: " + str(point_to_draw)
    # msg2screen(s,p,q)
    # pygame.display.update()

def in_boundary(trace_point):
    a,b = trace_point
    if a < 0 or b < 0 or a > dispWidth or b > dispHeight:
        return 0
    else:
        return 1

# def get_boundary_point(trace_point, m): # This function will be called only if the point is out of boundary :D
#     a,b = trace_point

def new_trace_the_shot(start_point, end_point, elevation, mouse_pos):
    a,b = end_point
    c,d = mouse_pos
    e,f = start_point
    
    move_dist       = sqrt((a-c)**2 + (b-d)**2)

    # Balls(self,(x,y),size, thickness=0, color=(0,0,255)):
    ball_point = Balls(start_point, 3, color=(255,0,0))
    
    # kkk = 2*pi/2
    kkk = pi
    slope_angle = elevation
    trace_angle = kkk - (slope_angle)

    # Ball.move(self,dist, angle, speed)
    ball_point.move(move_dist, trace_angle, speed = 8, smear=True)

    # p = dispWidth/4
    # q = 3*dispHeight/4
    # s = "tracing the shot....at angle : " + str(trace_angle*180/pi)
    s = "tracing the shot...................(" + str(slope_angle*180/pi) +").........(" + str(trace_angle*180/pi) + ")"
    print s
    # msg2screen(s,p,q)
    pygame.display.update()

# def new_stick_show(start_point, end_point, elevation):
#     a,b = end_point
#     e,f = start_point
    
#     move_dist       = sqrt((a-e)**2 + (b-f)**2)

#     # Balls(self,(x,y),size, thickness=0, color=(0,0,255)):
#     stick_ball_point = Balls(end_point, 5, color=(0,0,255))
    
#     # kkk = 2*pi/2
#     kkk = pi
#     slope_angle = elevation
#     trace_angle = kkk - (slope_angle)

#     # Ball.move(self,dist, angle, speed)
#     stick_ball_point.move_smear(move_dist, trace_angle, speed = 1.01)

#     pygame.display.update()

def gameLoop():
    gameExit = False
    gameOver = False
    stickLength = 100
    # stickList = []
    # prev_key = 0        # This is initialisation before the using in program :D
    # once = 0
    
    stick_loc = []
    no_of_balls = 3
    my_ball_size = 15
    all_balls = []              # List of my balls :D

    for i in xrange(no_of_balls):
        x = random.randint(my_ball_size, dispWidth - my_ball_size)
        y = random.randint(my_ball_size, dispHeight - my_ball_size)

        c1 = random.randint(0,255)
        c2 = random.randint(0,255)
        c3 = random.randint(0,255)

        all_balls.append(Balls((x,y), size = my_ball_size, color = (c1,c2,c3)))

    # Ball_1 = Balls((320,400),15)            # Fixed location ball
                                            # Initialising the ball here :D

    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    # screen = pygame.display.set_mode((dispHeight, dispWidth), 0, 32)
    while not gameExit:
        # print "General loop :D"
        while gameOver:
            gameDisplay.fill(GREEN)
            msg2screen("Game over, press Q to quit or C to continue.")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:

                # mods = pygame.key.get_mods()        # Assining a name, to use easily :D

                        
                if event.key == pygame.K_q:
                    gameOver = True
                # elif event.key == pygame.K_RCTRL: # This is for special R_CTRL key :D
                #     print "Inside the K_RCTRL loop :D"

        # I want to remove the border overloading problem. i.e. game should run even
        # after the stick crosses it. :D
        # stick will just come from other side, after it crosses the boundary :D

        #------------------
        # Ball_1 = Balls((320,400),15)            # Fixed location ball
        # Ball_2 = create_rand_Ball(40)           # Random location ball :D  # NOTE: This ball is not being usd currently :D
        # Ball_1.disp()

        show_pockets(2*my_ball_size)

        for my_ball in all_balls:       # Showing all my balls :D
            my_ball.disp()

        #Ball_2.disp()
        pygame.display.update()
        #------------------

        gameDisplay.fill(GREEN)

        mouse_pos = pygame.mouse.get_pos()

        # for x in xrange(0,640,20):
        #     pygame.draw.line(screen, (0, 0, 0), (x, 0), mouse_pos)              # (x,0) is start point and mouse_pos is end point :D
        #     pygame.draw.line(screen, (0, 0, 0), (x, 479), mouse_pos)

        # for y in xrange(0,480,20):
        #     pygame.draw.line(screen, (0, 0, 0), (0, y), mouse_pos)
        #     pygame.draw.line(screen, (0, 0, 0), (639, y), mouse_pos)
         # pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])
        
        # print "mouse location", mouse_pos
        # x = round(random.randrange(0, dispWidth - block_size)/10.0)*10
        mouse_butt = pygame.mouse.get_pressed()
        if mouse_butt[1] ==1:
            #move(self,dist, angle=self.angle, speed=self.speed):
            # temp1 = mouse_pos[0] - Ball_1.x
            # temp2 = -1* (mouse_pos[1] - Ball_1.y) # This -ve sign is to incorporate the inverted y-axis :D
            # if temp2 == 0:
            #     move_angle = (pi/2) * (temp1/abs(temp1)) # This is for the sign of than angle also :D
            # else:
            #     move_angle = atan(float(temp1)/temp2)
            # if mouse_pos[1] > Ball_1.y:
            #     move_angle += pi
            #     pass

            for my_ball in all_balls:

                move_angle = get_angle(mouse_pos, my_ball)

                # s = "Movement angle is " + str(move_angle*180/pi) + " in degrees " #:D
                # msg2screen(s,my_ball.x - 100, my_ball.y + 100)

                my_ball.move(50, move_angle,3)
                # Ball_1.move(50, pi/2, 1)
                pygame.display.update()
        #---------------
        # if mouse_butt[0] == 1:
        #     s = "left and right clicked "
        #     if mouse_butt[2]==0:
        #         s = "left pressed buttttttt right not clicked"
        #         msg2screen(s)
        #         pygame.display.update()
        #         pass
        #     msg2screen(s)
        #     pygame.display.update()
        # else:
        #     s = "left not pressed"
        #     msg2screen(s)
        #     pygame.display.update()
        #---------------
        
        # stick_loc = []
        if mouse_butt[0] == 1:

            # This logic is for saving the start point of stick :D
            # Otherwise its not possible to store the initial value of mouse_position :D
            temp = pygame.mouse.get_pos()
            mouse_pos = temp

            s,t = mouse_pos

            this_ball_status = 0
            # clicked_ball = []              #list of all balls which are clicked

            for my_ball in all_balls:
                this_ball_status = my_ball.is_clicked(s,t)
                
                if this_ball_status == 1:
                    clicked_ball = my_ball
                    break                           # Why breaking? Only single ball will be clicked, beacuase balls don't overlap :D

            if this_ball_status != 0:              # If mouse has left clicked on some ball then :D
                # def move(self,dist, angle, speed):
                move_angle  = get_angle(mouse_pos, clicked_ball)
                move_dist   = hypot(clicked_ball.x - mouse_pos[0], clicked_ball.y - mouse_pos[1])
                move_speed  = 3
                # clicked_ball.move(move_dist, move_angle, move_speed)
                clicked_ball.x = s
                clicked_ball.y = t

            else:                               # No ball is selected, hence continue your stick drawing :D
                stick_loc.append(temp)
                
                # if mouse_butt[2]==0:
                #     pass
                #--------------------------------------------------------------------
                mouse_pos = pygame.mouse.get_pos()
                
                x2 = mouse_pos[0] # First coordinate is x-cordinate :D
                y2 = mouse_pos[1]

                start_point = stick_loc[0]   # Here I am getting the start point value :D

                x1 = start_point[0]
                y1 = start_point[1]

                # slope of the line
                # m = float((y2-y1))/(x2-x1)              #          (y2-y1)
                                        #                (y-y1) =  ------- * (x-x1)                                      
                                                   #               (x2-x1) 
                # c = y1 - m*x1 # This is constant 

                # This checking for the distance between the two points greater than or less than the stickLength :D
                hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2)   
                while (hamming_dist > stickLength):
                    if abs(y2-y1) > abs(x2-x1):             # If the y side distnace is greater :D, so I will find point in that direction :D
                        if y2 > y1:
                            y2 = y2-1
                        else:
                            y2 = y2+1
                    else:
                        if x2 > x1:
                            x2 = x2-1
                        else:
                            x2 = x2+1

                    hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2) 

                end_point = (x2,y2)    # This is point that has been founf out successfully :D
                # (x,0) is start point and mouse_pos is end point :D
                # Last parameter is for the width of the line :D
                pygame.draw.line(gameDisplay, (0, 0, 0), start_point, end_point,10)           # This pretty bad line, no smppthness
                # pygame.draw.aaline(gameDisplay, (0, 0, 0), start_point, end_point,30)
                
                # pygame.draw.arc(gameDisplay, (255, 0, 0), ((100, 100), (200, 200)), 0, pi, 1)              
                mouse_butt = pygame.mouse.get_pressed()
                # print "mouse status", mouse_butt

                # This will move the stick if first button i.e. left is clicked
                # Distance of movement of stick will be given by the location of mouse from end of stick
                # Why?
                # This is kind of velocity thing
                # Farther the mouse more distance the stick will cover :D
                # NOTE: Stick will not cross the boundary of pool table :D
                pygame.display.update()                 
                #--------------------------------------------------------------------
            # Thought:
            # left click:       Fix the stick start point
            # middle click:     undo of left click and hang there freely
            # right click:      Hit the stick :D, and hang there freely

            
            # if mouse_butt[0] == 1:
            #     s = "only left"
            #     while (True):
            #         mouse_butt = pygame.mouse.get_pressed()
            #         if mouse_butt[1] == 1:
            #             s = "left -> middle"
            #             break
            #         elif mouse_butt[2] == 1:
            #             s = "left -> right"
            #             break
            #         break
                # ----------------------------------------------------------------------
                # Adding the ray tracing :D
                mouse_dist = sqrt((mouse_pos[0] - x1)**2 + (mouse_pos[1] - y1)**2)

                if (mouse_dist > stickLength):
                    
                    a,b = start_point
                    c,d = end_point
                    new_m = new_get_slope(a,b,c,d)  # Calculating this slope :D
                    
                    if new_m > 0:   # First and Third quadrant
                        if b < d:
                            elevation = pi + atan(new_m)
                        else:
                            elevation = atan(new_m)
                    else:           # Second and Fourth quadrant
                        if b < d:
                            elevation = pi + atan(new_m)
                        else:
                            elevation = 2*pi + atan(new_m)
                    # if abs(m)>1:
                    #     m = 1/m
                    for my_ball in all_balls:
                        my_ball.disp()
                        # Ball_1.disp()

                    # new_stick_show(start_point, end_point, elevation)

                    new_trace_the_shot(start_point, end_point, elevation, mouse_pos)
                    # print "elevation is :-------------------- (" + str(elevation*180/pi) + ")"

                if mouse_butt[2] == 1 : # & mouse_butt[0] == 0:
                    
                    x3 = mouse_pos[0] # First coordinate is x-cordinate :D
                    y3 = mouse_pos[1]

                    # x2,y2 are endpoint co-ordinates :D

                    # Movement distance :D
                    move_dist = sqrt((y2-y3)**2+(x2-x3)**2)

                    # if (x2-x1)!=0:
                    #     m1 = float(y2-y1)/(x2-x1)
                    #     print "in y", m1

                    # if (y2-y1)!=0:
                    #     m2 = float(x2-x1)/(y2-y1)
                    #     print "in x", m2

                    curr_dist = 1   # This is current distance achieved :D
                    # out_msg = "Moving distance is "  + str(move_dist)
                    # msg2screen(out_msg,dispWidth/4,dispHeight/4)

                    while (start_point[0] > 0) & (start_point[0] < dispWidth) & (start_point[1] > 0) & (start_point[1] < dispHeight) & (curr_dist < move_dist):
                        # hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2)   

                        m = get_slope(x1,y1,x2,y2)                        
                        if abs(m)>1:
                            m = 1/m

                        # -------------------------
                        # Note down the ordering of elements :D
                        start_point = get_points(x1,y1,x2,y2,curr_dist,m,0)         # choice = 0, for start point
                        end_point = get_points(x2,y2,x1,y1,curr_dist,m,1)           # choice = 1, for end point

                        curr_dist += 1
                        # Last parameter is for the width of the line :D
                        gameDisplay.fill(GREEN)
                        pygame.draw.line(gameDisplay, (255, 0, 0), start_point, end_point,20)           # This pretty bad line, no smppthness
                        pygame.display.update()
                        #---------
                        # If this moving stick hits a ball then, break from this loop (to stop stick movement)
                        # and move the ball :D
                        # Ball will moved by the "remaining" distance with which the stick was supposed to move :D
                        # That remaining distance is "move_dist-curr_dist"

                        # condition for checking the stick hits the ball
                        # if start_point == (Ball_1.x, Ball_1.y):

                        for my_ball in all_balls:

                            if ball_got_hit(start_point, my_ball):
                                ball_move_dist = move_dist - curr_dist

                                temp_angle = get_angle(end_point, my_ball)   # Passing the end point and Ball object to get the movement angle
                                move_angle = temp_angle + pi                # Why this??? Ball should move in opposite direction from where it is being hit :D
                                move_speed = 3                              # You can choose more high speed :D

                                my_ball.move_with_collision_correction(dist = ball_move_dist, angle = move_angle, speed = move_speed, list_of_ball_objects = all_balls)
                                # move_with_collision_correction(self,dist=None, angle = None, speed=3, list_of_ball_objects =[]):
                                pygame.display.update()
                                break
                                # move(self,dist, angle, speed):
                            #----------
                        temp_all_balls = [my_ball for my_ball in all_balls if my_ball.pocketed==0]
                        all_balls = temp_all_balls
                        # After looping out of the list, I must reassign it, with removing
                                                            # the pocketed balls :D
                        if all_balls == []: # If all balls are pocketed then, quit the game :D
                            gameOver = True
                        
                        pygame.display.update()
        
        else:
            # This is like whenever I am not holding the stick to initialise,
            # clear the points in that :D
            stick_loc = []
                
        clock.tick(FPS)
        # s = "Length of stick_loc is: "+ str(len(stick_loc))
        # msg2screen(s)
        pygame.display.update()

    pygame.quit()
    print "++++-----------------------------------++++"
    quit()

if __name__ == '__main__':
    gameLoop()
