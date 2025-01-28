from environs import Env


env = Env()
env.read_env()

"""Tokens"""
BOT_TOKEN = env.str("BOT_TOKEN")


"""Redis"""
redis_host = env.str("REDIS_HOST", None)
redis_port = env.str("REDIS_PORT", None)
