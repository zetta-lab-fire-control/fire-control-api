import redis


class RedisService:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):

        self.host = host
        self.port = port
        self.db = db

    @property
    def ttl(self) -> int:
        return 60

    @property
    def client(self):
        return redis.Redis(
            host=self.host, port=self.port, db=self.db, decode_responses=True
        )
