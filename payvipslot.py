from aiogram import types
from aiogram.dispatcher import FSMContext

from hendlers import cb_check_ban_user, set_new_click
from main import dp, bot
from config import admin_pay_slot, admin_get_cap_chat
from database import *
from keyboards import *
from states import BuyVipSlotStatesGroup
from translations import _
from youngkb import main_young_menu_ikb, info_from_bd, back_vip_prac_ikb


@dp.callback_query_handler(tour_cb.filter(action='send_check_vip_slot'))
async def cb_send_check_vip_slot(callback : types.CallbackQuery, callback_data : dict, state : FSMContext):
    await send_check_vip_part1(callback, callback_data, state)
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='change_check_vip_slot'))
async def cb_change_check_vip_slot(callback : types.CallbackQuery, callback_data : dict, state : FSMContext):
    await send_check_vip_part1(callback, callback_data, state)
    await callback.message.delete()
    await callback.answer()


async def send_check_vip_part1(callback, callback_data, state):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        await set_new_click(user_id)
        check = await get_check_vip_slot(callback_data['id'])
        for data in check:
            if data[10] == "prac":
                amount_slots = await get_amount_vip_prac(data[9])
                kb = back_vip_prac_ikb(lang)
                await send_check_vip_part2(amount_slots, callback, state, kb, callback_data, lang)
            elif data[10] == 'event':
                amount_slots = await get_amount_events(data[9])
                kb = back_pro_main(lang)
                await send_check_vip_part2(amount_slots, callback, state, kb, callback_data, lang)
            elif data[10] == 'vip_slot':
                amount_slots = await get_amount_vip_slot_time(data[9], data[17])
                kb = back_vip_slot_main_ikb(lang)
                await send_check_vip_part2(amount_slots, callback, state, kb, callback_data, lang)

async def send_check_vip_part2(amount_slots, callback, state, kb, callback_data, lang):
    if amount_slots == 0:
        await callback.message.answer(f"{_('К сожалению слотов больше не осталось!', lang)}\n"
                                      f"\n"
                                      f"{_('Если вы уже совершили оплату, выберите другое мероприятие такой же стоимости и отправьте туда чек или же обратитесь в 💬Подержку за возвратом денежных средств!🤗', lang)}",
                                      reply_markup=kb)
    else:
        async with state.proxy() as data:
            data['check_id'] = callback_data['id']
        await callback.message.answer(_("Отправьте чек:", lang),
                                      reply_markup=cancel_kb(lang))
        await BuyVipSlotStatesGroup.proof.set()


@dp.callback_query_handler(tour_cb.filter(action='confirm_buy_vip_slot'))
async def cb_confirm_buy_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.answer(_("Ожидайте подтверждения платежа!", lang),
                                  reply_markup=ReplyKeyboardRemove())
    check = await get_check_vip_slot(callback_data['id'])
    await set_new_click(callback.from_user.id)
    for data in check:
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
            price = await get_price_event(data[9])
            amount_slots = await get_amount_events(data[9])
            remaining_slots = amount_slots - 1
            await update_amount_event(data[9], remaining_slots)
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc_tour = await get_desc_prac_vip(data[9])
            price = await get_price_vip_prac(data[9])
            amount_slots = await get_amount_vip_prac(data[9])
            remaining_slots = amount_slots - 1
            await update_amount_vip_prac(data[9], remaining_slots)
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
            price = await get_price_vip_slot(data[9])
            amount_slots = await get_amount_vip_slot_time(data[9], data[17])
            remaining_slots = amount_slots - 1
            await update_amount_vip_slot(data[9], data[17], remaining_slots)
        if not data[3]:
            await bot.send_document(chat_id=admin_pay_slot,
                                    document=data[4],
                                    caption=f"Оплата №{data[8]}\n"
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
                                            f"USERNAME: {data[2]}",
                                    reply_markup=admin_check_pay_vip_slot(data[0]))
        else:
            await bot.send_photo(chat_id=admin_pay_slot,
                                 photo=data[3],
                                 caption=f"Оплата №{data[8]}\n"
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
                                         f"USERNAME: {data[2]}",
                                 reply_markup=admin_check_pay_vip_slot(data[0]))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='send_info_for_vip_slot'))
