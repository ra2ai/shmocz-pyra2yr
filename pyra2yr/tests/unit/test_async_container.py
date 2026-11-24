import asyncio
from unittest import IsolatedAsyncioTestCase

from pyra2yr.async_container import AsyncDict, AsyncDictClosed


class AsyncDictTest(IsolatedAsyncioTestCase):
    async def test_pending_reads_raises_error_on_close(self):
        results = AsyncDict()
        readers = [asyncio.create_task(results.get_item(i)) for i in range(2)]
        await asyncio.sleep(0)  # Let both readers reach the condition wait.
        await results.close()
        for reader in readers:
            with self.assertRaises(AsyncDictClosed):
                await asyncio.wait_for(reader, 1)

    async def test_missing_reads_and_new_writes_raises_error_after_close(self):
        results = AsyncDict()
        await results.put_item(1, "ready")
        await results.close()
        self.assertEqual(await results.get_item(1, remove=True), "ready")
        with self.assertRaises(AsyncDictClosed):
            await results.get_item(1, timeout=1)
        with self.assertRaises(AsyncDictClosed):
            await results.put_item(2, "late")

    async def test_get_missing_item_times_out(self):
        with self.assertRaises(TimeoutError):
            await AsyncDict().get_item(1, timeout=0)
