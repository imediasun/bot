import asyncio
from uuid import uuid4
from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp, bot
from config import *
from hendlers import check_ban_user, cb_check_ban_user, is_valid_url

from database import *
from keyboards import *
from youngkb import *
from states import AddadminStatesGroup, AdminSendMessagesStatesGroup, AddNewsStatesGroup, GetRandomUserStatesGroup



@dp.message_handler(commands=['admin'])
async def cd_admin(message: types.Message):
    user_id = message.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in admin_id or user_id in ceo:
            await message.answer("Выберите действие:",
                                 reply_markup=general_admin_kb())
        # elif user_id in ceo:
        #     await message.answer("Выберите действие:",
        #                          reply_markup=general_admin_kb())


@dp.message_handler(commands=['moderator'])
async def cd_moderator(message: types.Message):
    user_id = message.from_user.id
    moder_id = await get_moder_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in moder_id:
            await message.answer(text="Что вы хотите добавить?",
                                 reply_markup=admin_kb())
        elif user_id in ceo:
            await message.answer(text="Что вы хотите добавить?",
                                 reply_markup=admin_kb())



words_list = ["🤴ADD ADMIN", "ADD 🔥NEWS", "📊Статистика", "⬆️Сделать рассылку", "◀️YOUNG", "PRO▶️"]

@dp.message_handler(lambda message: message.text in words_list)
async def all_text(message: types.Message):
    global index
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    admin_id = await get_moder_id(user_id)
    moder_id = await get_moder_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in admin_id or user_id in ceo:
            if message.text == '🤴ADD ADMIN':
                await message.answer("Выберите действие",
                                     reply_markup=add_admin_kb())
            elif message.text == 'ADD 🔥NEWS':
                await message.answer("Выберите действие:",
                                     reply_markup=admin_news_ikb())
            elif message.text == '📊Статистика':
                await message.answer("Выберите действия:",
                                     reply_markup=admin_statistic_ikb())
            elif message.text == '⬆️Сделать рассылку':
                await message.answer("Отправьте фото:",
                                     reply_markup=admin_send_mess())
                await AdminSendMessagesStatesGroup.photo.set()
            elif message.text == '◀️YOUNG':
                await message.answer("Вы вернулись в YOUNG меню",
                                     reply_markup=main_young_menu_ikb(lang))
            elif message.text == 'PRO▶️':
                await message.answer("Вы вернулись в PRO меню",
                                     reply_markup=main_menu_kb(lang))
        elif user_id in moder_id:
            if message.text == '◀️YOUNG':
                await message.answer("Вы вернулись в YOUNG меню",
                                     reply_markup=main_young_menu_ikb(lang))
            elif message.text == 'PRO▶️':
                await message.answer("Вы вернулись в PRO меню",
                                     reply_markup=main_menu_kb(lang))


# ADMIN SEND MESS
@dp.callback_query_handler(tour_cb.filter(action='conf_add_send_mess'))
async def conf_add_send_mess(callback : types.CallbackQuery, callback_data : dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer("Рассылка успешно запущена!",
                                      reply_markup=general_admin_kb())
        mess = await get_send_mess(callback_data['id'])
        user_ids = await get_user_ids()
        for data in mess:
            if not data[3]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"Запущена рассылка!\n"
                                            f"\n"
                                            f"{data[2]}\n"
                                            f"\n"
                                            f"{data[4]}\n"
                                            f"\n"
                                            f"ID: {callback.from_user.id}\n"
                                            f"USERNAME: @{callback.from_user.username}")
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[3],
                                     caption=f"Запущена рассылка!\n"
                                             f"\n"
                                             f"{data[2]}\n"
                                             f"\n"
                                             f"{data[4]}\n"
                                             f"\n"
                                             f"ID: {callback.from_user.id}\n"
                                             f"USERNAME: @{callback.from_user.username}")
        for user in user_ids:
            for data in mess:
                if not data[4]:
                    ikb = None
                else:
                    ikb = text_url_ikb("Перейти", data[4])
                try:
                    if not data[3]:
                        await bot.send_message(chat_id=user,
                                               text=data[2],
                                               reply_markup=ikb)
                    else:
                        await bot.send_photo(chat_id=user,
                                             photo=data[3],
                                             caption=data[2],
                                             reply_markup=ikb)
                except:
                    await bot.send_message(chat_id=control_add_chat,
                                           text="❗️Ошибка в рассылке!")
                    await bot.send_message(chat_id=5580704087,
                                           text="❗️Ошибка в рассылке!")
            await asyncio.sleep(0.4)
        await callback.message.answer("✅Рассылка завершена!")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_send_mess'))