async def cb_send_info_for_vip_slot(callback : types.CallbackQuery, callback_data : dict, state : FSMContext):
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.answer(_("Отправьте название команды:", lang))
    await set_new_click(callback.from_user.id)
    async with state.proxy() as data:
        data['check_id'] = callback_data['id']
    await BuyVipSlotStatesGroup.team_name.set()
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='change_info_vip_slot'))
async def cb_change_info_vip_slot(callback : types.CallbackQuery, callback_data : dict, state : FSMContext):
    lang = await get_user_lang(callback.from_user.id)
    await set_new_click(callback.from_user.id)
    await callback.message.answer(_("Отправьте название команды:", lang))
    async with state.proxy() as data:
        data['check_id'] = callback_data['id']
    await BuyVipSlotStatesGroup.team_name.set()
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_info_vip_slot'))
async def cb_confirm_info_vip_slot(callback : types.CallbackQuery, callback_data : dict):
    await callback.message.delete()
    lang = await get_user_lang(callback.from_user.id)
    check = await get_check_vip_slot(callback_data['id'])
    profile = await get_profile(callback.from_user.id)
    await set_new_click(callback.from_user.id)
    if profile == 'pro':
        await callback.message.answer(f"{_('Благодарим за покупку!', lang)}\n"
                                      f"{_('Слот выдается в течение 20 минут(если покупка совершена за час до начала, слот будет выдан моментально).', lang)}",
                                      reply_markup=main_menu_kb(lang))
    elif profile == 'young':
        await callback.message.answer(f"{_('Благодарим за покупку!', lang)}\n"
                                      f"{_('Слот выдается в течение 20 минут(если покупка совершена за час до начала, слот будет выдан моментально).', lang)}",
                                      reply_markup=main_young_menu_ikb(lang))
    for data in check:
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc = await get_desc_event(data[9])
        elif data[10] == 'prac':
            tour_name = await get_vip_prac_name(data[9])
            desc = await get_desc_prac_vip(data[9])
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc = await get_desc_vip_slot(data[9])
        if not data[11] and not data[12]:
            await bot.send_message(chat_id=admin_get_cap_chat,
                                   text=f"Заказ №{data[8]}\n"
                                        f"\n"
                                        f"{tour_name}\n"
                                        f"\n"
                                        f"{desc}\n"
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
                                            f"{desc}\n"
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
                                         f"{desc}\n"
                                         f"TIME: {data[17]}:00\n"
                                         f"\n"
                                         f"{data[13]} | {data[14]} | {data[15]}\n"
                                         f"\n"
                                         f"USERNAME: {data[2]}",
                                 reply_markup=admin_get_cap_chat_ikb(data[0]))

    await callback.answer()


