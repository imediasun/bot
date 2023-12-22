from aiogram import types
from aiogram.dispatcher import FSMContext

from config import before_post_chat
from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp, bot

from keyboards import *
from youngkb import info_from_bd
from translations import _
from states import FreeteamStateGroup
from database.db import *
# user = types.User.id
# lang = get_user_lang(user)


@dp.message_handler(lambda message: message.text == '👥Free team')
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        await message.answer(_("Выберите действие:", lang),
                             reply_markup=free_team_main_ikb(lang))


cb_words_list = ["add_team", 'search_team', "yes_free_team", "change_free_team", "delete_free_team", "next_team",
                 "back_team_main"]

@dp.callback_query_handler(lambda callback: callback.data in cb_words_list)
async def all_free_agent_callbacks(callback: types.CallbackQuery):
    global index
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if callback.data == 'add_team':
            await set_new_click(callback.from_user.id)
            team = await get_team_profile(user_id)
            if not team:
                await callback.message.answer(_("Укажите название вашей команды:", lang),
                                              reply_markup=info_from_bd(f"❌{_('Отменить', lang)}"))
                await FreeteamStateGroup.team_name.set()
            else:
                await cb_info_free_team(callback, team)
                await callback.message.answer(_("Все верно?", lang),
                                              reply_markup=finish_team_profile_kb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'search_team':
            await set_new_click(callback.from_user.id)
            index = 0
            team = await select_team_profile()
            if not team:
                await callback.message.answer(_("Актуальных анкет нету!", lang))
            else:
                full_team = list(team)[index: index + 2]
                index += 2
                await callback.message.answer(_("Все актуальные анкеты:", lang),
                                              reply_markup=ReplyKeyboardRemove())
                await cb_info_free_team(callback, full_team)
                if len(full_team) < 2:
                    await callback.message.answer(_("Это все анкеты!", lang),
                                                  reply_markup=back_free_agent_main_ikb(lang))
                else:
                    await callback.message.answer(_("Продолжить просмотр анкет?", lang),
                                                  reply_markup=next_team_kb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'yes_free_team':
            await set_new_click(callback.from_user.id)
            await callback.message.answer(_("Ваша анкета опубликована!", lang),
                                          reply_markup=send_team_profile_kb(lang))
            team = await get_team_profile(user_id)
            for data in team:
                await bot.send_message(chat_id=before_post_chat,
                                       text=f"Free team\n"
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
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'change_free_team':
            await set_new_click(callback.from_user.id)
            team_name = await get_team_name(user_id=callback.message.chat.id)
            kb = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton(team_name)
            kb.add(btn1)
            await callback.message.answer(_("Укажите название команды:", lang),
                                          reply_markup=kb)
            await FreeteamStateGroup.new_team_name.set()
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'delete_free_team':
            await set_new_click(callback.from_user.id)
            await delete_team_profile(callback.message.chat.id)
            await callback.message.answer(_("Анкета успешно удалена!", lang),
                                          reply_markup=back_free_team_main_ikb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'next_team':
            await set_new_click(callback.from_user.id)
            team = await select_team_profile()
            full_team = list(team)[index: index + 2]
            index += 2
            await cb_info_free_team(callback, full_team)
            if len(full_team) < 2:
                await callback.message.answer(_("Это все анкеты!", lang),
                                              reply_markup=back_free_agent_main_ikb(lang))
            else:
                await callback.message.answer(_("Продолжить просмотр анкет?", lang),
                                              reply_markup=next_team_kb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'back_team_main':
            await set_new_click(callback.from_user.id)
            await callback.message.answer(_("Вы в FREE TEAM меню:", lang),
                                          reply_markup=free_team_main_ikb(lang))
            await callback.message.delete()
            await callback.answer()



@dp.message_handler(lambda message: len(message.text) > 30, state=FreeteamStateGroup.team_name)
async def check_nickname(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название команды не должно прeвышать 30 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.team_name)
async def load_team_name(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == f'❌{_("Отменить", lang)}':
        await set_new_click(message.from_user.id)
        await message.answer(_("Вы в FREE TEAM меню:", lang),
                             reply_markup=free_team_main_ikb(lang))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['team_name'] = message.text
        await message.answer(_("Укажите требования к возрасту игрока:", lang))
        await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=FreeteamStateGroup.age)
async def check_new_age(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=FreeteamStateGroup.age)
async def load_age1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("Каким языком должен владеть игрок?", lang),
                         reply_markup=choose_country_kb())
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=FreeteamStateGroup.teamspeak)
async def check_new_teamspeak(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=FreeteamStateGroup.teamspeak)
async def load_teamspeak1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['teamspeak'] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await FreeteamStateGroup.next()


@dp.message_handler(state=FreeteamStateGroup.teamspeak1)
async def load_teamspeak11(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    role = "Любая"
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data["teamspeak1"] = text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(role))
        await FreeteamStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(role))
        await FreeteamStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(lambda message: len(message.text) > 30, state=FreeteamStateGroup.role)
async def check_nickname(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Текст не должен превышать 30 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.role)
async def load_role1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['role'] = message.text
    await message.answer(_("Требования к девайсу игрока:", lang),
                         reply_markup=ReplyKeyboardRemove())
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 20, state=FreeteamStateGroup.device)
async def check_nickname(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не должно превышать 25 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.device)
async def load_device1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    await message.answer(_("Минимальный турнирный опыт?", lang))
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=FreeteamStateGroup.tournament)
async def check_new_tournament(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)", lang))