async def cb_edit_send_mess(callback : types.CallbackQuery, callback_data : dict):
    await admin_delete_send_mess(callback_data['id'])
    await callback.message.answer("🗑Рассылка успешно удалена!",
                                  reply_markup=general_admin_kb())
    await callback.message.delete()
    await callback.answer()

# STATISTIC
@dp.callback_query_handler(lambda callback : callback.data.startswith("get_random_"))
async def admin_get_random_user(callback : types.CallbackQuery, state : FSMContext):
    where = callback.data.split("_")[2]
    await callback.message.answer("Введите количество юзеров:")
    async with state.proxy() as data:
        data['where'] = where
    await GetRandomUserStatesGroup.amount.set()
    await callback.message.delete()
    await callback.answer()



# ADD ADMIN
cb_words_list = ["add_admin", "check_admin_list", "back_general_admin", "statistic_count", "all_statistic",
                 "user_click_stat", "free_agent_stat", "free_team_stat", "young_free_agent_stat", "young_free_team_stat",
                 "back_stat_menu"]

@dp.callback_query_handler(lambda callback : callback.data in cb_words_list)
async def all_callbacks(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    admin_id = await get_admin_id(user_id)
    if user_id in admin_id or user_id in ceo:
        if callback.data == 'add_admin':
            await callback.message.answer("Отправьте ID для выдачи админа:")
            await AddadminStatesGroup.admin_id.set()
            await callback.answer()
        elif callback.data == 'check_admin_list':
            admins = await get_admin_list()
            if not admins:
                await callback.message.answer("Актуальных админов нету!")
            else:
                await callback.message.answer("Все актуальные админы:")
                for data in admins:
                    await callback.message.answer(f"{data[4]}\n"
                                                  f"\n"
                                                  f"Должность: {data[3]}\n"
                                                  f"ID: {data[0]}\n"
                                                  f"username: {data[2]}",
                                                  reply_markup=check_admins(data[0]))
            await callback.answer()
        elif callback.data == 'back_general_admin':
            await callback.message.answer("Вы вернулись в ADMIN меню:",
                                          reply_markup=general_admin_kb())
            await callback.answer()

        # ADMIN STATISTIC
        elif callback.data == 'all_statistic':
            all_users = await get_amount_all_users()
            statistic_log = await get_time_log()
            day_log = statistic_log[3]
            week_log = statistic_log[2]
            month_log = statistic_log[1]
            year_log = statistic_log[0]
            await callback.message.answer(f"Актуальная статистика\n"
                                          f"\n"
                                          f"Количество пользователей: {all_users}\n"
                                          f"Активные: -\n"
                                          f"Не активные: -\n"
                                          f"\n"
                                          f"Новых пользователей за:\n"
                                          f"День: {day_log}\n"
                                          f"Неделю: {week_log}\n"
                                          f"Месяц: {month_log}\n"
                                          f"Год: {year_log}",
                                          reply_markup=admin_back_stat_menu_ikb())
            await callback.message.delete()
            await callback.answer()
        elif callback.data == "user_click_stat":
            all_clicks = await get_sum_click_users()
            await callback.message.answer(f"Статистика по количеству кликов юзеров\n"
                                          f"\n"
                                          f"Общее количество кликов: {all_clicks}\n"
                                          f"\n"
                                          f"Топ по количеству кликов:",
                                          reply_markup=admin_all_click_stat_ikb())
            await callback.message.delete()
            await callback.answer()
        elif callback.data == "free_agent_stat":
            all_free_agents = await get_amount_free_agents()
            await callback.message.answer(f"Статистика по FREE AGENTS\n"
                                          f"\n"
                                          f"Количество анкет: {all_free_agents}\n"
                                          f"\n"
                                          f"Выбрать рандомно:",
                                          reply_markup=admin_free_agent_stat_ikb())
            await callback.message.delete()
            await callback.answer()
        elif callback.data == "free_team_stat":
            all_free_teams = await get_amount_free_teams()
            await callback.message.answer(f"Статистика по FREE TEAMS\n"
                                          f"\n"
                                          f"Количество анкет: {all_free_teams}\n"
                                          f"\n"
                                          f"Выбрать рандомно:",
                                          reply_markup=admin_free_team_stat_ikb())
            await callback.message.delete()
            await callback.answer()
        elif callback.data == "young_free_agent_stat":
            all_free_teams_p = await get_amount_free_agents_p()
            await callback.message.answer(f"Статистика по YOUNG FREE AGENTS\n"
                                          f"\n"
                                          f"Количество анкет: {all_free_teams_p}\n"
                                          f"\n"
                                          f"Выбрать рандомно:",
                                          reply_markup=admin_young_fa_stat_ikb())
            await callback.message.delete()
            await callback.answer()
        elif callback.data == "young_free_team_stat":
            all_free_agents_p = await get_amount_free_teams_p()
            await callback.message.answer(f"Статистика по YOUNG FREE TEAMS\n"
                                          f"\n"
                                          f"Количество анкет: {all_free_agents_p}\n"
                                          f"\n"
                                          f"Выбрать рандомно:",
                                          reply_markup=admin_young_ft_stat_ikb())
            await callback.message.delete()
            await callback.answer()
        elif callback.data == "back_stat_menu":
            await callback.message.answer("Выберите действия:",
                                          reply_markup=admin_statistic_ikb())
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'statistic_count':
            await callback.message.delete()
            await callback.answer()

        # ADMIN NEWS
        elif callback.data == 'admin_add_news':
            await callback.message.answer("Отправьте название канала:",
                                          reply_markup=info_from_bd("❌Отменить"))
            await AddNewsStatesGroup.text.set()
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'check_news':
            all_news = await get_all_news()
            await callback.message.answer("Все актуальные каналы:")
            for data in all_news:
                await callback.message.answer(f"{data[2]}\n"
                                              f"\n"
                                              f"{data[3]}",
                                              reply_markup=delete_news_ikb(data[0]))
            await callback.message.answer("Это все актуальные каналы!")
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'confirm_add_news':
            await callback.message.answer("Канал успешно добавлен!",
                                          reply_markup=general_admin_kb())
            await callback.message.delete()
            await callback.answer()



# ADD ADMIN
@dp.callback_query_handler(tour_cb.filter(action='yes_add_admin'))
async def cb_conf_add_admin(callback : types.CallbackQuery, callback_data : dict):
    ban = await check_ban_user(callback)
    if not ban:
        await callback.message.answer("Админ успешно добавлен!",
                                      reply_markup=general_admin_kb())
        admin = await get_admin_profile(callback_data['id'])
        for data in admin:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Добавлен {data[4]}!\n"
                                        f"\n"
                                        f"ADMIN ID: {data[0]}\n"
                                        f"ADMIN USERNAME: {data[2]}\n"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: @{callback.from_user.username}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_admin_profile'))
async def cb_edit_admin(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban = await check_ban_user(callback)
    if not ban:
        admin_id = await get_admin_id(callback_data['id'])
        await callback.message.answer("Отправьте ID для выдачи админа:",
                                      reply_markup=info_from_bd(admin_id[0]))
        await AddadminStatesGroup.new_admin_id.set()
        async with state.proxy() as data:
            data['a_id'] = callback_data['id']
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_admin_profile'))
async def cb_delete_admin(callback: types.CallbackQuery, callback_data: dict):
    ban = await check_ban_user(callback)
    if not ban:
        await delete_admin(callback_data['id'])
        await callback.message.reply("Админ успешно удален!")
        admin = await get_admin_profile(callback_data['id'])
        for data in admin:
            await bot.send_message(chat_id=control_add_chat,
                                   text=f"Удален {data[4]}!\n"
                                        f"\n"
                                        f"ADMIN ID: {data[0]}\n"
                                        f"ADMIN USERNAME: {data[2]}\n"
                                        f"\n"
                                        f"ID: {callback.from_user.id}\n"
                                        f"USERNAME: @{callback.from_user.username}")
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='check_admin_profile'))
async def check_admin_profile(callback: types.CallbackQuery, callback_data: dict):
    ban = await check_ban_user(callback)
    if not ban:
        admin_profile = await get_admin_profile(callback_data['id'])
        for data in admin_profile:
            await callback.message.answer(f"{data[4]}\n"
                                          f"\n"
                                          f"Должность: {data[3]}\n"
                                          f"ID: {data[0]}\n"
                                          f"username: {data[2]}",
                                          reply_markup=check_admins(data[0]))
    await callback.message.delete()
    await callback.answer()


