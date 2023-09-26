from urllib.parse import urlparse
from aiogram import types
from aiogram.dispatcher import FSMContext

from main import dp

from database import *
from keyboards import *
from youngkb import main_young_menu_ikb
from states import *
from translations import _


@dp.message_handler(commands=['start'])
async def cd_start(message: types.Message):
    user_id = message.from_user.id
    ban = await check_ban_user(message)
    await insert_time_log(user_id)
    if not ban:
        await message.answer("Привет!\n"
                             "Выбери язык👇\n"
                             "\n"
                             "Hello!\n"
                             "Choose languege👇",
                             reply_markup=choose_country_kb())
        await LanguageStateGroup.language.set()
        await create_lang(user_id)


@dp.message_handler(lambda message: not message.text == 'Українська'
                                    and not message.text == 'English'
                                    and not message.text == 'Русский'
                                    and not message.text == "O'zbek"
                                    and not message.text == 'Қазақ'
                                    and not message.text == 'Türkçe',
                    state=LanguageStateGroup.language)
async def check_lang(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=LanguageStateGroup.language)
async def load_lang(message: types.Message, state: FSMContext):
    global lang_code, lang
    if message.text == 'Українська':
        lang_code = 'uk_UAH'
    elif message.text == 'English':
        lang_code = 'en_USD'
    elif message.text == 'Русский':
        lang_code = 'ru_RUB'
    elif message.text == "O'zbek":
        lang_code = 'uz_UZS'
    elif message.text == 'Қазақ':
        lang_code = 'kz_KZT'
    elif message.text == 'Türkçe':
        lang_code = 'tr_TRY'
    async with state.proxy() as data:
        data['language'] = lang_code.split('_')[-2]
    currency = lang_code.split('_')[-1]
    await edit_lang(state, currency, user_id=message.from_user.id)
    lang = await get_user_lang(message.from_user.id)
    await message.answer(f"{_('Пожалуйста, выберите тип аккаунта', lang)}:\n"
                         f"👶Young player - {_('для начинающих игроков которые играют праки/паблик', lang)}.\n"
                         f"👨PRO player - {_('для тех, кто играет турниры', lang)}.\n"
                         f"\n"
                         f"❗️{_('Вы можете сменить тип аккаунта в любое время', lang)}:\n"
                         f"👶Young player - {_('используйте команду', lang)} /player\n"
                         f"👨PRO player - {_('используйте команду', lang)} /proplayer",
                         reply_markup=choose_type_akk())
    await LanguageStateGroup.next()


@dp.message_handler(lambda message: not message.text == '👨PRO player'
                                    and not message.text == '👶Young player', state=LanguageStateGroup.profile)
async def check_profile(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    await message.answer(_("Такого варианта ответа нету!", lang))


@dp.message_handler(state=LanguageStateGroup.profile)
async def load_profile(message: types.Message, state: FSMContext):
    global profile_code
    lang = await get_user_lang(message.from_user.id)
    await set_new_click(message.from_user.id)
    if message.text == '👨PRO player':
        profile_code = 'pro'
        await message.answer(f"{_('Ваш', lang)} ID: {message.chat.id}\n"
                             f"{_('Что вас интересует', lang)}?",
                             reply_markup=main_menu_kb(lang))
    elif message.text == '👶Young player':
        await message.answer(f"{_('Ваш', lang)} ID: {message.chat.id}\n"
                             f"{_('Что вас интересует', lang)}?",
                             reply_markup=main_young_menu_ikb(lang))
        profile_code = 'young'
    async with state.proxy() as data:
        data['profile'] = profile_code
    await update_profile(profile_code, message.from_user.id)
    await state.finish()


@dp.message_handler(commands=['getchatid'])
async def cd_get_chat_id(message: types.Message):
    await message.answer(f"ID данного чата: {message.chat.id}")


# CheckUser
@dp.message_handler(commands=['checkuser'])
async def cd_check_user(message: types.Message):
    await message.answer("Отправьте ID юзера:")
    await CheckUserStatesGroup.user_id.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=CheckUserStatesGroup.user_id)
