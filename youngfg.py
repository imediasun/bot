from aiogram import types
from aiogram.dispatcher import FSMContext

from config import before_post_chat
from hendlers import cb_check_ban_user, check_ban_user, is_valid_url, set_new_click
from main import dp, bot

from database import *
from keyboards import *
from youngkb import *
from translations import _
from states import PracAgentStateGroup



@dp.message_handler(lambda message: message.text == '👤Free agentㅤ')
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        await message.answer(_("Выберите действие:", lang),
                             reply_markup=prac_agent_main_ikb(lang))


cb_words_list = ["add_agent_prac", "yes_prac_agent", "change_prac_agent", "delete_prac_agent",
                 "search_prac_agent", "next_prac_agent"]

@dp.callback_query_handler(lambda callback: callback.data in cb_words_list)
async def all_free_agent_callbacks(callback: types.CallbackQuery):
    global index
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if callback.data == 'add_agent_prac':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            agent = await get_prac_agent_profile(user_id)
            if not agent:
                await callback.message.answer(_("Укажите свой ник:", lang),
                                              reply_markup=cancel_kb(lang))
                await PracAgentStateGroup.nickname.set()
            else:
                await cb_send_free_agent_info(agent, callback)
                await callback.message.answer(_("Все верно?", lang),
                                              reply_markup=finish_prac_agent_ikb(lang))
            await callback.answer()
        elif callback.data == 'yes_prac_agent':
            await set_new_click(callback.from_user.id)
            await callback.message.answer(_("Ваша анкета опубликована!", lang),
                                          reply_markup=send_prac_agent_ikb(lang))
            agent = await get_prac_agent_profile(user_id)
            for data in agent:
                await bot.send_message(chat_id=before_post_chat,
                                       text=f"Free prac agent\n"
                                            f"\n"
                                            f"Nickname: {data[1]}\n"
                                            f"Age: {data[2]}\n"
                                            f"Teamspeak: {data[3]} {data[4]}\n"
                                            f"Device: {data[5]}\n"
                                            f"Practice games: {data[6]}\n"
                                            f"Highlights: {data[7]}\n"
                                            f"\n"
                                            f"{data[8]}\n"
                                            f"\n"
                                            f"{data[9]}\n"
                                            f"ID: {user_id}",
                                       reply_markup=admin_prac_edit_user(user_id))
            await callback.message.delete()
            await callback.answer()
        elif callback.data == 'change_prac_agent':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            nick = await get_nickname_prac_agent(user_id)
            await callback.message.answer(_("Укажите свой ник:", lang),
                                          reply_markup=info_from_bd(nick))
            await PracAgentStateGroup.new_nickname.set()
            await callback.answer()
        elif callback.data == 'delete_prac_agent':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            await delete_prac_agent_profile(user_id)
            await callback.message.answer(_("Анкета успешно удалена!", lang),
                                          reply_markup=main_young_menu_ikb(lang))
            await callback.answer()
        elif callback.data == 'search_prac_agent':
            index = 0
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            agent = await get_all_prac_agent()
            if not agent:
                await callback.message.answer(_("Актуальных анкет нету!", lang),
                                              reply_markup=back_young_main_kb(lang))
            else:
                all_agent = list(agent)[index: index + 2]
                index += 2
                await callback.message.answer(_("Все актуальные анкеты:", lang))
                await cb_send_free_agent_info(all_agent, callback)
                if len(all_agent) < 2:
                    await callback.message.answer(_("Это все анкеты!", lang),
                                                  reply_markup=back_young_main_kb(lang))
                else:
                    await callback.message.answer(_("Продолжить просмотр анкет?", lang),
                                                  reply_markup=next_prac_agent(lang))
            await callback.answer()
        elif callback.data == 'next_prac_agent':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            agent = await get_all_prac_agent()
            all_agent = list(agent)[index: index + 2]
            index += 2
            #
            if len(all_agent) < 2:
                await callback.message.answer(_("Это все анкеты!", lang),
                                              reply_markup=back_young_main_kb(lang))
            else:
                await callback.message.answer(_("Продолжить просмотр анкет?", lang),
                                              reply_markup=next_prac_agent(lang))
            await callback.answer()




@dp.message_handler(lambda message: len(message.text) > 15, state=PracAgentStateGroup.nickname)
async def check_prac_nickname(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Nickname не должен прeвышать 15 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.nickname)
async def load_prac_nick(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == f'❌{_("Отменить", lang)}':
        await set_new_click(message.from_user.id)
        await message.answer("Вы вернулись в главное меню:",
                             reply_markup=main_young_menu_ikb(lang))
        await state.finish()
    else:
        async with state.proxy() as data:
            data['nickname'] = message.text
        await message.answer(_("Сколько вам лет?", lang))
        await PracAgentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=PracAgentStateGroup.age)
