from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp, bot
from config import admin_get_cap_chat, all_payment_chat
from database import *
from keyboards import *
from states import BuyVipSlotStatesGroup
from translations import _
from youngkb import main_young_menu_ikb


@dp.callback_query_handler(tour_cb.filter(action='yes_pay_vip_slot'))
async def cb_admin_yes_pay_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    check = await get_check_vip_slot(callback_data['id'])
    for data in check:
        lang = await get_user_lang(data[1])
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
            price = await get_price_event(data[9])
            link = await get_link_event(data[9])
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc_tour = await get_desc_prac_vip(data[9])
            price = await get_price_vip_prac(data[9])
            link = await get_link_prac_vip(data[9])
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
            price = await get_price_vip_slot(data[9])
            link = await get_link_vip_slot(data[9])
        await callback.message.answer(f"✅Успешная оплата №{data[8]}")
        await bot.send_message(chat_id=data[1],
                               text=f"✅{_('Оплата прошла успешно!', lang)}\n"
                                    f"\n"
                                    f"⚡{_('Пожалуйста, перейдите по ссылке для доступа к кеп чату, а затем вернитесь в бота и нажмите ✅Перешел.', lang)}",
                               reply_markup=go_server_for_slot(link, data[0], lang))
        if not data[3]:
            await bot.send_document(chat_id=all_payment_chat,
                                    document=data[4],
                                    caption=f"✅Успешная оплата №{data[8]}\n"
                                            f"\n"
                                            f"{tour_name}\n"
                                            f"\n"
                                            f"{desc_tour}\n"
                                            f"TIME: {data[17]}:00\n"
                                            f"\n"
                                            f"Стоимость слота: {price}\n"
                                            f"\n"
                                            f"Оплата на сумму: {data[5]} {data[6]}\n"
                                            f"Способ оплаты: {data[7]}\n"
                                            f"\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: {data[2]}")
        else:
            await bot.send_photo(chat_id=all_payment_chat,
                                 photo=data[3],
                                 caption=f"✅Успешная оплата №{data[8]}\n"
                                         f"\n"
                                         f"{tour_name}\n"
                                         f"\n"
                                         f"{desc_tour}\n"
                                         f"TIME: {data[17]}:00\n"
                                         f"\n"
                                         f"Стоимость слота: {price}\n"
                                         f"\n"
                                         f"Оплата на сумму: {data[5]} {data[6]}\n"
                                         f"Способ оплаты: {data[7]}\n"
                                         f"\n"
                                         f"ID: {data[1]}\n"
                                         f"USERNAME: {data[2]}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='no_pay_vip_slot'))
async def cb_no_pay_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    await callback.message.delete()
    check = await get_check_vip_slot(callback_data['id'])
    profile = await get_profile(callback.from_user.id)
    for data in check:
        lang = await get_user_lang(data[1])
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
            amount_slots = await get_amount_events(data[9])
            remaining_slots = amount_slots + 1
            await update_amount_event(data[9], remaining_slots)
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc_tour = await get_desc_prac_vip(data[9])
            amount_slots = await get_amount_vip_prac(data[9])
            remaining_slots = amount_slots + 1
            await update_amount_vip_prac(data[9], remaining_slots)
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
            amount_slots = await get_amount_vip_slot_time(data[9], data[17])
            remaining_slots = amount_slots + 1
            await update_amount_vip_slot(data[9], data[17], remaining_slots)
        await callback.message.answer(f"❌Не успешная оплата №{data[8]}")
        if profile == "pro":
            await bot.send_message(chat_id=data[1],
                                   text=f"{_('Оплата не прошла!', lang)}\n"
                                        f"{_('Проверьте еще раз оплату или обратитесь в 💬Поддержку', lang)}",
                                   reply_markup=main_menu_kb(lang))
        elif profile == "young":
            await bot.send_message(chat_id=data[1],
                                   text=f"{_('Оплата не прошла!', lang)}\n"
                                        f"{_('Проверьте еще раз оплату или обратитесь в 💬Поддержку', lang)}",
                                   reply_markup=main_young_menu_ikb(lang))
        if not data[3]:
            await bot.send_document(chat_id=all_payment_chat,
                                    document=data[4],
                                    caption=f"❌Не успешная оплата №{data[8]}\n"
                                            f"\n"
                                            f"{tour_name}\n"
                                            f"\n"
                                            f"{desc_tour}\n"
                                            f"TIME: {data[17]}:00\n"
                                            f"\n"
                                            f"Оплата на сумму: {data[5]} {data[6]}\n"
                                            f"Способ оплаты: {data[7]}\n"
                                            f"\n"
                                            f"ID: {data[1]}\n"
                                            f"USERNAME: {data[2]}")
        elif not data[4]:
            await bot.send_photo(chat_id=all_payment_chat,
                                 photo=data[3],
                                 caption=f"❌Не успешная оплата №{data[8]}\n"
                                         f"\n"
                                         f"{tour_name}\n"
                                         f"\n"
                                         f"{desc_tour}\n"
                                         f"TIME: {data[17]}:00\n"
                                         f"\n"
                                         f"Оплата на сумму: {data[5]} {data[6]}\n"
                                         f"Способ оплаты: {data[7]}\n"
                                         f"\n"
                                         f"ID: {data[1]}\n"
                                         f"USERNAME: {data[2]}")
    await callback.answer()



@dp.callback_query_handler(tour_cb.filter(action='get_cap_chat'))
async def cb_get_cap_chat_vip(callback : types.CallbackQuery, callback_data : dict):
    check = await get_check_vip_slot(callback_data['id'])
    for data in check:
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
            amount = await get_amount2_events(data[9])
            new_amount = amount - 1
            await update_amount2_event(data[9], new_amount)
            if new_amount == 0:
                await delete_event(data[9])
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc_tour = await get_desc_prac_vip(data[9])
            amount = await get_amount2_vip_prac(data[9])
            new_amount = amount - 1
            await update_amount2_vip_prac(data[9], new_amount)
            if new_amount == 0:
                await admin_delete_vip_prac(data[9])
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
            amount = await get_amount2_vip_slot_time(data[9], data[17])
            new_amount = amount - 1
            await update_amount2_vip_slot(data[9], data[17], new_amount)
            amount_slots = await get_amount2_vip_slot(data[9])
            total_amount_slots = sum(amount[0] for amount in amount_slots)
            if total_amount_slots == 0:
                await delete_vip_slot(data[9])
        await callback.message.answer(f"✅Заказ №{data[8]} успешно выполнен!")
        await bot.send_message(chat_id=all_payment_chat,
                               text=f"✅Заказ №{data[8]} успешно выполнен!\n"
                                    f"\n"
                                    f"{tour_name}\n"
                                    f"\n"
                                    f"{desc_tour}\n"
                                    f"TIME: {data[17]}:00\n"
                                    f"\n"
                                    f"{data[13]} | {data[14]} | {data[15]}\n"
                                    f"\n"
                                    f"Оплата на сумму: {data[5]} {data[6]}\n"
                                    f"Способ оплаты: {data[7]}\n"
                                    f"\n"
                                    f"ID: {data[1]}\n"
                                    f"USERNAME: {data[2]}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='no_get_cap_chat'))
async def cb_get_cap_chat(callback : types.CallbackQuery, callback_data : dict):
    await callback.message.delete()
    check = await get_check_vip_slot(callback_data['id'])
    for data in check:
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc_tour = await get_desc_prac_vip(data[9])
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
        await callback.message.answer(f"❌Заказ №{data[8]} отменен!")
        await bot.send_message(chat_id=callback.from_user.id,
                               text=f"❌Заказ №{data[8]} не выполнен!\n"
                                    f"\n"
                                    f"{tour_name}\n"
                                    f"\n"
                                    f"{desc_tour}\n"
                                    f"TIME: {data[17]}:00\n"
                                    f"\n"
                                    f"{data[13]} | {data[14]} | {data[15]}\n"
                                    f"\n"
                                    f"USERNAME: {data[2]}",
                               reply_markup=admin_send_reason_vip_ikb(callback_data['id']))
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='send_reason_vip_slot'))
async def cb_send_reason_vip_slot(callback : types.CallbackQuery, callback_data : dict, state : FSMContext):
    await callback.message.reply("Укажите причину:")
    async with state.proxy() as data:
        data['check_id'] = callback_data['id']
    await BuyVipSlotStatesGroup.reason.set()
    await callback.message.delete()
    await callback.answer()

