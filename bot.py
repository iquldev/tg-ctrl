from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from mss import mss
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from screen_brightness_control import get_brightness

import json, asyncio, platform, psutil, pygetwindow, os, subprocess

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
    token = config_data["bot_token"]
    telegram_id = config_data["telegram_id"]
    
bot = Bot(token=token)
dp = Dispatcher()  

inlineboards = {
    'volumemenu': [
            [InlineKeyboardButton(text="➕ 10%", callback_data='vadd10')],
            [InlineKeyboardButton(text="🔇 Mute", callback_data='mute')],
            [InlineKeyboardButton(text="➖ 10%", callback_data='vsub10')],
            [InlineKeyboardButton(text="❌ Close", callback_data='close')]
    ],
    'controlmenu': [
            [InlineKeyboardButton(text="Shutdown", callback_data='shutdown')],
            [InlineKeyboardButton(text="Restart", callback_data='restart')],
            [InlineKeyboardButton(text="Sleep Mode", callback_data='sleep')],
            [InlineKeyboardButton(text="Hibernation", callback_data='hibernation')],
            [InlineKeyboardButton(text="Log out", callback_data='logout')],
            [InlineKeyboardButton(text="❌ Close", callback_data='close')]
    ],
    'mainmenu': [
            [InlineKeyboardButton(text="Volume 🔊", callback_data='volume')],
            [InlineKeyboardButton(text="Control 🔴", callback_data='control')],
            [InlineKeyboardButton(text="Functions ⚙️", callback_data='functions')]
    ],
    'funcmenu': [
            [InlineKeyboardButton(text="❌ Close", callback_data='close')]
    ]
}

def getbattery():
    try:
        battery = psutil.sensors_battery()
        percent = str(battery.percent)
    except Exception:
        return '❌'
    return percent

def getcpu():
    try:
        cpu = str(psutil.cpu_freq().current)
    except Exception:
        return '❌'
    return cpu

def getram():
    try:
        ram = {
                'percent' : str(psutil.virtual_memory().percent),
                'used' : psutil.virtual_memory().used / (1024 ** 3),
                'full' : psutil.virtual_memory().total / (1024 ** 3)
        }
    except Exception:
        ram = {
                'percent' : '❌',
                'used' : '❌',
                'full' : '❌'
        }
    return ram

def getdrive():
    try:
        drive = {
                'percent' : str(psutil.disk_usage('/').percent),
                'used' : psutil.disk_usage('/').used / (1024 ** 3),
                'full' : psutil.disk_usage('/').total / (1024 ** 3)
        }
    except Exception:
        drive = {
                'percent' : '❌',
                'used' :'❌',
                'full' : '❌'
        }
    return drive

def getapps():
    try:
        windows = [w for w in pygetwindow.getAllTitles() if w.strip()]
        runned = ''
        for window in windows:
            if window != 'Program Manager':
                program = '- ' + window.replace('\u200e', '') + '\n'
                runned += program
    except Exception:
        return '❌'
    return runned

def getspeaker():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
    except Exception:
        return '❌'
    return volume

def getvolume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        svolume = volume.GetMasterVolumeLevelScalar() * 100   
    except Exception:
        return '❌'
    return svolume

def brightness():
    try:
        brightness = get_brightness()
    except Exception:
        return '❌'
    return brightness[0]

def screen():
    try:
        with mss() as sct:
                sct.shot()
        screenshot = types.FSInputFile("monitor-1.png")
    except Exception:
        return '❌'
    return screenshot

def getwifi():
    # xd
    return True
    
def getbluetooth():
    try:
        command = (
            'Get-NetAdapter | Where-Object { $_.Name -like "*Bluetooth*" } | '
            'Select-Object -ExpandProperty Status'
        )
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True
        )
        
        output = result.stdout.strip()
        if output:
            return True
        else:
            return False
    except Exception as e:
        return False

