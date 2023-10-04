from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp, bot
from config import *
from hendlers import check_ban_user, cb_check_ban_user

from database import *
from keyboards import *
from youngkb import *
from translations import _
from states import BanStatesGroup



words_list = ["🛑BAN/UNBAN", "🔍Просмотреть анкеты"]

@dp.message_handler(lambda message: message.text in words_list)
async def all_text(message: types.Message):
    user_id = message.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in admin_id:
            if message.text == '🛑BAN/UNBAN':
                await message.answer("Выберите дейстивие:",
                                     reply_markup=admin_ban_menu())
            elif message.text == '🔍Просмотреть анкеты':
                await message.answer("Выберите действие:",
                                     reply_markup=check_users_profile())



@dp.callback_query_handler(tour_cb.filter(action='confirm_ban_user'))
async def cb_confirm_ban(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    admin_id = await get_admin_id(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if user_id in admin_id:
            await get_ban_user(callback_data['id'])
            await admin_delete_user(callback_data['id'])
            await admin_delete_user_team(callback_data['id'])
            await admin_delete_prac_user(callback_data['id'])
            await admin_delete_prac_team(callback_data['id'])
            reason = await get_reason_user(callback_data['id'])
            ban_time = await get_ban_time_user(callback_data['id'])
            await bot.send_message(chat_id=callback_data['id'],
                                   text=f"{_('Вы заблокированы в боте!', lang)}\n"
                                        f"{_('Причина', lang)}: {reason}\n"
                                        f"{_('Срок бана', lang)}: {ban_time}\n"
                                        f"{_('Ваш', lang)} ID: {callback.from_user.id}",
                                   reply_markup=ReplyKeyboardRemove())
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Блокировка пользователя!\n"
                                        f"Причина: {reason}\n"
                                        f"Срок бана: {ban_time}\n"
                                        f"ID: {callback_data['id']}\n"
                                        f"\n"
                                        f"ADMIN ID: {callback.from_user.id}\n"
                                        f"ADMIN USERNAME: @{callback.from_user.username}")
            await callback.message.answer("Вы заблокировали пользователя!",
                                          reply_markup=general_admin_kb())
        await callback.message.delete()
        await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='no_ban_user'))
