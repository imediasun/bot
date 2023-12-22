from random import randint
from uuid import uuid4
from aiogram import types
from aiogram.dispatcher import FSMContext

from config import active_uc_id, admin_pay_uc, admin_get_uc, ceo
from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp, bot

from keyboards import *
from translations import _
from states import BuyUCStatesGroup
from youngkb import info_from_bd, main_young_menu_ikb




@dp.message_handler(lambda message: message.text == '💸UC SHOP')
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        # await message.answer("Актуальные UC packs:",
        #                      reply_markup=ReplyKeyboardRemove())
        try:
            profile = await get_profile(message.from_user.id)
            active = await get_active_uc(active_uc_id)
            reason = await get_rsn_active_uc(active_uc_id)
            if active == 1:
                if profile == 'young':
                    await message.answer(reason,
                                         reply_markup=main_young_menu_ikb(lang))
                elif profile == 'pro':
                    await message.answer(reason,
                                         reply_markup=main_menu_kb(lang))
            else:
                uc_pack = await select_uc()
                currency = await get_region_currency(lang)
                amount_curr = await get_amount_curr(currency)
                info_uc = await get_all_info_uc_active(active_uc_id)
                ikb = InlineKeyboardMarkup()
                for data in uc_pack:
                    if currency == "USD":
                        amount = round(float(data[3]) * float(amount_curr), 2)
                    else:
                        amount = round(float(data[3]) * float(amount_curr))
                    btn1 = InlineKeyboardButton(text=f"💸{data[4]} UC - {amount} {currency}",
                                                callback_data=tour_cb.new(data[0], 'buy_uc'))
                    ikb.add(btn1)
                if profile == 'young':
                    back = InlineKeyboardButton(f"🔙{_('Назад', lang)}", callback_data="back_young_main")
                    ikb.add(back)
                elif profile == 'pro':
                    back = InlineKeyboardButton(f"🔙{_('Назад', lang)}", callback_data="back_main_menu")
                    ikb.add(back)
                for data in info_uc:
                    if not data[4]:
                        await message.answer(data[5],
                                             reply_markup=ikb)
                    else:
                        await message.answer_photo(photo=data[4],
                                                   caption=data[5],
                                                   reply_markup=ikb)
        except:
            await bot.send_message(chat_id=ceo[0],
                                   text="UC SHOP не активирован!")



@dp.callback_query_handler(tour_cb.filter(action='get_uc_pack'))
async def cb_get_uc_pack(callback : types.CallbackQuery, callback_data : dict):
    lang = await get_user_lang(callback.from_user.id)
    uc_pack = await get_uc_pack(callback_data['id'])
    currency = await get_region_currency(lang)
    amount_curr = await get_amount_curr(currency)
    ikb = InlineKeyboardMarkup()
    await set_new_click(callback.from_user.id)
    for data in uc_pack:
        amount = float(data[3]) * float(amount_curr)
        btn1 = InlineKeyboardButton(text=f"💸{round(amount, 0)} {currency}",
                                    callback_data=tour_cb.new(data[0], 'buy_uc'))
        ikb.add(btn1)
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=data[2],
                             reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()

