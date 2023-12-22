from uuid import uuid4
from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp, bot
from config import *
from hendlers import check_ban_user, cb_check_ban_user
from database import *
from keyboards import *
from translations import _
from youngkb import *
from states import UCStatesGroup, BuyUCStatesGroup


@dp.message_handler(lambda message: message.text == "💸UC SHOPㅤ")
async def cd_admin(message: types.Message):
    user_id = message.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in admin_id:
            await message.answer("Выберите действие:",
                                 reply_markup=admin_add_uc())


words_list = ["add_uc", "check_uc", "active_uc", "conf_active_uc", "change_active_uc", "deactive_uc",
              "conf_deactive_uc", "no_deactive_uc"]


@dp.callback_query_handler(lambda callback: callback.data in words_list)
async def cb_conf_add_uc(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ban = await cb_check_ban_user(callback)
    admin_id = await get_admin_id(user_id)
    if not ban:
        if user_id in admin_id:
            if callback.data == 'add_uc':
                await callback.message.answer("Отправьте цену:")
                await UCStatesGroup.price.set()
                await callback.answer()
            elif callback.data == 'check_uc':
                await callback.message.answer("Все актуальные UC паки:")
                uc_pack = await admin_select_uc()
                for data in uc_pack:
                    await callback.message.answer(f"Количество: {data[4]}\n"
                                                  f"Цена: {data[3]}",
                                                  reply_markup=admin_edit_uc(data[0]))
                await callback.message.answer("Это все юс паки!")
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'active_uc':
                await callback.message.answer("Отправьте текст(можно прикрепить фото):",
                                              reply_markup=info_from_bd("❌Отменить"))
                await UCStatesGroup.text.set()
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'conf_active_uc':
                info = await get_all_info_uc_active(active_uc_id)
                await callback.message.answer("✅UC SHOP активирован!",
                                              reply_markup=general_admin_kb())
                for data in info:
                    if not data[4]:
                        await bot.send_message(chat_id=control_add_chat,
                                               text=f"✅Активирован UC SHOP!\n"
                                                    f"\n"
                                                    f"{data[5]}\n"
                                                    f"\n"
                                                    f"ID: {callback.from_user.id}\n"
                                                    f"USERNAME: @{callback.from_user.username}")
                    else:
                        await bot.send_photo(chat_id=control_add_chat,
                                             photo=data[4],
                                             caption=f"✅Активирован UC SHOP!\n"
                                                     f"\n"
                                                     f"{data[5]}\n"
                                                     f"\n"
                                                     f"ID: {callback.from_user.id}\n"
                                                     f"USERNAME: @{callback.from_user.username}")
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'change_active_uc':
                await callback.message.answer("Отправьте текст(можно прикрепить фото):",
                                              reply_markup=info_from_bd("❌Отменить"))
                await UCStatesGroup.text.set()
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'deactive_uc':
                await callback.message.answer("Отправьте причину деактивации:")
                await UCStatesGroup.reason.set()
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'conf_deactive_uc':
                reason = await get_rsn_active_uc(active_uc_id)
                await update_uc_active(active_uc_id, user_id, 1)
                await callback.message.answer("❌UC SHOP деактивирован!")
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"❌Деактивирован UC SHOP!\n"
                                            f"\n"
                                            f"{reason}\n"
                                            f"\n"
                                            f"ID: {callback.from_user.id}\n"
                                            f"USERNAME: @{callback.from_user.username}")
                await callback.answer()
            elif callback.data == 'no_deactive_uc':
                await callback.message.answer("✅Вы отменили деактивацию!",
                                              reply_markup=general_admin_kb())
                await callback.message.delete()
                await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='admin_conf_add_uc'))
async def cb_conf_add_uc(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer("UC пак успешно добавлен!")
        uc_pack = await get_uc_pack(callback_data['id'])
        for data in uc_pack:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Добавлен UC пак!\n"
                                        f"\n"
                                        f"Количество: {data[4]}\n"
                                        f"Стоимость: {data[3]}\n"
                                        f"\n"
                                        f"ID: {data[1]}",
                                   reply_markup=control_add_uc_ikb(callback_data['id']))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_uc'))
