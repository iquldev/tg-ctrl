import json, asyncio, platform, psutil, pygetwindow, os, subprocess
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from mss import mss
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from screen_brightness_control import get_brightness
import webbrowser
import ctypes

def getbattery():
    try: return str(psutil.sensors_battery().percent)
    except: return '❌'
def getcpu():
    try: return str(psutil.cpu_freq().current)
    except: return '❌'
def getram():
    try:
        m = psutil.virtual_memory()
        return {"percent": str(m.percent), "used": m.used/(1024**3), "full": m.total/(1024**3)}
    except: return {"percent": "❌", "used": "❌", "full": "❌"}
def getdrive():
    try:
        d = psutil.disk_usage('/')
        return {"percent": str(d.percent), "used": d.used/(1024**3), "full": d.total/(1024**3)}
    except: return {"percent": "❌", "used": "❌", "full": "❌"}
def getapps():
    try:
        apps = [w for w in pygetwindow.getAllTitles() if w.strip() and w!="Program Manager"]
        return "\n".join("- " + w.replace('\u200e','') for w in apps)
    except: return '❌'
def getspeaker():
    try:
        dev = AudioUtilities.GetSpeakers()
        iface = dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return iface.QueryInterface(IAudioEndpointVolume)
    except: return None
def getvolume():
    try:
        spk = getspeaker()
        return spk.GetMasterVolumeLevelScalar()*100 if spk else '❌'
    except: return '❌'
def brightness():
    try:
        b = get_brightness()
        return b[0] if b else '❌'
    except: return '❌'
def screen():
    try:
        with mss() as sct: sct.shot()
        return types.FSInputFile("monitor-1.png")
    except: return '❌'
def getwifi(): return True
def getbluetooth():
    try:
        cmd = 'Get-NetAdapter | Where-Object { $_.Name -like "*Bluetooth*" } | Select-Object -ExpandProperty Status'
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        return bool(res.stdout.strip())
    except: return False

def run(data: str):
    if data.startswith("http://") or data.startswith("https://") or data.startswith("www."):
        url = data if data.startswith("http") else "http://" + data
        webbrowser.open(url)
        return f"Link {url} opened"

    if os.path.isdir(data):
        os.startfile(data)
        return f"Folder {data} opened"

    if os.path.isfile(data):
        os.startfile(data)
        return f"File {data} opened"

    try:
        subprocess.Popen(data)
        return f"Launching {data}"
    except Exception as e:
        return "Failed to launch the application"

def get_file(file_path):
    if not os.path.isfile(file_path):
        return None, "File not found"
    try:
        return types.FSInputFile(file_path), None
    except Exception:
        return None, "Failed to send file"
    
def create_window(text):
    ctypes.windll.user32.MessageBoxW(0, text, "Message", 0)

def shutdown_pc(delay_seconds=0):
    try:
        if delay_seconds == 0:
            os.system("shutdown /s /f /t 0")
        else:
            os.system(f"shutdown /s /f /t {delay_seconds}")
        return True
    except:
        return False

def cancel_shutdown():
    try:
        os.system("shutdown /a")
        return True
    except:
        return False

