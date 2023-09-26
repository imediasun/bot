from aiogram import types
from uuid import uuid4
from random import randint

from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp
from database import *
from keyboards import *
from translations import _


@dp.message_handler(lambda message : message.text == "👑VIP Slots")
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        if message.text == '👑VIP Slots':
            await message.answer(_("В какую стадию вам нужен VIP SLOT?", lang),
                                 reply_markup=vip_slot_main_ikb(lang))



@dp.callback_query_handler(lambda c : c.data.startswith('vip_slot_'))
async def cb_vip_slots(callback : types.CallbackQuery):
    global index
    stage = callback.data.split('_')[2]
    index = 0
    lang = await get_user_lang(callback.from_user.id)
    vip_slots = await get_vip_slots(stage)
    currency = await get_region_currency(lang)
    amount_curr = await get_amount_curr(currency)
    await set_new_click(callback.from_user.id)
    if not vip_slots:
        await callback.message.answer(_("Слотов в эту стадию нету!", lang),
                                      reply_markup=back_vip_slot_main_ikb(lang))
    else:
        await callback.message.answer(f"{_('Актуальные VIP SLOTS', lang)} {stage}:")
        all_vip_slots = list(vip_slots)[index: index + 2]
        index += 2
        for data in all_vip_slots:
            if currency == "USD":
                amount = round(float(data[5]) * float(amount_curr), 2)
            else:
                amount = round(float(data[5]) * float(amount_curr))
            if not data[3]:
                await callback.message.answer(text=f"{data[6]}\n"
                                                   f"\n"
                                                   f"{data[4]}\n"
                                                   f"\n"
                                                   f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                              reply_markup=buy_vip_slot_ikb(data[0], lang))
            else:
                await callback.message.answer_photo(photo=data[3],
                                                    caption=f"{data[6]}\n"
                                                            f"\n"
                                                            f"{data[4]}\n"
                                                            f"\n"
                                                            f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                                    reply_markup=buy_vip_slot_ikb(data[0], lang))
        if len(all_vip_slots) < 2:
            await callback.message.answer(_("Это все слоты!",lang),
                                          reply_markup=back_vip_slot_main_ikb(lang))
        else:
            await callback.message.answer(_("Продолжить просмотр?", lang),
                                          reply_markup=next_vip_slot_ikb(stage, lang))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='next_vip_slot'))
async def cb_next_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    global index
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(user_id)
    if not ban:
        currency = await get_region_currency(lang)
        amount_curr = await get_amount_curr(currency)
        vip_slots = await get_vip_slots(callback_data['id'])
        all_vip_slots = list(vip_slots)[index: index + 2]
        index += 2
        for data in all_vip_slots:
            if currency == "USD":
                amount = round(float(data[5]) * float(amount_curr), 2)
            else:
                amount = round(float(data[5]) * float(amount_curr))
            if not data[3]:
                await callback.message.answer(f"{data[6]}\n"
                                              f"\n"
                                              f"{data[4]}\n"
                                              f"\n"
                                              f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                              reply_markup=buy_vip_slot_ikb(data[0], lang))
            else:
                await callback.message.answer_photo(photo=data[3],
                                                    caption=f"{data[6]}\n"
                                                            f"\n"
                                                            f"{data[4]}\n"
                                                            f"\n"
                                                            f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                                    reply_markup=buy_vip_slot_ikb(data[0], lang))
        if len(all_vip_slots) < 2:
            await callback.message.answer(_("Это все слоты!", lang),
                                          reply_markup=back_vip_slot_main_ikb(lang))
        else:
            await callback.message.answer(_("Продолжить просмотр?", lang),
                                          reply_markup=next_vip_slot_ikb(callback_data['id'], lang))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(text="back_vip_slots")
async def all_callback(callback: types.CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(callback.from_user.id)
    if not ban:
        await callback.message.answer(_("Вы в VIP SLOTS меню:", lang),
                                      reply_markup=vip_slot_main_ikb(lang))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='buy_vip_slot'))
async def cb_buy_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    await buy_vip_slot(callback, callback_data, "")

@dp.callback_query_handler(tour_cb.filter(action='back_choose_time'))
async def cb_back_choose_time(callback : types.CallbackQuery, callback_data : dict):
    await buy_vip_slot(callback, callback_data, "back")