async def cb_edit_uc(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer("Отправьте цену:")
        await UCStatesGroup.new_price.set()
        async with state.proxy() as data:
            data['uc_id'] = callback_data['id']
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_uc'))
async def cb_delete_uc(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await delete_uc(callback_data['id'])
        await callback.message.answer("UC package успешно удален!")
        uc_pack = await get_uc_pack(callback_data['id'])
        for data in uc_pack:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удален UC пак!\n"
                                        f"\n"
                                        f"Количество: {data[4]}\n"
                                        f"Стоимость: {data[3]}\n"
                                        f"\n"
                                        f"ID: {data[1]}\n"
                                        f"USERNAME: {callback.from_user.username}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='yes_pay_uc'))
async def cb_admin_confirm_pay_uc(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.delete()
    check = await get_check_uc(callback_data['id'])
    for data in check:
        lang = await get_user_lang(data[1])
        await callback.message.answer(f"✅Успешная оплата №{data[8]}")
        await bot.send_message(chat_id=data[1],
                               text=f"✅{_('Оплата прошла успешно!', lang)}\n"
                                    f"\n"
                                    f"{_('Отправьте игровой ID и Nickname для пополнения UC', lang)}",
                               reply_markup=send_info_for_uc_ikb(data[0], lang))
        if not data[2]:
            await bot.send_document(chat_id=all_payment_chat,
                                    document=data[3],
                                    caption=f"✅Успешная оплата №{data[8]}\n"
                                            f"\n"
                                            f"Количество: {data[6]} UC\n"
                                            f"Оплата на сумму: {data[4]} {data[5]}\n"
                                            f"Способ оплаты: {data[7]}\n"
                                            f"\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: {data[9]}")
        else:
            await bot.send_photo(chat_id=all_payment_chat,
                                 photo=data[2],
                                 caption=f"✅Успешная оплата №{data[8]}\n"
                                         f"\n"
                                         f"Количество: {data[6]} UC\n"
                                         f"Оплата на сумму: {data[4]} {data[5]}\n"
                                         f"Способ оплаты: {data[7]}\n"
                                         f"\n"
                                         f"ID: {data[1]}\n"
                                         f"USERNAME: {data[9]}")
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='no_pay_uc'))
async def cb_admin_no_pay_uc(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.delete()
    lang = await get_user_lang(callback.from_user.id)
    check = await get_check_uc(callback_data['id'])
    profile = await get_profile(callback.from_user.id)
    for data in check:
        await callback.message.answer(f"❌Не успешная оплата №{data[8]}")
        if profile == 'young':
            await bot.send_message(chat_id=data[1],
                                   text=f"{_('Оплата не прошла!', lang)}\n"
                                        f"{_('Проверьте еще раз оплату или обратитесь в 💬Поддержку', lang)}",
                                   reply_markup=main_young_menu_ikb(lang))
        elif profile == 'pro':
            await bot.send_message(chat_id=data[1],
                                   text=f"{_('Оплата не прошла!', lang)}\n"
                                        f"{_('Проверьте еще раз оплату или обратитесь в 💬Поддержку', lang)}",
                                   reply_markup=main_menu_kb(lang))
        if not data[2]:
            await bot.send_document(chat_id=all_payment_chat,
                                    document=data[3],
                                    caption=f"❌Не успешная оплата №{data[8]}\n"
                                            f"\n"
                                            f"Количество: {data[6]} UC\n"
                                            f"Оплата на сумму: {data[4]} {data[5]}\n"
                                            f"Способ оплаты: {data[7]}\n"
                                            f"\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: {data[9]}")
        else:
            await bot.send_photo(chat_id=all_payment_chat,
                                 photo=data[2],
                                 caption=f"❌Не успешная оплата №{data[8]}\n"
                                         f"\n"
                                         f"Количество: {data[6]} UC\n"
                                         f"Оплата на сумму: {data[4]} {data[5]}\n"
                                         f"Способ оплаты: {data[7]}\n"
                                         f"\n"
                                         f"ID: {data[1]}\n"
                                         f"USERNAME: {data[9]}")
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='uc_sent'))
async def cb_sent_uc(callback: types.CallbackQuery, callback_data: dict):
    check = await get_check_uc(callback_data['id'])
    for data in check:
        await callback.message.answer(f"✅Заказ №{data[8]} успешно выполнен!")
        await bot.send_message(chat_id=all_payment_chat,
                               text=f"✅Заказ №{data[8]} успешно выполнен!\n"
                                    f"\n"
                                    f"Количество: {data[6]} UC\n"
                                    f"Сумма опалаты: {data[4]} {data[5]}\n"
                                    f"\n"
                                    f"GAME ID: {data[10]}\n"
                                    f"NICKNAME: {data[11]}\n"
                                    f"\n"
                                    f"ID: {data[1]}\n"
                                    f"USERNAME: {data[9]}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='no_uc_sent'))
async def cb_no_sent_uc(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    check = await get_check_uc(callback_data['id'])
    for data in check:
        await callback.message.answer(f"❌Заказ №{data[8]} отменен!")
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"❌Заказ №{data[8]} не выполнен!\n"
                                    f"\n"
                                    f"Количество: {data[6]} UC\n"
                                    f"Сумма опалаты: {data[4]} {data[5]}\n"
                                    f"\n"
                                    f"GAME ID: {data[10]}\n"
                                    f"NICKNAME: {data[11]}\n"
                                    f"\n"
                                    f"ID: {data[1]}\n"
                                    f"USERNAME: {data[9]}",
                               reply_markup=admin_rsn_no_send_uc_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='send_rsn_uc'))
