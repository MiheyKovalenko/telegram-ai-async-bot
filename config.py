import configparser

config = configparser.ConfigParser()
config.read('config.ini')

BOT_TOKEN = config['default']['bot_token']
ADMIN_ID = int(config['default']['admin_id'])
OPENAI_API_KEY = config['default']['openai_api_key']

PAID_USERS = []  # юзеры с доступом к GPT-4o
