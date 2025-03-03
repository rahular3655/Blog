from decouple import config

DEFENDER_LOGIN_FAILURE_LIMIT = config('DEFENDER_LOGIN_FAILURE_LIMIT', cast=int)  # Number of failed login attempts

DEFENDER_COOLOFF_TIME = config('DEFENDER_COOLOFF_TIME', cast=int)  # in seconds

DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME = config('DEFENDER_LOCK_OUT_BY_IP_AND_USERNAME', cast=bool)

DEFENDER_STORE_ACCESS_ATTEMPTS = config('DEFENDER_STORE_ACCESS_ATTEMPTS', cast=bool)
