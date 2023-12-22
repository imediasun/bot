import sys
sys.path.append('..')

from uuid import uuid4
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup

from main import dp, bot
from config import *
from hendlers import check_ban_user, cb_check_ban_user

from database.db import *
from keyboards import *
from youngkb import *
from states import AdminMusicStatesGroup
from database.db import *

words_list = ["MUSIC", "Обновить", "Загрузить", 'Просмотреть треки']

@dp.message_handler(lambda message : message.text in words_list)
async def cd_admin(message: types.Message):
    user_id = message.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in admin_id or user_id in ceo:
            print(admin_id)
            if message.text == 'MUSIC':
                await message.answer("Выберите действие:",
                                     reply_markup=admin_music_menu_kb())
            elif message.text == 'Обновить':
                await message.answer("Данная команда в разработке!")
                # await message.answer("Укажите что хотите обновить:",
                #                      reply_markup=admin_kind_music_kb())
                # await AdminMusicStatesGroup.kind.set()
            elif message.text == 'Загрузить':
                await AdminMusicStatesGroup.load_kind.set()
                await message.answer("Выберите действие:",
                                     reply_markup=admin_kind_music_kb())
            elif message.text == 'Просмотреть треки':
                music = await get_music_for_delete()
                await message.answer("Все актуальные треки:")
                for data in music:
                    await message.answer_audio(audio=data[4],
                                               caption=f"{data[3]} - {data[2]}",
                                               reply_markup=admin_edit_music_ikb(data[0]))
                await message.answer("Это все актуальные треки!")



