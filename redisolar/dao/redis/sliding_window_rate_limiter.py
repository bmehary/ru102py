# Uncomment for Challenge #7
import datetime
import random

from redis.client import Redis

from redisolar.dao.base import RateLimiterDaoBase
from redisolar.dao.redis.base import RedisDaoBase
from redisolar.dao.redis.key_schema import KeySchema

# Uncomment for Challenge #7
from redisolar.dao.base import RateLimitExceededException


class SlidingWindowRateLimiter(RateLimiterDaoBase, RedisDaoBase):
    """A sliding-window rate-limiter."""
    def __init__(self,
                 window_size_ms: float,
                 max_hits: int,
                 redis_client: Redis,
                 key_schema: KeySchema = None,
                 **kwargs):
        self.window_size_ms = window_size_ms
        self.max_hits = max_hits
        super().__init__(redis_client, key_schema, **kwargs)

    def hit(self, name: str):
        """Record a hit using the rate-limiter."""
        # START Challenge #7

        random_number = random.random()
        milliseconds = int(datetime.datetime.now().timestamp() * 1000)

        start_score = milliseconds - self.window_size_ms

        set_key = milliseconds
        set_score = f"{milliseconds}-{random_number}"
        key_name = self.key_schema.sliding_window_rate_limiter_key(
            name,
            self.window_size_ms,
            self.max_hits
        )

        p = self.redis.pipeline(transaction=True)

        p.zremrangebyscore(key_name, -1, start_score)
        p.zadd(key_name, mapping={set_score: set_key})
        p.zcard(key_name)
        _, _, hits = p.execute()

        if hits > self.max_hits:
            raise RateLimitExceededException()

        # END Challenge #7
