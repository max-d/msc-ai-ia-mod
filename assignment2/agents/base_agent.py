import time

from agents.lib import Message

"""
Basic Intelligence Agent Class This class represents Intelligence Agent's architecture: the agent percepts 
environment via sensors, analyse gathered data with an analysis module, and produces some actions via actuator. The 
class only implements modules communication logic, while all the business logic of modules is encapsulated into 
separated classes. The modes logic injected into Agent class through the "constructor" method by passing modules 
objects. This approach allows to create any amount of agents with same or different behaviour using just one 
universal Agent class with predefined structure, making implementation of multi agent system simpler and more 
transparent, and allowing to focus on implementing particular modules and creating new agent from building blocks 
rather than developing new agents from scratch.
"""


class Agent:

    def __init__(self, name, sensor, actuator, analysis_module):
        """Constructor for Agent class
        
        Args:
            name(string): module name, that will appear
                and logs and used for communication via Messages
            sensor(object): instance of sensor class, 
                which implements percept_environment() method
            actuator(object): instance of actuator class, 
                which implements act() method
            analysis_module(object): instance of analysis module class, which implements analyse() method

        """
        self.name = name
        self.sensor = sensor
        self.actuator = actuator
        self.analysis_module = analysis_module

    # read the sensor information and pass it to analysis module to find out actions
    def percept(self) -> Message:
        print("Agent[" + str(self.name) + "]: reading data from sensors")

        data = self.sensor.percept_environment()

        if data is not None:
            print("Agent[" + str(self.name) + "]: A new data has been obtained from sensors.")
        else:
            print("Agent[" + str(self.name) + "]: No obtained data from sensors")

        return data

    # run analysis
    def analyse(self, data: Message):
        return self.analysis_module.analyse(data)

    # run actuator
    def act(self, action, data: Message = None):
        self.actuator.act(action, data)

    def loop(self):
        """The main function and entrypoint to the Agent
        loop() method runs agent's routines:
            - read sensors to obtain data from environment or MessageQueue
            - analyse obtained data
            - react by updating environment or sending Message to another agent
        """
        print("\n==============================")
        print("Agent[" + str(self.name) + "]: Starting new agent's loop cycle")
        print("==============================")

        action = "skip"  # default action, if no data obtained, or no further actions required

        # percept environment, obtain data
        # data could be any raw information from environment or messages from other agents
        # it depends on particular sensor realisation
        # to obtain data method percept_environment() is being called from injected sensor module
        data = self.percept()

        self.between_actions_routine()

        # if there is a data obtained from sensor, it is being passed to analysis module
        if data is not None:
            print("Agent[" + str(self.name) + "]: Analyze obtained data.")
            action = self.analyse(data)
            print("Agent[" + str(self.name) + "]: Action obtained: " + str(action))
        # in other case, agent generates "skip" action
        else:
            print("Agent[" + str(self.name) + "]: No new data on sensors, skip action.")
            action = "skip"

        self.between_actions_routine()

        print("Agent[" + str(self.name) + "]: Execute the action " + str(action))

        # actuator provides an action in regard to obtained data and "action" obtained from analysis module
        self.act(action, data)

        self.between_actions_routine()

        print("Agent[" + str(self.name) + "]: loop end. Run post-loop routines.")
        self.post_loop_routine()

    def post_loop_routine(self):
        wait_time = 1
        print("Agent[" + str(self.name) + "]: Wait for " + str(wait_time) + " seconds")
        time.sleep(wait_time)

    def between_actions_routine(self):
        wait_time = 1
        time.sleep(wait_time)
