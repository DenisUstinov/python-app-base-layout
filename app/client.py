import aiohttp
import backoff


class Client:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = aiohttp.ClientSession()
        return cls._instance

    @backoff.on_exception(backoff.expo, (aiohttp.ClientError, aiohttp.ClientConnectorError), max_tries=3,)
    async def request(self, method: str, url: str, headers: dict = None, data: dict = None,):
        async with self.session.request(method, url, headers=headers, data=data) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"Request to {url} failed with status {response.status}",
                    headers=response.headers,
                )
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                return await response.json()
            else:
                return await response.text()

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()