# ADD NEWS
@dp.callback_query_handler(tour_cb.filter(action='delete_news'))
async def admin_delete_news(callback: types.CallbackQuery, callback_data: dict):
    await delete_news(callback_data['id'])
    await callback.message.answer("Канал успешно удален!",
                                  reply_markup=general_admin_kb())

    await callback.message.delete()
    await callback.answer()



# STATE ADD ADMIN
@dp.message_handler(state=AddadminStatesGroup.admin_id)
async def load_admin_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['admin_id'] = message.text
    user = await check_id_for_ban(data['admin_id'])
    admin = await get_admin_id(data['admin_id'])
    if not user:
        await message.answer("Такого пользователя нету в системе!",
                             reply_markup=general_admin_kb())
        await state.finish()
    elif not admin:
        await message.answer("Выберите тип аккаунта админа:",
                             reply_markup=type_admin_kb())
        await AddadminStatesGroup.next()
    else:
        await message.answer("Пользователь являеться админом:",
                             reply_markup=check_add_admin_ikb(data['admin_id']))
        await state.finish()


@dp.message_handler(state=AddadminStatesGroup.type_admin)
async def load_admin_type(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в ADMIN меню",
                             reply_markup=general_admin_kb())
        await state.finish()
    elif message.text == 'Moderator':
        async with state.proxy() as data:
            data['type_admin'] = 'Moderator'
        user = await bot.get_chat(data['admin_id'])
        username = user.username
        if not username:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd("Не указан"))
        else:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd(f"@{username}"))
        await AddadminStatesGroup.next()
    elif message.text == 'ADMIN':
        async with state.proxy() as data:
            data['type_admin'] = 'ADMIN'
        user = await bot.get_chat(data['admin_id'])
        username = user.username
        if not username:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd("Не указан"))
        else:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd(f"@{username}"))
        await AddadminStatesGroup.next()
    else:
        await message.answer("Такого варианта ответа нету!")
        await AddadminStatesGroup.type_admin.set()


