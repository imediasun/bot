from uuid import uuid4
from aiogram import types
from aiogram.dispatcher import FSMContext

from config import control_add_chat
from hendlers import check_ban_user, cb_check_ban_user, is_valid_url
from main import dp, bot
from keyboards import *
from states import TourStateGroup
from youngkb import info_from_bd



words_list = ["TOURNAMENT", "🔙Вернутся в меню админа", "Добавить турнир", "Просмотреть все турниры"]

@dp.message_handler(lambda message: message.text in words_list)
async def all_text(message: types.Message):
    global index
    user_id = message.from_user.id
    moder_id = await get_moder_id(user_id)
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in moder_id or user_id in admin_id:
            if message.text == 'TOURNAMENT':
                await message.answer("Выберите действие:",
                                     reply_markup=admin_tour_menu_kb())
            elif message.text == '🔙Вернутся в меню админа':
                await message.answer("Вы вернулись в меню админа:",
                                     reply_markup=admin_kb())
            elif message.text == 'Добавить турнир':
                await message.answer("Укажите формат турнира:",
                                     reply_markup=admin_format_kb())
                await TourStateGroup.format.set()
            elif message.text == 'Просмотреть все турниры':
                index = 0
                tour = await admin_read_tour()
                all_tour = list(tour)[index: index + 2]
                index += 2
                if not tour:
                    await message.answer("Турниров на данный момент нету!")
                else:
                    await message.answer("Все актуальные турниры:")
                    for data in all_tour:
                        if not data[3]:
                            await message.answer(text=f"{data[2]}\n"
                                                      f"\n"
                                                      f"{data[4]}\n"
                                                      f"\n"
                                                      f"{data[5]}",
                                                 reply_markup=admin_edit_kb(data[0]))
                        else:
                            await message.answer_photo(photo=data[3],
                                                       caption=f"{data[2]}\n"
                                                               f"\n"
                                                               f"{data[4]}\n"
                                                               f"\n"
                                                               f"{data[5]}",
                                                       reply_markup=admin_edit_kb(data[0]))
                    if len(all_tour) < 2:
                        await message.answer("Это все турниры!")
                    else:
                        await message.answer("Продолжить просмотр турниров?",
                                             reply_markup=admin_next_tour_kb())


@dp.callback_query_handler(text="admin_next_tour")
async def moder_next_tour(callback : types.CallbackQuery):
    global index
    tour = await admin_read_tour()
    all_tour = list(tour)[index: index + 2]
    index += 2
    for data in all_tour:
        if not data[3]:
            await callback.message.answer(text=f"{data[2]}\n"
                                               f"\n"
                                               f"{data[4]}\n"
                                               f"\n"
                                               f"{data[5]}",
                                          reply_markup=admin_edit_kb(data[0]))
        else:
            await callback.message.answer_photo(photo=data[3],
                                                caption=f"{data[2]}\n"
                                                        f"\n"
                                                        f"{data[4]}\n"
                                                        f"\n"
                                                        f"{data[5]}",
                                                reply_markup=admin_edit_kb(data[0]))
    if len(all_tour) < 2:
        await callback.message.answer("Это все турниры!")
    else:
        await callback.message.answer("Продолжить просмотр турниров?",
                                      reply_markup=admin_next_tour_kb())
    await callback.message.delete()
    await callback.answer()



