import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import dotenv


bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(storage=MemoryStorage())

dotenv.load_dotenv(".env")

token = os.environ['BOT_TOKEN']
if token == "":
    print("Please set BOT_TOKEN environment variable")
    exit(1)

chat_id = os.environ['CHAT_ID']
if chat_id == "":
    print("Please set CHAT_ID environment variable")
    exit(1)
