from aiogram import types
from aiogram.dispatcher import FSMContext
from uuid import uuid4

from config import control_add_chat
from hendlers import check_ban_user, cb_check_ban_user, is_valid_url
from main import dp, bot
from database import *
from keyboards import *
from youngkb import *
from states import AddPracVIPStatesGroup



@dp.message_handler(lambda message: message.text == "VIP SLOT PRAC")
async def all_text(message: types.Message):
    user_id = message.from_user.id
    moder_id = await get_moder_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in moder_id:
            await message.answer("Выберите действие:",
                                 reply_markup=admin_check_vip_prac_kb())



words_list = ["add_vip_prac", "check_all_vip_pracs", "delete"]

@dp.callback_query_handler(lambda callback : callback.data in words_list)
async def all_callbacks(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    ban = await cb_check_ban_user(callback)
    moder_id = await get_moder_id(user_id)
    if not ban:
        if user_id in moder_id:
            if callback.data == 'add_vip_prac':
                await callback.message.answer("Укажите время игр:",
                                              reply_markup=admin_put_time())
                await AddPracVIPStatesGroup.time.set()
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'check_all_vip_pracs':
                await callback.message.answer("Выберите время:",
                                              reply_markup=admin_time_vip_prac_ikb())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'delete':
                await callback.message.delete()
                await callback.answer()




# ADMIN YOUNG VIP PRAC
@dp.callback_query_handler(lambda c : c.data.startswith('admin_prac_vip_'))
async def cb_admin_next_vip_prac(callback : types.CallbackQuery):
    ban = await cb_check_ban_user(callback)
    if not ban:
        time = callback.data.split('_')[3]
        await callback.message.answer("Все актуальные VIP SLOTS:")
        pracs = await get_vip_pracs(time)
        for data in pracs:
            if not data[3]:
                await callback.message.answer(text=f"{data[6]}\n"
                                                   f"\n"
                                                   f"{data[2]}:00\n"
                                                   f"\n"
                                                   f"{data[5]}\n"
                                                   f"\n"
                                                   f"Количество: {data[8]}\n"
                                                   f"Цена: {data[4]}",
                                              reply_markup=admin_edit_vip_prac_kb(data[0]))
            else:
                await callback.message.answer_photo(photo=data[3],
                                                    caption=f"{data[6]}\n"
                                                            f"\n"
                                                            f"{data[2]}:00\n"
                                                            f"\n"
                                                            f"{data[5]}\n"
                                                            f"\n"
                                                            f"Количество: {data[8]}\n"
                                                            f"Цена: {data[4]}",
                                                    reply_markup=admin_edit_vip_prac_kb(data[0]))
        await callback.message.answer("Это все актуальные слоты!",
                                      reply_markup=admin_time_vip_prac_ikb())
    await callback.message.delete()
    await callback.answer()

@dp.callback_query_handler(tour_cb.filter(action='conf_add_vip_prac'))
async def admin_conf_add_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer("✅Прак успешно добавлен!",
                                      reply_markup=admin_kb())
        prac = await get_vip_prac(callback_data['id'])
        for data in prac:
            if not data[3]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Добавлен прак!\n"
                                            f"\n"
                                            f"{data[6]}\n"
                                            f"\n"
                                            f"{data[2]}\n"
                                            f"\n"
                                            f"{data[5]}\n"
                                            f"\n"
                                            f"Стоимость слота: {data[4]}\n"
                                            f"\n"
                                            f"{data[7]}\n"
                                            f"\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: @{callback.from_user.username}",
                                       reply_markup=admin_edit_post_vip_prac_ikb(data[0]))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[3],
                                     caption=f"Добавлен прак!\n"
                                             f"\n"
                                             f"{data[6]}\n"
                                             f"\n"
                                             f"{data[2]}\n"
                                             f"\n"
                                             f"{data[5]}\n"
                                             f"\n"
                                             f"Стоимость слота: {data[4]}\n"
                                             f"\n"
                                             f"{data[7]}\n"
                                             f"\n"
                                             f"ID: {data[1]}\n"
                                             f"USERNAME: @{callback.from_user.username}",
                                     reply_markup=admin_edit_post_vip_prac_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_vip_prac'))