# LOAD INFO FOR VIP SLOT/EVENT/PRAC
@dp.message_handler(content_types=['photo', 'document', 'text'], state=BuyVipSlotStatesGroup.proof)
async def load_proof_vip_slot(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    profile = await get_profile(message.from_user.id)
    if message.text == f'❌{_("Отменить", lang)}':
        await set_new_click(message.from_user.id)
        if profile == 'young':
            await message.answer(_("Вы вернулись в главное меню:", lang),
                                 reply_markup=main_young_menu_ikb(lang))
        elif profile == 'pro':
            await message.answer(_("Вы вернулись в главное меню:", lang),
                                 reply_markup=main_menu_kb(lang))
        await state.finish()
    elif message.content_type == 'photo':
        async with state.proxy() as data:
            data['proof'] = message.photo[0].file_id
        await update_pay_proof_vip_slot(data['proof'], data['check_id'])
        await message.answer_photo(photo=data['proof'],
                                   caption=_("Подтвердите платеж:", lang),
                                   reply_markup=confirm_buy_vip_slot(data['check_id'], lang))
        await state.finish()
    elif message.content_type == 'document':
        async with state.proxy() as data:
            data['proof'] = message.photo[0].file_id
        await update_pay_proof_d_vip_slot(data['proof'], data['check_id'])
        await message.answer_document(document=data['proof'],
                                      caption=_("Подтвердите платеж:", lang),
                                      reply_markup=confirm_buy_vip_slot(data['check_id'], lang))
        await state.finish()
    else:
        await message.answer(_("Отправьте чек документом/файлом!", lang))


@dp.message_handler(lambda message : len(message.text) > 30, state=BuyVipSlotStatesGroup.team_name)
async def check_team_name_vip_slot(message : types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название команды не дожно превышать 30 символов!", lang))

@dp.message_handler(state=BuyVipSlotStatesGroup.team_name)
async def load_team_name(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['team_name'] = message.text
    await message.answer(_("Укажите тег команды:", lang))
    await BuyVipSlotStatesGroup.next()


@dp.message_handler(lambda message : len(message.text) > 20, state=BuyVipSlotStatesGroup.team_tag)
async def check_team_name_vip_slot(message : types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Тег команды не дожно превышать 20 символов!", lang))

@dp.message_handler(state=BuyVipSlotStatesGroup.team_tag)
async def load_team_tag(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['team_tag'] = message.text
    await message.answer(_("Отправьте Discord/Telegram ник для доступа к кеп чату:", lang))
    await BuyVipSlotStatesGroup.next()


@dp.message_handler(lambda message : len(message.text) > 20, state=BuyVipSlotStatesGroup.cap)
async def check_team_name_vip_slot(message : types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Discord/Telegram ник не должен превышать 20 символов", lang))

@dp.message_handler(state=BuyVipSlotStatesGroup.cap)
async def load_cap(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['cap'] = message.text
    await message.answer(_("Отправьте логотип команды(фото или файл):", lang),
                         reply_markup=info_from_bd(_("Пропустить", lang)))
    await BuyVipSlotStatesGroup.next()


@dp.message_handler(content_types=['document', 'photo', 'text'], state=BuyVipSlotStatesGroup.logo)
async def load_logo(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        if message.content_type == 'photo':
            data['logo'] = message.photo[0].file_id
        elif message.content_type == 'document':
            data['logo'] = message.document.file_id
    if message.text == _("Пропустить", lang):
        await message.answer(f"Team name: {data['team_name']}\n"
                             f"Tag: {data['team_tag']}\n"
                             f"\n"
                             f"Discord/Telegram nickname: {data['cap']}",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(_("Все верно?", lang),
                             reply_markup=confirm_info_pay_vip_slot_ikb(data['check_id'], lang))
        await update_text_info_vip_slot(state)
        await state.finish()
    elif message.content_type == 'photo':
        await update_info_for_vip_slot(state)
        await message.answer_photo(photo=data['logo'],
                                   caption=f"Team name: {data['team_name']}\n"
                                           f"Tag: {data['team_tag']}\n"
                                           f"\n"
                                           f"Discord/Telegram nickname: {data['cap']}",
                                   reply_markup=ReplyKeyboardRemove())
        await message.answer(_("Все верно?", lang),
                             reply_markup=confirm_info_pay_vip_slot_ikb(data['check_id'], lang))

        await state.finish()
    elif message.content_type == 'document':
        await update_info_d_for_vip_slot(state)
        await message.answer_document(document=data['logo'],
                                      caption=f"Team name: {data['team_name']}\n"
                                              f"Tag: {data['team_tag']}\n"
                                              f"\n"
                                              f"Discord/Telegram nickname: {data['cap']}",
                                      reply_markup=ReplyKeyboardRemove())
        await message.answer(_("Все верно?", lang),
                             reply_markup=confirm_info_pay_vip_slot_ikb(data['check_id'], lang))

        await state.finish()
    else:
        await message.answer(_("Отправьте логотип команды файлом или фото!", lang))


@dp.message_handler(state=BuyVipSlotStatesGroup.reason)
async def load_reason_vip_slot(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    await update_reason_vip_slot(state)
    check = await get_check_vip_slot(data['check_id'])
    for data in check:
        if data[10] == "event":
            tour_name = await get_event_name(data[9])
            desc_tour = await get_desc_event(data[9])
        else:
            tour_name = await get_name_tour_vip_slot(data[9])
            desc_tour = await get_desc_vip_slot(data[9])
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"❌Заказ №{data[8]} не выполнен!\n"
                                    f"\n"
                                    f"Причина: {data[16]}\n"
                                    f"\n"
                                    f"{tour_name}\n"
                                    f"\n"
                                    f"{desc_tour}\n"
                                    f"TIME: {data[17]}\n"
                                    f"\n"
                                    f"{data[13]} | {data[14]} | {data[15]}\n"
                                    f"\n"
                                    f"USERNAME: {data[2]}",
                               reply_markup=admin_conf_reason_vip_ikb(data[0]))
    await state.finish()