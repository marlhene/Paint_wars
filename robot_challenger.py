# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : _________
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        translation = sensors[sensor_front]
        rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
        return translation, rotation, False

class Robot_traveler(Robot_player):
    """
    Robot ayant pour stratégie par défaut de s'éloigner le plus possible de la base.
    """

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None) :

        # Paramètres par défaut
        translation = sensors[sensor_front]
        rotation = 0

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # Parcours de l'arbre de décision :

        if(sensor_to_wall.index(min(sensor_to_wall)) == 0 and sensor_to_wall[0] < 0.3) : # Il y a un mur devant moi (coincé)
            PR = [1, 1, 1, 1, -1, -1, -1, -1]
            rotation = sum(PR[i]* sensor_to_wall[i] for i in range(8))
            translation = -(1-sensors[sensor_front])
        
        else:

            # Check si suivi
            if (self.memory and self.memory > min(sensor_to_robot[3:6])) : 
                translation = min(1, 2*sensors[sensor_front]) # Il y a qq derrière moi

                # Mise à jour mémoire
                self.memory = min(sensor_to_robot[3:6]) if min(sensor_to_robot[3:6]) < 1 else None

            else : 
            
                if(sensor_to_robot[0]+sensor_to_robot[1]+sensor_to_robot[7] < 3) :# Robot devant
                    idx = list(filter(lambda x : x in [0,1,7], sorted(range(8), key = lambda y : sensor_to_robot[y])))[0]

                    # Check si dans la même team
                    if (sensor_team[idx] == self.team) :
                        rotation = 1
                    else : rotation = 0.25
                
                else : # Adoption du comportement normal
                    P = [1, 0, 1, 1, -1, 1, 1, -1] # Paramètres optimisés pour maximiser la distance à l'origine dans robot_travelling.py
                    translation = math.tanh ( P[0] + P[1] * sensors[sensor_front_left] + P[2] * sensors[sensor_front] + P[3]* sensors[sensor_front_right] )
                    rotation = math.tanh ( P[4] + P[5] * sensors[sensor_front_left] + P[6] * sensors[sensor_front] + P[7] * sensors[sensor_front_right] )

        return translation, rotation, False

class Robot_homebody():
    """
    Robot qui priorise l'espace autour de lui

    """
    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None) :

        # Paramètres par défaut
        translation = sensors[sensor_front]
        rotation = 0

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # Parcours de l'arbre de décision :

        if(sensor_to_wall.index(min(sensor_to_wall)) == 0 and sensor_to_wall[0] < 0.3) : # Il y a un mur devant moi (coincé)
            PR = [1, 1, 1, 1, -1, -1, -1, -1]
            rotation = sum(PR[i]* sensor_to_wall[i] for i in range(8))
            translation = -(1-sensors[sensor_front])
        
        else:

            # Check si suivi
            if (self.memory != 1 and self.memory > min(sensor_to_robot[3:6])) : 
                translation = min(1, 2*sensors[sensor_front]) # Il y a qq derrière moi

                # Mise à jour mémoire
                self.memory = min(sensor_to_robot[3:6]) 

            else : 
                if(sensor_to_robot[0]+sensor_to_robot[1]+sensor_to_robot[7] < 3): # Robot devant
                    idx = list(filter(lambda x : x in [0,1,7], sorted(range(8), key = lambda y : sensor_to_robot[y])))[0]

                    # Check si dans la même team
                    if (sensor_team[idx] == self.team) :
                        rotation = 1
                    else : rotation = 0.25
                
                else : # Adoption du comportement normal
                    P = [1, 1, 1, 1, -1, 0, -1, -1] # Paramètres optimisés pour maximiser l'exploration autour de soi à l'aide de robot_homebody.py
                    translation = math.tanh ( P[0] + P[1] * sensors[sensor_front_left] + P[2] * sensors[sensor_front] + P[3]* sensors[sensor_front_right])
                    rotation = math.tanh ( P[4] + P[5] * sensors[sensor_front_left] + P[6] * sensors[sensor_front] + P[7] * sensors[sensor_front_right])*0.5

        return translation, rotation, False