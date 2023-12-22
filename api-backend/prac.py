from aiogram import types

from hendlers import check_ban_user, cb_check_ban_user, set_new_click
from main import dp
from keyboards import *
from translations import _
from youngkb import back_young_main_kb, next_prac, main_young_menu_ikb


@dp.message_handler(lambda message: message.text == "📋Practice game")
async def all_text(message: types.Message):
    user_id = message.from_user.id
    lang = await get_user_lang(user_id)
    ban = await check_ban_user(message)
    await set_new_click(message.from_user.id)
    if not ban:
        index = 0
        prac = await get_prac()
        if not prac:
            await message.answer(_("Актуальных праков нету!", lang),
                                 reply_markup=back_young_main_kb(lang))
        else:
            await message.answer(_("Все актуальные праки:", lang))
            all_prac = list(prac)[index: index + 3]
            index += 3
            for data in all_prac:
                if not data[2]:
                    await message.answer(text=data[3],
                                         reply_markup=text_url_ikb(f"🔗{_('Зарегистрироваться', lang)}", data[4]))
                else:
                    await message.answer_photo(photo=data[2],
                                               caption=data[3],
                                               reply_markup=text_url_ikb(f"🔗{_('Зарегистрироваться', lang)}", data[4]))
            if len(all_prac) < 3:
                await message.answer(_("Это все праки!", lang),
                                     reply_markup=back_young_main_kb(lang))
            else:
                await message.answer(_('Продолжить просмотр праков?', lang),
                                     reply_markup=next_prac(lang))


cb_words_list = ["next_prac", "back_young_main"]

@dp.callback_query_handler(lambda callback: callback.data in cb_words_list)
async def back_tour_main(callback: types.CallbackQuery):
    global index
    lang = await get_user_lang(callback.from_user.id)
    ban = await cb_check_ban_user(callback)
    if not ban:
        if callback.data == 'next_prac':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            prac = await get_prac()
            all_prac = list(prac)[index: index + 3]
            index += 3
            for data in all_prac:
                if not data[2]:
                    await callback.message.answer(text=data[3],
                                                  reply_markup=text_url_ikb(f"🔗{_('Зарегистрироваться', lang)}",
                                                                            data[4]))
                else:
                    await callback.message.answer_photo(photo=data[2],
                                                        caption=data[3],
                                                        reply_markup=text_url_ikb(
                                                            f"🔗{_('Зарегистрироваться', lang)}", data[4]))
            if len(all_prac) < 3:
                await callback.message.answer(_("Это все праки!", lang),
                                              reply_markup=back_young_main_kb(lang))
            else:
                await callback.message.answer(_("Продолжить просмотр праков?", lang),
                                              reply_markup=next_prac(lang))
            await callback.answer()
        elif callback.data == 'back_young_main':
            await set_new_click(callback.from_user.id)
            await callback.message.delete()
            await callback.message.answer(_("Вы вернулись в главное меню:", lang),
                                          reply_markup=main_young_menu_ikb(lang))
            await callback.answer()