@dp.callback_query_handler(tour_cb.filter(action='buy_uc'))
async def cb_buy_uc(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(callback.from_user.id)
    if not ban:
        payments = await get_payment()
        ikb = InlineKeyboardMarkup(row_width=1)
        for data in payments:
            btn1 = InlineKeyboardButton(f'{data[2]}', callback_data=f"uc_{data[0]}_{callback_data['id']}")
            ikb.add(btn1)
        back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_buy_uc")
        ikb.add(back)
        await callback.message.answer(_("Выберите способ оплаты:", lang),
                                      reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(text='back_buy_uc')
async def cb_back_buy_uc(callback : types.CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)
    profile = await get_profile(callback.from_user.id)
    uc_pack = await select_uc()
    currency = await get_region_currency(lang)
    amount_curr = await get_amount_curr(currency)
    info_uc = await get_all_info_uc_active(active_uc_id)
    ikb = InlineKeyboardMarkup()
    await set_new_click(callback.from_user.id)
    for data in uc_pack:
        if currency == "USD":
            amount = round(float(data[3]) * float(amount_curr), 2)
        else:
            amount = round(float(data[3]) * float(amount_curr))
        btn1 = InlineKeyboardButton(text=f"💸{data[4]} UC - {amount} {currency}",
                                    callback_data=tour_cb.new(data[0], 'buy_uc'))
        ikb.add(btn1)
    if profile == 'young':
        back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_young_main")
        ikb.add(back)
    elif profile == 'pro':
        back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_main_menu")
        ikb.add(back)
    for data in info_uc:
        if not data[4]:
            await callback.message.answer(data[5],
                                          reply_markup=ikb)
        else:
            await callback.message.answer_photo(photo=data[4],
                                                caption=data[5],
                                                reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='back_payment'))
async def cb_back_payment(callback: types.CallbackQuery, callback_data: dict):
    lang = await get_user_lang(callback.from_user.id)
    payments = await get_payment()
    ikb = InlineKeyboardMarkup(row_width=1)
    await set_new_click(callback.from_user.id)
    for data in payments:
        btn1 = InlineKeyboardButton(f'{data[2]}', callback_data=f"uc_{data[0]}_{callback_data['id']}")
        ikb.add(btn1)
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_buy_uc")
    ikb.add(back)
    await callback.message.answer(_("Выберите способ оплаты:", lang),
                                  reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('uc_'))
async def cb_card_for_pay(callback: types.CallbackQuery):
    await set_new_click(callback.from_user.id)
    ids = callback.data.split('_')
    card_id = ids[1]
    uc_id = ids[2]
    lang = await get_user_lang(callback.from_user.id)
    card = await get_card(card_id)
    price_uc = await get_price_uc(uc_id)
    amount_uc = await get_amount_uc(uc_id)
    currency = await get_bank_curr(card_id)
    amount_curr = await get_amount_curr(currency)
    if currency == "USD":
        amount = round(float(price_uc) * float(amount_curr), 2)
    elif currency == "USDT":
        amount = round(float(price_uc) * float(amount_curr), 2)
    else:
        amount = round(float(price_uc) * float(amount_curr))
    pay_id = str(uuid4())
    pay_number = randint(1000000, 9999999)
    username = f"@{callback.from_user.username}"
    await create_payment(pay_id, callback.from_user.id, username)
    for data in card:
        await callback.message.answer(f"{_('Актуальные реквизиты к оплате:', lang)}\n"
                                      f"\n"
                                      f"{data[3]}\n"
                                      f"\n"
                                      f"{_('Оплата', lang)} №{pay_number}\n"
                                      f"💸{_('Количество', lang)}: {amount_uc} UC\n"
                                      f"\n"
                                      f"💳{_('Сумма к оплате', lang)}: {amount} {currency}\n"
                                      f"\n"
                                      f"❗{_('После оплаты отправьте чек!', lang)}",
                                      reply_markup=pay_uc_ikb(pay_id, uc_id, lang))
        await update_payment_info(amount, currency, amount_uc, pay_id, data[2], pay_number)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='send_check_uc'))
