CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/6",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_CLASS": "redis.connection._HiredisParser",
            "REDIS_CLIENT_KWARGS": {
                # 'decode_responses': True
            },
            "CONNECTION_POOL_KWARGS": {
                # "max_connections": 1000,
                "retry_on_timeout": True,
                # 'decode_responses': True
            }
        }
    },
    'product': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/7",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PARSER_CLASS": "redis.connection._HiredisParser",
            "REDIS_CLIENT_KWARGS": {
                'decode_responses': False
            },
            "CONNECTION_POOL_KWARGS": {
                # "max_connections": 1000,
                "retry_on_timeout": True,
                'decode_responses': False
            }
        }
    },

}
