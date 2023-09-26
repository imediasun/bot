from aiogram import types
from aiogram.dispatcher import FSMContext

from config import before_post_chat
from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp, bot

from database import *
from keyboards import *
from youngkb import *
from translations import _
from states import PracTeamStateGroup


@dp.message_handler(lambda message: message.text == '👥Free teamㅤ')
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        await message.answer(_("Выберите действие:", lang),
                             reply_markup=prac_team_main_ikb(lang))


cb_words_list = ["add_team_prac", "yes_prac_team", "change_prac_team", "delete_prac_team", "search_prac_team",
                 "next_prac_team"]

@dp.callback_query_handler(lambda callback: callback.data in cb_words_list)
async def all_free_agent_callbacks(callback: types.CallbackQuery):
    global index
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if callback.data == 'add_team_prac':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            team = await get_prac_team_profile(user_id)
            if not team:
                await callback.message.answer(_("Укажите название вашей команды:", lang),
                                              reply_markup=cancel_kb(lang))
                await PracTeamStateGroup.team_name.set()
            else:
                await cb_send_info_team(team, callback)
                await callback.message.answer(_("Все верно?", lang),
                                              reply_markup=finish_prac_team_ikb(lang))
            await callback.answer()
        elif callback.data == 'yes_prac_team':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            await callback.message.answer(_("Ваша анкета опубликована!", lang),
                                          reply_markup=send_prac_team_ikb(lang))
            team = await get_prac_team_profile(user_id)
            for data in team:
                await bot.send_message(chat_id=before_post_chat,
                                       text=f"Free prac team\n"
                                            f"\n"
                                            f"Team name: {data[1]}\n"
                                            f"\n"
                                            f"Критерии игрока👇\n"
                                            f"Age: {data[2]}+\n"
                                            f"TeamSpeak: {data[3]} {data[4]}\n"
                                            f"Role: {data[5]}\n"
                                            f"Device: {data[6]}\n"
                                            f"Practice games: {data[7]}\n"
                                            f"\n"
                                            f"{data[8]}\n"
                                            f"\n"
                                            f"{data[9]}\n"
                                            f"ID: {data[0]}",
                                       reply_markup=admin_edit_prac_user_team(data[0]))
            await callback.answer()
        elif callback.data == 'change_prac_team':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            team_name = await get_prac_team_name(user_id)
            await callback.message.answer(_("Укажите название вашей команды:", lang),
                                          reply_markup=info_from_bd(team_name))
            await PracTeamStateGroup.new_team_name.set()
            await callback.answer()
        elif callback.data == 'delete_prac_team':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            await delete_prac_team(user_id)
            await callback.message.answer(_("Анкета успешно удалена!", lang),
                                          reply_markup=main_young_menu_ikb(lang))
            await callback.answer()
        elif callback.data == 'search_prac_team':
            await set_new_click(callback.from_user.id)
            index = 0
            await callback.message.delete()
            team = await get_all_prac_team()
            if not team:
                await callback.message.answer(_("На данный момент анкет нету!", lang),
                                              reply_markup=back_young_main_kb(lang))
            else:
                all_team = list(team)[index: index + 2]
                index += 2
                await callback.message.answer(_("Все актуальные анкеты:", lang))
                await cb_send_info_team(team, callback)
                if len(all_team) < 2:
                    await callback.message.answer(_("Это все анкеты!", lang),
                                                  reply_markup=back_young_main_kb(lang))
                else:
                    await callback.message.answer(_("Продолжить просмотр анкет?", lang),
                                                  reply_markup=next_prac_team(lang))
            await callback.answer()
        elif callback.data == 'next_prac_team':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            team = await get_all_prac_team()
            all_team = list(team)[index: index + 2]
            index += 2
            await cb_send_info_team(team, callback)
            if len(all_team) < 2:
                await callback.message.answer(_("Это все анкеты!", lang),
                                              reply_markup=back_young_main_kb(lang))
            else:
                await callback.message.answer(_("Это все анкеты!", lang),
                                              reply_markup=next_prac_team(lang))
            await callback.answer()




