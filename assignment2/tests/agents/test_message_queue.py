from unittest import TestCase

from agents.lib import MessageQueue, Message


class TestMessageQueue(TestCase):

    def setUp(self) -> None:
        self.queue = MessageQueue()

    def test_get(self):
        self.queue.append((Message("agent1", "agent2", "message")))

        fetched_message = self.queue.get("agent2")
        self.assertIsNotNone(fetched_message)

        fetched_message = self.queue.get("agent10")
        self.assertIsNone(fetched_message)

    def test_get_is_singleton(self):
        self.queue.append((Message("agent1", "agent2", "message")))

        # add a new instance to test it is a singleton implementation
        fetched_message = MessageQueue().get("agent2")
        self.assertIsNotNone(fetched_message)
