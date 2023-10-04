from uuid import uuid4

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import control_add_chat
from hendlers import check_ban_user, cb_check_ban_user, is_valid_url
from main import dp, bot
from database import *
from keyboards import *
from states import VIPslotStateGroup
from youngkb import info_from_bd




words_list = ["VIP SLOTS", "Добавить слот", "Просмотреть все слоты", "Удалить все слоты", "Qualificationㅤ", "1/4 STAGEㅤ",
              "1/2 STAGEㅤ", "FINAL STAGEㅤ", "GRAND-FINAL STAGEㅤ"]

@dp.message_handler(lambda message: message.text in words_list)
async def all_text(message: types.Message, state : FSMContext):
    global index
    user_id = message.from_user.id
    moder_id = await get_moder_id(user_id)
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in moder_id or user_id in admin_id:
            if message.text == 'VIP SLOTS':
                await message.answer("Выберите действие:",
                                     reply_markup=admin_vip_menu_kb())
            elif message.text == 'Добавить слот':
                await message.answer("Укажите стадию турнира:",
                                     reply_markup=admin_stage_vip_kb())
                tour_id = str(uuid4())
                await VIPslotStateGroup.stage.set()
                async with state.proxy() as data:
                    data['tour_id'] = tour_id
            elif message.text == 'Просмотреть все слоты':
                await message.answer("Выберите стадию:",
                                     reply_markup=admin_chek_vip_kb())
            elif message.text == "Удалить все слоты":
                await message.answer("Вы действительно хотите удалить все слоты?",
                                     reply_markup=admin_delete_all_vs_ikb())
            else:
                index = 0
                if message.text == "Qualificationㅤ":
                    await send_info_vip_slot("Qualification", message)
                elif message.text == "1/4 STAGEㅤ":
                    await send_info_vip_slot("1/4 STAGE", message)
                elif message.text == "1/2 STAGEㅤ":
                    await send_info_vip_slot("1/2 STAGE", message)
                elif message.text == "FINAL STAGEㅤ":
                    await send_info_vip_slot("FINAL STAGE", message)
                elif message.text == "GRAND-FINAL STAGEㅤ":
                    await send_info_vip_slot("GRAND-FINAL STAGE", message)





@dp.callback_query_handler(tour_cb.filter(action='delete_vip_slot'))
async def cb_delete_vip(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        vip_slot = await get_vip_slot(callback_data['id'])
        await delete_vip_slot(callback_data['id'])
        await callback.message.reply("Слот успешно удален!",
                                     reply_markup=admin_chek_vip_kb())
        for data in vip_slot:
            amount_slots = await get_amount_vip_slots_str(data[0])
            time = await get_time_vip_slot_str(data[0])
            if not data[3]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Удален VIP SLOT!\n"
                                            f"\n"
                                            f"{data[6]}\n"
                                            f"\n"
                                            f"{data[2]}\n"
                                            f"\n"
                                            f"{data[4]}\n"
                                            f"TIME: {time}\n"
                                            f"Количество: {amount_slots}\n"
                                            f"Цена: {data[5]}\n"
                                            f"\n"
                                            f"{data[7]}\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: @{callback.from_user.username}",
                                       reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[3],
                                     caption=f"Удален VIP SLOT!\n"
                                             f"\n"
                                             f"{data[6]}\n"
                                             f"\n"
                                             f"{data[2]}\n"
                                             f"\n"
                                             f"{data[4]}\n"
                                             f"TIME: {time}\n"
                                             f"Количество: {amount_slots}\n"
                                             f"Цена: {data[5]}\n"
                                             f"\n"
                                             f"{data[7]}\n"
                                             f"ID: {data[1]}\n"
                                             f"USERNAME: @{callback.from_user.username}",
                                     reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='admin_edit_vip_slot'))