async def check_prac_age(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=PracAgentStateGroup.age)
async def load_prac_age(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("На каком языке вы разговариваете?", lang),
                         reply_markup=choose_country_kb())
    await PracAgentStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=PracAgentStateGroup.teamspeak)
async def check_prac_teamspeak(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=PracAgentStateGroup.teamspeak)
async def load_prac_teamspeak(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data["teamspeak"] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await PracAgentStateGroup.next()


@dp.message_handler(state=PracAgentStateGroup.teamspeak1)
async def load_prac_teamspeak1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    if message.text == _("Пропустить", lang):
        async with state.proxy() as data:
            data["teamspeak1"] = ""
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=ReplyKeyboardRemove())
        await PracAgentStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=ReplyKeyboardRemove())
        await PracAgentStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(lambda message: len(message.text) > 25, state=PracAgentStateGroup.device)
async def check_prac_device(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не должно превышать 25 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.device)
async def load_prac_device(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    await message.answer(_("Сколько праков вы сыграли?", lang))
    await PracAgentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=PracAgentStateGroup.practice_games)
async def check_prac(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных праков(только цифры)!", lang))


@dp.message_handler(state=PracAgentStateGroup.practice_games)
async def load_prac(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['practice_games'] = message.text
    await message.answer(_('Отправте ссылку на свои хайлайты:', lang),
                         reply_markup=info_from_bd(_("Не записываю", lang)))
    await PracAgentStateGroup.next()


@dp.message_handler(state=PracAgentStateGroup.highilights)
async def load_prac_hl(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Не записываю", lang):
        async with state.proxy() as data:
            data['highilights'] = message.text
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=info_from_bd(_("Пропустить", lang)))
        await PracAgentStateGroup.next()
    elif not is_valid_url(message.text):
        await message.answer(_("Отправьте ссылку!", lang))
    else:
        async with state.proxy() as data:
            data['highilights'] = message.text
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=info_from_bd(_("Пропустить", lang)))
        await PracAgentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=PracAgentStateGroup.description)
async def check_prac_desc(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.description)
async def load_prac_desc(message: types.Message, state: FSMContext):
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
    await PracAgentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=PracAgentStateGroup.contact)
async def check_prac_contact(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.contact)
async def load_prac_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['contact'] = message.text
    await create_prac_agent(user_id)
    await edit_prac_agent(state, user_id)
    await send_free_agent_info(message, state)
    await state.finish()


# NEW
@dp.message_handler(lambda message: len(message.text) > 15, state=PracAgentStateGroup.new_nickname)
async def check_new_prac_nickname(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Nickname не должен прeвышать 15 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.new_nickname)
async def load_new_prac_nick(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['nickname'] = message.text
    age = await get_age_prac_agent(message.from_user.id)
    await message.answer(_("Сколько вам лет?", lang),
                         reply_markup=info_from_bd(age))
    await PracAgentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 100,
                    state=PracAgentStateGroup.new_age)
