import os, subprocess
import time
import pytz

from aiohttp import web
from datetime import datetime
from pyrogram import Client, filters

from ping import ping_server

app = Client("EenaduPapers",
             api_id=5540967,
             api_hash="eedf0196b0533f361b51b5b7082358e9",
             bot_token="6122593440:AAHUbLp73slAwbGON7U3cnlv8kYwIhurpLM",
             workers=50,
             max_concurrent_transmissions=20)

@app.on_message(filters.command('post'))
async def post(bot,message):
    chat_id=message.chat.id
    user_id=message.from_user.id
    msg_id = message.id
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    msg = await bot.send_message(message.from_user.id,'Getting All Papers',reply_to_message_id=message.id)
    date = now.strftime("%d-%m-%Y")
    subprocess.run(['python','eenadu.py'])
    await msg.edit("Uploading Papers to Telegram Channel")
    await bot.send_document("-1001532850156",f"Mains/Eenadu_TG {date}.pdf")
    await bot.send_document("-1001532850156",f"Mains/Eenadu_AP {date}.pdf")
    await bot.send_document("-1001532850156",f"Mains/Eenadu_GHYD {date}.pdf")
    await msg.edit("Done Uploading....")

@app.on_message(filters.command('ap'))
async def post(bot,message):
    chat_id=message.chat.id
    user_id=message.from_user.id
    msg_id = message.id
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    msg = await bot.send_message(message.from_user.id,'Getting All AP State Papers',reply_to_message_id=message.id)
    date = now.strftime("%Y-%m-%d")
    subprocess.run(['python','ap.py'])
    folder_path = "apdist"
    await bot.send_message("-1001532850156","AP District Papers")
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)


        await bot.send_document("-1001532850156",file_path)
        time.sleep(0.75)
    os.rmdir("apdist")
    await msg.edit("Done Uploading....")


@app.on_message(filters.command('ts'))
async def post(bot,message):
    chat_id=message.chat.id
    user_id=message.from_user.id
    msg_id = message.id
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    msg = await bot.send_message(message.from_user.id,'Getting All TS State Papers',reply_to_message_id=message.id)
    date = now.strftime("%Y-%m-%d")
    subprocess.run(['python','ts.py'])
    folder_path = "tsdist"
    await bot.send_message("-1001532850156","TSDistrict Papers")
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        await bot.send_document("-1001532850156",file_path)
        time.sleep(0.75)
    os.rmdir("tsdist")
    await msg.edit("Done Uploading....")

@app.on_message(filters.command('sun'))
async def post(bot,message):
    chat_id=message.chat.id
    user_id=message.from_user.id
    msg_id = message.id
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    msg = await bot.send_message(message.from_user.id,'Getting Sunday Papers',reply_to_message_id=message.id)
    date = now.strftime("%d-%m-%Y")
    subprocess.run(['python','sun.py'])
    folder_path = 'Sunday'
   # try:
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        await bot.send_document("-1001532850156",file_path)

    await msg.edit("Done Uploading....")
    os.rmdir("Sunday")
    #except:

     # await msg.edit("Papers Not Found")

routes = web.RouteTableDef()


@routes.get('/', allow_head=True)
async def root_route_handler(_):
    return web.json_response({'Status': 'Running'})


def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app


async def main():
    server = web.AppRunner(web_server())
    await server.setup()
    await web.TCPSite(server, '0.0.0.0', os.environ.get('PORT')).start()
    app.loop.create_task(ping_server())
    print('Server Started.')


app.start()
app.loop.run_until_complete(main())
app.loop.run_forever()