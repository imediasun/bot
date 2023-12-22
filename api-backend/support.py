import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from config import admin_support_chat, ceo
from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp, bot

from keyboards import *
from youngkb import info_from_bd, main_young_menu_ikb
from translations import _
from states import HelpStatesGroup, AnswerStatesGroup
from database.db import *

words_list = ["💬Поддержка", "💬SUPPORT", "💬Destek", '💬Підтримка', "💬Қолдау", "💬Қўллаб-қувватлаш"]

@dp.message_handler(lambda message: message.text in words_list)
async def all_text(message: types.Message):
    lang = await get_user_lang(message.from_user.id)
    ban = await check_ban_user(message)
    if not ban:
        await set_new_click(message.from_user.id)
        await message.answer(f"{_('Здравствуйте, отправьте Ваш вопрос(можно прикрепить фото)', lang)}:\n"
                             f"{_('График работы: 8:00 - 00:00 MSK', lang)}",
                             reply_markup=info_from_bd(f"❌{_('Отменить', lang)}"))
        await HelpStatesGroup.first_ques.set()



cb_words_list = ["ques", "back_main_menu"]

@dp.callback_query_handler(lambda callback : callback.data in cb_words_list)
async def all_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ban = await cb_check_ban_user(callback)
    lang = await get_user_lang(user_id)
    if not ban:
        if callback.data == 'ques':
            await set_new_click(callback.from_user.id)
            await callback.message.answer(_("Отправьте ваш вопрос(можно прикрепить фото):", lang),
                                          reply_markup=cancel_kb(lang))
            await HelpStatesGroup.first_ques.set()
            await callback.answer()
        elif callback.data == 'back_main_menu':
            await set_new_click(callback.from_user.id)
            await callback.message.answer(_("Вы вернулись в главное меню:", lang),
                                          reply_markup=main_menu_kb(lang))
            await callback.message.delete()
            await callback.answer()


# STATES HELP
# Questions
@dp.message_handler(content_types=['photo', 'text'], state=HelpStatesGroup.first_ques)
async def question1(message: types.Message, state: FSMContext):
    global chat_id_q, mess_id_ques
    lang = await get_user_lang(message.from_user.id)
    block = await get_block_user(message.from_user.id)
    try:
        chat_id_q = message.from_user.id
        lang_name = await get_lang_name(message.from_user.id)
        mess_id_ques = message.message_id
        if message.text == f'❌{_("Отменить", lang)}':
            await set_new_click(message.from_user.id)
            await open_supp_chat(message.from_user.id)
            profile = await get_profile(message.from_user.id)
            if profile == 'pro':
                await message.answer(_("Вы вернулись в главное меню:", lang),
                                     reply_markup=main_menu_kb(lang))
            elif profile == 'young':
                await message.answer(_("Вы вернулись в главное меню:", lang),
                                     reply_markup=main_young_menu_ikb(lang))
            await state.finish()
        else:
            if block == 2:
                await message.answer(_("Такого варианта ответа нету!", lang),
                                     reply_markup=info_from_bd(f'🔙{_("Главное меню", lang)}'))
            else:
                await close_supp_chat(message.from_user.id)
                async with state.proxy() as data:
                    if (message.content_type == 'photo'):
                        data['text'] = message.caption
                    else:
                        data['text'] = message.text
                await bot.send_message(chat_id=chat_id_q,
                                       text=f"{_('Вопрос успешно отправлен в 💬Поддержку!', lang)}\n"
                                            f"{_('Оператор свяжется с Вами в течение 10 минут, ожидайте...', lang)}",
                                       reply_markup=ReplyKeyboardRemove())
                if (message.content_type == 'photo'):
                    photo = message.photo[0].file_id
                    await bot.send_photo(chat_id=admin_support_chat,
                                         photo=photo,
                                         caption=f"Новый вопрос от пользователя @{message.from_user.username}\n"
                                                 f"ID: {message.from_user.id}\n"
                                                 f"Язык: {lang_name}\n"
                                                 f"\n"
                                                 f"Вопрос: {data['text']}",
                                         reply_markup=admin_help_kb())
                else:
                    await bot.send_message(chat_id=admin_support_chat,
                                           text=f"Новый вопрос от пользователя @{message.from_user.username}\n"
                                                f"ID: {message.from_user.id}\n"
                                                f"Язык: {lang_name}\n"
                                                f"\n"
                                                f"Вопрос: {data['text']}",
                                       reply_markup=admin_help_kb())
            await HelpStatesGroup.next()
    except:
        await bot.send_message(chat_id=ceo[0],
                               text="❗️Ошибка в поддержке со стороны пользователя!")


