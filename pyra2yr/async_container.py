import asyncio


class AsyncDictClosed(RuntimeError):
    """No more items can be added to this dictionary."""


class AsyncDict:
    def __init__(self):
        self._data = {}
        self._cond = asyncio.Condition()
        self._closed = False

    async def close(self):
        """Wake all readers. Items already stored remain available."""
        async with self._cond:
            self._closed = True
            self._cond.notify_all()

    async def get_item(self, key, timeout: float = None, remove: bool = False):
        async with self._cond:
            async with asyncio.timeout(timeout):
                await self._cond.wait_for(lambda: key in self._data or self._closed)
            if key not in self._data:
                raise AsyncDictClosed("dictionary closed before item was available")
            item = self._data[key]
            if remove:
                self._data.pop(key)
            return item

    async def put_item(self, key, value):
        async with self._cond:
            if self._closed:
                raise AsyncDictClosed("cannot add an item to a closed dictionary")
            if key in self._data:
                raise RuntimeError(f"key {key} exists")
            self._data[key] = value
            self._cond.notify_all()