async def cb_send_rsn_uc(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['uc_id'] = callback_data['id']
    await callback.message.answer("Отправьте причину:")
    await BuyUCStatesGroup.reason.set()
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='no_send_rsn_uc'))
async def cb_no_send_rsn_uc(callback: types.CallbackQuery, callback_data: dict):
    check = await get_check_uc(callback_data['id'])
    for data in check:
        await callback.message.answer(f"Заказ №{data[8]} не был отменен!")
        await bot.send_message(chat_id=admin_get_uc,
                               text=f"Заказ №{data[8]}\n"
                                    f"\n"
                                    f"GAME ID: {data[10]}\n"
                                    f"NICKNAME: {data[11]}\n"
                                    f"\n"
                                    f"Количество: {data[6]} UC\n"
                                    f"\n"
                                    f"USERNAME: {data[9]}",
                               reply_markup=admin_sent_uc_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_no_send_uc'))
async def cb_confirm_no_send_uc(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.delete()
    check = await get_check_uc(callback_data['id'])
    for data in check:
        await callback.message.answer(f"❌Заказ №{data[8]} отменен!")
        await bot.send_message(chat_id=all_payment_chat,
                               text=f"❌Заказ №{data[8]} не выполнен!\n"
                                    f"\n"
                                    f"Причина: {data[12]}\n"
                                    f"\n"
                                    f"Количество: {data[6]} UC\n"
                                    f"Сумма опалаты: {data[4]} {data[5]}\n"
                                    f"\n"
                                    f"GAME ID: {data[10]}\n"
                                    f"NICKNAME: {data[11]}\n"
                                    f"\n"
                                    f"ID: {data[1]}\n"
                                    f"USERNAME: {data[9]}")
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='reject_no_send_uc'))
async def cb_reject_no_send_uc(callback: types.CallbackQuery, callback_data: dict):
    check = await get_check_uc(callback_data['id'])
    for data in check:
        await callback.message.answer(f"Заказ №{data[8]} не был отменен!")
        await bot.send_message(chat_id=admin_get_uc,
                               text=f"Заказ №{data[8]}\n"
                                    f"\n"
                                    f"GAME ID: {data[10]}\n"
                                    f"NICKNAME: {data[11]}\n"
                                    f"\n"
                                    f"Количество: {data[6]} UC\n"
                                    f"\n"
                                    f"USERNAME: {data[9]}",
                               reply_markup=admin_sent_uc_ikb(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.message_handler(lambda message: not message.photo, state=UCStatesGroup.photo)
async def check_load_uc(message: types.Message):
    await message.answer("Отправьте фото!")


@dp.message_handler(content_types=['photo'], state=UCStatesGroup.photo)
async def load_uc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer("Отправьте цену:")
    await UCStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=UCStatesGroup.price)
async def check_load_uc_price(message: types.Message):
    await message.answer("Это не число!")


@dp.message_handler(state=UCStatesGroup.price)
async def load_uc_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Отправьте количество UC:")
    await UCStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=UCStatesGroup.amount_uc)