async def cb_no_ban(callback: types.CallbackQuery, callback_data: dict):
    await get_unban_user(callback_data['id'])
    await callback.message.answer("Вы отменили блокировку пользователя!",
                                  reply_markup=general_admin_kb())
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_unban_user'))
async def cb_confirm_unban_user(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await get_unban_user(callback_data['id'])
        await bot.send_message(chat_id=callback_data['id'],
                               text="Вы разблокированы в боте!")
        await bot.send_message(chat_id=control_add_chat,
                               text=f"Рвзблокировка пользователя!\n"
                                    f"ID: {callback_data['id']}\n"
                                    f"\n"
                                    f"ADMIN ID: {callback.from_user.id}\n"
                                    f"ADMIN USERNAME: @{callback.from_user.username}")
        await callback.message.answer("Вы разблокировали пользователя!",
                                      reply_markup=general_admin_kb())
    await callback.message.delete()
    await callback.answer()


# ADMIN DELETE AGENT/TEAM
@dp.callback_query_handler(tour_cb.filter(action='admin_delete_user'))
async def cb_delete_user(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.reply("Вы действительно хотите удалить анкету?",
                                 reply_markup=confirm_delete_user(callback_data['id']))
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_delete_user'))
async def cb_confirm_delete_agent(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await admin_delete_user(callback_data['id'])
        await callback.message.answer("Эта анкета успешно удалена!")
        user_agent = await get_user_agent(callback_data['id'])
        for data in user_agent:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удалена анкета FREE AGENT!\n"
                                        f"\n"
                                        f"USER ID: {data[0]}\n"
                                        f"USERNAME: {data[10]}"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: @{callback.from_user.username}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='admin_delete_user_team'))
async def cb_delete_team(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.reply("Вы действительно хотите удалить анкету?",
                                 reply_markup=confirm_delete_team(callback_data['id']))
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_delete_team'))
async def cb_confirm_delete_team(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await admin_delete_user_team(callback_data['id'])
        await callback.message.answer("Эта анкета успешно удалена!")
        user_agent = await get_user_team(callback_data['id'])
        for data in user_agent:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удалена анкета FREE TEAM!\n"
                                        f"\n"
                                        f"USER ID: {data[0]}\n"
                                        f"USERNAME: {data[10]}"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: @{callback.from_user.username}")
    await callback.message.delete()
    await callback.answer()


# ADMIN DELETE PRAC AGENT/TEAM
@dp.callback_query_handler(tour_cb.filter(action='admin_prac_delete_user'))
async def cb_delete_prac_agent(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.reply("Вы действительно хотите удалить анкету?",
                                 reply_markup=confirm_delete_prac_user(callback_data['id']))
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_delete_prac_user'))
async def cb_confirm_delete_prac_agent(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await admin_delete_prac_user(callback_data['id'])
        await callback.message.answer("Эта анкета успешно удалена!")
        user_agent = await get_prac_agent_profile(callback_data['id'])
        for data in user_agent:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удалена анкета FREE TEAM!\n"
                                        f"\n"
                                        f"USER ID: {data[0]}\n"
                                        f"USERNAME: {data[9]}"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: @{callback.from_user.username}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='admin_delete_prac_user_team'))
async def cb_delete_prac_team(callback: types.CallbackQuery, callback_data: dict):
    await callback.message.reply("Вы действительно хотите удалить анкету?",
                                 reply_markup=confirm_delete_prac_team(callback_data['id']))
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='confirm_delete_prac_team'))
async def cb_confirm_delete_prac_team(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await admin_delete_prac_team(callback_data['id'])
        await callback.message.answer("Эта анкета успешно удалена!")
        user_agent = await get_prac_team_profile(callback_data['id'])
        for data in user_agent:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удалена анкета FREE TEAM!\n"
                                        f"\n"
                                        f"USER ID: {data[0]}\n"
                                        f"USERNAME: {data[9]}"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: @{callback.from_user.username}")
    await callback.message.delete()
    await callback.answer()



cb_words_list = ["select_user", "no_delete_user", "check_all_users", "admin_choose_agent", "admin_next_agent",
              "admin_ban_user", "admin_unban_user"]

@dp.callback_query_handler(lambda callback : callback.data in cb_words_list)
async def all_callbacks(callback: types.CallbackQuery):
    index = 0
    user_id = callback.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if user_id in admin_id:
            if callback.data == 'select_user':
                await bot.send_message(chat_id=user_id,
                                       text="Отправьте ID:",
                                       reply_markup=info_from_bd("❌Отменить"))
                await BanStatesGroup.user_id.set()
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'no_delete_user':
                await callback.message.answer("Вы отменили удаление анкеты!")
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'check_all_users':
                await callback.message.answer("Выберите действие:",
                                              reply_markup=admin_choose_user())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_choose_agent':
                index = 0
                user = await get_all_users_agent()
                if not user:
                    await callback.message.answer("Актуальных анкет нету!")
                else:
                    all_user = list(user)[index: index + 2]
                    index += 2
                    await callback.message.answer("Все актуальные анкеты:")
                    await send_info_agent_team(all_user, "free_agent", callback.message)
                    if len(all_user) < 2:
                        await callback.message.answer("Это все анкеты!")
                    else:
                        await callback.message.answer("Желаете продолжить просмотр?",
                                                      reply_markup=admin_next_agent())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_next_agent':
                user = await get_all_users_agent()
                all_user = list(user)[index: index + 2]
                index += 2
                await send_info_agent_team(all_user, "free_agent", callback.message)
                if len(all_user) < 2:
                    await callback.message.answer("Это все анкеты!")
                else:
                    await callback.message.answer("Желаете продолжить просмотр?",
                                                  reply_markup=admin_next_agent())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_choose_team':
                index = 0
                team = await get_all_users_team()
                if not team:
                    await callback.message.answer("Актуальных анкет нету!")
                else:
                    all_team = list(team)[index: index + 2]
                    index += 2
                    await callback.message.answer("Все актуальные анкеты:")
                    await send_info_agent_team(all_team, "free_team", callback.message)
                    if len(all_team) < 2:
                        await callback.message.answer("Это все анкеты!")
                    else:
                        await callback.message.answer("Желаете продолжить просмотр?",
                                                      reply_markup=admin_next_team())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_next_team':
                team = await get_all_users_team()
                all_team = list(team)[index: index + 2]
                index += 2
                await send_info_agent_team(all_team, "free_team", callback.message)
                if len(all_team) < 2:
                    await callback.message.answer("Это все анкеты!")
                else:
                    await callback.message.answer("Желаете продолжить просмотр?",
                                                  reply_markup=admin_next_team())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_check_prac_agent':
                index = 0
                agent = await admin_get_all_prac_agent()
                all_agent = list(agent)[index: index + 2]
                index += 2
                if not agent:
                    await callback.message.answer("Актуальных анкет нету!")
                else:
                    await callback.message.answer("Все актуальные анкеты:")
                    await send_info_agent_team(all_agent, "free_prac_a", callback.message)
                    if len(all_agent) < 2:
                        await callback.message.answer("Это все актуальные анкеты!")
                    else:
                        await callback.message.answer("Желаете продолжить просмотр?",
                                                      reply_markup=admin_next_prac_agent())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_next_prac_agent':
                agent = await admin_get_all_prac_agent()
                all_agent = list(agent)[index: index + 2]
                index += 2
                await send_info_agent_team(all_agent, "free_prac_a", callback.message)
                if len(all_agent) < 2:
                    await callback.message.answer("Это все актуальные анкеты!")
                else:
                    await callback.message.answer("Желаете продолжить просмотр?",
                                                  reply_markup=admin_next_prac_agent())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_check_prac_team':
                index = 0
                team = await admin_get_all_prac_team()
                all_team = list(team)[index: index + 2]
                index += 2
                if not team:
                    await callback.message.answer("Актуальных анкет нету!")
                else:
                    await callback.message.answer("Все актуальные анкеты:")
                    await send_info_agent_team(all_team, "free_prac_t", callback.message)
                    if len(all_team) < 2:
                        await callback.message.answer("Это все актуальные анкеты!")
                    else:
                        await callback.message.answer("Желаете продолжить просмотр?",
                                                      reply_markup=admin_next_prac_team())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_next_prac_team':
                team = await admin_get_all_prac_team()
                all_team = list(team)[index: index + 2]
                index += 2
                await send_info_agent_team(all_team, "free_prac_t", callback.message)
                if len(all_team) < 2:
                    await callback.message.answer("Это все актуальные анкеты!")
                else:
                    await callback.message.answer("Желаете продолжить просмотр?",
                                                  reply_markup=admin_next_prac_team())
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_ban_user':
                await bot.send_message(chat_id=user_id,
                                       text="Отправьте ID:",
                                       reply_markup=info_from_bd("❌Отменить"))
                await BanStatesGroup.ban_user_id.set()
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'admin_unban_user':
                await callback.message.answer("Отправьте ID:",
                                              reply_markup=info_from_bd("❌Отменить"))
                await BanStatesGroup.unban.set()
                await callback.message.delete()
                await callback.answer()



@dp.message_handler(lambda message: not message.text.isdigit() and len(message.text) > 15, state=BanStatesGroup.user_id)
async def check_id(message: types.Message):
    await message.answer("ID не должно превышать 15 символов(использовать можно только цифры)!")


@dp.message_handler(state=BanStatesGroup.user_id)
async def load_user_ban(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в главное меню:",
                             reply_markup=general_admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['user_id'] = message.text
        user = await get_user_agent(data['user_id'])
        team = await get_user_team(data['user_id'])
        prac_agent = await get_prac_agent(data['user_id'])
        prac_team = await get_prac_team(data['user_id'])
        await send_info_agent_team(user, "free_agent", message)
        if not user:
            await message.answer("Такого пользователя в FREE AGENT нету!",
                                 reply_markup=general_admin_kb())
        await send_info_agent_team(team, "free_team", message)
        if not team:
            await message.answer("Такого пользователя в FREE TEAM нету!",
                                 reply_markup=general_admin_kb())
        await send_info_agent_team(prac_agent, "free_prac_a", message)
        if not prac_agent:
            await message.answer("Такого пользователя в FREE PRAC AGENT нету!",
                                 reply_markup=general_admin_kb())
        await send_info_agent_team(prac_team, "free_prac_t", message)
        if not prac_team:
            await message.answer("Такого пользователя в FREE PRAC TEAM нету!",
                                 reply_markup=general_admin_kb())
        await state.finish()


@dp.message_handler(lambda message: not message.text.isdigit() and len(message.text) > 15,
                    state=BanStatesGroup.ban_user_id)
async def check_id(message: types.Message):
    await message.answer("ID не должно превышать 15 символов(использовать можно только цифры)!")


@dp.message_handler(state=BanStatesGroup.ban_user_id)
async def load_ban_user_id(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в главное меню:",
                             reply_markup=general_admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['ban_user_id'] = message.text
        ban_user_id = await check_id_for_ban(data['ban_user_id'])
        if ban_user_id is None:
            await message.answer("Такого пользователя нету в системе!",
                                 reply_markup=general_admin_kb())
            await state.finish()
        elif ban_user_id in ceo:
            await message.answer("Вы не можете забанить создателя!",
                                 reply_markup=general_admin_kb())
            await bot.send_message(chat_id=ceo,
                                   text=f"Вас пытались забанить!\n"
                                        f"\n"
                                        f"ID: {message.from_user.id}\n"
                                        f"USERNAME: @{message.from_user.username}")
            await state.finish()
        else:
            check_block = await get_block_user(data['ban_user_id'])
            if check_block == 1:
                await message.answer("Этот пользователь уже заблокирован!",
                                     reply_markup=general_admin_kb())
                await state.finish()
            else:
                await message.answer("Укажите причину бана:",
                                     reply_markup=ReplyKeyboardRemove())
                await BanStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=BanStatesGroup.reason)
async def check_ban_reason(message: types.Message):
    await message.answer("Текст не должен превышать 40 символов!")


@dp.message_handler(state=BanStatesGroup.reason)
async def load_reason(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    await message.answer("Укажите срок бана:")
    await BanStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=BanStatesGroup.ban_time)
async def check_ban_reason(message: types.Message):
    await message.answer("Текст не должен превышать 40 символов!")


@dp.message_handler(state=BanStatesGroup.ban_time)
async def load_ban_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ban_time'] = message.text
    await load_ban_info(state, data['ban_user_id'])
    await state.finish()
    await message.answer(f"ID: {data['ban_user_id']}\n"
                         f"Причина: {data['reason']}\n"
                         f"Срок бана: {data['ban_time']}")
    await message.answer("Подтвердите бан этого пользователя:",
                         reply_markup=confirm_ban_user(data['ban_user_id']))


@dp.message_handler(state=BanStatesGroup.unban)
async def unban_user(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в главное меню:",
                             reply_markup=general_admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['unban'] = message.text
        ban_user_id = await check_id_for_ban(data['unban'])
        if not ban_user_id:
            await message.answer("Такого пользователя нету в системе!",
                                 reply_markup=general_admin_kb())
            await state.finish()
        else:
            check_block = await get_block_user(data['unban'])
            if check_block == 0:
                await message.answer("Этот пользователь не заблокирован!",
                                     reply_markup=general_admin_kb())
                await state.finish()
            else:
                await message.answer("Подтвердите разблокировку этого пользователя:",
                                     reply_markup=confirm_unban_user_kb(data['unban']))
                await state.finish()



async def send_info_agent_team(info, format, message):
    for data in info:
        if format == "free_agent":
            await message.answer(f"Free agent\n"
                                 f"\n"
                                 f"Nickname: {data[1]}\n"
                                 f"Age: {data[2]}\n"
                                 f"Teamspeak: {data[3]} {data[4]}\n"
                                 f"Device: {data[5]}\n"
                                 f"Tournament: {data[6]}\n"
                                 f"Finals: {data[7]}\n"
                                 f"Highlights: {data[8]}\n"
                                 f"\n"
                                 f"{data[9]}\n"
                                 f"\n"
                                 f"{data[10]}\n"
                                 f"ID: {data[0]}",
                                 reply_markup=admin_edit_user(data[0]))
        elif format == "free_team":
            await message.answer(f"Free team\n"
                                 f"\n"
                                 f"Team name: {data[1]}\n"
                                 f"\n"
                                 f"Критерии игрока👇\n"
                                 f"Age: {data[2]}+\n"
                                 f"TeamSpeak: {data[3]} {data[4]}\n"
                                 f"Role: {data[5]}\n"
                                 f"Device: {data[6]}\n"
                                 f"Tournament: {data[7]}\n"
                                 f"Finals: {data[8]}\n"
                                 f"\n"
                                 f"{data[9]}\n"
                                 f"\n"
                                 f"{data[10]}\n"
                                 f"ID: {data[0]}",
                                 reply_markup=admin_edit_user_team(data[0]))
        elif format == "free_prac_a":
            await message.answer(f"Free prac agent\n"
                                 f"\n"
                                 f"Nickname: {data[1]}\n"
                                 f"Age: {data[2]}\n"
                                 f"Teamspeak: {data[3]} {data[4]}\n"
                                 f"Device: {data[5]}\n"
                                 f"Practice games: {data[6]}\n"
                                 f"Highlights: {data[7]}\n"
                                 f"\n"
                                 f"{data[8]}"
                                 f"\n"
                                 f"{data[9]}\n"
                                 f"ID: {data[0]}",
                                 reply_markup=admin_prac_edit_user(data[0]))
        elif format == "free_prac_t":
            await message.answer(f"Free prac team\n"
                                 f"\n"
                                 f"Team name: {data[1]}\n"
                                 f"\n"
                                 f"Критерии игрока👇\n"
                                 f"Age: {data[2]}\n"
                                 f"Teamspeak: {data[3]} {data[4]}\n"
                                 f"Role: {data[5]}"
                                 f"Device: {data[6]}\n"
                                 f"Practice games: {data[7]}\n"
                                 f"\n"
                                 f"{data[8]}"
                                 f"\n"
                                 f"{data[9]}\n"
                                 f"ID: {data[0]}",
                                 reply_markup=admin_edit_prac_user_team(data[0]))