import sys
sys.path.append(".")

from database.db import *

from aiogram import executor


async def on_startup(_):

   await db_start()


if __name__ == '__main__':
    # main
    from hendlers import dp
    from payvipslot import dp
    from ucshop import dp
    from music import dp
    from support import dp
    # pro
    from tour import dp
    from vipslots import dp
    from events import dp
    from freeagent import dp
    from freeteam import dp
    # young
    from prac import dp
    from pracvipslot import dp
    from youngfg import dp
    from youngft import dp
    # moder
    from modertour import dp
    from modervipslot import dp
    from moderevent import dp
    from moderyoungpg import dp
    from moderyoungvsp import dp
    # admin
    from admin.admin import dp
    from admin.adminban import dp
    from admin.adminmusic import dp
    from admin.adminpayment import dp
    from admin.adminpayvs import dp
    from admin.adminucshop import dp
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)