@dp.message_handler(state=FreeteamStateGroup.tournament)
async def load_tournament1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['tournament'] = message.text
    await message.answer(_("Минимальный опыт финалов?", lang))
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 1000,
                    state=FreeteamStateGroup.finals)
async def check_new_finals(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)!", lang))


@dp.message_handler(state=FreeteamStateGroup.finals)
async def load_finals1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['finals'] = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(_("Пропустить", lang))
    kb.add(btn)
    await message.answer(_("Расскажите что-то о состве или укажите какие-то дополнительные требования:", lang),
                         reply_markup=kb)
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=FreeteamStateGroup.description)
async def check_desc(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.description)
async def load_description1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data['description'] = text
    else:
        async with state.proxy() as data:
            data['description'] = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton(f"@{message.from_user.username}")
    kb.add(btn1)
    await message.answer(_("Укажите свой телеграм для связи:", lang),
                         reply_markup=kb)
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=FreeteamStateGroup.contact)
async def check_new_contact(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.contact)
async def load_contact1(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['contact'] = message.text
    await create_team_profile(user_id)
    await update_team_profile(state, user_id)
    await send_free_team_info(message, state)
    await state.finish()




# NEW
@dp.message_handler(lambda message: len(message.text) > 30, state=FreeteamStateGroup.new_team_name)
async def check_new_team_name1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название команды не должно прeвышать 30 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_team_name)
async def load_new_team_name1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == f'{_("Отменить", lang)}':
        await message.answer(_("Вы в FREE TEAM меню:", lang),
                             reply_markup=free_team_main_ikb(lang))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['team_name'] = message.text
        age = await get_age_team(user_id=message.from_user.id)
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = KeyboardButton(age)
        kb.add(btn1)
        await message.answer(_("Укажите требования к возрасту игрока:", lang),
                             reply_markup=kb)
        await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=FreeteamStateGroup.new_age)
async def check_new_age1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_age)
async def load_new_age1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("Каким языком должен владеть игрок?", lang),
                         reply_markup=choose_country_kb())
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=FreeteamStateGroup.new_teamspeak)
async def check_new_teamspeak1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_teamspeak)
async def load_new_teamspeak12(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['teamspeak'] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await FreeteamStateGroup.next()


@dp.message_handler(state=FreeteamStateGroup.new_teamspeak1)
async def load_new_teamspeak11(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    role = await get_role_team(message.from_user.id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data["teamspeak1"] = text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(role))
        await FreeteamStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(role))
        await FreeteamStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))



