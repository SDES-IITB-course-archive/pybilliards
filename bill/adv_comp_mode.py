#!/usr/bin/python
#
# This is implementation of COMP mode.
# Computer will play and pocket the balls available on screen, with some factor of intellengece (manually set)
# ----------------------------------------------------------------------------------------------------------
import pygame
import random
from math import *

from classes_and_modules.all_functions import *
from classes_and_modules.env_variables import *
from classes_and_modules.Balls_class import Balls

pygame.init()
pygame.display.update()
# ballsurface = pygame.Surface((50, 50))
# pygame.draw.circle(ballsurface, (0,0,255), (25, 25), 25)
# gameDisplay.blit(ballsurface, (x,y))
# pygame.display.flip()


def gameLoop():
    gameExit = False
    gameOver = False
    stickLength = 100
    # stickList = []
    # prev_key = 0        # This is initialisation before the using in program
    # once = 0
    # stick_loc = []
    # no_of_balls = 10    # 3
    # my_ball_size = 20   # 25

    all_balls = []              # List of balls

    # The white cue ball positioning and initialization (random for now)
    for i in xrange(1):
        x = random.randint(my_ball_size, dispWidth - my_ball_size)
        y = random.randint(my_ball_size, dispHeight - my_ball_size)
        white_ball = Balls((x, y), size=my_ball_size, thickness=6, color=WHITE)
        white_ball.disp()

    # Other balls initialization
    for i in xrange(no_of_balls):
        x = random.randint(my_ball_size, dispWidth - my_ball_size)
        y = random.randint(my_ball_size, dispHeight - my_ball_size)

        c1 = random.randint(0, 255)
        c2 = random.randint(0, 255)
        c3 = random.randint(0, 255)

        all_balls.append(Balls((x, y), size=my_ball_size, color=(c1, c2, c3)))
    # screen = pygame.display.set_mode((dispHeight, dispWidth), 0, 32)
    while not gameExit:
        while gameOver:
            gameDisplay.fill(GREEN)
            msg2screen("Game over, press Q to quit or C to continue.")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
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
                if event.key == pygame.K_q:
                    gameOver = True

        # gameDisplay.fill(BLACK)
        gameDisplay.fill(GREEN)
        # scoreDisplay.fill(red)
        my_pocket_size = 2*my_ball_size
        show_pockets(my_pocket_size)

        for my_ball in all_balls:  # Put all balls
            my_ball.disp()
        white_ball.disp()  # Put white ball
        pygame.display.update()

        mouse_pos = pygame.mouse.get_pos()

        # list_of_balls_with_white = [a_ball for a_ball in all_balls]
        list_of_balls_with_white = all_balls + [white_ball]

        mouse_butt = pygame.mouse.get_pressed()
        if mouse_butt[1] == 1:
            # Pressed by the user manually, to start COMP to hit the right shot
            # Next shot placement, which ball to hit, is decided by the COMP,
            # depending on the some other factors (or may be randomly)

            my_pocket_size = 2 * my_ball_size
            show_pockets(my_pocket_size)

            # balls_ok_to_hit = []
            # Following loop will extract hittable balls from all_balls :D
            # Then we will decide which one to hit from those :D
            for my_ball in all_balls:
                # List of other ball except current ball :D
                list_of_other_balls = all_balls[:]
                list_of_other_balls.remove(my_ball)
                balls_to_be_tested = []
                for other_ball in list_of_other_balls:
                    dist_white_other = hypot(white_ball.x-other_ball.x, white_ball.y-other_ball.y)
                    dist_my_other = hypot(my_ball.x-other_ball.x, my_ball.y-other_ball.y)
                    # Distance between white and other ball,
                    # and my_ball and other ball

                    dist_my_white = hypot(white_ball.x - my_ball.x, white_ball.y - my_ball.y)
                    if (dist_my_white > dist_white_other) & (dist_my_white > dist_my_other):
                        # test this other_ball location,
                        # since it is in between my_ball and white_ball
                        balls_to_be_tested.append(other_ball)
                p, q = my_ball.x + 10, my_ball.y + 10
                # s = "T: " + str(len(balls_to_be_tested))
                # msg2screen(s, p, q)
                # pygame.display.update()
                if len(balls_to_be_tested) == 0:
                    my_ball.ok_to_hit = 1
                else:
                    x1, y1 = white_ball.x, white_ball.y
                    x2, y2 = my_ball.x, my_ball.y

                    # Testing for balls and their distance
                    for test_ball in balls_to_be_tested:
                        x3, y3 = test_ball.x, test_ball.y

                        # I will find of the perpendicular distance of
                        # point (x3, y3) from the line formed by the
                        # two points (x2, y2), and (x1, y1)

                        # Line equation in the form of Ax+ By+ C = 0
                        # formed by the two points x2,y2 and x1,y1 is
                        A = tan(atan2(y2-y1, x2-x1))  # slope of line
                        B = -1
                        C = y1 - A*x1
                        # formula is permutation from two point line equation

                        # Perpendicular distance is given by
                        # Reference: goo.gl/mUFJSh
                        perp_dist = abs(A*x3 + B*y3 + C) / hypot(A, B)
                        if perp_dist > 2*(test_ball.size + white_ball.size):
                            # Here multiplier 2 is taken to be sure of distance
                            my_ball.in_line_with_white_ball = 1
                        else:
                            my_ball.in_line_with_white_ball = 0
                            # Why to break? Beacause this means that some comes
                            # between line of sight, hence can't test break it
                            break

                    if my_ball.in_line_with_white_ball == 1:
                        # If that ball is hittable after testing will all balls
                        my_ball.ok_to_hit = 1
                    else:
                        my_ball.ok_to_hit = 0

            balls_ok_to_hit = [a_ball for a_ball in all_balls if a_ball.ok_to_hit == 1]
            # So hittable balls are extracted :D
            # This small loop will show which are able show hittable balls, some timepass programming :D
            for hit_ball in balls_ok_to_hit:
                p,q = hit_ball.x + 20, hit_ball.y + 20
                s = "OK to hit"
                msg2screen(s,p,q)
                pygame.display.update()

            # at_least_one_ball_hit = 0       # 0 is for NO
            p,q = dispWidth/2, dispHeight/2

            s = "Ok to hit balls is " + str(len(balls_ok_to_hit))
            # print balls_ok_to_hit
            msg2screen(s,p,q)

            ok_to_hit_but_cannot_be_pocketed = 0

            #==============
            # Clearing the angles and their distances :D
            
            # all_balls_with_white = [a_ball for a_ball in all_balls]
            # all_balls_with_white.append(white_ball)
            for a_ball in list_of_balls_with_white:
                a_ball.angle    = 0
                a_ball.dist     = 0
            #==============

            for hit_ball in balls_ok_to_hit:
                # if hit_ball.ok_to_hit == 1:     # Not needed actually, but being sure
                # Tracing the shot for white
                white_ball_loc  = (white_ball.x, white_ball.y)
                hit_ball_loc     = (hit_ball.x, hit_ball.y)

                
                all_balls_except_hit_ball_but_with_white_ball = [a_ball for a_ball in all_balls if a_ball != hit_ball]
                all_balls_except_hit_ball_but_with_white_ball.append(white_ball)
                
                # print "No. of Passing balls for tracing is " + str(len(all_balls_except_hit_ball_but_with_white_ball))
                will_it_be_pocketed = trace_for_while_ball_shot(hit_ball_loc, white_ball_loc, all_balls_except_hit_ball_but_with_white_ball)

                    # p, q = hit_ball.x + 30, hit_ball.y + 30
                    
                #============
                my_pocket_size = 2*my_ball_size
                show_pockets(my_pocket_size)
                #============
                if will_it_be_pocketed == 1:
                    
                    temp_angle = get_angle(white_ball_loc, hit_ball)   # Passing the end point and Ball object to get the movement angle
                    move_angle = temp_angle + pi

                    # Here I am giving dist between 50 and 150, it is high distance :D. Its required so that ball can be hit hard :D
                    # rand_dist = random.randint(50,150)
                    rand_dist = 100

                    # list_of_balls_with_white = [a_ball for a_ball in all_balls]
                    # list_of_balls_with_white.append(white_ball)

                    # white_ball.move_with_collision_correction(dist = rand_dist, angle = move_angle, list_of_ball_objects = list_of_balls_with_white)

                    white_ball.dist = rand_dist
                    white_ball.angle = move_angle

                    move_my_all_balls(list_of_balls_with_white)

                    # at_least_one_ball_hit = 1               # 1 is for YES, on ball got hit, hence breaking :D

                    # p, q = hit_ball.x + 30, hit_ball.y + 30
                    # s = "is being hit :D"
                    # print s
                    # msg2screen(s,p,q)
                    # Why are your breaking?
                    # Ans: Since in one chance COMP hit one ball
                    break;
                else:
                    ok_to_hit_but_cannot_be_pocketed += 1

            #--------------------------------------------
            # Rotational moving
            # white_ball will try to see at different angles to hit the ball, which can not be pocketed
            # directly, but ok to hit
            #
            # For a ball from list of such above balls, angle of white_ball will be varied and its path 
            # will be traced, if that ball can be pocketed, then loop will break, and white_ball will
            # hit it. I will set a flag, rotate_pocketed = 1
            if (ok_to_hit_but_cannot_be_pocketed == len(balls_ok_to_hit)) & (len(balls_ok_to_hit) > 0):
                my_pocket_size = 2*my_ball_size
                show_pockets(my_pocket_size)

                for a_ball in balls_ok_to_hit:
                    dist_sep = hypot(a_ball.x - white_ball.x, a_ball.y - white_ball.y)
                    tangent_dist = hypot(dist_sep, a_ball.size)
                    half_cone_angle = acos(dist_sep/tangent_dist)

                    angle_resolution = 5
                    # 10 parts to revolve through 2 * half_cone_angle
                    print "Half cone angle is :%d"%(half_cone_angle*180/pi)
                    white_ball.angle = get_angle(white_ball_loc, a_ball) - half_cone_angle + pi
                    base_angle = white_ball.angle

                    rotate_pocketed = 0
                    for i in xrange(angle_resolution):
                        # a_ball_loc = (a_ball.x, a_ball.y)
                        # white_ball_loc = (white_ball.x, white_ball.y)
                        # all_balls_except_a_ball_but_with_white_ball = [temp_ball for temp_ball in list_of_balls_with_white if temp_ball != a_ball]
                        pygame.display.update()
                        # will_it_be_pocketed = trace_for_rotated_white_ball_shot(a_ball, white_ball, all_balls_except_a_ball_but_with_white_ball)
                        print "White ball's angle is: %d" %(white_ball.angle*180/pi)
                        will_it_be_pocketed = trace_for_rotated_white_ball_shot(a_ball, white_ball, list_of_balls_with_white)
                        if will_it_be_pocketed == 1:
                            print "|--------------------------|"
                            print "|---Yo billaird I got you--|"
                            print "|--------------------------|"
                            rotate_pocketed = 1
                            break
                        white_ball.angle = base_angle + 2*(i+1)*half_cone_angle/angle_resolution
                        print "Ball status %d @%d" %(will_it_be_pocketed, i)

                    if rotate_pocketed == 1:
                        # white_ball.move_with_collision_correction(dist = 50, angle = white_ball.angle, list_of_ball_objects = list_of_balls_with_white)
                        white_ball.dist = 50
                        move_my_all_balls(list_of_balls_with_white)
            #--------------------------------------------

            # #===============================
            # # Below is random hitting :D
            
            # if (ok_to_hit_but_cannot_be_pocketed == len(balls_ok_to_hit)) & (len(balls_ok_to_hit) > 0):
            #     #============
            #     my_pocket_size = 2*my_ball_size
            #     show_pockets(my_pocket_size)
            #     #============

            #     # This means that, there is atleast one ball which can be hit, but cannot be pocketed,
            #     # then, out of those balls_ok_to_hit, choose any one randomly and hit it :D
                
            #     print "Choosing ball randomly to hit"
            #     temp_loc = random.randint(0,len(balls_ok_to_hit)-1)
            #     rand_ball_to_hit = balls_ok_to_hit[temp_loc]

            #     # temp_angle = get_angle(white_ball_loc, rand_ball_to_hit)   # Passing the end point and Ball object to get the movement angle
            #     # move_angle = temp_angle + pi

            #     # # Here I am giving dist between 50 and 150, it is high distance :D. Its required so that ball can be hit hard :D
            #     # # rand_dist = random.randint(50,150)
            #     # rand_dist = 300

            #     # list_of_balls_with_white = [a_ball for a_ball in all_balls]
            #     # list_of_balls_with_white.append(white_ball)

            #     # white_ball.move_with_collision_correction(dist = rand_dist, angle = move_angle, list_of_ball_objects = list_of_balls_with_white)

            #     #===============================
            #     temp_angle = get_angle(white_ball_loc, rand_ball_to_hit)   # Passing the end point and Ball object to get the movement angle
            #     move_angle = temp_angle + pi

            #     # Here I am giving dist between 50 and 150, it is high distance :D. Its required so that ball can be hit hard :D
            #     # rand_dist = random.randint(50,150)
            #     rand_dist = 100

            #     # list_of_balls_with_white = [a_ball for a_ball in all_balls]
            #     # list_of_balls_with_white.append(white_ball)

            #     # white_ball.move_with_collision_correction(dist = rand_dist, angle = move_angle, list_of_ball_objects = list_of_balls_with_white)

            #     white_ball.dist = rand_dist
            #     white_ball.angle = move_angle

            #     move_my_all_balls(list_of_balls_with_white)
            #     #===============================

            if len(balls_ok_to_hit) == 0:
                gameOver = True

            temp_all_balls = [my_ball for my_ball in all_balls if my_ball.pocketed==0]
            all_balls = temp_all_balls

            if white_ball.pocketed == 1:
                white_ball = Balls((x,y), size = my_ball_size, thickness = 6, color = (255,255,255))
            # After looping out of the list, I must reassign it, with removing
                                                # the pocketed balls :D
            if all_balls == []: # If all balls are pocketed then, quit the game :D
                gameOver = True
            
            pygame.display.update()
        #=====================================================================================================================
        # if mouse_butt[1] == 1:
        #     for my_ball in all_balls:

        #         move_angle = get_angle(mouse_pos, my_ball)

        #         # s = "Movement angle is " + str(move_angle*180/pi) + " in degrees " #:D
        #         # msg2screen(s,my_ball.x - 100, my_ball.y + 100)

        #         my_ball.move(50, move_angle,3)
        #         # Ball_1.move(50, pi/2, 1)
        #         pygame.display.update()
        #=====================================================================================================================
        
        

        if mouse_butt[0] == 1:      

            my_pocket_size = 2*my_ball_size
            show_pockets(my_pocket_size)

            # for my_ball in all_balls:
            #     my_ball.disp()
            # white_ball.disp()

            # This logic is for saving the start point of stick :D
            # Otherwise its not possible to store the initial value of mouse_position :D
            temp = pygame.mouse.get_pos()
            mouse_pos = temp

            s,t = mouse_pos

            this_ball_status = 0
            # clicked_ball = []              #list of all balls which are clicked
            # list_of_balls_with_white = [a_ball for a_ball in all_balls]
            # list_of_balls_with_white.append(white_ball)

            for my_ball in list_of_balls_with_white:
                this_ball_status = my_ball.is_clicked(s,t)
                
                if this_ball_status == 1:
                    clicked_ball = my_ball
                    break                           # Why breaking? Only single ball will be clicked, beacuase balls don't overlap :D

            if this_ball_status != 0:              # If mouse has left clicked on some ball then :D
                # def move(self,dist, angle, speed):
                # move_angle  = get_angle(mouse_pos, clicked_ball)
                # move_dist   = hypot(clicked_ball.x - mouse_pos[0], clicked_ball.y - mouse_pos[1])
                # move_speed  = 3
                # clicked_ball.move(move_dist, move_angle, move_speed)
                clicked_ball.x = s
                clicked_ball.y = t

                stick_loc = []                  # Don't know is it right or not. Works without it also :D

            else:                               # No ball is selected, hence continue your stick drawing :D
                
                stick_loc.append(temp)
                
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

                end_point = (x2,y2)    # This is point that has been found out successfully :D
                # (x,0) is start point and mouse_pos is end point :D
                # Last parameter is for the width of the line :D
                pygame.draw.line(gameDisplay, (0, 0, 0), start_point, end_point,10)           # This pretty bad line, no smppthness
                
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
                    
                        # Ball_1.disp()

                    # new_stick_show(start_point, end_point, elevation)

                    new_trace_the_shot(start_point, end_point, elevation, mouse_pos)
                    pygame.display.update()
                    # print "elevation is :-------------------- (" + str(elevation*180/pi) + ")"

                if mouse_butt[2] == 1 : # & mouse_butt[0] == 0:
                    mouse_pos = pygame.mouse.get_pos()
                    x3 = mouse_pos[0] # First coordinate is x-cordinate :D
                    y3 = mouse_pos[1]

                    # x2,y2 are endpoint co-ordinates :D

                    # Movement distance :D
                    # move_dist = sqrt((y2-y3)**2+(x2-x3)**2)
                    move_dist = hypot(y2-y3, x2-x3)

                    curr_dist = 1   # This is current distance achieved :D
                    # out_msg = "Moving distance is "  + str(move_dist)
                    # msg2screen(out_msg,dispWidth/4,dispHeight/4)

                    while (start_point[0] > 0) & (start_point[0] < dispWidth) & (start_point[1] > 0) & (start_point[1] < dispHeight) & (curr_dist < move_dist):
                        # hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2)
                        m = get_slope(x1, y1, x2, y2)
                        if abs(m) > 1:
                            m = 1/m
                        # Note down the ordering of elements :D
                        start_point = get_points(x1, y1, x2, y2, curr_dist, m, 0)  # choice = 0, for start point
                        end_point = get_points(x2, y2, x1, y1, curr_dist, m, 1)  # choice = 1, for end point
                        curr_dist += 2
                        # Last parameter is for the width of the line :D
                        # gameDisplay.fill(GREEN)
                        pygame.draw.line(gameDisplay, (255, 0, 0), start_point, end_point,20)           # This pretty bad line, no smppthness
                        pygame.display.update()
                        # If this moving stick hits a ball then, break from this loop (to stop stick movement)
                        # and move the ball :D
                        # Ball will moved by the "remaining" distance with which the stick was supposed to move :D
                        # That remaining distance is "move_dist-curr_dist"

                        # condition for checking the stick hits the ball
                        # if start_point == (Ball_1.x, Ball_1.y):

                        # all_balls_with_white = [a_ball for a_ball in all_balls]
                        # all_balls_with_white.append(white_ball)
                        for my_ball in list_of_balls_with_white:

                            if ball_got_hit(start_point, my_ball):
                                ball_move_dist = move_dist - curr_dist

                                temp_angle = get_angle(end_point, my_ball)   # Passing the end point and Ball object to get the movement angle
                                move_angle = temp_angle + pi                # Why this??? Ball should move in opposite direction from where it is being hit :D
                                move_speed = 10                              # You can choose more high speed :D

                                # my_ball.move_with_collision_correction(dist = ball_move_dist, angle = move_angle, speed = move_speed, list_of_ball_objects = all_balls_with_white)
                                my_ball.dist = ball_move_dist
                                my_ball.angle = move_angle
                                my_ball.speed = move_speed

                                move_my_all_balls(list_of_balls_with_white)
                                # move_with_collision_correction(self,dist=None, angle = None, speed=3, list_of_ball_objects =[]):
                                # pygame.display.update()

                                curr_dist = move_dist
                                # This will ensure the stick (red) will not move any further after hitting a ball :D
                                break
                                # move(self,dist, angle, speed):
                            #----------
                        if white_ball.pocketed == 1:
                            x = random.randint(my_ball_size, dispWidth - my_ball_size)
                            y = random.randint(my_ball_size, dispHeight - my_ball_size)

                            c1 = 255            # white ball
                            c2 = 255
                            c3 = 255
                            white_ball = Balls((x,y), size = my_ball_size, thickness = 6, color = (255,255,255))
                            white_ball.disp()

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
        # pygame.display.update()

    pygame.quit()
    print "++++-----------------------------------++++"
    quit()

if __name__ == '__main__':
    gameLoop()