async def admin_edit_vip_prac(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer("Укажите время игр:",
                                      reply_markup=admin_put_time())
        await AddPracVIPStatesGroup.new_time.set()
        async with state.proxy() as data:
            data['tour_id'] = callback_data['id']
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_vip_prac'))
async def cb_delete_vip_prac(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await admin_delete_vip_prac(callback_data['id'])
        await callback.message.reply("Вы успешно удалили VIP PRAC!",
                                     reply_markup=admin_kb())
        prac = await get_vip_prac(callback_data['id'])
        for data in prac:
            if not data[3]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Удален прак!\n"
                                            f"\n"
                                            f"{data[6]}\n"
                                            f"\n"
                                            f"{data[2]}\n"
                                            f"\n"
                                            f"{data[5]}\n"
                                            f"\n"
                                            f"Стоимость слота: {data[4]}\n"
                                            f"\n"
                                            f"{data[7]}\n"
                                            f"\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: @{callback.from_user.username}",
                                       reply_markup=admin_edit_post_vip_prac_ikb(data[0]))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[3],
                                     caption=f"Удален прак!\n"
                                             f"\n"
                                             f"{data[6]}\n"
                                             f"\n"
                                             f"{data[2]}\n"
                                             f"\n"
                                             f"{data[5]}\n"
                                             f"\n"
                                             f"Стоимость слота: {data[4]}\n"
                                             f"\n"
                                             f"{data[7]}\n"
                                             f"\n"
                                             f"ID: {data[1]}\n"
                                             f"USERNAME: @{callback.from_user.username}",
                                     reply_markup=admin_edit_post_vip_prac_ikb(data[0]))
    await callback.answer()



@dp.message_handler(lambda message: not message.text == '15:00'
                                    and not message.text == '18:00'
                                    and not message.text == '21:00'
                                    and not message.text == '00:00'
                                    and not message.text == '❌Отменить', state=AddPracVIPStatesGroup.time)
async def check_load_time_vip_prac(message: types.Message):
    await message.answer("Такого варианта ответа нету!")

@dp.message_handler(state=AddPracVIPStatesGroup.time)
async def load_time_prac_vip(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['time'] = message.text.split(':')[0]
        await message.answer("Отправьте баннер прака:",
                             reply_markup=info_from_bd("Пропустить"))
        await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not message.photo
                                    and not message.text == 'Пропустить', state=AddPracVIPStatesGroup.photo)
async def check_load_photo_prac_vip(message: types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['photo', 'text'], state=AddPracVIPStatesGroup.photo)
async def load_photo_prac_vip(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['photo'] = ""
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправь информацию о праке:",
                         reply_markup=ReplyKeyboardRemove())
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: len(message.text) > 100, state=AddPracVIPStatesGroup.desc)
async def check_load_desc_prac_vip(message: types.Message):
    await message.answer("Описание ивента не должно превышать 100 символов!")

@dp.message_handler(state=AddPracVIPStatesGroup.desc)
async def load_desc_prac_vip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer("Отправьте стоимость слота:")
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=AddPracVIPStatesGroup.price)
async def check_load_price_prac_vip(message: types.Message):
    await message.answer("Отправьте стоимость числом!")

@dp.message_handler(state=AddPracVIPStatesGroup.price)
async def load_price_prac_vip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Отправьте название прака:")
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: len(message.text) > 50, state=AddPracVIPStatesGroup.tour_name)
async def check_load_tour_prac_vip(message: types.Message):
    await message.answer("Название турнира не должно превышать 50 символов!")

@dp.message_handler(state=AddPracVIPStatesGroup.tour_name)
async def load_name_prac_vip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tour_name'] = message.text
    await message.answer("Укажите количество слотов:")
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=AddPracVIPStatesGroup.amount)
async def check_amount_prac_vip(message: types.Message):
    await message.answer("Отправьте количество цыфрами!")

@dp.message_handler(state=AddPracVIPStatesGroup.amount)
async def load_amount_prac_vip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.answer("Отправьте ссылку на прак:")
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not is_valid_url(message.text), state=AddPracVIPStatesGroup.link)
async def check_load_link_prac_vip(message: types.Message):
    await message.answer("Это не ссылка!")

