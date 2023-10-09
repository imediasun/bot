import asyncio
import multiprocessing
import disnake
from aiogram import Dispatcher, Bot, executor, types
from disnake.ext import commands as commands_ds

from config import *

bot = Bot(TG_TOKEN)
dp = Dispatcher(bot=bot)

intents = disnake.Intents.all()
bot_ds = commands_ds.Bot(command_prefix="/", intents=intents)


async def send_ds_mess(channel_id, mess):
    channel = bot_ds.get_channel(channel_id)
    print(channel)
    await channel.send(mess)


@bot_ds.event
async def on_ready():
    # await send_ds_mess(1159239010930130976, "hello world")
    print(f'Logged in as {bot_ds.user.name}')
    await send_ds_mess(1160219846571733042, "jjj")


@dp.message_handler(commands=['start'])
async def cd_start(message: types.Message):
    await message.answer("Привет друг!")
    channel = bot_ds.get_channel(1160219846571733042)
    print(channel)
    await channel.send("hello world")


async def send_mess():
    await bot.send_message(chat_id=1810112650,
                           text="I`m here!")


@bot_ds.command()
async def start(ctx):
    await ctx.send("hi!")
    await send_mess()
    await send_ds_mess(1159239010930130976, "hello world")


def run_tg_bot():
    executor.start_polling(dp,
                           skip_updates=True)


def run_ds_bot():
    bot_ds.run(token=DS_TOKEN)


if __name__ == "__main__":
    discord_process = multiprocessing.Process(target=run_ds_bot)
    telegram_process = multiprocessing.Process(target=run_tg_bot)

    discord_process.start()
    telegram_process.start()

    discord_process.join()
    telegram_process.join()