async def check_load_user_id(message: types.Message):
    await message.answer("Введите ID!")


@dp.message_handler(state=CheckUserStatesGroup.user_id)
async def load_check_user_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
    user = await get_user_lang(data['user_id'])
    if not user:
        await message.answer("Данного пользователя нету в базе!")
    else:
        await message.answer("Данный пользователь есть в базе!")
    await state.finish()


@dp.message_handler(commands=['player'])
async def cd_player(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(message.from_user.id)
    if not ban:
        await message.answer(f"{_('Ваш', lang)} ID: {message.from_user.id}\n"
                             f"{_('Что вас интересует', lang)}?",
                             reply_markup=main_young_menu_ikb(lang))
        await update_profile("young", message.from_user.id)


@dp.message_handler(commands=['proplayer'])
async def cd_pro_player(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(message.from_user.id)
    if not ban:
        await message.answer(f"{_('Твой', lang)} ID: {message.chat.id}\n"
                             f"{_('Что вас интересует', lang)}?",
                             reply_markup=main_menu_kb(lang))
        await update_profile("pro", message.from_user.id)


@dp.message_handler(commands=['finish'], state='*')
async def cd_finish(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message.from_user.id)
    await set_new_click(message.from_user.id)
    await message.answer(f"{_('Пожалуйста, выберите тип аккаунта', lang)}:\n"
                         f"👶Young player - {_('используйте команду', lang)} /player\n"
                         f"👨PRO player - {_('используйте команду', lang)} /proplayer")
    await state.finish()


# NEWS
@dp.message_handler(lambda message: message.text == "🔥NEWS")
async def news_text(message: types.Message):
    global index
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(message.from_user.id)
    if not ban:
        all_news = await get_all_news()
        profile = await get_profile(message.from_user.id)
        if not all_news:
            await message.answer(_("На данный момент эта функция недоступна!", lang))
        else:
            news_kb = InlineKeyboardMarkup()
            for data in all_news:
                btn1 = InlineKeyboardButton(text=data[2],
                                            url=data[3])
                news_kb.add(btn1)
            if profile == 'pro':
                back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_main_menu")
                news_kb.add(back)
            elif profile == 'young':
                back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data="back_young_main")
                news_kb.add(back)
            if len(all_news) < 2:
                await message.answer(_("Наш телеграм канал с актуальными новостями:", lang),
                                     reply_markup=news_kb)
            else:
                await message.answer(_("Наши телеграм каналы с актуальными новостями:", lang),
                                     reply_markup=news_kb)


def is_valid_url(text):
    parsed = urlparse(text)
    return bool(parsed.scheme and parsed.netloc)


async def check_ban_user(message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    block = await get_block_user(user_id)
    reason = await get_reason_user(user_id)
    ban_time = await get_ban_time_user(user_id)
    if block == 1:
        await message.answer(f"{_('Вы заблокированы в боте!', lang)}\n"
                             f"{_('Причина', lang)}: {reason}\n"
                             f"{_('Срок бана', lang)}: {ban_time}\n"
                             f"{_('Ваш', lang)} ID: {message.from_user.id}")
        return True


async def cb_check_ban_user(callback):
    user_id = callback.from_user.id
    lang = await get_user_lang(user_id)
    block = await get_block_user(user_id)
    reason = await get_reason_user(user_id)
    ban_time = await get_ban_time_user(user_id)
    if block == 1:
        await callback.message.answer(f"{_('Вы заблокированы в боте!', lang)}\n"
                                      f"{_('Причина', lang)}: {reason}\n"
                                      f"{_('Срок бана', lang)}: {ban_time}\n"
                                      f"{_('Ваш', lang)} ID: {user_id}")
        await callback.answer()
        return True


async def set_new_click(user_id):
    amount_click = await get_amount_click(user_id)
    if not amount_click:
        await update_click(1, user_id)
    else:
        new_amount_click = amount_click + 1
        await update_click(new_amount_click, user_id)
