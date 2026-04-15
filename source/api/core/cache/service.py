from datetime import datetime, timezone
from fastapi import BackgroundTasks
from fastapi_cache import FastAPICache


class CacheService:
    @staticmethod
    async def _clear_namespace_async(namespace: str):

        await FastAPICache.clear(namespace=namespace)

    @staticmethod
    def clear_cache(
        namespace: str, background_tasks: BackgroundTasks = BackgroundTasks()
    ):

        background_tasks.add_task(CacheService._clear_namespace_async, namespace)

    @staticmethod
    async def block_token(token: str, expire_at: float):
        backend = FastAPICache.get_backend()

        now = datetime.now(timezone.utc).timestamp()
        ttl = int(expire_at - now)

        if ttl > 0:
            await backend.set(f"blocklist:{token}", "revoked", ttl)

    @staticmethod
    async def is_token_blocked(token: str) -> bool:
        backend = FastAPICache.get_backend()
        result = await backend.get(f"blocklist:{token}")
        return result is not None
