from unittest import TestCase

from agents.dna_agent import DNARequestSensor, DNARequestActuator, DNAAnalysisModule
from agents.lib import MessageQueue, Message, CasesDatabase


class TestDNARequestSensor(TestCase):

    def setUp(self):
        self.sensor = DNARequestSensor("Agent1")
        self.message_queue = MessageQueue()

    def test_percept_environment(self):
        message = Message("", "Agent1", "any message")
        self.message_queue.append(message)

        storedMessage = self.sensor.percept_environment()

        self.assertEqual(message, storedMessage)

    def test_percept_environment_none_message(self):
        storedMessage = self.sensor.percept_environment()

        self.assertIsNone(storedMessage)


class TestDNARequestActuator(TestCase):

    def setUp(self):
        self.actuator = DNARequestActuator("Agent1")
        self.message_queue = MessageQueue()

    def test_act(self):
        outbound_message = f"(tell: (record-exists ?dna_sample_found True))"
        message = Message("dnaAgent", "discoveryAgent", outbound_message)
        self.actuator.act("dna_sample_found", None)

        sentMessage = self.message_queue.get("discoveryAgent")
        self.assertEqual(message.message, sentMessage.message)


class TestDNAAnalysisModule(TestCase):

    def setUp(self):
        db = CasesDatabase([
            [1, 1, 1]
        ])
        self.analysisModule = DNAAnalysisModule(db)

    def test_analyse_found(self):
        message = Message("","",f"(ask: (record-exists ?sample [1, 1, 1]))")
        result = self.analysisModule.analyse(message)

        foundResult = self.analysisModule.db.found_data.pop()
        self.assertEqual("dna_sample_found", result)
        self.assertEqual(foundResult, "[1, 1, 1]")
        self.assertEqual(0, len(self.analysisModule.db.discarded_data))

    def test_analyse_not_found(self):
        message = Message("","",f"(ask: (record-exists ?sample [1, 1, 2]))")
        result = self.analysisModule.analyse(message)

        discardedResult = self.analysisModule.db.discarded_data.pop()
        self.assertEqual("dna_sample_not_found", result)
        self.assertEqual(discardedResult, "[1, 1, 2]")
        self.assertEqual(0, len(self.analysisModule.db.found_data))


