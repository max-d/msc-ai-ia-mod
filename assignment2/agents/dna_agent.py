from agents.lib import MessageQueue, Message, CasesDatabase
import ast

from util.kqml_parser import KQMLParser

kqml_parser = KQMLParser()

class DNARequestSensor:
    def __init__(self, name):
        self.message_queue = MessageQueue()
        self.name = name

    def percept_environment(self):

        print("DNARequest Sensor: look for new messages")
        message = self.message_queue.get(self.name)
        if message is not None:
            print("DNARequest Sensor: got a message")

        return message


class DNARequestActuator:
    def __init__(self, name):
        self.message_queue = MessageQueue()
        self.name = name

    def act(self, action, data):
        print("DNARequestActuator: do the action: " + str(action))

        found = action == "dna_sample_found"

        if found:
            outbound_message = f"(tell: (record-exists ?dna_sample_found {found}))"
        else:
            outbound_message = f"(skip: (record-exists ?dna_sample_found {found}))"

        message = Message("dnaAgent", "discoveryAgent", outbound_message)
        self.message_queue.append(message)


class DNAAnalysisModule:

    def __init__(self, db: CasesDatabase):
        self.db = db

    # Analyse the data obtained from environment ()
    def analyse(self, data: Message):

        # perform db search for DNA sample
        sample = kqml_parser.get_comparer(data.message, "sample")

        self.db.print_data()
        print("DNAAnalysisModule: perform search of sample " + str(sample) + " in DNA database")

        # we use ast to convert the message string "[x, x, x]" into an array of integers
        exists = ast.literal_eval(sample) in self.db.data

        if exists:
            self.db.add(sample)
            return "dna_sample_found"
        else:
            self.db.discard(sample)
            print("DNAAnalysisModule: sample wasn't found in DNA database")
            print("DNAAnalysisModule: DNA sample added to discarded database")
            return "dna_sample_not_found"

