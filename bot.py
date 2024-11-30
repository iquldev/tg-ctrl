from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

from mss import mss
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import json, asyncio, platform, psutil, pygetwindow

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
    token = config_data["bot_token"]
    telegram_id = config_data["telegram_id"]
    
bot = Bot(token=token)
dp = Dispatcher()  

@dp.message(Command("start"))
async def start(message: types.Message):
    if str(message.from_user.id) == telegram_id:
        infomessage = await bot.send_message(chat_id=message.chat.id, text="⌛ Collecting information...")
        
        battery = psutil.sensors_battery()
        percent = str(battery.percent)
        
        cpu = str(psutil.cpu_freq().current)
        ram = {
            'percent' : str(psutil.virtual_memory().percent),
            'used' : psutil.virtual_memory().used / (1024 ** 3),
            'full' : psutil.virtual_memory().total / (1024 ** 3)
        }
        drive = {
            'percent' : str(psutil.disk_usage('/').percent),
            'used' : psutil.disk_usage('/').used / (1024 ** 3),
            'full' : psutil.disk_usage('/').total / (1024 ** 3)
        }
        
        windows = [w for w in pygetwindow.getAllTitles() if w.strip()]
        runned = ''
        for window in windows:
            if window != 'Program Manager':
                program = '- ' + window.replace('\u200e', '') + '\n'
                runned += program
                
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        svolume = volume.GetMasterVolumeLevelScalar() * 100       
        
        mess = f'{platform.node()} ({percent}% 🔋)\n\n⚡ CPU: {cpu}Mhz \n🗂️ RAM: {ram['percent']}% ({round(ram['used'], 1)} Gb/{round(ram['full'])} Gb) \n💿 Disk: {drive['percent']}% ({round(drive['used'], 1)} Gb/{round(drive['full'])} Gb) \n\n📱 Runned: {runned} \n🔊 Volume: {int(round(svolume, 0))}%'
        
        with mss() as sct:
            sct.shot()
        screenshot = types.FSInputFile("monitor-1.png")
        
        await bot.delete_message(chat_id=message.chat.id, message_id=infomessage.message_id)
        await bot.send_photo(chat_id=message.chat.id, photo=screenshot, caption=mess, parse_mode=ParseMode.MARKDOWN)
        
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())    