@dp.message_handler(content_types=['text', 'photo'], state=HelpStatesGroup.second_ques)
async def question2(message : types.Message, state : FSMContext):
    global chat_id_q, mess_id_ques
    lang = await get_user_lang(message.from_user.id)
    block = await get_block_user(message.from_user.id)
    try:
        chat_id_q = message.from_user.id
        profile = await get_profile(chat_id_q)
        if message.text == f'❌{_("Отменить", lang)}':
            # await bot.delete_message(chat_id=admin_support_chat, message_id=mess_id_ques)
            await set_new_click(message.from_user.id)
            await open_supp_chat(message.from_user.id)
            if profile == 'pro':
                await message.answer(_("Вы вернулись в главное меню:", lang),
                                     reply_markup=main_menu_kb(lang))
            elif profile == 'young':
                await message.answer(_("Вы вернулись в главное меню:", lang),
                                     reply_markup=main_young_menu_ikb(lang))
            await state.finish()
        elif message.text == f'❌{_("Закрыть чат", lang)}':
            await open_supp_chat(message.from_user.id)
            await bot.send_message(chat_id=ans_admin_id,
                                   text=f"❌Пользователь @{message.from_user.username} покинул чат!\n"
                                        f"ID: {chat_id_q}",
                                   reply_markup=info_from_bd("🔙Главное меню"))
            if profile == 'pro':
                await bot.send_message(chat_id=chat_id_q,
                                       text=f"{_('Были рады помочь!', lang)}😊\n"
                                            f"{_('Желаем успехов и хорошего дня!', lang)}😘",
                                       reply_markup=main_menu_kb(lang))
            elif profile == 'young':
                await bot.send_message(chat_id=chat_id_q,
                                       text=f"{_('Были рады помочь!', lang)}😊\n"
                                            f"{_('Желаем успехов и хорошего дня!', lang)}😘",
                                       reply_markup=main_young_menu_ikb(lang))
            await state.finish()
        elif message.text == f'🔙{_("Главное меню", lang)}':
            await set_new_click(message.from_user.id)
            await open_supp_chat(message.from_user.id)
            if profile == 'pro':
                await message.answer(_("Вы вернулись в главное меню:", lang),
                                     reply_markup=main_menu_kb(lang))
            elif profile == 'young':
                await message.answer(_("Вы вернулись в главное меню:", lang),
                                     reply_markup=main_young_menu_ikb(lang))
            await state.finish()
        else:
            if block == 2:
                await message.answer(_("Такого варианта ответа нету!", lang),
                                     reply_markup=info_from_bd(f'🔙{_("Главное меню", lang)}'))
            else:
                async with state.proxy() as data:
                    if (message.content_type == 'photo'):
                        data['text'] = message.caption
                    else:
                        data['text'] = message.text
                if (message.content_type == 'photo'):
                    photo = message.photo[0].file_id
                    await bot.send_photo(chat_id=ans_admin_id,
                                         photo=photo,
                                         caption=data['text'],
                                         reply_markup=info_from_bd(f"❌{_('Закрыть чат', lang)}"))
                else:
                    await bot.send_message(chat_id=ans_admin_id,
                                           text=data['text'],
                                           reply_markup=info_from_bd(f"❌{_('Закрыть чат', lang)}"))
    except:
        await bot.send_message(chat_id=ceo[0],
                               text="❗️Ошибка в поддержке со стороны пользователя!")




# Answers
@dp.callback_query_handler(text='answer')
async def admin_answer(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f"ID: {chat_id_q}\n"
                                f"Ответ пользователю:",
                           reply_markup=admin_send_ans_ikb())
    await callback.answer()
    await asyncio.sleep(15)
    await callback.message.delete()


@dp.callback_query_handler(text='admin_send_ans')
async def admin_send_ans(callback : types.CallbackQuery):
    global ans_admin_id
    ans_admin_id = callback.from_user.id
    await callback.message.answer("Введите ответ:",
                                  reply_markup=info_from_bd("❌Закрыть чат"))
    await AnswerStatesGroup.first_answer.set()
    await callback.answer()


