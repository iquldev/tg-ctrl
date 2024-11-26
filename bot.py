from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import json, asyncio

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
    token = config_data["bot_token"]
    telegram_id = config_data["telegram_id"]
    
bot = Bot(token=token)
dp = Dispatcher()  

@dp.message(Command("start"))
async def start(message: types.Message):
    if str(message.from_user.id) == telegram_id:
        await message.answer('hi!')
        
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())    