@dp.message_handler(lambda message: len(message.text) > 30, state=PracTeamStateGroup.team_name)
async def check_nickname_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название команды не должно прeвышать 30 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.team_name)
async def load_team_name_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == f'❌{_("Отменить", lang)}':
        await set_new_click(message.from_user.id)
        await message.answer(_("Вы вернулись в главное меню:", lang),
                             reply_markup=main_young_menu_ikb(lang))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['team_name'] = message.text
        await message.answer(_("Укажите требования к возрасту игрока:", lang))
        await PracTeamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=PracTeamStateGroup.age)
async def check_new_age_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=PracTeamStateGroup.age)
async def load_age1_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("Каким языком должен владеть игрок?", lang),
                         reply_markup=choose_country_kb())
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=PracTeamStateGroup.teamspeak)
async def check_prac_teamspeak_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=PracTeamStateGroup.teamspeak)
async def load_teamspeak1_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['teamspeak'] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await PracTeamStateGroup.next()


@dp.message_handler(state=PracTeamStateGroup.teamspeak1)
async def load_teamspeak11_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data["teamspeak1"] = text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(_("Любая", lang)))
        await PracTeamStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(_("Любая", lang)))
        await PracTeamStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))



@dp.message_handler(lambda message: len(message.text) > 30, state=PracTeamStateGroup.role)
async def check_role_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Текст не должен превышать 30 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.role)
async def load_role1_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['role'] = message.text
    await message.answer(_("Требования к девайсу игрока:", lang),
                         reply_markup=ReplyKeyboardRemove())
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 20, state=PracTeamStateGroup.device)
async def check_prac_device_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не доллжно превышать 20 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.device)
async def load_prac_device1_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    await message.answer(_("Минимальный опыт праков?", lang))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=PracTeamStateGroup.practice_games)
async def check_prac_games_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных праков(только цифры)!", lang))


@dp.message_handler(state=PracTeamStateGroup.practice_games)
async def load_prac_games_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['practice_games'] = message.text
    await message.answer(_("Расскажите что-то о состве или укажите какие-то дополнительные требования.", lang),
                         reply_markup=info_from_bd(_("Пропустить", lang)))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=PracTeamStateGroup.description)
async def check_prac_desc_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.description)
async def load_prac_description1_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data['description'] = text
    else:
        async with state.proxy() as data:
            data['description'] = message.text
    text = f"@{message.from_user.username}"
    await message.answer(_("Укажите свой телеграм для связи:", lang),
                         reply_markup=info_from_bd(text))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=PracTeamStateGroup.contact)
async def check_prac_contact_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.contact)
async def load_prac_contact1_team(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    async with state.proxy() as data:
        data['contact'] = message.text
    await create_prac_team(user_id)
    await edit_prac_team(state, user_id)
    await message.answer(_("Так выглядит ваша анкета:", lang))
    await send_info_team(data, message)
    await message.answer(_("Все верно?", lang),
                         reply_markup=finish_prac_team_ikb(lang))
    await state.finish()


@dp.message_handler(lambda message: len(message.text) > 30, state=PracTeamStateGroup.new_team_name)
async def check_new_prac_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название команды не должно прeвышать 30 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_team_name)
async def load_new_prac_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['team_name'] = message.text
    age = await get_prac_age_team(message.from_user.id)
    await message.answer(_("Укажите требования к возрасту игрока:", lang),
                         reply_markup=info_from_bd(age))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=PracTeamStateGroup.new_age)
async def check_new_prac_age_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_age)
async def load_new_prac_age_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("Каким языком должен владеть игрок?", lang),
                         reply_markup=choose_country_kb())
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=PracTeamStateGroup.new_teamspeak)
async def check_new_teamspeak_prac_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_teamspeak)
async def load_new_teamspeak_prac_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['teamspeak'] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await PracTeamStateGroup.next()


