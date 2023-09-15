from random import randint
from uuid import uuid4
from aiogram import types

from hendlers import check_ban_user, cb_check_ban_user
from main import dp
from database import *
from keyboards import *
from translations import _
from youngkb import vip_prac_time_ikb, back_vip_prac_ikb, buy_vip_prac_ikb, next_vip_prac_ikb, pay_vip_prac_ikb


@dp.message_handler(lambda message: message.text == "👑VIP Slotsㅤ")
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    if not ban:
        await message.answer(_("Выберите время сесси(MSK):", lang),
                             reply_markup=vip_prac_time_ikb(lang))



@dp.callback_query_handler(text="back_vip_prac")
async def back_tour_main(callback: types.CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer(_("Вы вернулись в VIP Slots меню:", lang),
                                      reply_markup=vip_prac_time_ikb(lang))
        await callback.message.delete()
        await callback.answer()


# VIP PRAC
@dp.callback_query_handler(lambda c : c.data.startswith('prac_vip_'))
async def cb_prac_vip(callback : types.CallbackQuery):
    global index
    index = 0
    time = callback.data.split('_')[2]
    lang = await get_user_lang(callback.from_user.id)
    prac = await get_vip_pracs(time)
    if not prac:
        await callback.message.answer(_("На данное время слотов нету!", lang),
                                      reply_markup=back_vip_prac_ikb(lang))
    else:
        all_prac = list(prac)[index: index + 2]
        index += 2
        await callback.message.answer(_("Все актуальные слоты:", lang))
        for data in all_prac:
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
                                              reply_markup=buy_vip_prac_ikb(data[0], lang))
            else:
                await callback.message.answer_photo(photo=data[3],
                                                    caption=f"{data[6]}\n"
                                                            f"\n"
                                                            f"{data[5]}\n"
                                                            f"TIME: {_(f'{data[2]}:00 MSK', lang)}\n"
                                                            f"\n"
                                                            f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                                    reply_markup=buy_vip_prac_ikb(data[0], lang))
        if len(all_prac) < 2:
            await callback.message.answer(_("Это все слоты!", lang),
                                          reply_markup=back_vip_prac_ikb(lang))
        else:
            await callback.message.answer(_("Продолжить просмотр?", lang),
                                          reply_markup=next_vip_prac_ikb(time, lang))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='next_vip_prac'))
async def next_vip_prac(callback : types.CallbackQuery, callback_data : dict):
    global index
    lang = await get_user_lang(callback.from_user.id)
    prac = await get_vip_pracs(callback_data['id'])
    all_prac = list(prac)[index: index + 2]
    index += 2
    for data in all_prac:
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
                                          reply_markup=buy_vip_prac_ikb(data[0], lang))
        else:
            await callback.message.answer_photo(photo=data[3],
                                                caption=f"{data[6]}\n"
                                                        f"\n"
                                                        f"{data[5]}\n"
                                                        f"TIME: {_(f'{data[2]}:00 MSK', lang)}\n"
                                                        f"\n"
                                                        f"{_('Стоимость слота', lang)}: {amount} {currency}",
                                                reply_markup=buy_vip_prac_ikb(data[0], lang))
    if len(all_prac) < 2:
        await callback.message.answer(_("Это все слоты!", lang),
                                      reply_markup=back_vip_prac_ikb(lang))
    else:
        await callback.message.answer(_("Продолжить просмотр?", lang),
                                      reply_markup=next_vip_prac_ikb(callback_data['id'], lang))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='buy_vip_prac'))
async def cb_buy_vip_prac(callback : types.CallbackQuery, callback_data : dict):
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        payments = await get_payment()
        ikb = InlineKeyboardMarkup()
        for data in payments:
            btn1 = InlineKeyboardButton(data[2], callback_data=f"vip_prac_{data[0]}_{callback_data['id']}")
            ikb.add(btn1)
        back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_vip_prac")
        ikb.add(back)
        await callback.message.reply(_("Выберите способ оплаты:", lang),
                                     reply_markup=ikb)
    await callback.answer()


@dp.callback_query_handler(lambda c : c.data.startswith('vip_prac_'))
async def cb_card_vip_prac(callback : types.CallbackQuery):
    ids = callback.data.split('_')
    card_id = ids[2]
    tour_id = ids[3]
    lang = await get_user_lang(callback.from_user.id)
    price = await get_price_vip_prac(tour_id)
    tour_name = await get_vip_prac_name(tour_id)
    time = await get_time_prac_vip(tour_id)
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
    await create_pay_event(pay_id, callback.from_user.id, "prac", username)
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
                                      reply_markup=pay_vip_prac_ikb(pay_id, tour_id, lang))
        await update_pay_vip_slot(pay_id, pay_number, tour_id, data[2], amount, currency, time)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='back_payment_prac_vip'))
async def cb_back_prac_vip(callback : types.CallbackQuery, callback_data : dict):
    lang = await get_user_lang(callback.from_user.id)
    payments = await get_payment()
    ban = await cb_check_ban_user(callback)
    if not ban:
        ikb = InlineKeyboardMarkup()
        for data in payments:
            btn1 = InlineKeyboardButton(data[2], callback_data=f"vip_prac_{data[0]}_{callback_data['id']}")
            ikb.add(btn1)
        back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_vip_prac")
        ikb.add(back)
        await callback.message.answer(f"{_('Выберите способ оплаты:', lang)}",
                                      reply_markup=ikb)
    await callback.message.delete()
    await callback.answer()