async def check_load_amount_uc(message: types.Message):
    await message.answer("Это не число!")


@dp.message_handler(state=UCStatesGroup.amount_uc)
async def load_amount_uc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount_uc'] = message.text
    uc_id = str(uuid4())
    await create_uc_pack(state, uc_id, user_id=message.from_user.id)
    await message.answer(f"Количество: {data['amount_uc']} UC\n"
                         f"Цена: {data['price']}")
    await message.reply("Все верно?",
                        reply_markup=admin_conf_add_uc_ikb(uc_id))
    await state.finish()


@dp.message_handler(lambda message: not message.photo, state=UCStatesGroup.new_photo)
async def check_new_load_uc(message: types.Message):
    await message.answer("Отправьте фото!")


@dp.message_handler(content_types=['photo'], state=UCStatesGroup.new_photo)
async def load_new_photo_uc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer("Отправьте цену:")
    await UCStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=UCStatesGroup.new_price)
async def check_load_new_uc_price(message: types.Message):
    await message.answer("Это не число!")


@dp.message_handler(state=UCStatesGroup.new_price)
async def load_uc_new_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Отправьте количество UC:")
    await UCStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit(), state=UCStatesGroup.new_amount_uc)
async def check_load_new_amount_uc(message: types.Message):
    await message.answer("Это не число!")


@dp.message_handler(state=UCStatesGroup.new_amount_uc)
async def load_new_amount_uc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount_uc'] = message.text
    await update_uc_pack(state, message.from_user.id)
    # await message.answer_photo(photo=data['photo'],
    #                            caption=f"Количество: {data['amount_uc']}\n"
    #                                    f"Цена: {data['price']}")
    await message.answer(f"Количество: {data['amount_uc']} UC\n"
                         f"Цена: {data['price']}")
    await message.reply("Все верно?",
                        reply_markup=admin_conf_add_uc_ikb(data['uc_id']))
    await state.finish()


@dp.message_handler(state=UCStatesGroup.reason)
async def active_uc_rsn(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=general_admin_kb())
    else:
        async with state.proxy() as data:
            data['reason'] = message.text
        await update_uc_rsn_active(active_uc_id, data['reason'])
        await message.answer(f"❌Подтвердите деактивацию UC SHOPa!\n"
                             f"\n"
                             f"{data['reason']}",
                             reply_markup=conf_rsn_active_uc_ikb())
    await state.finish()


@dp.message_handler(content_types=['text', 'photo'], state=UCStatesGroup.text)
async def load_banner_uc(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=general_admin_kb())
    else:
        await set_active(active_uc_id)
        async with state.proxy() as data:
            if message.content_type == 'photo':
                data['text'] = message.caption
            else:
                data['text'] = message.text
        if message.content_type == 'photo':
            photo = message.photo[0].file_id
            await update_info_uc_active(active_uc_id, message.from_user.id, 0, photo, data['text'])
            await message.answer_photo(photo=photo,
                                       caption=data['text'])
        else:
            await update_info_uc_active(active_uc_id, message.from_user.id, 0, "", data['text'])
            await bot.send_message(chat_id=control_add_chat,
                                   text=data['text'])
        await message.answer("Все верно?",
                             reply_markup=conf_active_uc())
    await state.finish()