# ADMIN MUSIC
@dp.callback_query_handler(tour_cb.filter(action='confirm_add_music'))
async def confirm_add_music(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if user_id in admin_id:
            await callback.message.answer("Трек успешно добавлен!",
                                          reply_markup=admin_kb())
            music = await get_music(callback_data['id'])
            for data in music:
                await bot.send_audio(chat_id=control_add_chat,
                                     audio=data[4],
                                     caption=f"Добавлен трек\n"
                                             f"\n"
                                             f"ADMIN ID: {callback.from_user.id}\n"
                                             f"USERNAME: @{callback.from_user.username}"
                                             f"\n"
                                             f"{data[2]} - {data[3]}",
                                     reply_markup=admin_edit_music_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()



@dp.callback_query_handler(tour_cb.filter(action='delete_music'))
async def admin_delete_music(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if user_id in admin_id:
            await delete_music(callback_data['id'])
            await callback.message.reply("Музыка успешно удалена!")
            music = await get_music(callback_data['id'])
            for data in music:
                await bot.send_audio(chat_id=control_add_chat,
                                     audio=data[4],
                                     caption=f"Удален трек!\n"
                                             f"\n"
                                             f"ADMIN ID: {callback.from_user.id}\n"
                                             f"USERNAME: @{callback.from_user.username}"
                                             f"\n"
                                             f"{data[2]} - {data[3]}",
                                     reply_markup=admin_edit_music_ikb(data[0]))
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_music'))
async def edit_music(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = callback.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if user_id in admin_id:
            await callback.message.answer("Выберите действие:",
                                          reply_markup=admin_kind_music_kb())
            await AdminMusicStatesGroup.new_load_kind.set()
            async with state.proxy() as data:
                data['music_id'] = callback_data['id']
    await callback.answer()


# MUSIC
# @dp.callback_query_handler(lambda c: c.data.startswith('get_music_'))
# async def get_music_for_user(callback: types.CallbackQuery):
#     global index
#     index = 0
#     music_id = callback.data.split('_')[-1]
#     await callback.message.answer("Ожидайте идет загрузка!")
#     music_file = await get_music_file(music_id)
#     bot = await callback.bot.me
#     await callback.message.answer_audio(audio=bytes(music_file),
#                                         caption=f"Скачано при помощи: @{bot.username}")



# STATES MUSIC
@dp.message_handler(state=AdminMusicStatesGroup.kind)
async def admin_load_music(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=admin_kb())
    elif message.text == '🔍Вся музыка':
        await message.answer("Обновление успешно запущено!")
        async with state.proxy() as data:
            data['kind'] = message.text
        # await delete_all_music(data['kind'])
        storage_number = 1
        link = "https://sound-boss.net"
        for storage in range(1474):
            response = requests.get(f"{link}/page/{storage_number}/").text
            soup = BeautifulSoup(response, 'lxml')
            block = soup.find('div', class_='section')
            all_music = block.find_all('div', class_='play-item fx-row fx-middle js-item')
            for music in all_music:
                music_block = music.find('a', class_='play-dl play-btn')
                music_link = music_block.get('href')
                music_bytes = requests.get(f'{link}{music_link}').content
                artist = music.find('div', class_='play-artist nowrap').text
                music_name = music.find('div', class_='play-title nowrap').text
                # await create_all_music(message.from_user.id, artist, music_name, music_bytes, data['kind'])
            print(f"Загрузил {storage_number} страницу!")
            storage_number += 1
        await message.answer("✅Обновлене успешно завершено")
    elif message.text == '🔥Популярное':
        await message.answer("Обновление успешно запущено!")
        async with state.proxy() as data:
            data['kind'] = message.text
    await state.finish()


@dp.message_handler(lambda message: not message.text == '❌Отменить'
                                    and not message.text == '🔥Популярная',
                    state=AdminMusicStatesGroup.load_kind)
async def check_load_kind_music(message: types.Message):
    await message.answer("Такого варианта ответа нету!")


@dp.message_handler(state=AdminMusicStatesGroup.load_kind)
async def admin_load_music(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=admin_kb())
        await state.finish()
    elif message.text == '🔥Популярная':
        async with state.proxy() as data:
            data['kind'] = message.text
        await message.answer("Отправьте трек:")
        await AdminMusicStatesGroup.next()


@dp.message_handler(lambda message: not message.audio, state=AdminMusicStatesGroup.music_file)
async def check_load_music_file(message: types.Message):
    await message.answer("Отправьте аудио файл!")


@dp.message_handler(content_types=['audio'], state=AdminMusicStatesGroup.music_file)
async def load_music_audio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['music_file'] = message.audio.file_id
    await message.answer("Отправьте название трека:")
    await AdminMusicStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 30, state=AdminMusicStatesGroup.name)
async def check_load_name(message: types.Message):
    await message.answer("Название трека не должно превышать 30 символов!")


@dp.message_handler(state=AdminMusicStatesGroup.name)
async def load_music_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Укажите исполнителя:")
    await AdminMusicStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 30, state=AdminMusicStatesGroup.artist)
async def check_load_name(message: types.Message):
    await message.answer("Имя артиста не должно превышать 30 символов!")


@dp.message_handler(state=AdminMusicStatesGroup.artist)
async def load_music_artist(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['artist'] = message.text
    music_id = str(uuid4())
    await create_all_music(message.from_user.id, music_id, state)
    await message.answer_audio(audio=data['music_file'],
                               caption=f"{data['name']} - {data['artist']}")
    await message.answer("Все верно?",
                         reply_markup=admin_confirm_music_ikb(music_id))
    await state.finish()


@dp.message_handler(lambda message: not message.text == '❌Отменить'
                                    and not message.text == '🔥Популярная',
                    state=AdminMusicStatesGroup.new_load_kind)
async def check_load_new_kind_music(message: types.Message):
    await message.answer("Такого варианта ответа нету!")


@dp.message_handler(state=AdminMusicStatesGroup.new_load_kind)
async def admin_load_music(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=admin_kb())
        await state.finish()
    elif message.text == '🔥Популярная':
        async with state.proxy() as data:
            data['kind'] = message.text
        await message.answer("Отправьте трек:")
        await AdminMusicStatesGroup.next()


@dp.message_handler(lambda message: not message.audio, state=AdminMusicStatesGroup.new_music_file)
async def check_load_music_file(message: types.Message):
    await message.answer("Отправьте аудио файл!")


@dp.message_handler(content_types=['audio'], state=AdminMusicStatesGroup.new_music_file)
async def load_music_audio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['music_file'] = message.audio.file_id
    await message.answer("Отправьте название трека:")
    await AdminMusicStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 30, state=AdminMusicStatesGroup.name)
async def check_load_name(message: types.Message):
    await message.answer("Название трека не должно превышать 30 символов!")


@dp.message_handler(state=AdminMusicStatesGroup.new_name)
async def load_music_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Укажите исполнителя:")
    await AdminMusicStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 30, state=AdminMusicStatesGroup.artist)
async def check_load_name(message: types.Message):
    await message.answer("Имя артиста не должно превышать 30 символов!")


@dp.message_handler(state=AdminMusicStatesGroup.new_artist)
async def load_music_artist(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['artist'] = message.text
    await update_popular_music(state, message.from_user.id)
    await message.answer_audio(audio=data['music_file'],
                               caption=f"{data['name']} - {data['artist']}")
    await bot.send_audio(chat_id=control_add_chat,
                         audio=data['music_file'],
                         caption=f"Изминен трек\n"
                                 f"\n"
                                 f"ADMIN ID: {message.from_user.id}\n"
                                 f"\n"
                                 f"{data['name']} - {data['artist']}",
                         reply_markup=admin_edit_music_ikb(data['music_id']))
    await message.answer("Все верно?",
                         reply_markup=admin_confirm_music_ikb(data['music_id']))
    await state.finish()