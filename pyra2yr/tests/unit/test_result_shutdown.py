import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from pyra2yr.network import ClientClosedError, DualClient
from ra2yrproto import core


class ResultShutdownTest(IsolatedAsyncioTestCase):
    async def test_acknowledged_command_raises_error_on_stop(self):
        client = DualClient("localhost", 0)
        # No real poll task.
        with patch.object(client, "_poll_loop", new_callable=AsyncMock):
            client.connect()
        ack = core.RunCommandAck(id=1, queue_id=0)
        with patch.object(client, "run_client_command", AsyncMock(return_value=ack)):
            command = asyncio.create_task(client.exec_command(None))
            await asyncio.wait_for(client._queue_set.wait(), 1)
            await client.stop()
            with self.assertRaises(ClientClosedError):
                await asyncio.wait_for(command, 1)
