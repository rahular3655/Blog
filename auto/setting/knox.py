from datetime import timedelta

from decouple import config

KNOX_SETTINGS = {
    'DATETIME_FORMAT': 'iso-8601',  # Specify the desired date format here
}

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(hours=24),
    'USER_SERIALIZER': 'accounts.serializers.users.UserSerializer',
    'TOKEN_LIMIT_PER_USER': 5,
    'AUTO_REFRESH': False,
    # 'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}

REST_KNOX_MAX_TOKENS_PER_USER = config('REST_KNOX_MAX_TOKENS_PER_USER', cast=int, default=5)