@dp.callback_query(F.data == 'close')
async def close(call: CallbackQuery):
    inline = inlineboards['mainmenu']
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    
    percent = getbattery()
        
    cpu = getcpu()
    ram = getram()
    drive = getdrive()
        
    runned = getapps()
                
    volume = getvolume()    
    bright = brightness()
        
    mess = f'{platform.node()} ({percent}% 🔋)\n\n⚡ CPU: {cpu}Mhz \n🗂️ RAM: {ram['percent']}% ({round(ram['used'], 1)} Gb/{round(ram['full'])} Gb) \n💿 Disk: {drive['percent']}% ({round(drive['used'], 1)} Gb/{round(drive['full'])} Gb) \n\n📱 Runned: {runned} \n🔊 Volume: {int(round(volume, 0))}%\n☀️ Brightness: {bright}%'
    
    await bot.edit_message_caption(caption=mess, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    
@dp.callback_query(F.data == 'vadd10')
async def editvolume(call: CallbackQuery):
    inline = inlineboards['volumemenu']
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    
    speaker = getspeaker()
    volume = getvolume()
    newvolume = min((volume / 100) + 0.1, 1.0)
    speaker.SetMasterVolumeLevelScalar(newvolume, None)
    
    await bot.edit_message_caption(caption=f'🔊 Volume: {int(round(newvolume * 100, 0))}%', chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    
@dp.callback_query(F.data == 'vsub10')
async def editvolume(call: CallbackQuery):
    inline = inlineboards['volumemenu']
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    
    speaker = getspeaker()
    volume = getvolume()
    newvolume = max((volume / 100) - 0.1, 0.0)
    speaker.SetMasterVolumeLevelScalar(newvolume, None)
    
    await bot.edit_message_caption(caption=f'🔊 Volume: {int(round(newvolume * 100, 0))}%', chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)   
    
@dp.callback_query(F.data == 'mute')
async def editvolume(call: CallbackQuery):
    inline = inlineboards['volumemenu']
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    
    speaker = getspeaker()
    speaker.SetMasterVolumeLevelScalar(0.0, None)
    
    await bot.edit_message_caption(caption=f'🔊 Volume: 0%', chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)              

@dp.callback_query(F.data == 'volume')
async def editvolume(call: CallbackQuery):
    inline = inlineboards['volumemenu']
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    
    volume = getvolume()
    
    await bot.edit_message_caption(caption=f'🔊 Volume: {int(round(volume, 0))}%', chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
    
@dp.callback_query(F.data == 'shutdown')
async def shutdown(call: CallbackQuery):
    os.system("shutdown /s /f /t 0")
    
    await call.message.answer('Done 👌')    
    
@dp.callback_query(F.data == 'restart')
async def restart(call: CallbackQuery):
    os.system("shutdown /r /f /t 0")
    
    await call.message.answer('Done 👌')
    
@dp.callback_query(F.data == 'sleep')
async def sleep(call: CallbackQuery):
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    await call.message.answer('Done 👌')    
    
@dp.callback_query(F.data == 'hibernation')
async def hibernation(call: CallbackQuery):
    os.system("shutdown /h")
    
    await call.message.answer('Done 👌')     
    
@dp.callback_query(F.data == 'logout')
async def logout(call: CallbackQuery):
    os.system("shutdown /l")
    
    await call.message.answer('Done 👌')           
    
@dp.callback_query(F.data == 'control')
async def control(call: CallbackQuery):
    inline = inlineboards['controlmenu']
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    
    percent = getbattery()
        
    cpu = getcpu()
    ram = getram()
    drive = getdrive()
        
    runned = getapps()
                
    volume = getvolume()    
    bright = brightness()
        
    mess = f'{platform.node()} ({percent}% 🔋)\n\n⚡ CPU: {cpu}Mhz \n🗂️ RAM: {ram['percent']}% ({round(ram['used'], 1)} Gb/{round(ram['full'])} Gb) \n💿 Disk: {drive['percent']}% ({round(drive['used'], 1)} Gb/{round(drive['full'])} Gb) \n\n📱 Runned: {runned} \n🔊 Volume: {int(round(volume, 0))}%\n☀️ Brightness: {bright}%'
    
    await bot.edit_message_caption(chat_id=call.message.chat.id, caption=mess, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard, message_id=call.message.message_id)
    
@dp.callback_query(F.data == 'functions')
async def editvolume(call: CallbackQuery):
    inline = inlineboards['funcmenu']
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
    
    wifi = getwifi()
    wifistate = '🟢' if wifi else '🔴'
    bt = getbluetooth()
    btstate = '🟢' if bt else '🔴'
    
    await bot.edit_message_caption(caption=f'🛜 Wi-Fi: {wifistate}\n📲 Bluetooth: {btstate}', chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)    

@dp.message(Command("start"))
async def start(message: types.Message):
    if str(message.from_user.id) == telegram_id:
        infomessage = await bot.send_message(chat_id=message.chat.id, text="⌛ Collecting information...")
        
        percent = getbattery()
        
        cpu = getcpu()
        ram = getram()
        drive = getdrive()
        
        runned = getapps()
                
        volume = getvolume()    
        bright = brightness()
        
        mess = f'{platform.node()} ({percent}% 🔋)\n\n⚡ CPU: {cpu}Mhz \n🗂️ RAM: {ram['percent']}% ({round(ram['used'], 1)} Gb/{round(ram['full'])} Gb) \n💿 Disk: {drive['percent']}% ({round(drive['used'], 1)} Gb/{round(drive['full'])} Gb) \n\n📱 Runned: {runned} \n🔊 Volume: {int(round(volume, 0))}%\n☀️ Brightness: {bright}%'
        
        screenshot = screen()
        
        inline = inlineboards['mainmenu']
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline)
        
        await bot.send_photo(chat_id=message.chat.id, photo=screenshot, caption=mess, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)
        await bot.delete_message(chat_id=message.chat.id, message_id=infomessage.message_id)
        
async def main():
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())    