async def cb_admin_edit_vip(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.reply("Укажите стадию турнира:",
                                     reply_markup=admin_stage_vip_kb())
        await VIPslotStateGroup.new_stage.set()
        async with state.proxy() as data:
            data['tour_id'] = callback_data['id']
    await callback.message.delete()
    await callback.answer()

@dp.callback_query_handler(tour_cb.filter(action='confirm_add_vip_slot'))
async def cb_conf_add_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer("✅Слот успешно добавлен!",
                                      reply_markup=admin_kb())
        vip_slot = await get_vip_slot(callback_data['id'])
        for data in vip_slot:
            amount_slots = await get_amount_vip_slots_str(data[0])
            time = await get_time_vip_slot_str(data[0])
            if not data[3]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Добавлен VIP SLOT!\n"
                                            f"\n"
                                            f"{data[6]}\n"
                                            f"\n"
                                            f"{data[2]}\n"
                                            f"\n"
                                            f"{data[4]}\n"
                                            f"TIME: {time}\n"
                                            f"Количество: {amount_slots}\n"
                                            f"Цена: {data[5]}\n"
                                            f"\n"
                                            f"{data[7]}\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: @{callback.from_user.username}",
                                       reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[3],
                                     caption=f"Добавлен VIP SLOT!\n"
                                             f"\n"
                                             f"{data[6]}\n"
                                             f"\n"
                                             f"{data[2]}\n"
                                             f"\n"
                                             f"{data[4]}\n"
                                             f"TIME: {time}\n"
                                             f"Количество: {amount_slots}\n"
                                             f"Цена: {data[5]}\n"
                                             f"\n"
                                             f"{data[7]}\n"
                                             f"ID: {data[1]}\n"
                                             f"USERNAME: @{callback.from_user.username}",
                                     reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='admin_next_vip_slot'))
async def cb_admin_next_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    global index
    ban = await cb_check_ban_user(callback)
    if not ban:
        vip_slots = await get_vip_slots(callback_data['id'])
        all_vip_slots = list(vip_slots)[index: index + 2]
        index += 2
        for data in all_vip_slots:
            amount_slots = await get_amount_vip_slots_str(data[0])
            time = await get_time_vip_slot_str(data[0])
            if not data[3]:
                await callback.message.answer(f"{data[6]}\n"
                                              f"\n"
                                              f"{data[2]}\n"
                                              f"\n"
                                              f"{data[4]}\n"
                                              f"TIME: {time}\n"
                                              f"\n"
                                              f"Количество: {amount_slots}\n"
                                              f"Цена: {data[5]}\n"
                                              f"\n"
                                              f"{data[7]}",
                                              reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
            else:
                await callback.message.answer(f"{data[6]}\n"
                                              f"\n"
                                              f"{data[2]}\n"
                                              f"\n"
                                              f"{data[4]}\n"
                                              f"TIME: \n"
                                              f"\n"
                                              f"Количество: {amount_slots}\n"
                                              f"Цена: {data[5]}\n"
                                              f"\n"
                                              f"{data[7]}",
                                              reply_markup=admin_edit_post_vip_slot_ikb(data[0]))
        if len(all_vip_slots) < 2:
            await callback.message.answer("Это все слоты!")
        else:
            await callback.message.answer("Продолжить просмотр?",
                                          reply_markup=admin_next_vip_slot_ikb(callback_data['id']))
    await callback.message.delete()
    await callback.answer()


cb_words_list = ["delete_all_vip_slot", "no_delete_all_vip_slot"]

@dp.callback_query_handler(lambda callback : callback.data in cb_words_list)
async def all_callbacks(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    ban = await cb_check_ban_user(callback)
    moder = await get_moder_id(user_id)
    admin = await get_admin_id(user_id)
    if not ban:
        if user_id in moder or user_id in admin:
            if callback.data == 'delete_all_vip_slot':
                await delete_all_vip_slot()
                await callback.message.answer("Все VIP Slots успешно удалены!")
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Удалены все VIP SLOTS!\n"
                                            f"\n"
                                            f"ID: {callback.from_user.id}\n"
                                            f"username: {callback.from_user.username}")
            elif callback.data == 'no_delete_all_vip_slot':
                await callback.message.answer("Вы вернулись в меню модератора",
                                              reply_markup=admin_kb())
    await callback.message.delete()
    await callback.answer()




@dp.message_handler(lambda message : not message.text == 'Qualification'
                                     and not message.text == '1/4 STAGE'
                                     and not message.text == '1/2 STAGE'
                                     and not message.text == 'FINAL STAGE'
                                     and not message.text == 'GRAND-FINAL STAGE'
                                     and not message.text == '❌Отменить', state=VIPslotStateGroup.stage)
async def check_load_vip_slot(message : types.Message):
    await message.answer("Такого варианта ответа нету!")

@dp.message_handler(state=VIPslotStateGroup.stage)
async def load_stage_vip(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в меню админа:",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['stage'] = message.text
        await message.answer("Укажите время проведения:",
                             reply_markup=set_time_vip_slot_kb())
        await VIPslotStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 15, state=VIPslotStateGroup.time)
async def check_load_time_vs(message : types.Message):
    await message.answer("Вы превысили лимит по символов!")

@dp.message_handler(state=VIPslotStateGroup.time)
async def load_time_vip_slot(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await message.answer("Отправьте баннер турнира:",
                         reply_markup=info_from_bd("Пропустить"))
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : not message.photo and not message.text == 'Пропустить', state=VIPslotStateGroup.photo)
async def check_load_photo_vip(message : types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['photo', 'text'], state=VIPslotStateGroup.photo)
async def load_photo_vip(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['photo'] = ""
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправьте название турнира:",
                         reply_markup=ReplyKeyboardRemove())
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 100, state=VIPslotStateGroup.tour_name)
async def check_load_tour_name_vip(message : types.Message):
    await message.answer("Название турнира не должно превышать 100 символов!")