@dp.message_handler(state=PracTeamStateGroup.new_teamspeak1)
async def load_new_teamspeak1_prac_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    role = await get_prac_role_team(message.from_user.id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data["teamspeak1"] = text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(role))
        await PracTeamStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите на какую роль вам нужен игрок:", lang),
                             reply_markup=info_from_bd(role))
        await PracTeamStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(lambda message: len(message.text) > 30, state=PracTeamStateGroup.new_role)
async def check_new_role1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Текст не должен превышать 30 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_role)
async def load_new_role_prac_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['role'] = message.text
    device = await get_prac_device_team(message.from_user.id)
    await message.answer(_("Укажите требования к девайсу игрока:", lang),
                         reply_markup=info_from_bd(device))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 25, state=PracTeamStateGroup.new_device)
async def check_new_device_prac_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не доллжно превышать 25 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_device)
async def load_new_device_prac_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    pracs = await get_prac_game_team(message.from_user.id)
    await message.answer(_("Минимальный опыт праков?", lang),
                         reply_markup=info_from_bd(pracs))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=PracTeamStateGroup.new_practice_games)
async def check_new_prac_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных праков(только цифры)!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_practice_games)
async def load_new_prac_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['practice_games'] = message.text
    await message.answer(_("Расскажите что-то о состве или укажите какие-то дополнительные требования.", lang),
                         reply_markup=info_from_bd(_("Оставить прошлый текст", lang)))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=PracTeamStateGroup.new_description)
async def check_new_desc_prac_team(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_description)
async def load_new_desc_prac_team(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Оставить прошлый текст", lang):
        text = ""
        async with state.proxy() as data:
            data['description'] = text
    else:
        async with state.proxy() as data:
            data['description'] = message.text
    text = f"@{message.from_user.username}"
    await message.answer(_("Укажите свой телеграм для связи:", lang),
                         reply_markup=info_from_bd(text))
    await PracTeamStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 33, state=PracTeamStateGroup.new_contact)
async def check_new_contact1(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=PracTeamStateGroup.new_contact)
async def load_new_contact1(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    async with state.proxy() as data:
        data['contact'] = message.text
    await edit_prac_team(state, user_id)
    await message.answer(_("Так выглядит ваша анкета:", lang))
    await send_info_team(data, message)
    await message.answer(_("Все верно?", lang),
                         reply_markup=finish_prac_team_ikb(lang))
    await state.finish()


async def send_info_team(data, message):
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
                                  f"Practice games: {data['practice_games']}\n"
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
                                  f"Practice games: {data['practice_games']}\n"
                                  f"\n"
                                  f"{data['description']}\n"
                                  f"\n"
                                  f"{data['contact']}")


async def cb_send_info_team(team, callback):
    for data in team:
        if not data[8]:
            await callback.message.answer(f"Free team\n"
                                          f"\n"
                                          f"Team name: {data[1]}\n"
                                          f"\n"
                                          f"Критерии игрока👇\n"
                                          f"Age: {data[2]}\n"
                                          f"Teamspeak: {data[3]} {data[4]}\n"
                                          f"Role: {data[5]}\n"
                                          f"Device: {data[6]}\n"
                                          f"Practice games: {data[7]}\n"
                                          f"\n"
                                          f"{data[9]}",
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(f"Free team\n"
                                          f"\n"
                                          f"Team name: {data[1]}\n"
                                          f"\n"
                                          f"Критерии игрока👇\n"
                                          f"Age: {data[2]}\n"
                                          f"Teamspeak: {data[3]} {data[4]}\n"
                                          f"Role: {data[5]}\n"
                                          f"Device: {data[6]}\n"
                                          f"Practice games: {data[7]}\n"
                                          f"\n"
                                          f"{data[8]}\n"
                                          f"\n"
                                          f"{data[9]}",
                                          reply_markup=ReplyKeyboardRemove())