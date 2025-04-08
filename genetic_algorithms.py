
from robot import * 
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = [] # [param, translation, rotation, distance]
    it_per_evaluation = 400
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]
    current_score = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation
        self.evaluations = evaluations
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()
    

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")
        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        
        if(self.trial*3 > 500):
            self.param = self.bestParam[-1].copy() # Récupération des paramètres
            print("Paramètre meilleur : ", self.bestParam)

        elif self.iteration % self.it_per_evaluation == 0: # 400 tours 
            
            if self.iteration > 0:
                # Stockage dans best_param :
                print ("\tparameters           =",self.param)
                print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                
                
            # Comparaison des stratégies
            self.current_score +=self.log_sum_of_translation*(1-abs(self.log_sum_of_rotation))

            if (self.trial %3 == 0 and (not(self.bestParam) or self.bestParam[-2] > self.current_score)):
                self.bestParam = ([self.trial, self.current_score, self.param.copy()])
                self.current_score = 0
                self.theta_0 = random.choice([0,90,180,360])
                self.param = [random.randint(-1, 1) for i in range(8)]

            # Génération des nouveaux points de début
            self.trial = self.trial + 1
            print("Trying strategy no.",self.trial//3, " position initiale ", self.trial %3)
            self.iteration = self.iteration + 1
            return 0, 0, True # ask for reset

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1        

        return translation, rotation, False

    def genetic_algorithm(params, mu=1, lambd=1) : 
        change = random.randint(0, len(params)-1)
        child = params[:change] + [math.abs(params[change]-1)] + params[change+1:]
        return child