@dp.message_handler(state=VIPslotStateGroup.tour_name)
async def load_tour_name_vip(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['tour_name'] = message.text
    await message.answer("Отправьте стоимость слота:")
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : not message.text.isdigit(), state=VIPslotStateGroup.price)
async def check_load_price_vip(message : types.Message):
    await message.answer("Отправьте ценну цыфрами!")

@dp.message_handler(state=VIPslotStateGroup.price)
async def load_price_vip(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Отправьте информацию о турнире:")
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 300, state=VIPslotStateGroup.desc)
async def check_load_desc_vip(message : types.Message):
    await message.answer("Описание турнира не должно первышать 300 символов!")

@dp.message_handler(state=VIPslotStateGroup.desc)
async def load_desc_vip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer("Отправьте количество слотов:\n"
                         "Пример: /2/2/")
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 20, state=VIPslotStateGroup.amount)
async def check_load_amount_vip_slot(message : types.Message):
    await message.answer("Отправьте количество цыфрами!")

@dp.message_handler(state=VIPslotStateGroup.amount)
async def load_amount_vip_slot(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.answer("Отправьте ссылку на турнир:")
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : not is_valid_url(message.text), state=VIPslotStateGroup.link)
async def check_load_link_vip(message : types.Message):
    await message.answer("Отправьте ссылку!")

