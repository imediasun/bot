from aiogram import types
from aiogram.dispatcher import FSMContext

from config import before_post_chat
from main import dp, bot
from hendlers import check_ban_user, cb_check_ban_user, is_valid_url, set_new_click

from keyboards import *
from youngkb import info_from_bd
from translations import _
from states import FreeagentStateGroup
from database.db import *

@dp.message_handler(lambda message: message.text == '👤Free agent')
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        await message.answer(_("Выберите действие:", lang),
                             reply_markup=free_agent_main_ikb(lang))


cb_words_list = ["add_agent", "search_agent", "yes_free_agent", "change_free_agent", "delete_free_agent", "next_agent",
                 "back_free_agent_main"]


@dp.callback_query_handler(lambda callback: callback.data in cb_words_list)
async def all_free_agent_callbacks(callback: types.CallbackQuery):
    global index
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if callback.data == 'add_agent':
            await set_new_click(callback.from_user.id)
            agent = await get_agent_profile(user_id)
            if not agent:
                await callback.message.answer(_("Укажите свой ник:", lang),
                                              reply_markup=cancel_kb(lang))
                await FreeagentStateGroup.nickname.set()
            else:
                await cb_info_free_agent(callback, agent)
                await callback.message.answer(_("Все верно?", lang),
                                              reply_markup=finish_agent_profile_kb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'search_agent':
            await set_new_click(callback.from_user.id)
            index = 0
            agent = await search_agent()
            if not agent:
                await callback.message.answer(_("Актуальных анкет нету!", lang),
                                              reply_markup=back_free_team_main_ikb(lang))
            else:
                await callback.message.answer(_("Все актуальные анкеты:", lang),
                                              reply_markup=ReplyKeyboardRemove())
                full_agent = list(agent)[index: index + 2]
                index += 2
                await cb_info_free_agent(callback, full_agent)
                if len(full_agent) < 2:
                    await callback.message.answer(_("Это все анкеты!", lang),
                                                  reply_markup=back_free_team_main_ikb(lang))
                else:
                    await callback.message.answer(_("Продолжить просмотр анкет?", lang),
                                                  reply_markup=next_agent_kb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'yes_free_agent':
            await set_new_click(callback.from_user.id)
            await callback.message.answer(_("Ваша анкета опубликована!", lang),
                                          reply_markup=send_agent_profil_ikb(lang))
            agent = await get_agent_profile(user_id)
            for data in agent:
                await bot.send_message(chat_id=before_post_chat,
                                       text=f"Free agent\n"
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
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'change_free_agent':
            await set_new_click(callback.from_user.id)
            nick = await get_nickname_agent(user_id=callback.message.chat.id)
            kb = ReplyKeyboardMarkup(resize_keyboard=True)
            btn = KeyboardButton(nick)
            kb.add(btn)
            await callback.message.answer(_("Укажите свой ник:", lang),
                                          reply_markup=kb)
            await FreeagentStateGroup.new_nickname.set()
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'delete_free_agent':
            await set_new_click(callback.from_user.id)
            await delete_profile(user_id=callback.message.chat.id)
            await callback.message.answer(_("Анкета успешно удалена!", lang),
                                          reply_markup=free_agent_main_ikb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'next_agent':
            await set_new_click(callback.from_user.id)
            agent = await search_agent()
            full_agent = list(agent)[index: index + 2]
            index += 2
            await cb_info_free_agent(callback, full_agent)
            if len(full_agent) < 2:
                await callback.message.answer(_("Это все анкеты!", lang),
                                              reply_markup=back_free_team_main_ikb(lang))
            else:
                await callback.message.answer(_("Продолжить просмотр анкет?", lang),
                                              reply_markup=next_agent_kb(lang))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'back_free_agent_main':
            await set_new_click(callback.from_user.id)
            await callback.message.answer(_("Вы в FREE AGENT меню:", lang),
                                          reply_markup=free_agent_main_ikb(lang))
            await callback.message.delete()
            await callback.answer()






@dp.message_handler(lambda message: len(message.text) > 15, state=FreeagentStateGroup.nickname)
async def check_nickname(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Nickname не должен прeвышать 15 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.nickname)
async def load_nick(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == f'❌{_("Отменить", lang)}':
        await set_new_click(message.from_user.id)
        await message.answer(_("Вы в FREE AGENT меню:", lang),
                             reply_markup=free_agent_main_ikb(lang))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['nickname'] = message.text
        await message.answer(_("Сколько вам лет?", lang))
        await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=FreeagentStateGroup.age)
async def check_age(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=FreeagentStateGroup.age)
async def load_age(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("На каком языке вы разговариваете?", lang),
                         reply_markup=choose_country_kb())
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=FreeagentStateGroup.teamspeak)
async def check_teamspeak(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=FreeagentStateGroup.teamspeak)
async def load_teamspeak(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data["teamspeak"] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await FreeagentStateGroup.next()


@dp.message_handler(state=FreeagentStateGroup.teamspeak1)
async def load_teamspeak1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    if message.text == _("Пропустить", lang):
        async with state.proxy() as data:
            data["teamspeak1"] = ""
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=ReplyKeyboardRemove())
        await FreeagentStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=ReplyKeyboardRemove())
        await FreeagentStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(lambda message: len(message.text) > 25, state=FreeagentStateGroup.device)
async def check_device(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не должно превышать 25 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.device)
async def load_device(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    await message.answer(_("Сколько турниров вы сыграли?", lang))
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=FreeagentStateGroup.tournament)
async def check_tournament(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)!", lang))


@dp.message_handler(state=FreeagentStateGroup.tournament)
async def load_tour(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['tournament'] = message.text
    await message.answer(_("Сколько финалов вы сыграли?", lang))
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 1000,
                    state=FreeagentStateGroup.finals)
async def check_finals(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)!", lang))


@dp.message_handler(state=FreeagentStateGroup.finals)
async def load_finals(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['finals'] = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(_("Не записываю", lang))
    kb.add(btn)
    await message.answer(_("Отправте ссылку на свои хайлайты:", lang),
                         reply_markup=kb)
    await FreeagentStateGroup.next()


@dp.message_handler(state=FreeagentStateGroup.highilights)
async def load_hl(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Не записываю", lang):
        async with state.proxy() as data:
            data['highilights'] = message.text
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        btn = KeyboardButton(_("Пропустить", lang))
        kb.add(btn)
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=kb)
        await FreeagentStateGroup.next()
    elif not is_valid_url(message.text):
        await message.answer(_("Отправьте ссылку!", lang))
    else:
        async with state.proxy() as data:
            data['highilights'] = message.text
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        btn = KeyboardButton(_("Пропустить", lang))
        kb.add(btn)
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=kb)
        await FreeagentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=FreeagentStateGroup.description)
async def check_desc(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.description)
async def load_desc(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data['description'] = text
    else:
        async with state.proxy() as data:
            data['description'] = message.text
    kb_username = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text=f"@{message.from_user.username}")
    kb_username.add(btn1)
    await message.answer(_("Укажите свой телеграм для связи:", lang),
                         reply_markup=kb_username)
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=FreeagentStateGroup.contact)
async def check_contact(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.contact)
async def load_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['contact'] = message.text
    await create_agent(message.from_user.id)
    await edit_agent(state, user_id)
    await send_free_agent_info(message, state)
    await state.finish()