@dp.message_handler(lambda message: len(message.text) > 40, state=AddadminStatesGroup.username)
async def check_admin_username(message: types.Message):
    await message.answer("username не должен превышать 40 символов!")


@dp.message_handler(state=AddadminStatesGroup.username)
async def load_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await message.answer("Ведите должность админа:",
                         reply_markup=ReplyKeyboardRemove())
    await AddadminStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 50, state=AddadminStatesGroup.job_title)
async def check_admin_job_title(message: types.Message):
    await message.answer("Описание должности не должно превышать 50 символов!")


@dp.message_handler(state=AddadminStatesGroup.job_title)
async def load_gob_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job_title'] = message.text
    await add_admin(state, user_id=message.from_user.id)
    await state.finish()
    await message.answer(f"Добавление {data['type_admin']}a\n"
                         f"\n"
                         f"ID: {data['admin_id']}\n"
                         f"username: {data['username']}\n"
                         f"Должность: {data['job_title']}")
    await message.answer("Все верно?",
                         reply_markup=confirm_add_admin(data['admin_id']))


# UPDATE ADMIN PROFILE
@dp.message_handler(state=AddadminStatesGroup.new_admin_id)
async def load_new_admin_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['admin_id'] = message.text
    user = await check_id_for_ban(data['admin_id'])
    admin = await get_admin_id(data['a_id'])
    if not user:
        await message.answer("Такого пользователя нету в системе!\n"
                             "Отправьте правильный ID:",
                             reply_markup=info_from_bd(admin))
        await AddadminStatesGroup.new_admin_id.set()
    else:
        await message.answer("Выберите тип аккаунта админа:",
                             reply_markup=type_admin_kb())
        await AddadminStatesGroup.next()


