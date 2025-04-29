# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : BENAMER BELKACEM Inès - 21204927
#  Prénom Nom No_étudiant/e : COMBO Lyna - 21201927
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import math

nb_robots = 0
random.seed(None)

class Robot_player(Robot):

    team_name = "Citron abandonné sur la table" 
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = random.choice([-1,1])              # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.memory = 0
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view, sensor_robot, sensor_team=None):
        translation = sensors[sensor_front]
        rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1

        
        # match self.id :

        if self.id==0 : # Traveler
            ennemi = False
            for i in range(8) :
                    if sensors[i]<0.4 and sensor_view[i]==2 and sensor_robot[i]!=self.team : # Si on a un robot de l'équipe adverse à proximité
                        ennemi = True
                        ennemis.append(sensors[i])
                    else :
                        ennemis.append(0)
                        
            if ennemi : 
                rotation = sum([ennemis[i]*(sensors[i]) for i in range(8)]) + math.tanh ( P[4] + P[5] * sensors[sensor_front_left] + P[6] * sensors[sensor_front] + P[7] * sensors[sensor_front_right])
                
            else : 
                rotation = math.tanh ( P[4] + P[5] * sensors[sensor_front_left] + P[6] * sensors[sensor_front] + P[7] * sensors[sensor_front_right] )
 
                
            
            
            P = [1, 0, 1, 1, -1, 1, 1, -1] # Paramètres optimisés pour maximiser la distance à l'origine dans robot_travelling.py
            translation = math.tanh ( P[0] + P[1] * sensors[sensor_front_left] + P[2] * sensors[sensor_front] + P[3]* sensors[sensor_front_right] )

        elif self.id==1 : #Homebody
            if(sensors.index(min(sensors)) in [0,1,7] and min(sensors) <0.6) : # Est-ce qu'il y a quelque chose devant moi ?
                P = [1, 1, 0, 0, 0, 0, 0, 1] # Paramètres optimisés dans robot_homebody.py
                rotation = sum([P[i]*sensors[i] for i in range(8)] )
                translation = sum([P[i]*sensors[i] for i in range(8)] )
            else : 
                P = [1, 0, 1, 1, random.choice([-1,1,0]), 1, 1, -1]
                translation = math.tanh ( P[0] + P[1] * sensors[sensor_front_left] + P[2] * sensors[sensor_front] + P[3]* sensors[sensor_front_right] )
                rotation = math.tanh ( P[4] + P[5] * sensors[sensor_front_left] + P[6] * sensors[sensor_front] + P[7] * sensors[sensor_front_right] )
        
   
        elif self.id==2 : # Straight Foward
            if sensor_view[sensors.index(min(sensors))]==1 and min(sensors) <0.02 :
                self.memory += 1
        
            if( self.memory> 5 or (sensor_view[sensors.index(min(sensors))]==1 and sensor_robot[sensors.index(min(sensors))]==self.team) or (sensor_view[sensors.index(min(sensors))]==1 and sensors.index(min(sensors)) not in [3,4,5] and (sensors[sensor_front] < 0.5 or min(sensors) < 0.3) and (abs(sensors.index(min(sensors))) - (sensors.index(min(sensors)))+4)%8> 0.05) ) :
                            rotation = 1 if sum(sensors[1:4]) > sum(sensors[5:]) else -1
                            translation = 0.2

            else : 
                self.memory = 0         
                ennemi = False
                ennemis = []
                P = [0, 1, 1, -1, 0, -1, 0, 1]
                
                for i in range(8) :
                    if sensors[i]<0.4 and sensor_view[i]==2 and sensor_robot[i]!=self.team : # Si on a un robot de l'équipe adverse à proximité
                        ennemi = True
                        ennemis.append(sensors[i])
                    else :
                        ennemis.append(0)
                        
                if ennemi : 
                    rotation = sum([ennemis[i]*(1-sensors[i]) for i in range(8)]) + math.tanh ( P[4] + P[5] * sensors[sensor_front_left] + P[6] * sensors[sensor_front] + P[7] * sensors[sensor_front_right])
                
                else : 
                    # Sinon : tout droit
                    
                    rotation = math.tanh ( P[4] + P[5] * sensors[sensor_front_left] + P[6] * sensors[sensor_front] + P[7] * sensors[sensor_front_right])
            
                translation = math.tanh ( P[0] + P[1] * sensors[sensor_front_left] + P[2] * sensors[sensor_front] + P[3]* sensors[sensor_front_right])

        elif self.id==3 : #Avoider
            PR = [-1, -1, 0, 0, 0, 0, 0, -1 ] 

            translation = sensors[sensor_front]*0.3
            rotation = sum([PR[i]*(1-sensors[i]) for i in range(8)])*0.4
            

        return translation, rotation, False