# NEW
@dp.message_handler(lambda message: len(message.text) > 15, state=FreeagentStateGroup.new_nickname)
async def check_new_nickname(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Nickname не должен прeвышать 15 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_nickname)
async def load_new_nick(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == f'❌{_("Отменить", lang)}':
        await message.answer("Вы в FREE AGENT меню:",
                             reply_markup=free_agent_main_ikb(lang))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['nickname'] = message.text
        age = await get_age_agent(user_id=message.from_user.id)
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = KeyboardButton(age)
        kb.add(btn1)
        await message.answer(_("Сколько вам лет?", lang),
                             reply_markup=kb)
        await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=FreeagentStateGroup.new_age)
async def check_new_age(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_age)
async def load_new_age(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("На каком языке вы разговариваете?", lang),
                         reply_markup=choose_country_kb())
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=FreeagentStateGroup.new_teamspeak)
async def check_new_teamspeak(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_teamspeak)
async def load_new_teamspeak(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['teamspeak'] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await FreeagentStateGroup.next()


@dp.message_handler(state=FreeagentStateGroup.new_teamspeak1)
async def load_new_teamspeak1(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    device = await get_device_agent(user_id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    if message.text == _("Пропустить", lang):
        async with state.proxy() as data:
            data["teamspeak1"] = ""
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=info_from_bd(device))
        await FreeagentStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=info_from_bd(device))
        await FreeagentStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(lambda message: len(message.text) > 25, state=FreeagentStateGroup.new_device)
async def check_new_device(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не должно превышать 25 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_device)
async def load_new_device(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    tour = await get_tournament_agent(user_id=message.from_user.id)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(tour)
    kb.add(btn)
    await message.answer(_("Сколько турниров вы сыграли?", lang),
                         reply_markup=kb)
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=FreeagentStateGroup.new_tournament)
async def check_new_tournament(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_tournament)
async def load_new_tour(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['tournament'] = message.text
    finals = await get_finals_agent(user_id=message.from_user.id)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(finals)
    kb.add(btn)
    await message.answer(_("Сколько финалов вы сыграли?", lang),
                         reply_markup=kb)
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 1000,
                    state=FreeagentStateGroup.new_finals)
async def check_new_finals(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных турниров(использовать можно только цифры)!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_finals)
async def load_new_finals(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['finals'] = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(_("Оставить прошлую ссылку", lang))
    kb.add(btn)
    await message.answer(_("Отправте ссылку на свои хайлайты:", lang),
                         reply_markup=kb)
    await FreeagentStateGroup.next()


@dp.message_handler(state=FreeagentStateGroup.new_highilights)
async def load_new_hl(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Оставить прошлую ссылку", lang):
        text = await get_hl_agent(user_id=message.from_user.id)
        async with state.proxy() as data:
            data['highilights'] = text
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=desc_agent_kb(lang))
        await FreeagentStateGroup.next()
    elif not is_valid_url(message.text):
        await message.answer(_("Отправьте ссылку!", lang))
    else:
        async with state.proxy() as data:
            data['highilights'] = message.text
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=desc_agent_kb(lang))
        await FreeagentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=FreeagentStateGroup.new_description)
