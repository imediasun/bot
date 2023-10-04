from aiogram import types
from aiogram.dispatcher import FSMContext
import requests
from bs4 import BeautifulSoup
from time import time

from main import dp, bot
from config import *
from hendlers import cb_check_ban_user, check_ban_user

from database import *
from keyboards import *
from youngkb import *
from states import AddCurrencyStatesGroup, AdminPayStatesGroup



@dp.message_handler(lambda message: message.text == "💳PAYMENTS")
async def all_text(message: types.Message):
    user_id = message.from_user.id
    admin_id = await get_admin_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if user_id in admin_id:
            await message.answer("Выберите действие:",
                                 reply_markup=admin_add_pay())


cb_words_list = ["confirm_add_card", "check_pay", "update_currency", "check_currency", "add_currency",
                 "confirm_add_currency"]

@dp.callback_query_handler(lambda callback : callback.data in cb_words_list)
async def all_callbacks(callback : types.CallbackQuery):
    ban = await cb_check_ban_user(callback)
    if not ban:
        if callback.data == 'confirm_add_card':
            await callback.message.delete()
            await callback.message.answer("✅Карта успешно добавлена!",
                                          reply_markup=general_admin_kb())
            await callback.answer()
        elif callback.data == 'check_pay':
            await callback.message.delete()
            cards = await check_pay()
            await callback.message.answer("Актуальные реквизиты:")
            for data in cards:
                await callback.message.answer(f"{data[2]} {data[4]}\n"
                                              f"\n"
                                              f"{data[3]}",
                                              reply_markup=edit_pay_ikb(data[0]))
            await callback.message.answer("Это все актуальные реквизиты!")
            await callback.answer()
        elif callback.data == 'update_currency':
            await callback.message.answer("🚀Обновление запущено!")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
            }
            nec_cur = ["KZT", "TRY", "UAH", "USD", "UZS"]
            response = requests.get("https://www.alta.ru/currency/", headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            card = soup.find_all("tr")
            for curr in card:
                if curr.find("td", class_="t-center pCurrency_code d-flex") is None:
                    pass
                else:
                    cod = curr.find("td", class_="t-center pCurrency_code d-flex") \
                        .find("span", class_="gray col-50 t-left ml5 m-ml2").text
                    for q in range(0, 5):
                        if cod == nec_cur[q]:
                            how = curr.find("td", class_="t-right").find("span", class_="mr10 m-mr0").text
                            nominal = curr.find("td", class_="t-left").find("span", class_="gray").text.replace("(",
                                                                                                                "").replace(
                                ")", "").replace("за", "")
                            cur_index = int(nominal) / float(how)
                            await delete_currency(cod)
                            await create_rate(cod, cur_index)
            await delete_currency("RUB")
            await create_rate("RUB", 1)
            await callback.message.answer("✅Обновление успешно завершено!")
            await callback.answer()
        elif callback.data == 'check_currency':
            currency = await get_all_currency()
            for data in currency:
                await callback.message.answer(f"1 RUB = {data[1]} {data[0]}",
                                              reply_markup=delete_currency_ikb(data[0]))
            await callback.message.answer("Все актуальные ваоюты!")
            await callback.answer()
        elif callback.data == 'add_currency':
            await callback.message.answer("Укажите наименование валюты:")
            await AddCurrencyStatesGroup.currency.set()
            await callback.answer()
        elif callback.data == 'confirm_add_currency':
            await callback.message.answer("Вы вернулись в главное меню:",
                                          reply_markup=general_admin_kb())
            await callback.message.delete()
            await callback.answer()


# ADMIN PAY
@dp.callback_query_handler(text='add_pay')
async def cb_add_card(callback : types.CallbackQuery, state : FSMContext):
    ban = await cb_check_ban_user(callback)
    if not ban:
        card_id = int(time())
        await create_pay(card_id, callback.from_user.id)
        async with state.proxy() as data:
            data['card_id'] = card_id
        await callback.message.answer("Укажите банк оплаты",
                                      reply_markup=admin_card_kb())
        await AdminPayStatesGroup.bank.set()
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_card'))
async def cb_delete_pay(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await delete_pay(callback_data['id'])
        await callback.message.reply("Карта успешно удалена!",
                                     reply_markup=general_admin_kb())
        await bot.send_message(chat_id=ceo,
                               text=f"Удалена карта!\n"
                                    f"\n"
                                    f"ID: {callback.from_user.id}\n"
                                    f"USERNAME: @{callback.from_user.username}")
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_card'))
async def cb_edit_pay(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await callback.message.answer("Укажите банк",
                                      reply_markup=admin_card_kb())
        await AdminPayStatesGroup.bank.set()
        async with state.proxy() as data:
            data['card_id'] = callback_data['id']
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_currency'))
async def cb_delete_currency(callback: types.CallbackQuery, callback_data: dict):
    await delete_currency(callback_data['id'])
    await callback.message.reply("Валюта успешно удалена!",
                                 reply_markup=general_admin_kb())
    await bot.send_message(chat_id=control_add_chat,
                           text=f"Удалена валюта!\n"
                                f"\n"
                                f"ID: {callback.from_user.id}\n"
                                f"USERNAME: @{callback.from_user.username}")
    await callback.answer()



# ADD PAY METHOD
@dp.message_handler(state=AdminPayStatesGroup.bank)
async def load_bank(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bank'] = message.text
    currency = await get_all_currency()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for data in currency:
        btn1 = KeyboardButton(text=data[0])
        kb.add(btn1)
    await message.answer("Укажите курс валюты:",
                         reply_markup=kb)
    await AdminPayStatesGroup.next()


@dp.message_handler(state=AdminPayStatesGroup.currency)
async def load_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency'] = message.text
    await message.answer("Отправьте номер карты:")
    await AdminPayStatesGroup.next()


@dp.message_handler(state=AdminPayStatesGroup.card)
async def load_card(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['card'] = message.text
    await update_pay(state, message.from_user.id)
    await message.answer(text=f"{data['bank']} {data['currency']}\n"
                              f"\n"
                              f"{data['card']}")
    await message.answer("Все верно?",
                         reply_markup=confirm_add_card_ikb(data['card_id']))
    await state.finish()



# ADD CURRENCY
@dp.message_handler(state=AddCurrencyStatesGroup.currency)
async def load_currency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['currency'] = message.text
        currency = await check_currency(data['currency'])
    if not currency:
        await message.answer("Отправьте курс:")
        await AddCurrencyStatesGroup.next()
    else:
        await message.answer("Данная валюта уже добавлена!")
        await state.finish()


@dp.message_handler(state=AddCurrencyStatesGroup.amount)
async def load_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await create_rate(data['currency'], data['amount'])
    await message.answer(f"1 RUB = {data['amount']} {data['currency']}",
                         reply_markup=confirm_add_currency(data['currency']))
    await state.finish()