@dp.message_handler(lambda message: len(message.text) > 30, state=FreeteamStateGroup.new_role)
async def check_new_role1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Текст не должен превышать 30 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_role)
async def load_new_role1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['role'] = message.text
    device = await get_device_team(user_id=message.from_user.id)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(device)
    kb.add(btn1)
    await message.answer(_("Требования к девайсу игрока:", lang),
                         reply_markup=kb)
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 25, state=FreeteamStateGroup.new_device)
async def check_new_device1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не доллжно превышать 25 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_device)
async def load_new_device1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    tour = await get_tournament_team(user_id=message.from_user.id)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(tour)
    kb.add(btn1)
    await message.answer(_("Минимальный турнирный опыт?", lang),
                         reply_markup=kb)
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=FreeteamStateGroup.new_tournament)
async def check_new_tournament1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_tournament)
async def load_new_tournament1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['tournament'] = message.text
    finals = await get_finals_team(user_id=message.from_user.id)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(finals)
    kb.add(btn1)
    await message.answer(_("Минимальный опыт финалов?", lang),
                         reply_markup=kb)
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 1000,
                    state=FreeteamStateGroup.new_finals)
async def check_new_finals1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)!", lang))

@dp.message_handler(state=FreeteamStateGroup.new_finals)
async def load_new_finals1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['finals'] = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(_("Оставить прошлый текст",lang))
    kb.add(btn)
    await message.answer(_("Расскажите что-то о состве или укажите какие-то дополнительные требования:", lang),
                         reply_markup=kb)
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=FreeteamStateGroup.new_description)
async def check_new_desc1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_description)
async def load_new_description1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Оставить прошлый текст", lang):
        text = ""
        async with state.proxy() as data:
            data['description'] = text
    else:
        async with state.proxy() as data:
            data['description'] = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton(f"@{message.from_user.username}")
    kb.add(btn1)
    await message.answer(_("Укажите свой телеграм для связи:", lang),
                         reply_markup=kb)
    await FreeteamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 33, state=FreeteamStateGroup.new_contact)
async def check_new_contact1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=FreeteamStateGroup.new_contact)
async def load_new_contact1(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['contact'] = message.text
    await update_team_profile(state, user_id)
    await send_free_team_info(message, state)
    await state.finish()

async def send_free_team_info(message, state):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        await message.answer(_("Так выглядит ваша анкета:", lang),
                             reply_markup=ReplyKeyboardRemove())
        if not data['description']:
            await message.answer(text=f"Free team\n"
                                      f"\n"
                                      f"Team name: {data['team_name']}\n"
                                      f"\n"
                                      f"Критерии игрока👇\n"
                                      f"Age: {data['age']}+\n"
                                      f"TeamSpeak: {data['teamspeak']} {data['teamspeak1']}\n"
                                      f"Role: {data['role']}\n"
                                      f"Device: {data['device']}\n"
                                      f"Tournaments: {data['tournament']}\n"
                                      f"Finals: {data['finals']}\n"
                                      f"\n"
                                      f"{data['contact']}")
        else:
            await message.answer(text=f"Free team\n"
                                      f"\n"
                                      f"Team name: {data['team_name']}\n"
                                      f"\n"
                                      f"Критерии игрока👇\n"
                                      f"Age: {data['age']}+\n"
                                      f"TeamSpeak: {data['teamspeak']} {data['teamspeak1']}\n"
                                      f"Role: {data['role']}\n"
                                      f"Device: {data['device']}\n"
                                      f"Tournaments: {data['tournament']}\n"
                                      f"Finals: {data['finals']}\n"
                                      f"\n"
                                      f"{data['description']}\n"
                                      f"\n"
                                      f"{data['contact']}")
        await message.answer(_("Все верно?", lang),
                             reply_markup=finish_team_profile_kb(lang))


async def cb_info_free_team(callback, team):
    for data in team:
        if not data[9]:
            await callback.message.answer(f"Free team\n"
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
                                          f"{data[10]}")
        else:
            await callback.message.answer(f"Free team\n"
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
                                          f"{data[10]}")
        return True