async def check_desc(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_description)
async def load_new_desc(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Оставить прошлый текст", lang):
        desc = await get_desc_agent(message.from_user.id)
        async with state.proxy() as data:
            data['description'] = desc
    else:
        async with state.proxy() as data:
            data['description'] = message.text
    kb_username = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text=f"@{message.from_user.username}")
    kb_username.add(btn1)
    await message.answer(_("Укажите свой телеграм для связи:", lang),
                         reply_markup=kb_username)
    await FreeagentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=FreeagentStateGroup.new_contact)
async def check_new_contact(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=FreeagentStateGroup.new_contact)
async def load_new_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['contact'] = message.text
    await edit_agent(state, user_id)
    await send_free_agent_info(message, state)
    await state.finish()


async def send_free_agent_info(message, state):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        await message.answer(_("Так выглядит ваша анкета:", lang),
                             reply_markup=ReplyKeyboardRemove())
        if not data['description']:
            await message.answer(f"Free agent\n"
                                 f"\n"
                                 f"Nickname: {data['nickname']}\n"
                                 f"Age: {data['age']}\n"
                                 f"Teamspeak: {data['teamspeak']} {data['teamspeak1']}\n"
                                 f"Device: {data['device']}\n"
                                 f"Tournament: {data['tournament']}\n"
                                 f"Finals: {data['finals']}\n"
                                 f"Highlights: {data['highilights']}\n"
                                 f"\n"
                                 f"{data['contact']}")
        else:
            await message.answer(f"Free agent\n"
                                 f"\n"
                                 f"Nickname: {data['nickname']}\n"
                                 f"Age: {data['age']}\n"
                                 f"Teamspeak: {data['teamspeak']} {data['teamspeak1']}\n"
                                 f"Device: {data['device']}\n"
                                 f"Tournament: {data['tournament']}\n"
                                 f"Finals: {data['finals']}\n"
                                 f"Highlights: {data['highilights']}\n"
                                 f"\n"
                                 f"{data['description']}\n"
                                 f"\n"
                                 f"{data['contact']}")
        await message.answer(_("Все верно?", lang),
                             reply_markup=finish_agent_profile_kb(lang))


async def cb_info_free_agent(callback, agent):
    for data in agent:
        if not data[9]:
            await callback.message.answer(f"Free agent\n"
                                          f"\n"
                                          f"Nickname: {data[1]}\n"
                                          f"Age: {data[2]}\n"
                                          f"Teamspeak: {data[3]} {data[4]}\n"
                                          f"Device: {data[5]}\n"
                                          f"Tournament: {data[6]}\n"
                                          f"Finals: {data[7]}\n"
                                          f"Highlights: {data[8]}\n"
                                          f"\n"
                                          f"{data[10]}",
                                          reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.answer(f"Free agent\n"
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
                                          f"{data[10]}",
                                          reply_markup=ReplyKeyboardRemove())
        return True
