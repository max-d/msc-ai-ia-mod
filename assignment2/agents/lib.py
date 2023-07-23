import random

from util.file_system_emulator import FileSystemEmulator


# agent's knowledge databases
class CasesDatabase:

    def __init__(self, data):
        self.data = data
        self.found_data = set()
        self.discarded_data = set()

    def add(self, record):
        self.found_data.add(record)

    def discard(self, record):
        self.discarded_data.add(record)

    def print_data(self):
        print("\nDatabase: show all stored DNA data.")
        for row in self.data:
            print("\tDNA sample: " + str(row))
        print("\n")


class Message:
    def __init__(self, from_agent, to_agent, message):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message = message


# Simple messages queue for communication between agents
# Singleton used to save a shared state
class MessageQueue(object):
    _shared_borg_state = {}
    queue = []

    def __new__(cls, *args, **kwargs):
        obj = super(MessageQueue, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_borg_state
        return obj

    def append(self, message: Message):
        self.queue.append(message)

    # get any message for agent
    def get(self, agent) -> Message:
        for message in self.queue:
            if message.to_agent == agent:
                index = self.queue.index(message)
                return self.queue.pop(index)

        return None

    def print_all(self):
        print("MessageQueue messages")
        for row in self.queue:
            print("\tFrom: " + str(row.from_agent) + ", To: " + str(row.to_agent) + ", Message: " + str(row.message))


# FS Environment simple agent
# generates test data that represents DNA requests as inputs to multi-agent system
# by legend requests are made by creating text files in some directory
class FsEnvironment:
    def __init__(self, file_system_emulator: FileSystemEmulator):
        self.file_system_emulator = file_system_emulator

    # test function: environment provides random document - a request for DNA analysis for new or present case
    # (Message to discoveryAgent) for real prototype, it should be FS reading code which makes searches on accessible
    # filesystems
    def generate_random_samples(self):
        files = self.file_system_emulator.read_files()

        if len(files) == 0:
            random_sample = self.file_system_emulator.add_random_sample()
            print(f"Fyle system: New file {random_sample} with DNA request has been sent")
