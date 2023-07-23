from agents.lib import MessageQueue, Message
from util.file_system_emulator import FileSystemEmulator
from util.kqml_parser import KQMLParser

kqml_parser = KQMLParser()

# Coordinator Agent's sensors
class DiscoverySensor:
    def __init__(self, file_system_emulator: FileSystemEmulator):
        self.file_system_emulator = file_system_emulator
        self.message_queue = MessageQueue()

    def percept_environment(self) -> Message:
        # First, let's see if there are any responses from other agents
        response = self.message_queue.get("discoveryAgent")
        action = "skip"

        if response is not None:
            action = kqml_parser.get_action(response.message)

        if action == "tell":
            return response

        # Let's check if there are new files in the file system that we need to ask if exist
        files = self.file_system_emulator.read_files()
        if len(files) > 0:
            file = files[0]
            sample = self.file_system_emulator.read_content(file)
            kqml_message = f"(ask: (record-exists ?sample {sample}))"

            # soft delete file after it has been processed
            self.file_system_emulator.soft_delete_file(file)

            return Message("fs", "dnaAgent", kqml_message)


# Coordinator Agent's actuator
class DiscoveryActuator:
    def __init__(self):
        self.message_queue = MessageQueue()

    def act(self, action, data: Message):
        print("CoordinatorActuator: do the action: " + str(action))

        # these are outbound messages to other agents
        if action == "ask":
            message = Message("discoveryAgent", "dnaAgent", data.message)
            self.message_queue.append(message)
            return action

        # these are inbound messages from other agents
        elif action == "tell":
            criteria = kqml_parser.get_criteria(data.message)
            if "dna_sample_found" in criteria:
                result = kqml_parser.get_comparer(data.message, "dna_sample_found")
                if result == "True":
                    print(f"Sample {data.message} found in db. Sending notification ...")
                else:
                    print(f"Sample {data.message} not found in db.")

                return f"dna_sample_found {result}"
        else:
            print("CoordinatorActuator Error: no action received")
            return None


# Analytical module for the Agent, which provides an action in response to environment data (DNASampleRequest)
# Possible actions returned: skip, ask, notify_sample_not_found, notify_sample_found, error
class discoveryAnalysisModule:

    # Analyse the data obtained from environment
    def analyse(self, data: Message):
        return kqml_parser.get_action(data.message)
