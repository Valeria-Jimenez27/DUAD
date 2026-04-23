import redis
import os
import json
from dotenv import load_dotenv
load_dotenv()


class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "PLACEHOLDER"),
            port=int(os.getenv("REDIS_PORT", 15310)),
            password=os.getenv("REDIS_PASSWORD", "PLACEHOLDER"),
            decode_responses=False,
        )
        connection_status = self.redis_client.ping()
        if connection_status:
            print("Connection created successfully")

    def store_data(self, key, value, time_to_live=300):
        try:
            serialized = json.dumps(value)
            if time_to_live is None:
                self.redis_client.set(key, serialized)
            else:
                self.redis_client.setex(key, time_to_live, serialized)
        except redis.RedisError as error:
            print(f"An error occurred while storing data in Redis: {error}")

    def check_key(self, key):
        try:
            key_exists = self.redis_client.exists(key)
            if key_exists:
                ttl = self.redis_client.ttl(key)
                return True, ttl
            return False, None
        except redis.RedisError as error:
            print(f"An error occurred while checking a key in Redis: {error}")
            return False, None

    def get_data(self, key):
        try:
            output = self.redis_client.get(key)
            if output is not None:
                return json.loads(output.decode("utf-8"))
            return None
        except redis.RedisError as error:
            print(f"An error occurred while retrieving data from Redis: {error}")
            return None

    def delete_data(self, key):
        try:
            output = self.redis_client.delete(key)
            return output == 1
        except redis.RedisError as error:
            print(f"An error occurred while deleting data from Redis: {error}")
            return False

    def delete_data_with_pattern(self, pattern):
        try:
            for key in self.redis_client.scan_iter(match=pattern):
                self.delete_data(key)
        except redis.RedisError as error:
            print(f"An error occurred while deleting data with pattern in Redis: {error}")


cache_manager = CacheManager()