@dp.message_handler(state=AddPracVIPStatesGroup.link)
async def load_link_prac_vip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    tour_id = str(uuid4())
    await create_vip_prac(state, tour_id, message.from_user.id)
    if not data['photo']:
        await message.answer(f"{data['tour_name']}\n"
                             f"\n"
                             f"{data['time']}:00\n"
                             f"\n"
                             f"{data['desc']}\n"
                             f"\n"
                             f"Количество: {data['amount']}\n"
                             f"Стоимость слота: {data['price']}\n"
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
                                           f"Стоимость слота: {data['price']}\n"
                                           f"\n"
                                           f"{data['link']}")
    await message.answer("Все верно?",
                         reply_markup=conf_add_vip_prac_ikb(tour_id))
    await state.finish()

@dp.message_handler(lambda message: not message.text == '15:00'
                                    and not message.text == '18:00'
                                    and not message.text == '21:00'
                                    and not message.text == '00:00'
                                    and not message.text == '❌Отменить', state=AddPracVIPStatesGroup.new_time)
async def check_load_new_time_vip_prac(message: types.Message):
    await message.answer("Такого варианта ответа нету!")

@dp.message_handler(state=AddPracVIPStatesGroup.new_time)
async def load_new_time_vip_prac(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['time'] = message.text.split(':')[0]
    await message.answer("Отправьте баннер прака:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not message.photo
                                    and not message.text == "Пропустить", state=AddPracVIPStatesGroup.new_photo)
async def check_load_new_photo_vip_prac(message: types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['photo', 'text'], state=AddPracVIPStatesGroup.new_photo)
async def load_new_photo_vip_prac(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            photo = await get_photo_prac_vip(data['tour_id'])
            data['photo'] = photo
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправь информацию о праке:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: len(message.text) > 100, state=AddPracVIPStatesGroup.new_desc)
async def check_load_new_desc_vip_prac(message: types.Message):
    await message.answer("Описание прака не должно превышать 100 символов!")

@dp.message_handler(state=AddPracVIPStatesGroup.new_desc)
async def load_new_desc_vip_prac(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            desc = await get_desc_prac_vip(data['tour_id'])
            data['desc'] = desc
    else:
        async with state.proxy() as data:
            data['desc'] = message.text
    await message.answer("Отправьте стоимость слота:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not message.text.isdigit()
                                    and not message.text == 'Пропустить', state=AddPracVIPStatesGroup.new_price)
async def check_load_new_price_vip_prac(message: types.Message):
    await message.answer("Отправьте ценну числом!")

@dp.message_handler(state=AddPracVIPStatesGroup.new_price)
async def load_new_price_vip_prac(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            price = await get_price_vip_prac(data['tour_id'])
            data['price'] = price
    else:
        async with state.proxy() as data:
            data['price'] = message.text
    await message.answer("Отправьте название прака:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: len(message.text) > 50, state=AddPracVIPStatesGroup.new_tour_name)
async def check_load_new_name_vip_prac(message: types.Message):
    await message.answer("Название турнира не должно превышать 50 символов!")

@dp.message_handler(state=AddPracVIPStatesGroup.new_tour_name)
async def load_new_vip_prac_name(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            prac_name = await get_vip_prac_name(data['tour_id'])
            data['tour_name'] = prac_name
    else:
        async with state.proxy() as data:
            data['tour_name'] = message.text
    await message.answer("Отправьте количество слотов:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=AddPracVIPStatesGroup.new_amount)
async def check_new_amount_prac_vip(message: types.Message):
    await message.answer("Только число!")

@dp.message_handler(state=AddPracVIPStatesGroup.new_amount)
async def load_new_amount_prac_vip(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            amount = await get_amount_vip_prac(data['tour_id'])
            data['amount'] = amount
    else:
        async with state.proxy() as data:
            data['amount'] = message.text
    await message.answer("Отправьте ссылку на прак:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracVIPStatesGroup.next()

@dp.message_handler(lambda message: not is_valid_url(message.text)
                                    and not message.text == 'Пропустить', state=AddPracVIPStatesGroup.new_link)
async def check_load_new_link_vip_prac(message: types.Message):
    await message.answer("Это не ссылка!")

@dp.message_handler(state=AddPracVIPStatesGroup.new_link)
async def load_event_new_link(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            link = await get_link_prac_vip(data['tour_id'])
            data['link'] = link
    else:
        async with state.proxy() as data:
            data['link'] = message.text
    await update_vip_prac(state, message.from_user.id)
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
                         reply_markup=conf_add_vip_prac_ikb(data['tour_id']))
    await state.finish()