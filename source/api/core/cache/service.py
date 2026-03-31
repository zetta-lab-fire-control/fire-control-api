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
