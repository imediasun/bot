from aiogram import types
from aiogram.dispatcher import FSMContext
from uuid import uuid4

from config import control_add_chat
from hendlers import check_ban_user, cb_check_ban_user, is_valid_url
from main import dp, bot
from database import *
from keyboards import *
from youngkb import info_from_bd
from states import EventStateGroup



words_list = ['EVENT', "Добавить ивент", "Просмотреть все ивенты", "🕒15:00ㅤ", "🕒18:00ㅤ", "🕒21:00ㅤ",
              "🕒00:00ㅤ"]

@dp.message_handler(lambda message: message.text in words_list)
async def all_text(message: types.Message):
    global index
    user_id = message.from_user.id
    moder_id = await get_moder_id(user_id)
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in moder_id or user_id in admin_id:
            if message.text == 'EVENT':
                await message.answer("Выберите действие:",
                                     reply_markup=admin_menu_event_kb())
            elif message.text == 'Добавить ивент':
                await message.answer("Укажите время ивента:",
                                     reply_markup=admin_put_time())
                await EventStateGroup.time.set()
            elif message.text == 'Просмотреть все ивенты':
                await message.answer("Выберите время ивента:",
                                     reply_markup=admin_search_time())
            else:
                if message.text == '🕒15:00ㅤ':
                    await send_info_event("15", message)
                elif message.text == '🕒18:00ㅤ':
                    await send_info_event("18", message)
                elif message.text == '🕒21:00ㅤ':
                    await send_info_event("21", message)
                elif message.text == '🕒00:00ㅤ':
                    await send_info_event("00", message)



# ADMIN EVENTS
@dp.callback_query_handler(tour_cb.filter(action='admin_next_event'))
async def cb_admin_next_event(callback : types.CallbackQuery, callback_data : dict):
    global index
    ban = await cb_check_ban_user(callback)
    if not ban:
        lang = await get_user_lang(callback.from_user.id)
        events = await get_events(callback_data['id'])
        all_events = list(events)[index: index + 2]
        index += 2
        for data in all_events:
            currency = await get_region_currency(lang)
            amount_curr = await get_amount_curr(currency)
            amount = float(data[4]) * float(amount_curr)
            if not data[3]:
                await callback.message.answer(f"{data[6]}\n"
                                              f"\n"
                                              f"{data[5]}\n"
                                              f"\n"
                                              f"Стоимость слота: {round(amount, 0)} {currency}\n"
                                              f"\n"
                                              f"{data[7]}",
                                              reply_markup=admin_edit_event_kb(data[0]))
            else:
                await callback.message.answer_photo(photo=data[3],
                                                    caption=f"{data[6]}\n"
                                                            f"\n"
                                                            f"{data[5]}\n"
                                                            f"\n"
                                                            f"Стоимость слота: {round(amount, 0)} {currency}\n"
                                                            f"\n"
                                                            f"{data[7]}",
                                                    reply_markup=admin_edit_event_kb(data[0]))
        if len(all_events) < 2:
            await callback.message.answer("Это все слоты!",
                                          reply_markup=admin_menu_event_kb())
        else:
            await callback.message.answer("Продолжить просмотр?",
                                          reply_markup=admin_next_event_ikb(callback_data['id']))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='conf_add_event'))
async def cb_conf_add_event(callback : types.CallbackQuery, callback_data : dict):
    ban = await check_ban_user(callback)
    if not ban:
        await callback.message.answer("✅Ивент успешно добавлен!",
                                      reply_markup=admin_kb())
        event = await get_event(callback_data['id'])
        for data in event:
            if not data[3]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Добавлен ивент!\n"
                                            f"\n"
                                            f"{data[6]}\n"
                                            f"\n"
                                            f"{data[2]}"
                                            f"\n"
                                            f"{data[5]}\n"
                                            f"\n"
                                            f"Цена: {data[4]}\n"
                                            f"\n"
                                            f"{data[7]}\n"
                                            f"\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: @{callback.from_user.username}",
                                       reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[3],
                                     caption=f"{data[6]}\n"
                                             f"\n"
                                             f"{data[2]}"
                                             f"\n"
                                             f"{data[5]}\n"
                                             f"\n"
                                             f"Цена: {data[4]}\n"
                                             f"\n"
                                             f"{data[7]}\n"
                                             f"\n"
                                             f"ID: {data[1]}\n"
                                             f"USERNAME: @{callback.from_user.username}",
                                     reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_event'))
