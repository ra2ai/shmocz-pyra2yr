import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from pyra2yr.network import DualClient, WebSocketClient


class PollShutdownTest(IsolatedAsyncioTestCase):
    async def test_stop_before_queue_id(self):
        client = DualClient("localhost", 0)
        client.connect()
        await asyncio.sleep(0)  # Let the poll loop reach _queue_set.wait().
        await client.stop()
        self.assertTrue(client._poll_task.cancelled())
        self.assertFalse(client._queue_set.is_set())
        self.assertTrue(all(conn.task.done() for conn in client.conns.values()))

    async def test_stop_while_waiting_for_poll_reply(self):
        client = DualClient("localhost", 0, timeout=60)
        conn = WebSocketClient(client.uri)
        client.conns["poll"] = conn
        client.make_poll_blocking = Mock()
        client.queue_id = 0
        client._queue_set.set()
        client._poll_task = asyncio.create_task(client._poll_loop())
        # Consume the request but never send a reply. Only accept close().
        await asyncio.wait_for(conn.in_queue.get(), 1)
        conn.task = asyncio.create_task(conn.in_queue.get())
        await asyncio.wait_for(client.stop(), 1)
        self.assertTrue(client._poll_task.cancelled())
        self.assertIsNone(conn.task.result())
