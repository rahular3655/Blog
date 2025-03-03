from decouple import config

SALT_ENCRYPTION_KEY = config('SALT_ENCRYPTION_KEY')

PASSWORD_RESET_AGE = config('PASSWORD_RESET_AGE', cast=int)

ACCOUNT_VERIFICATION_AGE = config('ACCOUNT_VERIFICATION_AGE', cast=int)

# For random number creation using in otp generation
RANDOM_INT_FROM = config('RANDOM_INT_FROM', cast=int)

RANDOM_INT_TO = config('RANDOM_INT_TO', cast=int)