async def cb_send_check_uc(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(user_id)
    if not ban:
        async with state.proxy() as data:
            data['uc_id'] = callback_data['id']
        await callback.message.answer(_("Отправьте чек:", lang),
                                      reply_markup=info_from_bd(f"❌{_('Отменить', lang)}"))
        await BuyUCStatesGroup.proof.set()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_payment_uc'))
async def cb_confirm_pay_uc(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(callback.from_user.id)
    await update_buy_time_uc(callback_data['id'])
    if not ban:
        await callback.message.answer(_("Ожидайте подтверждения платежа!", lang),
                                      reply_markup=ReplyKeyboardRemove())
        check = await get_check_uc(callback_data['id'])
        for data in check:
            if not data[2]:
                await bot.send_document(chat_id=admin_pay_uc,
                                        document=data[3],
                                        caption=f"Оплата №{data[8]}\n"
                                                f"\n"
                                                f"Количество: {data[6]} UC\n"
                                                f"Оплата на сумму: {data[4]} {data[5]}\n"
                                                f"Способ оплаты: {data[7]}\n"
                                                f"\n"
                                                f"ID: {data[1]}\n"
                                                f"USERNAME: {data[9]}",
                                        reply_markup=check_pay_uc(data[0]))
            else:
                await bot.send_photo(chat_id=admin_pay_uc,
                                     photo=data[2],
                                     caption=f"Оплата №{data[8]}\n"
                                             f"\n"
                                             f"Количество: {data[6]} UC\n"
                                             f"Оплата на сумму: {data[4]} {data[5]}\n"
                                             f"Способ оплаты: {data[7]}\n"
                                             f"\n"
                                             f"ID: {data[1]}\n"
                                             f"USERNAME: {data[9]}",
                                     reply_markup=check_pay_uc(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='change_check_uc'))
async def cb_change_check_uc(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(user_id)
    if not ban:
        async with state.proxy() as data:
            data['uc_id'] = callback_data['id']
        await callback.message.answer(_("Отправьте чек:", lang),
                                      reply_markup=info_from_bd(f"❌{_('Отменить', lang)}"))
        await BuyUCStatesGroup.proof.set()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_info_pay_uc'))
async def cb_confirm_info_uc(callback: types.CallbackQuery, callback_data: dict):
    lang = await get_user_lang(callback.from_user.id)
    check = await get_check_uc(callback_data['id'])
    profile = await get_profile(callback.from_user.id)
    await set_new_click(callback.from_user.id)
    if profile == 'young':
        await callback.message.answer(f"{_('Благодарим за покупку!', lang)}\n"
                                      f"{_('UC поступят Вам на счет в течении 20 минут', lang)}",
                                      reply_markup=main_young_menu_ikb(lang))
    elif profile == 'pro':
        await callback.message.answer(f"{_('Благодарим за покупку!', lang)}\n"
                                      f"{_('UC поступят Вам на счет в течении 20 минут', lang)}",
                                      reply_markup=main_menu_kb(lang))
    for data in check:
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


@dp.callback_query_handler(tour_cb.filter(action='change_pay_info_uc'))
async def cb_change_pay_info_uc(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    lang = await get_user_lang(callback.from_user.id)
    await set_new_click(callback.from_user.id)
    await callback.message.answer(_("Отправьте ваш игровой ID:", lang))
    await BuyUCStatesGroup.game_id.set()
    async with state.proxy() as data:
        data['uc_id'] = callback_data['id']
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='send_info_for_uc'))
async def cb_send_info_for_uc(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    lang = await get_user_lang(callback.from_user.id)
    await set_new_click(callback.from_user.id)
    await callback.message.answer(_("Отправьте ваш игровой ID:", lang))
    async with state.proxy() as data:
        data['uc_id'] = callback_data['id']
    await BuyUCStatesGroup.game_id.set()
    await callback.answer()



# PAYMENT STATE
@dp.message_handler(content_types=['photo', 'document', 'text'], state=BuyUCStatesGroup.proof)
async def load_proof_uc(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        if message.content_type == 'photo':
            data['proof'] = message.photo[0].file_id
        elif message.content_type == 'document':
            data['proof'] = message.document.file_id
    if message.text == f'❌{_("Отменить", lang)}':
        await message.answer(_("Вы вернулись в главное меню:", lang),
                             reply_markup=main_menu_kb(lang))
        await state.finish()
    elif message.content_type == 'photo':
        await update_payment(data['proof'], data['uc_id'])
        await message.answer_photo(photo=data['proof'],
                                   caption=_("Подтвердите платеж:", lang),
                                   reply_markup=confirm_payment_uc(data['uc_id'], lang))
        await state.finish()
    elif message.content_type == 'document':
        await update_payment_d(data['proof'], data['uc_id'])
        await message.answer_document(document=data['proof'],
                                      caption=_("Подтвердите платеж:", lang),
                                      reply_markup=confirm_payment_uc(data['uc_id'], lang))
        await state.finish()
    else:
        await message.answer(_("Отправьте чек документом/файлом!", lang))

@dp.message_handler(lambda message : not message.text.isdigit(), state=BuyUCStatesGroup.game_id)
async def check_game_id_uc(message : types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Игровой ID содержит только цифры!", lang))

@dp.message_handler(lambda message : len(message.text) > 10, state=BuyUCStatesGroup.game_id)
async def check_game_id_uc(message : types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Игровой ID не должен превышать 10 символов!", lang))

@dp.message_handler(state=BuyUCStatesGroup.game_id)
async def load_game_id_uc(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['game_id'] = message.text
    await message.answer(_("Отправьте ваш Nickname:", lang))
    await BuyUCStatesGroup.next()

@dp.message_handler(lambda message : len(message.text) > 15, state=BuyUCStatesGroup.nick)
async def check_load_nick(message : types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Игровой NICKNAME не должен превышать 15 символов!", lang))

@dp.message_handler(state=BuyUCStatesGroup.nick)
async def load_nick_uc(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['nick'] = message.text
    await update_pay_info(state)
    await message.answer(f"{_('Данные для пополнения', lang)} UC:\n"
                         f"\n"
                         f"ID: {data['game_id']}\n"
                         f"Nickname: {data['nick']}\n"
                         f"\n"
                         f"❗️{_('ID и Nickname обезательно должны совпадать, в противном случае UC не будут зачислены!', lang)}")
    await message.answer(_("Все верно?", lang),
                         reply_markup=confirm_info_pay_uc_ikb(data['uc_id'], lang))
    await state.finish()

@dp.message_handler(state=BuyUCStatesGroup.reason)
async def load_reason_uc(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    await update_reason_uc(data['reason'], data['uc_id'])
    check = await get_check_uc(data['uc_id'])
    for data in check:
        await message.answer(f"❌Заказ №{data[8]} не выполнен!\n"
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
                             f"USERNAME: {data[9]}",
                             reply_markup=admin_confirm_no_send_uc_ikb(data[0]))
    await state.finish()