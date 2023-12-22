from random import randint
from aiogram import types
from uuid import uuid4

from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp
from keyboards import *
from translations import _
from database.db import *


@dp.message_handler(lambda message : message.text == "💥Events")
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        index = 0
        events = await get_all_events()
        if not events:
            await message.answer(_("Актуальных EVENTS нету!", lang),
                                 reply_markup=back_pro_main(lang))
        else:
            await message.answer(_("Все актуальные EVENTS:", lang),
                                 reply_markup=ReplyKeyboardRemove())
            all_events = list(events)[index: index + 2]
            index += 2
            currency = await get_region_currency(lang)
            amount_curr = await get_amount_curr(currency)
            for data in all_events:
                if currency == "USD":
                    amount = round(float(data[4]) * float(amount_curr), 2)
                else:
                    amount = round(float(data[4]) * float(amount_curr))
                if not data[3]:
                    await message.answer(f"{data[6]}\n"
                                         f"\n"
                                         f"{data[5]}\n"
                                         f"TIME: {_(f'{data[2]}:00 MSK', lang)}\n"
                                         f"\n"
                                         f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                         reply_markup=buy_event_ikb(data[0], lang))
                else:
                    await message.answer_photo(photo=data[3],
                                               caption=f"{data[6]}\n"
                                                       f"\n"
                                                       f"{data[5]}\n"
                                                       f"TIME: {_(f'{data[2]}:00 MSK', lang)}\n"
                                                       f"\n"
                                                       f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                               reply_markup=buy_event_ikb(data[0], lang))
            if len(all_events) < 2:
                await message.answer(_("Это все слоты!", lang),
                                     reply_markup=back_pro_main(lang))
            else:
                await message.answer(_("Продолжить просмотр?", lang),
                                     reply_markup=next_events_ikb(lang))



@dp.callback_query_handler(text='next_event')
async def cb_next_event(callback: types.CallbackQuery):
    global index
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(callback.from_user.id)
    if not ban:
        events = await get_all_events()
        all_events = list(events)[index: index + 2]
        index += 2
        for data in all_events:
            currency = await get_region_currency(lang)
            amount_curr = await get_amount_curr(currency)
            if currency == "USD":
                amount = round(float(data[4]) * float(amount_curr), 2)
            else:
                amount = round(float(data[4]) * float(amount_curr))
            if not data[3]:
                await callback.message.answer(f"{data[6]}\n"
                                              f"\n"
                                              f"{data[5]}\n"
                                              f"TIME: {_(f'{data[2]}:00 MSK', lang)}\n"
                                              f"\n"
                                              f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                              reply_markup=buy_event_ikb(data[0], lang))
            else:
                await callback.message.answer_photo(photo=data[3],
                                                    caption=f"{data[6]}\n"
                                                            f"\n"
                                                            f"{data[5]}\n"
                                                            f"TIME: {_(f'{data[2]}:00 MSK', lang)}\n"
                                                            f"\n"
                                                            f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                                    reply_markup=buy_event_ikb(data[0], lang))
        if len(all_events) < 2:
            await callback.message.answer(_("Это все слоты!", lang),
                                          reply_markup=back_pro_main(lang))
        else:
            await callback.message.answer(_("Продолжить просмотр?", lang),
                                          reply_markup=next_events_ikb(lang))
        await callback.message.delete()
        await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='buy_slot_event'))
async def cb_buy_event_slot(callback : types.CallbackQuery, callback_data : dict):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    amount_slots = await get_amount_events(callback_data['id'])
    await set_new_click(callback.from_user.id)
    if not ban:
        if amount_slots == 0:
            await callback.message.answer(_("К сожалению, слотов больше не осталось!", lang),
                                          reply_markup=back_pro_main(lang))
        else:
            payments = await get_payment()
            ikb = InlineKeyboardMarkup()
            for data in payments:
                btn1 = InlineKeyboardButton(data[2], callback_data=f"event_{data[0]}_{callback_data['id']}")
                ikb.add(btn1)
            back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_main_menu")
            ikb.add(back)
            await callback.message.answer(_("Выберите способ оплаты:", lang),
                                          reply_markup=ikb)
    await callback.answer()

@dp.callback_query_handler(lambda c : c.data.startswith('event_'))
async def cb_pay_event(callback : types.CallbackQuery):
    await set_new_click(callback.from_user.id)
    ids = callback.data.split('_')
    card_id = ids[1]
    tour_id = ids[2]
    lang = await get_user_lang(callback.from_user.id)
    amount_slots = await get_amount_events(tour_id)
    if amount_slots == 0:
        await callback.message.answer(_("К сожалению, слотов больше не осталось!", lang),
                                      reply_markup=back_pro_main(lang))
    else:
        price = await get_price_event(tour_id)
        tour_name = await get_event_name(tour_id)
        time = await get_time_event(tour_id)
        card = await get_card(card_id)
        currency = await get_bank_curr(card_id)
        amount_curr = await get_amount_curr(currency)
        if currency == "USD":
            amount = round(float(price) * float(amount_curr), 2)
        elif currency == "USDT":
            amount = round(float(price) * float(amount_curr), 2)
        else:
            amount = round(float(price) * float(amount_curr))
        pay_id = str(uuid4())
        pay_number = randint(1000000, 9999999)
        username = f"@{callback.from_user.username}"
        await create_pay_event(pay_id, callback.from_user.id, "event", username)
        for data in card:
            await callback.message.answer(f"{_('Актуальные реквизиты к оплате:', lang)}\n"
                                          f"\n"
                                          f"{data[3]}\n"
                                          f"\n"
                                          f"{_('Оплата', lang)} №{pay_number}\n"
                                          f"{_('Название', lang)}: {tour_name}\n"
                                          f"{_('Время', lang)}: {_(f'{time}:00 MSK', lang)}\n"
                                          f"\n"
                                          f"💳{_('Сумма к оплате', lang)}: {amount} {currency}\n"
                                          f"\n"
                                          f"❗{_('После оплаты отправьте чек!', lang)}",
                                          reply_markup=pay_event_ikb(pay_id, tour_id, lang))
            await update_pay_vip_slot(pay_id, pay_number, tour_id, data[2], amount, currency, time)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='back_payment_event'))
async def cb_back_pay_event(callback : types.CallbackQuery, callback_data : dict):
    lang = await get_user_lang(callback.from_user.id)
    payments = await get_payment()
    await set_new_click(callback.from_user.id)
    ikb = InlineKeyboardMarkup()
    for data in payments:
        btn1 = InlineKeyboardButton(data[2], callback_data=f"event_{data[0]}_{callback_data['id']}")
        ikb.add(btn1)
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_main_menu")
    ikb.add(back)
    await callback.message.answer(_("Выберите способ оплаты:", lang),
                                  reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()