async def buy_vip_slot(callback, callback_data, type):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    amount_slots = await get_amount_vip_slot(callback_data['id'])
    total_amount_slots = sum(amount[0] for amount in amount_slots)
    if not ban:
        await set_new_click(callback.from_user.id)
        if total_amount_slots == 0:
            await callback.message.answer(_("К сожалению слотов больше не осталось!", lang),
                                          reply_markup=back_vip_slot_main_ikb(lang))
            await callback.message.delete()
            await callback.answer()
        else:
            times = await get_times_vip_slot(callback_data['id'])
            ikb = InlineKeyboardMarkup()
            for time in times:
                btn = InlineKeyboardButton(_(f"{time[0]}:00", lang),
                                           callback_data=f"choose_time_{time[0]}_{callback_data['id']}")
                ikb.add(btn)
            back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_vip_slots')
            ikb.add(back)
            await callback.message.reply(_("Выберите время(MSK):", lang),
                                         reply_markup=ikb)
            if type == "back":
                await callback.message.delete()
                await callback.answer()
            else:
                await callback.answer()


@dp.callback_query_handler(lambda c : c.data.startswith('choose_time_'))
async def cb_check_payment_vip_slot(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    elements = callback.data.split('_')
    time = elements[2]
    tour_id = elements[3]
    payments = await get_payment()
    amount_slots = await get_amount_vip_slot_time(tour_id, time)
    if not ban:
        await set_new_click(callback.from_user.id)
        if amount_slots == 0:
            await callback.message.answer(_("К сожалению слотов больше не осталось!", lang),
                                          reply_markup=back_vip_slot_main_ikb(lang))
        else:
            ikb = InlineKeyboardMarkup()
            for data in payments:
                btn1 = InlineKeyboardButton(data[2], callback_data=f"card_vip_slot_{data[0]}_{tour_id}_{time}")
                ikb.add(btn1)
            back = InlineKeyboardButton(f'🔙{_("Назад", lang)}',
                                        callback_data=tour_cb.new(tour_id, "back_choose_time"))
            ikb.add(back)
            await callback.message.answer(_("Выберите способ оплаты:", lang),
                                          reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('card_vip_slot_'))
async def cb_card_for_pay_vip_slot(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ids = callback.data.split('_')
    card_id = ids[3]
    tour_id = ids[4]
    time = ids[5]
    amount_slots = await get_amount_vip_slot_time(tour_id, time)
    ban = await cb_check_ban_user(callback)
    if not ban:
        await set_new_click(callback.from_user.id)
        if amount_slots == 0:
            await callback.message.answer(_("К сожалению слотов больше не осталось!", lang),
                                          reply_markup=back_vip_slot_main_ikb(lang))
        else:
            card = await get_card(card_id)
            stage = await get_stage_vip_slot(tour_id)
            tour_name = await get_name_tour_vip_slot(tour_id)
            price_slot = await get_price_vip_slot(tour_id)
            currency = await get_bank_curr(card_id)
            amount_curr = await get_amount_curr(currency)
            if currency == "USD":
                amount = round(float(price_slot) * float(amount_curr), 2)
            elif currency == "USDT":
                amount = round(float(price_slot) * float(amount_curr), 2)
            else:
                amount = round(float(price_slot) * float(amount_curr))
            pay_number = randint(1000000, 9999999)
            pay_id = str(uuid4())
            username = f"@{callback.from_user.username}"
            await create_pay_vip_slot(pay_id, callback.from_user.id, "vip_slot", username)
            for data in card:
                await callback.message.answer(f"{_('Актуальные реквизиты к оплате:', lang)}\n"
                                              f"\n"
                                              f"{data[3]}\n"
                                              f"\n"
                                              f"{_('Оплата', lang)} №{pay_number}\n"
                                              f"{_('Название', lang)}: {tour_name}\n"
                                              f"{_('Стадия', lang)}: {stage}\n"
                                              f"{_('Время', lang)}: {_(f'{time}:00 MSK', lang)}\n"
                                              f"\n"
                                              f"💳{_('Сумма к оплате', lang)}: {amount} {currency}\n"
                                              f"\n"
                                              f"❗{_('После оплаты отправьте чек!', lang)}",
                                              reply_markup=pay_vip_slot_ikb(pay_id, lang))
                await update_pay_vip_slot(pay_id, pay_number, tour_id, data[2], amount, currency, time)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='back_payment_vip_slot'))
async def cb_back_pay_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    lang = await get_user_lang(callback.from_user.id)
    check = await get_check_vip_slot(callback_data['id'])
    payments = await get_payment()
    ikb = InlineKeyboardMarkup()
    await set_new_click(callback.from_user.id)
    for data in check:
        for card in payments:
            btn1 = InlineKeyboardButton(card[2], callback_data=f"card_vip_slot_{card[0]}_{data[9]}_{data[17]}")
            ikb.add(btn1)
        back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data=tour_cb.new(data[9], "back_choose_time"))
        ikb.add(back)
    await callback.message.answer(_("Выберите способ оплаты:", lang),
                                  reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()