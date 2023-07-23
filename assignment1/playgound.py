import random
import time

# basic Intelligence Agent class
class Agent:
    def __init__(self, sensor, actuator, analysis_module):
        self.sensor = sensor
        self.actuator = actuator
        self.analysis_module = analysis_module

    # read the sensord information and pass it to analysis module to find out actions 
    def percept(self, environment):
        print("Agent: reading data from sensors")
        data = self.sensor.percept_environment(environment)
        
        if data != None:
            print("A new data has been obtained from sensors.")
            return data
        else:
            print("No obtained data from sensors")
            return None


    #run analysis
    def analyse(self, data):
        return self.analysis_module.analyse(data)

    def act(self, action, data = None):
        self.actuator.act(action)

    def loop(self, environment):
        print("\n==============================")
        print("Starting new agent's loop cycle")
        print("==============================")

        action = "skip" #default action, if no data obtained, or no further actions required

        data = self.percept(environment)

        self.between_actions_routine()

        if data != None:
            print("Agent: Sensors' data obtained.")
            print("Agent: Request's case: " + str(data.case))
            print("Agent: Request's DNA sample: " + str(data.sample))
            print("Agent: Analize obtained data.")
            action = self.analyse(data)
            print("Agent: Action obtained: " + str(action))

        else:
            print("Agent: No new data on sensors, skip action.")
            action = "skip"
        
        self.between_actions_routine()

        print("Agent: Execute the action " + str(action))
        self.act(action, data)
        
        self.between_actions_routine()

        print("Agent: loop end. Run post-loop routines.")
        self.post_loop_routine()
    
    def post_loop_routine(self):
        wait_time = 3
        print("Wait for " + str(wait_time) + " seconds")
        time.sleep(wait_time)

    def between_actions_routine(self):
        wait_time = 1
        time.sleep(wait_time)

class DNASampleRequest:
    def __init__(self, dna_sample, case):
        self.case = case
        self.sample = dna_sample

class DNASampleDbRecord:
    def __init__(self, case, dna_sample):
        self.case = case
        self.sample = dna_sample

#Test Filesystem Environment
class FsEnvironment:

    # test function: environment provides random document - a request for DNA analysis for new or present case (DNASampleRequest)
    # for real prototype, it should be FS reading code which makes searches on accessible filesystems
    def generate_random_events(self) -> DNASampleRequest:
        return DNASampleRequest(
            [random.randint(1,3), random.randint(1,3), random.randint(1,3)], #DNA sample is a random array of 1-3 sequence (to simplify cases)
            random.randint(1,10) #random case number
            )

#agent's sensors
class FilesystemSensor:
    def __init__(self):
        pass
    def percept_environment(self, environment: FsEnvironment = None):
            return environment

#agent's actuators
class CoordinatorActuator:
    def act(self, action, data = None):
        print("Actuator: do the action: " + str(action))

#agent's knowledge databases
class CasesDatabase:
    def __init__(self, data):
        self.data = data
    
    def add(self, record):
        self.data.append(record)

    def print_data(self):
        print("\n\Database: show all stored data.")
        for row in self.data:
            print("\tCase: " + str(row.case) + ", DNA sample: " + str(row.sample))
        print("\n")

#Agent's ML models, which performs DNA matches
class CasesModel:       
     def match(self, data, database):
         
         #empty array for matched records
         result = []
         
         #loop through the database to find the case by DNA sample
         for row in database.data:
             if row.sample == data.sample:
                 result.append(row)

         return result
     
     def match_strict(self, data, database):
         #loop through the database to find the case by DNA sample
         for row in database.data:
             if row.sample == data.sample and row.case == data.case:
                 return True
             
             return False

# Analytical module for the Agent, which provides an action in response to environment data (DNASampleRequest)
# Possible actions returned: skip, notify_sample_added, notify_sample_found
class CoordinatorAnalysisModule:
    def __init__(self, knowledge_database, model):
        self.knowledge_database = knowledge_database
        self.model = model

    # Analyse the data obtained from environment ()
    def analyse(self, data):

        action = "skip"
        self.knowledge_database.print_data()

        result = self.model.match(data, self.knowledge_database)

        if result == []:
            print("Analysis Module: DNA sample wasn't found in database. Add new sample to the database.")
            self.knowledge_database.add(DNASampleDbRecord(data.case, data.sample))
            action = "notify_sample_added"

        else:
            print("Analysis Module: DNA sample was found in database.")
            for row in result:
                print("Analysis Module: DNA sample: " + str(row.sample) +  " Case ID: " + str(row.case))
            
            if not self.model.match_strict(data, self.knowledge_database):
                print("Analysis Module: DNA sample has been found, but for different case. Add record for new case.")
                self.knowledge_database.add(DNASampleDbRecord(data.case, data.sample))
            
            action = "notify_sample_found"

        return action


# ============================================ Playground ===================================================

# Create test DNA sample database
# DNASampleDbRecord([case id], [dna sequence])
db = CasesDatabase([
    DNASampleDbRecord(1, [1,1,1]),
    DNASampleDbRecord(2, [1,2,2]),
    DNASampleDbRecord(3, [1,3,1]),
    DNASampleDbRecord(4, [3,3,1]),
    DNASampleDbRecord(5, [2,2,2]),
]);

# Initiate Coordinator Agent
# Set up sensor, actuator and analysis module's objects
# CoordinatorAnalysisModule also demands database driver and ML model whoch will perform matches of DNA samples
# For simplisity ML Model will perform direct search in randomply generated DNA Samples database
coordinatorAgent = Agent(
    FilesystemSensor(),
    CoordinatorActuator(),
    CoordinatorAnalysisModule(
        db, CasesModel()
    )
)


# Create test Filesystem Environment
env = FsEnvironment()

# Start eternal loop and feed the agent with randomply generated data
while 1:
    
    # The "loop" method of the Agent takes current environment and reads it state
    coordinatorAgent.loop(env.generate_random_events())