@dp.message_handler(state=AddadminStatesGroup.new_type_admin)
async def load_new_type_admin(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в ADMIN меню",
                             reply_markup=general_admin_kb())
        await state.finish()
    elif message.text == 'Moderator':
        async with state.proxy() as data:
            data['type'] = 'Moderator'
        user = await bot.get_chat(data['a_id'])
        username = user.username
        if not username:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd("Не указан"))
        else:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd(f"@{username}"))
        await AddadminStatesGroup.next()
    elif message.text == 'ADMIN':
        async with state.proxy() as data:
            data['type'] = 'ADMIN'
        user = await bot.get_chat(data['admin_id'])
        username = user.username
        if not username:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd("Не указан"))
        else:
            await message.answer("Отправьте username админа:",
                                 reply_markup=info_from_bd(f"@{username}"))
        await AddadminStatesGroup.next()
    else:
        await message.answer("Такого варианта ответа нету!")
        await AddadminStatesGroup.new_type_admin.set()


@dp.message_handler(lambda message: len(message.text) > 40, state=AddadminStatesGroup.new_username)
async def check_new_admin_username(message: types.Message):
    await message.answer("username не должен превышать 40 символов!")


@dp.message_handler(state=AddadminStatesGroup.new_username)
async def load_new_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await message.answer("Введите должность админа:",
                         reply_markup=ReplyKeyboardRemove())
    await AddadminStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 50, state=AddadminStatesGroup.new_job_title)
async def check_new_admin_job_title(message: types.Message):
    await message.answer("Описание должности не должно превышать 50 символов!")


@dp.message_handler(state=AddadminStatesGroup.new_job_title)
async def load_new_job_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job_title'] = message.text
    await update_admin(state, message.from_user.id)
    await message.answer(f"Изминение {data['type']}a\n"
                         f"\n"
                         f"ID: {data['admin_id']}\n"
                         f"username: {data['username']}\n"
                         f"Должность админа: {data['job_title']}")
    await message.answer("Все верно?",
                         reply_markup=confirm_add_admin(data['admin_id']))
    await state.finish()



# STATES ADD NEWS
@dp.message_handler(lambda message: len(message.text) > 40, state=AddNewsStatesGroup.text)
async def check_news_text(message: types.Message):
    await message.answer("Название телеграм канала не должно превышать 40 символов!")
    # ans_admin_id