@dp.callback_query_handler(tour_cb.filter(action='no_send_rsn_vip_slot'))
async def cb_no_send_reason_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    await callback.message.delete()
    check = await get_check_vip_slot(callback_data['id'])
    for data in check:
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc_tour = await get_desc_prac_vip(data[9])
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
        if not data[11] and not data[12]:
            await bot.send_message(chat_id=admin_get_cap_chat,
                                   text=f"Заказ №{data[8]}\n"
                                        f"\n"
                                        f"{tour_name}\n"
                                        f"\n"
                                        f"{desc_tour}\n"
                                        f"TIME: {data[17]}:00\n"
                                        f"\n"
                                        f"{data[13]} | {data[14]} | {data[15]}\n"
                                        f"\n"
                                        f"USERNAME: {data[2]}",
                                   reply_markup=admin_get_cap_chat_ikb(data[0]))
        elif not data[11]:
            await bot.send_document(chat_id=admin_get_cap_chat,
                                    document=data[12],
                                    caption=f"Заказ №{data[8]}\n"
                                            f"\n"
                                            f"{tour_name}\n"
                                            f"\n"
                                            f"{desc_tour}\n"
                                            f"TIME: {data[17]}:00\n"
                                            f"\n"
                                            f"{data[13]} | {data[14]} | {data[15]}\n"
                                            f"\n"
                                            f"USERNAME: {data[2]}",
                                    reply_markup=admin_get_cap_chat_ikb(data[0]))
        elif not data[12]:
            await bot.send_photo(chat_id=admin_get_cap_chat,
                                 photo=data[11],
                                 caption=f"Заказ №{data[8]}\n"
                                         f"\n"
                                         f"{tour_name}\n"
                                         f"\n"
                                         f"{desc_tour}\n"
                                         f"TIME: {data[17]}:00\n"
                                         f"\n"
                                         f"{data[13]} | {data[14]} | {data[15]}\n"
                                         f"\n"
                                         f"USERNAME: {data[2]}",
                                 reply_markup=admin_get_cap_chat_ikb(data[0]))
    await callback.answer()

@dp.callback_query_handler(tour_cb.filter(action='conf_send_rsn_vip_slot'))
async def cb_conf_send_rsn_vip(callback : types.CallbackQuery, callback_data : dict):
    check = await get_check_vip_slot(callback_data['id'])
    for data in check:
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc_tour = await get_desc_prac_vip(data[9])
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
        await callback.message.answer(f"❌Заказ №{data[8]} отменен!")
        await bot.send_message(chat_id=all_payment_chat,
                               text=f"❌Заказ №{data[8]} не выполнен!\n"
                                    f"\n"
                                    f"Причина: {data[16]}\n"
                                    f"\n"
                                    f"{tour_name}\n"
                                    f"\n"
                                    f"{desc_tour}\n"
                                    f"TIME: {data[17]}:00\n"
                                    f"\n"
                                    f"{data[13]} | {data[14]} | {data[15]}\n"
                                    f"\n"
                                    f"USERNAME: {data[2]}")
    await callback.message.delete()
    await callback.answer()