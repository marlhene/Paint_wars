# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 0
arena = 1
position = False 
max_iterations = 2000 #401*500

# affichage

display_welcome_message = False
verbose_minimal_progress = True # display iterations
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_dumb as rd, robot_braintenberg_avoider as rba, robot_braintenberg_loveBot as rbl, robot_subsomption as rbs

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    #x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    robots.append(rbs.Robot_player(4, 10, 0, name="Ines", team="A"))
    robots.append(rd.Robot_player(4, 20, 0, name="Lyna", team="A"))
    robots.append(rd.Robot_player(4, 30, 0, name="Lyna", team="A"))
    robots.append(rd.Robot_player(4, y_center, 0, name="Lyna", team="A"))

    robots.append(rd.Robot_player(80, 10, 0, name="Ines", team="A"))
    robots.append(rd.Robot_player(80, 20, 0, name="Lyna", team="A"))
    robots.append(rd.Robot_player(80, 30, 0, name="Lyna", team="A"))
    robots.append(rd.Robot_player(80, y_center, 0, name="Lyna", team="A"))
    return robots
