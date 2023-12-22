from aiogram import types

from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp
from keyboards import *
from translations import _
from database.db import *

words_list = ["📋Tournament"]


@dp.message_handler(lambda message: message.text in words_list)
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(user_id)
    if not ban:
        if message.text == '📋Tournament':
            await message.answer(_("Выберите формат турнира:", lang),
                                 reply_markup=tour_main_ikb(lang))


@dp.callback_query_handler(text="back_tour_main")
async def back_tour_main(callback: types.CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(callback.from_user.id)
    if not ban:
        await callback.message.answer(_("Вы в TOURNAMENT меню:", lang),
                                      reply_markup=tour_main_ikb(lang))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('tour_'))
async def cb_tour(callback: types.CallbackQuery):
    index = 0
    lang = await get_user_lang(callback.from_user.id)
    tour_format = callback.data.split('_')[1]
    tour = await get_tours(tour_format)
    ban = await cb_check_ban_user(callback)
    await set_new_click(callback.from_user.id)
    if not ban:
        if not tour:
            await callback.message.answer(_("На данный момент турниров нету!", lang),
                                          reply_markup=back_pro_main(lang))
        else:
            full_tour = list(tour)[index: index + 2]
            index += 2
            await callback.message.answer(_("Все актуальные турниры:", lang))
            for data in full_tour:
                if not data[3]:
                    await callback.message.answer(text=data[4],
                                                  reply_markup=text_url_ikb(f"🔗{_('Зарегистрироваться', lang)}", data[5]))
                else:
                    await callback.message.answer_photo(photo=data[3],
                                                        caption=data[4],
                                                        reply_markup=text_url_ikb(f"🔗{_('Зарегистрироваться', lang)}",
                                                                                  data[5]))
            if len(full_tour) < 2:
                await callback.message.answer(_("Это все актуальные турниры!", lang),
                                              reply_markup=back_tour_main_ikb(lang))
            else:
                await callback.message.answer(_("Продолжить просмотр турниров?", lang),
                                              reply_markup=next_tour_ikb(tour_format, lang))
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='next_tour'))
async def cb_next_tour(callback: types.CallbackQuery, callback_data: dict):
    global index
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    await set_new_click(callback.from_user.id)
    if not ban:
        tour = await get_tours(callback_data['id'])
        full_tour = list(tour)[index: index + 2]
        index += 2
        for data in full_tour:
            if not data[3]:
                await callback.message.answer(text=data[4],
                                              reply_markup=text_url_ikb(f"🔗{_('Зарегистрироваться', lang)}", data[5]))
            else:
                await callback.message.answer_photo(photo=data[3],
                                                    caption=data[4],
                                                    reply_markup=text_url_ikb(f"🔗{_('Зарегистрироваться', lang)}", data[5]))
        if len(full_tour) < 2:
            await callback.message.answer(_("Это все актуальные турниры!", lang),
                                          reply_markup=back_tour_main_ikb(lang))
        else:
            await callback.message.answer(_("Продолжить просмотр турниров?", lang),
                                          reply_markup=next_tour_ikb(callback_data['id'], lang))
    await callback.message.delete()
    await callback.answer()