inlineboards = {
    'volumemenu': [
        [InlineKeyboardButton(text="➕ 10%", callback_data="vadd10")],
        [InlineKeyboardButton(text="🔇 Mute", callback_data="mute")],
        [InlineKeyboardButton(text="➖ 10%", callback_data="vsub10")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close")]
    ],
    'controlmenu': [
        [InlineKeyboardButton(text="Shutdown ⏻", callback_data="shutdown")],
        [InlineKeyboardButton(text="Restart", callback_data="restart")],
        [InlineKeyboardButton(text="Sleep Mode", callback_data="sleep")],
        [InlineKeyboardButton(text="Hibernation", callback_data="hibernation")],
        [InlineKeyboardButton(text="Log out", callback_data="logout")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close")]
    ],
    'shutdownmenu': [
        [InlineKeyboardButton(text="Now", callback_data="shutdown_now")],
        [InlineKeyboardButton(text="1m", callback_data="shutdown_1m")],
        [InlineKeyboardButton(text="15m", callback_data="shutdown_15m")],
        [InlineKeyboardButton(text="30m", callback_data="shutdown_30m")],
        [InlineKeyboardButton(text="1h", callback_data="shutdown_1h")],
        [InlineKeyboardButton(text="6h", callback_data="shutdown_6h")],
        [InlineKeyboardButton(text="12h", callback_data="shutdown_12h")],
        [InlineKeyboardButton(text="🚫 Cancel", callback_data="shutdown_cancel")],
        [InlineKeyboardButton(text="❌ Close", callback_data="close")]
    ],
    'mainmenu': [
        [InlineKeyboardButton(text="Volume 🔊", callback_data="volume")],
        [InlineKeyboardButton(text="Control 🔴", callback_data="control")],
        [InlineKeyboardButton(text="Functions ⚙️", callback_data="functions")],
        [InlineKeyboardButton(text="Commands ❔", callback_data="commands")]
    ],
    'funcmenu': [
        [InlineKeyboardButton(text="❌ Close", callback_data="close")]
    ]
}

def register_handlers(dp, bot, telegram_id):
    @dp.callback_query(F.data == 'close')
    async def close(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['mainmenu'])
        msg = (f'{platform.node()} ({getbattery()}% 🔋)\n\n'
               f'⚡ CPU: {getcpu()}Mhz \n'
               f'🗂️ RAM: {getram()["percent"]}% ({round(getram()["used"],1)} Gb/{round(getram()["full"])} Gb) \n'
               f'💿 Disk: {getdrive()["percent"]}% ({round(getdrive()["used"],1)} Gb/{round(getdrive()["full"])} Gb) \n\n'
               f'📱 Runned: {getapps()} \n\n'
               f'🔊 Volume: {int(round(getvolume(),0))}%\n'
               f'☀️ Brightness: {brightness()}%')
        await bot.edit_message_caption(caption=msg, chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    @dp.callback_query(F.data == 'vadd10')
    async def vadd10(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['volumemenu'])
        spk = getspeaker()
        vol = getvolume()
        newvol = min((vol/100)+0.1, 1.0)
        spk.SetMasterVolumeLevelScalar(newvol, None)
        await bot.edit_message_caption(caption=f'🔊 Volume: {int(round(newvol*100,0))}%', chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    @dp.callback_query(F.data == 'vsub10')
    async def vsub10(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['volumemenu'])
        spk = getspeaker()
        vol = getvolume()
        newvol = max((vol/100)-0.1, 0.0)
        spk.SetMasterVolumeLevelScalar(newvol, None)
        await bot.edit_message_caption(caption=f'🔊 Volume: {int(round(newvol*100,0))}%', chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    @dp.callback_query(F.data == 'mute')
    async def mute(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['volumemenu'])
        spk = getspeaker()
        spk.SetMasterVolumeLevelScalar(0.0, None)
        await bot.edit_message_caption(caption='🔊 Volume: 0%', chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    @dp.callback_query(F.data == 'volume')
    async def volume_handler(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['volumemenu'])
        vol = getvolume()
        await bot.edit_message_caption(caption=f'🔊 Volume: {int(round(vol,0))}%', chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    @dp.callback_query(F.data == 'shutdown')
    async def shutdown_handler(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['shutdownmenu'])
        await bot.edit_message_caption(
            caption='⏻ Choose shutdown time:',
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb
        )

    @dp.callback_query(F.data == 'shutdown_now')
    async def shutdown_now_handler(call: CallbackQuery):
        shutdown_pc(0)
        await call.message.answer('💻 PC will shutdown now!')

    @dp.callback_query(F.data == 'shutdown_1m')
    async def shutdown_1m_handler(call: CallbackQuery):
        shutdown_pc(60)
        await call.message.answer('⏱️ PC will shutdown in 1 minute!')
        await close(call)

    @dp.callback_query(F.data == 'shutdown_15m')
    async def shutdown_15m_handler(call: CallbackQuery):
        shutdown_pc(900)
        await call.message.answer('⏱️ PC will shutdown in 15 minutes!')
        await close(call)

    @dp.callback_query(F.data == 'shutdown_30m')
    async def shutdown_30m_handler(call: CallbackQuery):
        shutdown_pc(1800)
        await call.message.answer('⏱️ PC will shutdown in 30 minutes!')
        await close(call)

    @dp.callback_query(F.data == 'shutdown_1h')
    async def shutdown_1h_handler(call: CallbackQuery):
        shutdown_pc(3600)
        await call.message.answer('⏱️ PC will shutdown in 1 hour!')
        await close(call)

    @dp.callback_query(F.data == 'shutdown_6h')
    async def shutdown_6h_handler(call: CallbackQuery):
        shutdown_pc(21600)
        await call.message.answer('⏱️ PC will shutdown in 6 hours!')
        await close(call)

    @dp.callback_query(F.data == 'shutdown_12h')
    async def shutdown_12h_handler(call: CallbackQuery):
        shutdown_pc(43200)
        await call.message.answer('⏱️ PC will shutdown in 12 hours!')
        await close(call)

    @dp.callback_query(F.data == 'shutdown_cancel')
    async def shutdown_cancel_handler(call: CallbackQuery):
        if cancel_shutdown():
            await call.message.answer('🚫 Shutdown cancelled!')
        else:
            await call.message.answer('❌ No scheduled shutdown to cancel')
        await close(call)

    @dp.callback_query(F.data == 'restart')
    async def restart_handler(call: CallbackQuery):
        os.system("shutdown /r /f /t 0")
        await call.message.answer('Done 👌')

    @dp.callback_query(F.data == 'sleep')
    async def sleep_handler(call: CallbackQuery):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        await call.message.answer('Done 👌')

    @dp.callback_query(F.data == 'hibernation')
    async def hibernation_handler(call: CallbackQuery):
        os.system("shutdown /h")
        await call.message.answer('Done 👌')

    @dp.callback_query(F.data == 'logout')
    async def logout_handler(call: CallbackQuery):
        os.system("shutdown /l")
        await call.message.answer('Done 👌')

    @dp.callback_query(F.data == 'control')
    async def control_handler(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['controlmenu'])
        msg = (f'{platform.node()} ({getbattery()}% 🔋)\n\n'
               f'⚡ CPU: {getcpu()}Mhz \n'
               f'🗂️ RAM: {getram()["percent"]}% ({round(getram()["used"],1)} Gb/{round(getram()["full"])} Gb) \n'
               f'💿 Disk: {getdrive()["percent"]}% ({round(getdrive()["used"],1)} Gb/{round(getdrive()["full"])} Gb) \n\n'
               f'📱 Runned: {getapps()} \n'
               f'🔊 Volume: {int(round(getvolume(),0))}%\n'
               f'☀️ Brightness: {brightness()}%')
        await bot.edit_message_caption(caption=msg, chat_id=call.message.chat.id,
                                       message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    @dp.callback_query(F.data == 'functions')
    async def functions_handler(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['funcmenu'])
        wifi = getwifi()
        bt = getbluetooth()
        await bot.edit_message_caption(caption=f'🛜 Wi-Fi: {"🟢" if wifi else "🔴"}\n📲 Bluetooth: {"🟢" if bt else "🔴"}',
                                       chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    @dp.callback_query(F.data == 'commands')
    async def commands_handler(call: CallbackQuery):
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="❌ Close", callback_data="close")]])
        commands_text = (
            "/run – open an app, website (www.example.com), folder, or file (C:\\Windows)\n\n"
            "/get – get the file from the specified path (e.g., C:\\Windows\\notepad.exe), limit: 50MB\n\n"
            "/window – will create a window with your text\n\n"
            "/cancel_shutdown – cancel scheduled shutdown"
        )
        await bot.edit_message_caption(
            caption=commands_text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb
        )

    @dp.message(Command("start"))
    async def start_message(message: types.Message):
        if str(message.from_user.id) == telegram_id:
            infomsg = await bot.send_message(chat_id=message.chat.id, text="⌛ Collecting information...")
            msg = (f'{platform.node()} ({getbattery()}% 🔋)\n\n'
                   f'⚡ CPU: {getcpu()}Mhz \n'
                   f'🗂️ RAM: {getram()["percent"]}% ({round(getram()["used"],1)} Gb/{round(getram()["full"])} Gb) \n'
                   f'💿 Disk: {getdrive()["percent"]}% ({round(getdrive()["used"],1)} Gb/{round(getdrive()["full"])} Gb) \n\n'
                   f'📱 Runned: {getapps()} \n\n'
                   f'🔊 Volume: {int(round(getvolume(),0))}%\n'
                   f'☀️ Brightness: {brightness()}%')
            kb = InlineKeyboardMarkup(inline_keyboard=inlineboards['mainmenu'])
            screenshot = screen()
            await bot.send_photo(chat_id=message.chat.id, photo=screenshot, caption=msg,
                                 parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
            await bot.delete_message(chat_id=message.chat.id, message_id=infomsg.message_id)

    @dp.message(Command("run"))
    async def run_command(message: types.Message):
        if str(message.from_user.id) != telegram_id:
            return
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Incorrect command usage (not enough arguments)")
            return
        data = args[1].strip()
        result = run(data)
        await message.reply(result)

    @dp.message(Command("get"))
    async def get_command(message: types.Message):
        if str(message.from_user.id) != telegram_id:
            return
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply("Incorrect command usage (not enough arguments)")
            return
        file_path = args[1].strip()
        file_obj, error = get_file(file_path)
        if error:
            await message.reply(error)
            return
        sending_msg = await message.reply("⏳ Sending the file...")
        await message.reply_document(file_obj)
        await sending_msg.delete()
        
    @dp.message(Command("window"))
    async def handle_window_command(message: types.Message):
        text = message.text.removeprefix("/window").strip()
        
        if not text:
            await message.reply("Incorrect command usage (not enough arguments)")
            return
        
        create_window(text)
        await message.reply("Done 👌")

    @dp.message(Command("cancel_shutdown"))
    async def cancel_shutdown_command(message: types.Message):
        if str(message.from_user.id) != telegram_id:
            return
        
        if cancel_shutdown():
            await message.reply("🚫 Shutdown cancelled!")
        else:
            await message.reply("❌ No scheduled shutdown to cancel")

async def run_bot():
    global bot, dp
    with open("config.json", "r") as f:
        cfg = json.load(f)
    token, telegram_id = cfg["bot_token"], cfg["telegram_id"]
    bot = Bot(token=token)
    dp = Dispatcher()
    register_handlers(dp, bot, telegram_id)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(run_bot())