async def check_new_prac_age(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящий возраст(только цифры)!", lang))


@dp.message_handler(state=PracAgentStateGroup.new_age)
async def load_new_prac_age(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['age'] = message.text
    await message.answer(_("На каком языке вы разговариваете?", lang),
                         reply_markup=choose_country_kb())
    await PracAgentStateGroup.next()


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == 'Қазақ'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Türkçe', state=PracAgentStateGroup.new_teamspeak)
async def check_new_prac_teamspeak(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=PracAgentStateGroup.new_teamspeak)
async def load_new_prac_teamspeak(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data["teamspeak"] = message.text
    await message.answer(_("Пожеланию можете указать дополнительный язык:", lang),
                         reply_markup=choose_teamspeak_kb(lang))
    await PracAgentStateGroup.next()


@dp.message_handler(state=PracAgentStateGroup.new_teamspeak1)
async def load_new_prac_teamspeak1(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    device = await get_device_prac_agent(message.from_user.id)
    lang_list = ["Українська", "English", "Русский", "Қазақ", "O'zbek", "Türkçe"]
    if message.text == _("Пропустить", lang):
        text = ""
        async with state.proxy() as data:
            data["teamspeak1"] = text
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=info_from_bd(device))
        await PracAgentStateGroup.next()
    elif message.text in lang_list:
        async with state.proxy() as data:
            data["teamspeak1"] = message.text
        await message.answer(_("Укажите название своего девайса:", lang),
                             reply_markup=info_from_bd(device))
        await PracAgentStateGroup.next()
    else:
        await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(lambda message: len(message.text) > 20, state=PracAgentStateGroup.new_device)
async def check_new_prac_device(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Название девайса не должно превышать 25 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.new_device)
async def load_new_prac_device(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['device'] = message.text
    pracs = await get_amount_prac_agent(message.from_user.id)
    await message.answer(_("Сколько праков вы сыграли?", lang),
                         reply_markup=info_from_bd(pracs))
    await PracAgentStateGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 10000,
                    state=PracAgentStateGroup.new_practice_games)
async def check_new_prac(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Укажите настоящие количество сиграных праков(только цифры)!", lang))


@dp.message_handler(state=PracAgentStateGroup.new_practice_games)
async def load_new_prac(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        data['practice_games'] = message.text
    await message.answer(_("Отправте ссылку на свои хайлайты:", lang),
                         reply_markup=info_from_bd(_("Оставить прошлую ссылку", lang)))
    await PracAgentStateGroup.next()


@dp.message_handler(state=PracAgentStateGroup.new_highilights)
async def load_new_prac_hl(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    hl = await get_hl_prac_agent(message.from_user.id)
    if message.text == _("Оставить прошлую ссылку", lang):
        async with state.proxy() as data:
            data['highilights'] = hl
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=info_from_bd(_("Оставить прошлый текст", lang)))
        await PracAgentStateGroup.next()
    elif not is_valid_url(message.text):
        await message.answer(_("Отправьте ссылку!", lang))
    else:
        async with state.proxy() as data:
            data['highilights'] = message.text
        await message.answer(_("Расскажите о себе, своих планах на игру, в каких командах играли.", lang),
                             reply_markup=info_from_bd(_("Оставить прошлый текст", lang)))
        await PracAgentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 100, state=PracAgentStateGroup.new_description)
async def check_new_prac_desc(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваше сообщение не должно превышать 100 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.new_description)
async def load_new_prac_desc(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    if message.text == _("Оставить прошлый текст", lang):
        desc = await get_desc_prac_agent(message.from_user.id)
        async with state.proxy() as data:
            data['description'] = desc
    else:
        async with state.proxy() as data:
            data['description'] = message.text
    text = f"@{message.from_user.username}"
    await message.answer(_("Укажите свой телеграм для связи:", lang),
                         reply_markup=info_from_bd(text))
    await PracAgentStateGroup.next()


@dp.message_handler(lambda message: len(message.text) > 40, state=PracAgentStateGroup.new_contact)
async def check_new_prac_contact(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Ваш ник не должен превышать 40 символов!", lang))


@dp.message_handler(state=PracAgentStateGroup.new_contact)
async def load_new_prac_contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['contact'] = message.text
    await edit_prac_agent(state, user_id)
    await send_free_agent_info(message, state)
    await state.finish()


async def cb_send_free_agent_info(all_agent, callback):
    for data in all_agent:
        if not data[8]:
            await callback.message.answer(f"Free agent\n"
                                          f"\n"
                                          f"Nickname: {data[1]}\n"
                                          f"Age: {data[2]}\n"
                                          f"Teamspeak: {data[3]} {data[4]}\n"
                                          f"Device: {data[5]}\n"
                                          f"Practice games: {data[6]}\n"
                                          f"Highlights: {data[7]}\n"
                                          f"\n"
                                          f"{data[9]}")
        else:
            await callback.message.answer(f"Free agent\n"
                                          f"\n"
                                          f"Nickname: {data[1]}\n"
                                          f"Age: {data[2]}\n"
                                          f"Teamspeak: {data[3]} {data[4]}\n"
                                          f"Device: {data[5]}\n"
                                          f"Practice games: {data[6]}\n"
                                          f"Highlights: {data[7]}\n"
                                          f"\n"
                                          f"{data[8]}\n"
                                          f"\n"
                                          f"{data[9]}")


async def send_free_agent_info(message, state):
    lang = await get_user_lang(message.from_user.id)
    async with state.proxy() as data:
        await message.answer(_("Так выглядит ваша анкета:", lang))
        if not data['description']:
            await message.answer(f"Free agent\n"
                                 f"\n"
                                 f"Nickname: {data['nickname']}\n"
                                 f"Age: {data['age']}\n"
                                 f"Teamspeak: {data['teamspeak']} {data['teamspeak1']}\n"
                                 f"Device: {data['device']}\n"
                                 f"Practice games: {data['practice_games']}\n"
                                 f"Highlights: {data['highilights']}\n"
                                 f"\n"
                                 f"{data['contact']}",
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(f"Free agent\n"
                                 f"\n"
                                 f"Nickname: {data['nickname']}\n"
                                 f"Age: {data['age']}\n"
                                 f"Teamspeak: {data['teamspeak']} {data['teamspeak1']}\n"
                                 f"Device: {data['device']}\n"
                                 f"Practice games: {data['practice_games']}\n"
                                 f"Highlights: {data['highilights']}\n"
                                 f"\n"
                                 f"{data['description']}\n"
                                 f"\n"
                                 f"{data['contact']}",
                                 reply_markup=ReplyKeyboardRemove())
        await message.answer(_("Все верно?", lang),
                             reply_markup=finish_prac_agent_ikb(lang))