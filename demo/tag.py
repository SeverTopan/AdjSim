"""
    
"""

from adjsim import simulation, agent, utility

def move(environment, source_agent):
    movment = numpy.Array(sin(source_agent.movement_theta), cos(source_agent.movement_theta))
    movement *= source_agent.movement_theta
    source_agent.pos += movement
    source_agent.complete = True

def tag(environment, source_agent):  

    if not source_agent.is_it:
        return

    nearest_neighbour = environment.indies.spatial.nearest_neighbour(source_agent)

    if utility.distance(nearest_neighbour, source_agent) > 5:
        return

    nearest_neighbour.is_it = True
    source_agent.is_it = False
    nearest_neighbour.complete = True

def loss_function(environment, source_agent):
    return float(source_agent.is_it)

def perception(environment, source_agent):
    nearest_neighbour = environment.indies.spatial.nearest_neighbour(source_agent)
    return (nearest_neighbour.x, nearest_neighbour.y, nearest_neighbour.is_it)

def intelligence(observation, loss, source_agent):
    # stuff
    return move


class Tagger(Agent):

    def __init__(self, pos):
        super(tagger, self).__init__()

        self.is_it = False
        
        @mutable_action_parameter(float, 0, 360)
        self.movement_theta

        @mutable_action_parameter(float, 0, 10)
        self.movement_rho

        self.action_suite = [move, tag]
        self.loss_function = loss_function
        self.intelligence = intelligence


def generate_environment(simulation):
    simulation.environment.clear()

    for i in range(5):
       for j in range(5):
           simulation.environemnt.agents.add(Tagger([10 * i, 10* j]))