@dp.message_handler(state=VIPslotStateGroup.link)
async def load_link_vip_slot(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['link'] = message.text
    tour_id = str(uuid4())
    times = data['time'].split('/')
    amounts = data['amount'].split('/')
    await create_vip_slots(state, user_id, tour_id, times, amounts)
    if not data['photo']:
        await message.answer(f"{data['tour_name']}\n"
                             f"\n"
                             f"{data['stage']}\n"
                             f"\n"
                             f"{data['desc']}\n"
                             f"TIME: {data['time']}\n"
                             f"\n"
                             f"Количество: {data['amount']}\n"
                             f"Цена: {data['price']}\n"
                             f"\n"
                             f"{data['link']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['tour_name']}\n"
                                           f"\n"
                                           f"{data['stage']}\n"
                                           f"\n"
                                           f"{data['desc']}\n"
                                           f"TIME: {data['time']}\n"
                                           f"\n"
                                           f"Количество: {data['amount']}\n"
                                           f"Цена: {data['price']}\n"
                                           f"\n"
                                           f"{data['link']}")
    await message.answer("Все верно?",
                         reply_markup=admin_confirm_vip_slot_ikb(tour_id))
    await state.finish()




@dp.message_handler(lambda message : not message.text == 'Qualification'
                                     and not message.text == '1/4 STAGE'
                                     and not message.text == '1/2 STAGE'
                                     and not message.text == 'FINAL STAGE'
                                     and not message.text == 'GRAND-FINAL STAGE'
                                     and not message.text == '❌Отменить', state=VIPslotStateGroup.new_stage)
async def check_load_new_stage_vip_slot(message : types.Message):
    await message.answer("Такого варианта ответа нету!")

@dp.message_handler(state=VIPslotStateGroup.new_stage)
async def load_new_stage_vip(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['stage'] = message.text
        await message.answer("Укажите время проведения:",
                             reply_markup=set_time_vip_slot_kb())
        await VIPslotStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 15, state=VIPslotStateGroup.new_time)
async def check_load_new_time_vs(message: types.Message):
    await message.answer("Вы превысили лимит по символам!")

@dp.message_handler(state=VIPslotStateGroup.new_time)
async def load_new_time_vip_slot(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
    await message.answer("Отправьте баннер турнира:",
                         reply_markup=info_from_bd("Пропустить"))
    await VIPslotStateGroup.next()

@dp.message_handler(lambda message : not message.photo and not message.text == 'Пропустить', state=VIPslotStateGroup.new_photo)
async def check_load_new_photo_vip(message : types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['photo', 'text'], state=VIPslotStateGroup.new_photo)
async def load_new_photo_vip(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['photo'] = ""
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправьте название турнира:",
                         reply_markup=info_from_bd("Пропустить"))
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 100, state=VIPslotStateGroup.new_tour_name)
async def check_load_new_tour_name_vip(message : types.Message):
    await message.answer("Название турнира не должно превышать 100 символов!")

@dp.message_handler(state=VIPslotStateGroup.new_tour_name)
async def load_new_tour_name(message : types.Message, state : FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            tour_name = await get_name_tour_vip_slot(data['tour_id'])
            data['tour_name'] = tour_name
    else:
        async with state.proxy() as data:
            data['tour_name'] = message.text
    await message.answer("Отправьте стоимость слота:",
                         reply_markup=info_from_bd("Пропустить"))
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : not message.text.isdigit() and not message.text == 'Пропустить', state=VIPslotStateGroup.new_price)
async def check_load_new_price_vip(message : types.Message):
    await message.answer("Отправьте ценну цыфрами!")

@dp.message_handler(state=VIPslotStateGroup.new_price)
async def load_new_price_vip(message : types.Message, state : FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            price = await get_price_vip_slot(data['tour_id'])
            data['price'] = price
    else:
        async with state.proxy() as data:
            data['price'] = message.text
    await message.answer("Отправьте информацию о турнире:",
                         reply_markup=info_from_bd("Пропустить"))
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 300, state=VIPslotStateGroup.new_desc)
async def check_load_new_desc_vip(message : types.Message):
    await message.answer("Описание турнира не должно первышать 300 символов!")

@dp.message_handler(state=VIPslotStateGroup.new_desc)
async def load_new_desc_vip(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            desc = await get_desc_vip_slot(data['tour_id'])
            data['desc'] = desc
    else:
        async with state.proxy() as data:
            data['desc'] = message.text
    amount = await get_amount_vip_slots_str(data['tour_id'])
    await message.answer("Отправьте количество слотов:",
                         reply_markup=info_from_bd(amount))
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : len(message.text) > 20, state=VIPslotStateGroup.new_amount)
async def check_new_load_amount_vip_slot(message : types.Message):
    await message.answer("Отправьте количество цыфрами!")

@dp.message_handler(state=VIPslotStateGroup.new_amount)
async def load_new_amount_vip_slot(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.answer("Отправьте ссылку на турнир:",
                         reply_markup=info_from_bd("Пропустить"))
    await VIPslotStateGroup.next()


@dp.message_handler(lambda message : not is_valid_url(message.text) and not message.text == 'Пропустить', state=VIPslotStateGroup.new_link)
async def check_load_new_link_vip(message : types.Message):
    await message.answer("Отправьте ссылку!")

@dp.message_handler(state=VIPslotStateGroup.new_link)
async def load_new_link_vip_slot(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    if message.text == "Пропустить":
        async with state.proxy() as data:
            link = await get_link_vip_slot(data['tour_id'])
            data['link'] = link
    else:
        async with state.proxy() as data:
            data['link'] = message.text
    times = data['time'].split('/')
    amounts = data['amount'].split('/')
    await update_vip_slots(state, user_id, times, amounts)
    if not data['photo']:
        await message.answer(f"{data['tour_name']}\n"
                             f"\n"
                             f"{data['stage']}\n"
                             f"\n"
                             f"{data['desc']}\n"
                             f"TIME: {data['time']}\n"
                             f"\n"
                             f"Количество: {data['amount']}\n"  
                             f"Цена: {data['price']}\n"
                             f"\n"
                             f"{data['link']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['tour_name']}\n"
                                           f"\n"
                                           f"{data['stage']}\n"
                                           f"\n"
                                           f"{data['desc']}\n"
                                           f"TIME: {data['time']}\n"
                                           f"\n"
                                           f"Количество: {data['amount']}\n"
                                           f"Цена: {data['price']}\n"
                                           f"\n"
                                           f"{data['link']}")
    await message.answer("Все верно?",
                         reply_markup=admin_confirm_vip_slot_ikb(data['tour_id']))
    await state.finish()


async def send_info_vip_slot(stage, message):
    global index
    vip_slots = await get_vip_slots(stage)
    if not vip_slots:
        await message.answer("Слотов в эту стадию нету!")
    else:
        await message.answer(f"Актуальные VIP SLOTS на {stage}:")
        all_vip_slots = list(vip_slots)[index: index + 2]
        index += 2
        for data in all_vip_slots:
            amount_slots = await get_amount_vip_slots_str(data[0])
            time = await get_time_vip_slot_str(data[0])
            if not data[3]:
                await message.answer(f"{data[6]}\n"
                                     f"\n"
                                     f"{data[2]}\n"
                                     f"\n"
                                     f"{data[4]}\n"
                                     f"TIME: {time}\n"
                                     f"Количество: {amount_slots}\n"
                                     f"Цена: {data[5]}\n"
                                     f"\n"
                                     f"{data[7]}",
                                     reply_markup=admin_edit_vip_slot_ikb(data[0]))
            else:
                await message.answer_photo(photo=data[3],
                                           caption=f"{data[6]}\n"
                                                   f"\n"
                                                   f"{data[2]}\n"
                                                   f"\n"
                                                   f"{data[4]}\n"
                                                   f"TIME: {time}\n"
                                                   f"Количество: {amount_slots}\n"
                                                   f"Цена: {data[5]}\n"
                                                   f"\n"
                                                   f"{data[7]}",
                                           reply_markup=admin_edit_vip_slot_ikb(data[0]))
        if len(all_vip_slots) < 2:
            await message.answer("Это все слоты!")
        else:
            await message.answer("Продолжить просмотр?",
                                 reply_markup=admin_next_vip_slot_ikb(stage))