@dp.callback_query_handler(text='ignore')
async def admin_ignore(callback: types.CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.reply("Вы проигнорировали сообщение!")
    await bot.send_message(chat_id=chat_id_q,
                           text=_("Извините, но ваш вопрос неясен или некорректен. Можете пожалуйста уточнить свой вопрос?", lang),
                           reply_markup=ques_kb(lang))
    await callback.message.delete()
    await callback.answer()



@dp.message_handler(content_types=['photo', 'text'], state=AnswerStatesGroup.first_answer)
async def answer(message: types.Message, state: FSMContext):
    lang = await get_user_lang(chat_id_q)
    try:
        if message.text == '❌Закрыть чат':
            await close_supp_chat(chat_id_q)
            chat = await bot.get_chat(chat_id=chat_id_q)
            await message.answer(f"❌Чат с пользователем @{chat.username} завершен!\n"
                                 f"ID: {chat_id_q}",
                                 reply_markup=main_menu_kb(lang))
            profile = await get_profile(chat_id_q)
            if profile == 'pro':
                await bot.send_message(chat_id=chat_id_q,
                                       text=f"{_('Были рады помочь!', lang)}😊\n"
                                            f"{_('Желаем успехов и хорошего дня!', lang)}😘",
                                       reply_markup=info_from_bd(f"🔙{_('Главное меню', lang)}"))
            elif profile == 'young':
                await bot.send_message(chat_id=chat_id_q,
                                       text=f"{_('Были рады помочь!', lang)}😊\n"
                                            f"{_('Желаем успехов и хорошего дня!', lang)}😘",
                                       reply_markup=info_from_bd(f"🔙{_('Главное меню', lang)}"))
            await state.finish()
        elif message.text == '🔙Главное меню':
            await message.answer(_("Вы вернулись в главное меню:", lang),
                                 reply_markup=main_menu_kb(lang))
            await state.finish()
        else:
            await open_supp_chat(message.from_user.id)
            async with state.proxy() as data:
                if (message.content_type == 'photo'):
                    data['text'] = message.caption
                else:
                    data['text'] = message.text
                await state.finish()
                if (message.content_type == 'photo'):
                    photo = message.photo[0].file_id
                    await bot.send_photo(chat_id=chat_id_q,
                                         photo=photo,
                                         caption=data['text'],
                                         reply_markup=info_from_bd(f"❌{_('Закрыть чат', lang)}"))
                else:
                    await bot.send_message(chat_id=chat_id_q,
                                           text=data['text'],
                                           reply_markup=info_from_bd(f"❌{_('Закрыть чат', lang)}"))
            await AnswerStatesGroup.next()
    except:
        await bot.send_message(chat_id=ceo[0],
                               text="❗️Ошибка в поддержке со стороны админа!")


@dp.message_handler(content_types=['text', 'photo'], state=AnswerStatesGroup.second_answer)
async def second_answer(message : types.Message, state : FSMContext):
    lang = await get_user_lang(chat_id_q)
    try:
        if message.text == "❌Закрыть чат":
            await close_supp_chat(chat_id_q)
            chat = await bot.get_chat(chat_id=chat_id_q)
            await message.answer(f"❌Чат с пользователем @{chat.username} завершен!\n"
                                 f"ID: {chat_id_q}",
                                 reply_markup=main_menu_kb(lang))
            await bot.send_message(chat_id=chat_id_q,
                                   text=f"{_('Были рады помочь!', lang)}😊\n"
                                        f"{_('Желаем успехов и хорошего дня!', lang)}😘",
                                   reply_markup=info_from_bd(f"🔙{_('Главное меню', lang)}"))
            # await HelpStatesGroup.first_ques.set
            await state.finish()
        elif message.text == '🔙Главное меню':
            await message.answer(_("Вы вернулись в главное меню:", lang),
                                 reply_markup=main_menu_kb(lang))
            await state.finish()
        else:
            async with state.proxy() as data:
                if (message.content_type == 'photo'):
                    data['text'] = message.caption
                else:
                    data['text'] = message.text
                await state.finish()
                if (message.content_type == 'photo'):
                    photo = message.photo[0].file_id
                    await bot.send_photo(chat_id=chat_id_q,
                                         photo=photo,
                                         caption=data['text'],
                                         reply_markup=info_from_bd(f"❌{_('Закрыть чат', lang)}"))
                else:
                    await bot.send_message(chat_id=chat_id_q,
                                           text=data['text'],
                                           reply_markup=info_from_bd(f"❌{_('Закрыть чат', lang)}"))
    except:
        await bot.send_message(chat_id=ceo[0],
                               text="❗️Ошибка в поддержке со стороны aдмина!")