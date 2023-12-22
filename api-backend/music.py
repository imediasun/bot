from aiogram import types

from main import dp
from hendlers import check_ban_user, cb_check_ban_user, set_new_click

from keyboards import *
from translations import _
from youngkb import *
from states import MusicStatesGroup
from database.db import *

words_list = ["🎶MUSIC", "🔍Поиск", "🚀Новинки", "🔥Популярная"]

@dp.message_handler(lambda message : message.text in words_list)
async def news_text(message: types.Message):
    global index
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if message.text == '🎶MUSIC':
            await set_new_click(user_id)
            index = 0
            music = await get_popular_music()
            profile = await get_profile(message.from_user.id)
            if not music:
                if profile == 'young':
                    await message.answer(_("На данный момент эта функция недоступна!", lang),
                                         reply_markup=back_young_main_kb(lang))
                elif profile == 'pro':
                    await message.answer(_("На данный момент эта функция недоступна!", lang),
                                         reply_markup=back_pro_main(lang))
            else:
                all_music = list(music)[index: index + 5]
                ikb = InlineKeyboardMarkup()
                for data in all_music:
                    btn_music = InlineKeyboardButton(f"{data[3]} - {data[2]}",
                                                     callback_data=f'get_popular_music_{data[0]}')
                    ikb.add(btn_music)
                if profile == 'young':
                    next = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_popular_music')
                    back_main = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
                    if len(all_music) >= 5:
                        ikb.add(back_main, next)
                    else:
                        ikb.add(back_main)
                elif profile == 'pro':
                    next = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_popular_music')
                    back_main = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
                    if len(all_music) >= 5:
                        ikb.add(back_main, next)
                    else:
                        ikb.add(back_main)
                await message.answer(_("Все актуальные треки:", lang),
                                     reply_markup=ikb)
        elif message.text == '🔍Поиск':
            await set_new_click(user_id)
            await message.answer("Введите название или исполнителя песни:")
            await MusicStatesGroup.text.set()
        elif message.text == '🚀Новинки':
            await set_new_click(user_id)
            pass
        elif message.text == '🔥Популярная':
            await set_new_click(user_id)
            await get_popular_music()


@dp.callback_query_handler(lambda c: c.data.startswith('get_popular_music_'))
async def get_popular_music_for_user(callback: types.CallbackQuery):
    global index
    index = 0
    ban = await cb_check_ban_user(callback)
    if not ban:
        music = callback.data.split('_')[3]
        print(music)
        music_file = await get_music_file(music)
        bot = await callback.bot.me
        await callback.message.answer_audio(audio=music_file,
                                            caption=f"@{bot.username}")
    await callback.answer()

cb_words_list = ["next_all_music", "back_all_music", "next_popular_music", "back_popular_music", ]

@dp.callback_query_handler(lambda callback : callback.data in cb_words_list)
async def confirm_add_music(callback: types.CallbackQuery):
    global index, prev_index
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if callback.data == 'next_all_music':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            await get_next_all_music()
            await callback.answer()
        elif callback.data == 'back_all_music':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            await get_back_all_music()
            await callback.answer()
        elif callback.data == 'next_popular_music':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            index += 5
            prev_index = index + 5
            music = await get_popular_music()
            all_music = list(music)[index: index + 5]
            ikb = InlineKeyboardMarkup()
            for data in all_music:
                btn_music = InlineKeyboardButton(f"{data[3]} - {data[2]}",
                                                 callback_data=f'get_popular_music_{data[0]}')
                ikb.add(btn_music)
            next = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_popular_music')
            back_btn = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_popular_music')
            if len(all_music) < 5:
                ikb.add(back_btn)
            else:
                ikb.add(back_btn, next)
            # if len(all_music) > 5:
            #     ikb.add(back_btn)
            # else:
            #     ikb.add(back_btn, next)
            await callback.message.answer(_("Все актуальные треки:", lang),
                                          reply_markup=ikb)
            await callback.answer()
        elif callback.data == 'back_popular_music':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            index -= 5
            prev_index = index - 5
            profile = await get_profile(callback.from_user.id)
            music = await get_popular_music()
            all_music = list(music)[index: index + 5]
            ikb = InlineKeyboardMarkup()
            for data in all_music:
                btn_music = InlineKeyboardButton(f"{data[3]} - {data[2]}",
                                                 callback_data=f'get_popular_music_{data[0]}')
                ikb.add(btn_music)
            next = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_popular_music')
            back_btn = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_popular_music')
            if prev_index >= 0:
                ikb.add(back_btn, next)
            elif len(all_music) >= 5:
                if profile == 'young':
                    back_main = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
                    ikb.add(back_main, next)
                elif profile == 'pro':
                    back_main = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
                    ikb.add(back_main, next)
            await callback.message.answer(_("Все актуальные треки:", lang),
                                          reply_markup=ikb)
            await callback.answer()