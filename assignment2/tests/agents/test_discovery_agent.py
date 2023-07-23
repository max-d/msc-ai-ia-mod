import shutil
from unittest import TestCase

from agents.discovery_agent import DiscoverySensor, DiscoveryActuator, discoveryAnalysisModule
from agents.lib import MessageQueue, Message
from util.file_system_emulator import FileSystemEmulator


class TestDiscoverySensor(TestCase):

    def setUp(self):
        self.fs = FileSystemEmulator("test", "test_delete")
        self.sensor = DiscoverySensor(self.fs)
        self.messageQueue = MessageQueue()

    def tearDown(self) -> None:
        # clear test folders
        shutil.rmtree(self.fs.directory)
        shutil.rmtree(self.fs.deleted_directory)

    def test_percept_environment_read_files(self):
        sample = self.fs.add_random_sample()
        content = self.fs.read_content(sample)
        result = self.sensor.percept_environment()

        self.assertEqual("fs", result.from_agent)
        self.assertEqual("dnaAgent", result.to_agent)
        self.assertEqual(f"(ask: (record-exists ?sample {content}))", result.message)

    def test_percept_environment_receive_tell_message(self):
        content = f"(tell: (record-exists ?dna_sample_found {True}))"
        message = Message("dnaAgent", "discoveryAgent", content)
        self.messageQueue.append(message)

        result = self.sensor.percept_environment()
        self.assertEqual("dnaAgent", result.from_agent)
        self.assertEqual("discoveryAgent", result.to_agent)
        self.assertEqual(content, result.message)


class TestDiscoveryActuator(TestCase):

    def setUp(self):
        self.actuator = DiscoveryActuator()
        self.messageQueue = MessageQueue()

    def test_act_ask(self):
        message = Message("agent1", "agent2", "any message")
        result = self.actuator.act("ask", message)
        sentMessage = self.messageQueue.get("dnaAgent")

        self.assertEqual("ask", result)
        self.assertEqual("any message", sentMessage.message)

    def test_act_tell(self):
        message = Message("agent1", "agent2", "(tell: (record-exists ?dna_sample_found True))")
        result = self.actuator.act("tell", message)
        sentMessage = self.messageQueue.get("dnaAgent")

        self.assertEqual("dna_sample_found True", result)
        self.assertIsNone(sentMessage)


class TestdiscoveryAnalysisModule(TestCase):

    def setUp(self):
        self.analysisModule = discoveryAnalysisModule()

    def test_analyse(self):
        data = Message("","", "(tell: (record-exists ?dna_sample_found True))")
        result = self.analysisModule.analyse(data)

        self.assertEqual("tell", result)