@dp.callback_query_handler(tour_cb.filter(action='confirm_add_tour'))
async def cb_confirm_add_tour(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        tour = await admin_get_tour(callback_data['id'])
        for data in tour:
            if not data[3]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Добавлен турнир {data[2]}\n"
                                            f"\n"
                                            f"MODER ID: {data[1]}\n"
                                            f"\n"
                                            f"{data[4]}\n"
                                            f"\n"
                                            f"{data[5]}",
                                       reply_markup=admin_edit_post_tour_ikb(data[0]))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[3],
                                     caption=f"Добавлен турнир {data[2]}\n"
                                             f"\n"
                                             f"MODER ID: {data[1]}\n"
                                             f"\n"
                                             f"{data[4]}\n"
                                             f"\n"
                                             f"{data[5]}",
                                     reply_markup=admin_edit_post_tour_ikb(data[0]))
        await callback.message.answer("Турнир успешно добавлен!",
                                      reply_markup=admin_kb())
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_tour'))
async def cb_edit_tour(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.reply("Укажите формат турнира:",
                                     reply_markup=admin_format_kb())
        await TourStateGroup.new_format.set()
        async with state.proxy() as data:
            data['tour_id'] = callback_data['id']
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_tour'))
async def cb_delete_tour(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await delete_tour(callback_data['id'])
        await callback.message.reply("Турнир успешно удален!",
                                     reply_markup=admin_kb())
        tour = await admin_get_tour(callback_data['id'])
        for data in tour:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удален турнир!\n"
                                        f"\n"
                                        f"{data[2]}\n"
                                        f"\n"
                                        f"{data[4]}\n"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: {callback.from_user.username}")
    await callback.answer()





@dp.message_handler(lambda message: not message.text == 'Squad'
                                    and not message.text == 'Duo'
                                    and not message.text == 'TDM'
                                    and not message.text == '❌Отменить', state=TourStateGroup.format)
async def check_tour_format(message: types.Message):
    await message.answer("Такого варианта ответа нету!")


@dp.message_handler(state=TourStateGroup.format)
async def load_format(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['format'] = message.text
        await message.answer("Отправь баннер турнира:",
                             reply_markup=info_from_bd("Пропустить"))
        await TourStateGroup.next()


@dp.message_handler(lambda message: not message.photo
                                    and not message.text == 'Пропустить', state=TourStateGroup.photo)
async def check_tour_photo(message: types.Message):
    await message.answer("Отправьте фото!")


@dp.message_handler(content_types=['photo', 'text'], state=TourStateGroup.photo)
async def load_photo_tournament(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['photo'] = ""
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправь информацию о турнире:",
                         reply_markup=info_from_bd("Пропустить"))
    await TourStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 300, state=TourStateGroup.desc)
async def check_tour_desc(message: types.Message):
    await message.answer("Описание турнира не должно превышать 300 символов!")


@dp.message_handler(state=TourStateGroup.desc)
async def load_desc_tour(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['desc'] = ""
    else:
        async with state.proxy() as data:
            data['desc'] = message.text
    await message.answer("Отправьте ссылку на турнир:")
    await TourStateGroup.next()


@dp.message_handler(lambda message: not is_valid_url(message.text), state=TourStateGroup.url)
async def check_tour_url(message: types.Message):
    await message.answer("Отправьте ссылку!")


@dp.message_handler(state=TourStateGroup.url)
async def load_tour_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
    tour_id = str(uuid4())
    await create_tour(state, message.from_user.id, tour_id)
    await message.answer("Так выглядит информация о турнире:")
    if data['photo'] == "":
        await message.answer(text=f"{data['format']}\n"
                                  f"\n"
                                  f"{data['desc']}\n"
                                  f"\n"
                                  f"{data['url']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['format']}\n"
                                           f"\n"
                                           f"{data['desc']}\n"
                                           f"\n"
                                           f"{data['url']}")
    await message.answer("Все верно?",
                         reply_markup=confirm_add_tour_ikb(tour_id))
    await state.finish()




@dp.message_handler(lambda message: not message.text == 'Squad'
                                    and not message.text == 'Duo'
                                    and not message.text == 'TDM'
                                    and not message.text == '❌Отменить', state=TourStateGroup.new_format)
async def check_tour_format(message: types.Message):
    await message.answer("Такого варианта ответа нету!")


@dp.message_handler(state=TourStateGroup.new_format)
async def load_new_format_tour(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['format'] = message.text
        await message.answer("Отправьте баннер турнира:",
                             reply_markup=info_from_bd("Оставить прошлый"))
        await TourStateGroup.next()


@dp.message_handler(lambda message: not message.photo
                                    and not message.text == 'Оставить прошлый', state=TourStateGroup.new_photo)
async def check_tour_photo(message: types.Message):
    await message.answer("Отправьте фото!")


@dp.message_handler(content_types=['photo', 'text'], state=TourStateGroup.new_photo)
async def load_new_photo_tour(message: types.Message, state: FSMContext):
    if message.text == 'Оставить прошлый':
        async with state.proxy() as data:
            banner = await get_banner_tour(data['tour_id'])
            data['photo'] = banner
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправьте информацию о турнире:",
                         reply_markup=info_from_bd("Пропустить"))
    await TourStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 300, state=TourStateGroup.new_desc)
async def check_tour_desc(message: types.Message):
    await message.answer("Описание турнира не должно превышать 300 символов!")


@dp.message_handler(state=TourStateGroup.new_desc)
async def load_new_desc_tour(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            desc = await get_tour_desc(data['tour_id'])
            data['desc'] = desc
    else:
        async with state.proxy() as data:
            data['desc'] = message.text
    await message.answer("Отправьте ссылку на турнир:",
                         reply_markup=info_from_bd("Пропустить"))
    await TourStateGroup.next()


@dp.message_handler(lambda message: not is_valid_url(message.text) and not message.text == 'Пропустить', state=TourStateGroup.new_url)
async def check_tour_url(message: types.Message):
    await message.answer("Отправьте ссылку!")


@dp.message_handler(state=TourStateGroup.new_url)
async def load_new_tour_url(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            url = await get_tour_url(data['tour_id'])
            data['url'] = url
    else:
        async with state.proxy() as data:
            data['url'] = message.text
    await admin_update_tour(state, message.from_user.id)
    await message.answer("Так выглядит информация о турнире:")
    if not data['photo']:
        await message.answer(text=f"{data['format']}\n"
                                  f"\n"
                                  f"{data['desc']}\n"
                                  f"\n"
                                  f"{data['url']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['format']}\n"
                                           f"\n"
                                           f"{data['desc']}\n"
                                           f"\n"
                                           f"{data['url']}")
    await message.answer("Все верно?",
                         reply_markup=confirm_add_tour_ikb(data['tour_id']))
    await state.finish()