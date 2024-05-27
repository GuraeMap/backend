from app.config.config import default
from redis import Redis


redis_session = Redis(host=default.REDIS_HOST, port=default.REDIS_PORT)
