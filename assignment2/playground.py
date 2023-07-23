# Playground for demonstration of basic concepts of multi agent system

from agents.discovery_agent import DiscoveryActuator, discoveryAnalysisModule, DiscoverySensor
from agents.lib import FsEnvironment, FsEnvironment, MessageQueue, CasesDatabase
from agents.base_agent import Agent
from agents.dna_agent import DNAAnalysisModule, DNARequestActuator, DNARequestSensor
from util.file_system_emulator import FileSystemEmulator

# Create test DNA sample database
# array[dna sequence]
# for simplicity and transparency we use simple array of 3 integers
# however, any complex solution for DNA database could be implemented
db = CasesDatabase([
    [1, 1, 1],
    [1, 1, 2],
    [1, 2, 3],
    [2, 1, 1],
    [2, 1, 2],
    [2, 2, 3],
    [3, 1, 1],
    [3, 1, 2],
    [3, 2, 3],
])

# Initialize new message queue
# For simplicity we implement MessageQueue as Singleton, 
# which may represent any remote queue manages accessible through TCP connection (RabbitMQ, etc.)
# or some other solution which allow to share state among the system components.   
messageQueue = MessageQueue()
messageQueue.queue = []

# These directories will be used to store new generated samples and to soft-delete them
sample_directory = "samples"
deleted_samples_directory = "deleted_samples"

file_system_emulator = FileSystemEmulator(sample_directory, deleted_samples_directory)

# Initiate Coordinator Agent
# Set up sensor, actuator and analysis module's objects
discoveryAgent = Agent(
    "discoveryAgent",
    DiscoverySensor(file_system_emulator),
    DiscoveryActuator(),
    discoveryAnalysisModule()
)

# danAgent performs serches in the DNA database
# Its modules should implement database driver and ML model which will perform matches of DNA samples
# For simplisity ML Model will perform direct search in randomply generated DNA Samples database
dnaAgent = Agent(
    "dnaAgent",
    DNARequestSensor("dnaAgent"),
    DNARequestActuator("dnaAgent"),
    DNAAnalysisModule(db),
)

# Create test Filesystem Environment
file_environment = FsEnvironment(file_system_emulator)

# Start eternal loop and feed agents with randomply generated data
try:
    # main eternal loop
    while 1:
        # create random DNA request
        file_environment.generate_random_samples()

        # The "loop" method of the Agent takes current environment (MessageQueue) and reads its state
        discoveryAgent.loop()
        dnaAgent.loop()
except KeyboardInterrupt:
    print("\nUser interruption detected. Exiting...\n")
    if len(db.found_data) > 0:
        print("********** Samples found during analysis **********")
        print("dna sample")
        for row in db.found_data:
            print(row)

    else:
        print("********** No samples found during analysis **********")

    print("\n")

    if len(db.discarded_data) > 0:
        print("********** Samples discarded during analysis **********")
        print("dna sample")
        for row in db.discarded_data:
            print(row)