@dp.message_handler(state=AddNewsStatesGroup.text)
async def load_news_text(message: types.Message, state: FSMContext):
    if message.text == '❌Отменить':
        await message.answer("Вы вернулись в ADMIN меню",
                             reply_markup=general_admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['text'] = message.text
        await message.answer("Отправьте ссылку на канал:",
                             reply_markup=ReplyKeyboardRemove())
        await AddNewsStatesGroup.next()


@dp.message_handler(lambda message: not is_valid_url(message.text), state=AddNewsStatesGroup.url)
async def check_news_url(message: types.Message):
    await message.answer("Это не ссылка!")


@dp.message_handler(state=AddNewsStatesGroup.url)
async def load_news_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
    news_id = str(uuid4())
    await create_news(state, message.from_user.id, news_id)
    await message.answer(f"{data['text']}\n"
                         f"\n"
                         f"{data['url']}")
    await bot.send_message(chat_id=control_add_chat,
                           text=f"Добавлен канал в NEWS\n"
                                f"\n"
                                f"ID: {message.from_user.id}\n"
                                f"{data['text']}\n"
                                f"\n"
                                f"{data['url']}\n",
                           reply_markup=delete_news_ikb(news_id))
    await message.answer("Все верно?",
                         reply_markup=confirm_add_news(news_id))
    await state.finish()


# STATES SEND MESSAGE
@dp.message_handler(lambda message : not message.photo
                                     and not message.text == 'Пропустить'
                                     and not message.text == '❌Отменить', state=AdminSendMessagesStatesGroup.photo)
async def check_load_photo_send_mess(message : types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['text', 'photo'], state=AdminSendMessagesStatesGroup.photo)
async def load_photo_send_mess(message : types.Message, state : FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['photo'] = ""
        await message.answer("Отправьте текст:",
                             reply_markup=ReplyKeyboardRemove())
        await AdminSendMessagesStatesGroup.next()
    elif message.text == '❌Отменить':
        await message.answer("Вы вернулись в админ меню:",
                             reply_markup=general_admin_kb())
        await state.finish()
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await message.answer("Отправьте текст:",
                             reply_markup=ReplyKeyboardRemove())
        await AdminSendMessagesStatesGroup.next()

@dp.message_handler(state=AdminSendMessagesStatesGroup.desc)
async def load_desc_send_mess(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer("Отправьте ссылку:",
                         reply_markup=info_from_bd("Пропустить"))
    await AdminSendMessagesStatesGroup.next()


@dp.message_handler(lambda message : not is_valid_url(message.text) and not message.text == 'Пропустить', state=AdminSendMessagesStatesGroup.link)
async def check_load_link_send_mess(message : types.Message):
    await message.answer('Отправьте ссылку!')

@dp.message_handler(state=AdminSendMessagesStatesGroup.link)
async def load_link_send_mess(message : types.Message, state : FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            data['link'] = ""
    else:
        async with state.proxy() as data:
            data['link'] = message.text
    post_id = str(uuid4())
    await create_send_mess(state, post_id, message.from_user.id)
    if not data['photo']:
        await message.answer(f"{data['desc']}\n"
                             f"\n"
                             f"{data['link']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['desc']}\n"
                                           f"\n"
                                           f"{data['link']}")
    await message.answer("Все верно?",
                         reply_markup=conf_add_send_mess_ikb(post_id))
    await state.finish()


# STATISTIC
@dp.message_handler(lambda message : not message.text.isdigit(), state=GetRandomUserStatesGroup.amount)
async def check_random_user(message : types.Message):
    await message.answer("Введите число!")

@dp.message_handler(state=GetRandomUserStatesGroup.amount)
async def get_random_user(message : types.Message, state : FSMContext):
    number = 1
    async with state.proxy() as data:
        data['amount'] = message.text
    if data['where'] == "clickers":
        click = await get_top_clickers(data['amount'])
        for data in click:
            try:
                user_chat = await bot.get_chat(data[0])
                await message.answer(f"#{number}\n"
                                     f"\n"
                                     f"Количество кликов: {data[7]}\n"
                                     f"\n"
                                     f"ID: {data[0]}\n"
                                     f"username: @{user_chat.username}")
                number +=1
            except:
                await message.answer(f"Чат #{number} не найден!")
                number +=1
    elif data['where'] == "fa":
        agents = await get_random_users(data['amount'], "info_player")
        for data in agents:
            user_chat = await bot.get_chat(data[0])
            await message.answer(f"#{number}\n"
                                 f"\n"
                                 f"ID: {data[0]}\n"
                                 f"username: @{user_chat.username}")
            number += 1
    elif data['where'] == "ft":
        agents = await get_random_users(data['amount'], "info_team")
        for data in agents:
            user_chat = await bot.get_chat(data[0])
            await message.answer(f"#{number}\n"
                                 f"\n"
                                 f"ID: {data[0]}\n"
                                 f"username: @{user_chat.username}")
    elif data['where'] == "youngfa":
        agents = await get_random_users(data['amount'], "young_player")
        for data in agents:
            user_chat = await bot.get_chat(data[0])
            await message.answer(f"#{number}\n"
                                 f"\n"
                                 f"ID: {data[0]}\n"
                                 f"username: @{user_chat.username}")
    elif data['where'] == "youngft":
        agents = await get_random_users(data['amount'], "young_team")
        for data in agents:
            user_chat = await bot.get_chat(data[0])
            await message.answer(f"#{number}\n"
                                 f"\n"
                                 f"ID: {data[0]}\n"
                                 f"username: @{user_chat.username}")
    await state.finish()