async def cb_delete_event(callback: types.CallbackQuery, callback_data: dict):
    ban = await check_ban_user(callback)
    if not ban:
        await delete_event(callback_data['id'])
        event = await get_event(callback_data['id'])
        await callback.message.reply("Ивент успешно удален!",
                                     reply_markup=admin_search_time())
        for data in event:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удален ивент!\n"
                                        f"\n"
                                        f"{data[6]}\n"
                                        f"\n"
                                        f"{data[2]}:00\n"
                                        f"\n"
                                        f"{data[5]}\n"
                                        f"\n"
                                        f"Цена: {data[4]}\n"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: @{callback.from_user.username}")
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_event'))
async def cb_edit_event(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban = await check_ban_user(callback)
    if not ban:
        await callback.message.answer("Укажите время ивента:",
                                      reply_markup=admin_put_time())
        await EventStateGroup.new_time.set()
        async with state.proxy() as data:
            data['tour_id'] = callback_data['id']
    await callback.message.delete()
    await callback.answer()



# STATES
@dp.message_handler(lambda message : not message.text == '15:00'
                                     and not message.text == '18:00'
                                     and not message.text == '21:00'
                                     and not message.text == '00:00'
                                     and not message.text == '❌Отменить', state=EventStateGroup.time)
async def check_load_time_event(message : types.Message):
    await message.answer("Такого варианта ответа нету!")

@dp.message_handler(state=EventStateGroup.time)
async def load_time_event(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['time'] = message.text.split(':')[0]
        await message.answer("Отправьте баннер ивента:",
                             reply_markup=info_from_bd("Пропустить"))
        await EventStateGroup.next()


@dp.message_handler(lambda message : not message.photo
                                     and not message.text == 'Пропустить', state=EventStateGroup.photo)
async def check_load_photo_event(message : types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['photo', 'text'], state=EventStateGroup.photo)
async def load_photo_event(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['photo'] = ""
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправь информацию об ивенте:",
                         reply_markup=ReplyKeyboardRemove())
    await EventStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 300, state=EventStateGroup.desc)
async def check_load_desc_event(message : types.Message):
    await message.answer("Описание ивента не должно превышать 300 символов!")

@dp.message_handler(state=EventStateGroup.desc)
async def load_desc_event(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer("Отправьте стоимость слота:")
    await EventStateGroup.next()


@dp.message_handler(lambda message : not message.text.isdigit(), state=EventStateGroup.price)
async def check_load_price_event(message : types.Message):
    await message.answer("Отправьте стоимость числом!")

@dp.message_handler(state=EventStateGroup.price)
async def load_price_event(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Отправьте название ивента:")
    await EventStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 100, state=EventStateGroup.tour_name)
async def check_load_tour_name(message : types.Message):
    await message.answer("Название турнира не должно превышать 100 символов!")

@dp.message_handler(state=EventStateGroup.tour_name)
async def load_event_name(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['tour_name'] = message.text
    await message.answer("Отправьте количество слотов:")
    await EventStateGroup.next()


@dp.message_handler(lambda message : not message.text.isdigit(), state=EventStateGroup.amount)
async def check_load_amount_event(message : types.Message):
    await message.answer("Отправьте число!")

@dp.message_handler(state=EventStateGroup.amount)
async def load_amount_event(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.answer("Отправьте ссылку на ивент:")
    await EventStateGroup.next()


@dp.message_handler(lambda message : not is_valid_url(message.text), state=EventStateGroup.link)
async def check_load_link_event(message : types.Message):
    await message.answer("Это не ссылка!")

@dp.message_handler(state=EventStateGroup.link)
async def load_event_link(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    tour_id = str(uuid4())
    await create_events(state, tour_id, message.from_user.id)
    if not data['photo']:
        await message.answer(f"{data['tour_name']}\n"
                             f"\n"
                             f"{data['time']}:00\n"
                             f"\n"
                             f"{data['desc']}\n"
                             f"\n"
                             f"Количество: {data['amount']}\n"
                             f"Цена: {data['price']}\n"
                             f"\n"
                             f"{data['link']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['tour_name']}\n"
                                           f"\n"
                                           f"{data['time']}:00\n"
                                           f"\n"
                                           f"{data['desc']}\n"
                                           f"\n"
                                           f"Количество: {data['amount']}\n"
                                           f"Цена: {data['price']}\n"
                                           f"\n"
                                           f"{data['link']}")
    await message.answer("Все верно?",
                         reply_markup=conf_add_event_ikb(tour_id))
    await state.finish()




@dp.message_handler(lambda message : not message.text == '15:00'
                                     and not message.text == '18:00'
                                     and not message.text == '21:00'
                                     and not message.text == '00:00'
                                     and not message.text == '❌Отменить', state=EventStateGroup.new_time)
async def check_load_new_time_event(message : types.Message):
    await message.answer("Такого варианта ответа нету!")

@dp.message_handler(state=EventStateGroup.new_time)
async def load_new_time_event(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['time'] = message.text.split(':')[0]
        await message.answer("Отправьте баннер ивента:",
                             reply_markup=info_from_bd("Пропустить"))
        await EventStateGroup.next()


@dp.message_handler(lambda message : not message.photo
                                     and not message.text == "Пропустить", state=EventStateGroup.new_photo)
async def check_load_new_photo_event(message : types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['photo', 'text'], state=EventStateGroup.new_photo)
async def load_new_photo_event(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            photo = await get_photo_event(data['tour_id'])
            data['photo'] = photo
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправь информацию об ивенте:",
                         reply_markup=info_from_bd("Пропустить"))
    await EventStateGroup.next()

@dp.message_handler(lambda message : len(message.text) > 300, state=EventStateGroup.new_desc)
async def check_load_new_desc_event(message : types.Message):
    await message.answer("Описание ивента не должно превышать 300 символов!")

@dp.message_handler(state=EventStateGroup.new_desc)
async def load_new_desc_event(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            desc = await get_desc_event(data['tour_id'])
            data['desc'] = desc
    else:
        async with state.proxy() as data:
            data['desc'] = message.text
    await message.answer("Отправьте стоимость слота:",
                         reply_markup=info_from_bd("Пропустить"))
    await EventStateGroup.next()


@dp.message_handler(lambda message : not message.text.isdigit()
                                     and not message.text == 'Пропустить', state=EventStateGroup.new_price)
async def check_load_new_price_event(message : types.Message):
    await message.answer("Отправьте ценну числом!")

@dp.message_handler(state=EventStateGroup.new_price)
async def load_new_price_event(message : types.Message, state : FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            price = await get_price_event(data['tour_id'])
            data['price'] = price
    else:
        async with state.proxy() as data:
            data['price'] = message.text
    await message.answer("Отправьте название ивента:",
                         reply_markup=info_from_bd("Пропустить"))
    await EventStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 100, state=EventStateGroup.new_tour_name)
async def check_load_new_tour_name(message : types.Message):
    await message.answer("Название турнира не должно превышать 100 символов!")

@dp.message_handler(state=EventStateGroup.new_tour_name)
async def load_new_event_name(message : types.Message, state : FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            event_name = await get_event_name(data['tour_id'])
            data['tour_name'] = event_name
    else:
        async with state.proxy() as data:
            data['tour_name'] = message.text
    amount = await get_amount_events(data['tour_id'])
    await message.answer("Отправьте количество слотов:",
                         reply_markup=info_from_bd(amount))
    await EventStateGroup.next()


@dp.message_handler(lambda message : not message.text.isdigit(), state=EventStateGroup.new_amount)
async def check_new_load_amount_event(message : types.Message):
    await message.answer("Отправьте число!")

@dp.message_handler(state=EventStateGroup.new_amount)
async def load_new_amount_event(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.answer("Отправьте ссылку на ивент:",
                         reply_markup=info_from_bd("Пропустить"))
    await EventStateGroup.next()


@dp.message_handler(lambda message : not is_valid_url(message.text)
                                     and not message.text == 'Пропустить', state=EventStateGroup.new_link)
async def check_load_new_link_event(message : types.Message):
    await message.answer("Это не ссылка!")

@dp.message_handler(state=EventStateGroup.new_link)
async def load_event_new_link(message : types.Message, state : FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            link = await get_link_event(data['tour_id'])
            data['link'] = link
    else:
        async with state.proxy() as data:
            data['link'] = message.text
    await update_event(state, message.from_user.id)
    if not data['photo']:
        await message.answer(f"{data['tour_name']}\n"
                             f"\n"
                             f"{data['time']}:00\n"
                             f"\n"
                             f"{data['desc']}\n"
                             f"\n"
                             f"Количество: {data['amount']}\n"
                             f"Цена: {data['price']}\n"
                             f"\n"
                             f"{data['link']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['tour_name']}\n"
                                           f"\n"
                                           f"{data['time']}:00\n"
                                           f"\n"
                                           f"{data['desc']}\n"
                                           f"\n"
                                           f"Количество: {data['amount']}\n"
                                           f"Цена: {data['price']}\n"
                                           f"\n"
                                           f"{data['link']}")
    await message.answer("Все верно?",
                         reply_markup=conf_add_event_ikb(data['tour_id']))
    await state.finish()


async def send_info_event(time, message):
    index = 0
    events = await get_events(time)
    if not events:
        await message.answer("Слотов на это время нету!")
    else:
        await message.answer(f"Все актуальные ивенты на {time}:00:")
        all_events = list(events)[index: index + 2]
        index += 2
        for data in all_events:
            if not data[3]:
                await message.answer(f"{data[6]}\n"
                                     f"\n"
                                     f"{data[2]}:00\n"
                                     f"\n"
                                     f"{data[5]}\n"
                                     f"\n"
                                     f"Стоимость слота: {data[4]}\n"
                                     f"\n"
                                     f"{data[7]}",
                                     reply_markup=admin_edit_event_kb(data[0]))
            else:
                await message.answer_photo(photo=data[3],
                                           caption=f"{data[6]}\n"
                                                   f"\n"
                                                   f"{data[2]}:00\n"
                                                   f"\n"
                                                   f"{data[5]}\n"
                                                   f"\n"
                                                   f"Стоимость слота: {data[4]}\n"
                                                   f"\n"
                                                   f"{data[7]}",
                                           reply_markup=admin_edit_event_kb(data[0]))
        if len(all_events) < 2:
            await message.answer("Это все слоты!",
                                 reply_markup=admin_menu_event_kb())
        else:
            await message.answer("Продолжить просмотр?",
                                 reply_markup=admin_next_event_ikb(time))