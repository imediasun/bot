from aiogram import types
from aiogram.dispatcher import FSMContext
from uuid import uuid4

from config import control_add_chat
from hendlers import check_ban_user, cb_check_ban_user, is_valid_url
from main import dp, bot
from database import *
from keyboards import *
from youngkb import *
from states import AddPracStatesGroup




@dp.message_handler(lambda message: message.text == "PRACTICE GAME")
async def all_text(message: types.Message):
    global index
    user_id = message.from_user.id
    moder_id = await get_moder_id(user_id)
    ban = await check_ban_user(message)
    if not ban:
        if message.from_user.id in moder_id:
            await message.answer("Выберите действие:",
                                 reply_markup=admin_prac_game_kb())


words_list = ["add_prac", "check_all_pracs"]

@dp.callback_query_handler(lambda callback : callback.data in words_list)
async def all_callbacks(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    ban = await cb_check_ban_user(callback)
    moder_id = await get_moder_id(user_id)
    if not ban:
        if user_id in moder_id:
            if callback.data == 'add_prac':
                await callback.message.answer("Отправь баннер праков:",
                                              reply_markup=admin_skip_kb())
                await AddPracStatesGroup.photo.set()
                await callback.message.delete()
                await callback.answer()
            elif callback.data == 'check_all_pracs':
                all_prac = await admin_get_pracs()
                if not all_prac:
                    await callback.message.answer("Праков на данный момент нету!")
                else:
                    await callback.message.answer("Все актуальные праки:")
                    for data in all_prac:
                        if not data[2]:
                            await callback.message.answer(text=f"{data[3]}\n"
                                                               f"\n"
                                                               f"ID: {data[1]}\n"
                                                               f"\n"
                                                               f"{data[4]}",
                                                          reply_markup=admin_edit_prac_kb(data[0]))
                        else:
                            await callback.message.answer_photo(photo=data[2],
                                                                caption=f"{data[3]}\n"
                                                                        f"\n"
                                                                        f"ID: {data[1]}\n"
                                                                        f"\n"
                                                                        f"{data[4]}",
                                                                reply_markup=admin_edit_prac_kb(data[0]))
                    await callback.message.answer("Это все актуальные праки!")
                await callback.message.delete()
                await callback.answer()




@dp.callback_query_handler(tour_cb.filter(action='confirm_add_prac'))
async def confirm_add_prac(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        prac = await admin_get_prac(callback_data['id'])
        for data in prac:
            if not data[2]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"{data[3]}\n"
                                            f"\n"
                                            f"{data[4]}\n"
                                            f"\n"
                                            f"ID: {callback.from_user.id}\n"
                                            f"USERNAME: @{callback.from_user.username}",
                                       reply_markup=admin_edit_post_prac_ikb(callback_data['id']))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[2],
                                     caption=f"{data[3]}\n"
                                             f"\n"
                                             f"{data[4]}\n"
                                             f"\n"
                                             f"ID: {callback.from_user.id}\n"
                                             f"USERNAME: @{callback.from_user.username}",
                                     reply_markup=admin_edit_post_prac_ikb(callback_data['id']))
        await callback.message.answer("Прак успешно добавлен!",
                                      reply_markup=admin_kb())
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='edit_young_prac'))
async def young_edit_prac(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.answer("Отправьте новый баннер праков:",
                                  reply_markup=photo_kb(lang))
    await AddPracStatesGroup.new_photo.set()
    async with state.proxy() as data:
        data['id'] = callback_data['id']
    await callback.answer()


@dp.callback_query_handler(tour_cb.filter(action='delete_young_prac'))
async def young_delete_prac(callback: types.CallbackQuery, callback_data: dict):
    ban = await cb_check_ban_user(callback)
    if not ban:
        await admin_delete_prac(callback_data['id'])
        await callback.message.reply("Вы успешно удалили прак!",
                                     reply_markup=admin_kb())
        prac = await admin_get_prac(callback_data['id'])
        for data in prac:
            if not data[2]:
                await bot.send_message(chat_id=control_add_chat,
                                       text=f"{data[3]}\n"
                                            f"\n"
                                            f"{data[4]}",
                                       reply_markup=admin_edit_post_prac_ikb(callback_data['id']))
            else:
                await bot.send_photo(chat_id=control_add_chat,
                                     photo=data[2],
                                     caption=f"{data[3]}\n"
                                             f"\n"
                                             f"{data[4]}",
                                     reply_markup=admin_edit_post_prac_ikb(callback_data['id']))
    await callback.answer()





@dp.message_handler(lambda message: not message.photo and not message.text == 'Пропустить',
                    state=AddPracStatesGroup.photo)
async def check_prac_photo(message: types.Message):
    await message.answer("Отправьте фото!")


@dp.message_handler(content_types=['photo', 'text'], state=AddPracStatesGroup.photo)
async def load_prac_photo(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        text = ""
        async with state.proxy() as data:
            data['photo'] = text
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправьте информацию о праке:",
                         reply_markup=admin_skip_kb())
    await AddPracStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 300, state=AddPracStatesGroup.desc)
async def check_prac_desc(message: types.Message):
    await message.answer("Описание турнира не должно превышать 300 символов!")


@dp.message_handler(state=AddPracStatesGroup.desc)
async def load_prac_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Пропустить':
            data['desc'] = ""
        else:
            data['desc'] = message.text
    await message.answer("Отправьте ссылку на прак:",
                         reply_markup=ReplyKeyboardRemove())
    await AddPracStatesGroup.next()


@dp.message_handler(lambda message: not is_valid_url(message.text), state=AddPracStatesGroup.url)
async def check_prac_url(message: types.Message):
    await message.answer("Отправьте ссылку!")


@dp.message_handler(state=AddPracStatesGroup.url)
async def load_prac_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
    prac_id = str(uuid4())
    await create_prac(state, message.from_user.id, prac_id)
    if data['photo'] == "":
        await message.answer(text=f"{data['desc']}\n"
                                  f"\n"
                                  f"{data['url']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['desc']}\n"
                                           f"\n"
                                           f"{data['url']}")
    await message.answer("Все верно?",
                         reply_markup=admin_confirm_add_prac_ikb(prac_id))
    await state.finish()





@dp.message_handler(lambda message: not message.photo
                                    and not message.text == 'Пропустить'
                                    and not message.text == 'Оставить прошлый',
                    state=AddPracStatesGroup.new_photo)
async def check_prac_photo(message: types.Message):
    await message.answer("Отправьте фото!")

@dp.message_handler(content_types=['photo', 'text'], state=AddPracStatesGroup.new_photo)
async def load_new_prac_photo(message: types.Message, state: FSMContext):
    if message.text == 'Оставить прошлый':
        async with state.proxy() as data:
            photo = await get_photo_prac(data['id'])
            data['photo'] = photo
    elif message.text == 'Пропустить':
        async with state.proxy() as data:
            data['photo'] = ""
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await message.answer("Отправьте информацию о праке:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracStatesGroup.next()


@dp.message_handler(lambda message: len(message.text) > 300, state=AddPracStatesGroup.new_desc)
async def check_prac_desc(message: types.Message):
    await message.answer("Описание турнира не должно превышать 300 символов!")


@dp.message_handler(state=AddPracStatesGroup.new_desc)
async def load_prac_desc(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            desc = await get_desc_prac(data['id'])
            data['desc'] = desc
    else:
        async with state.proxy() as data:
            data['desc'] = message.text
    await message.answer("Отправьте ссылку на турнир:",
                         reply_markup=info_from_bd("Пропустить"))
    await AddPracStatesGroup.next()


@dp.message_handler(lambda message: not is_valid_url(message.text)
                                    and not message.text == 'Пропустить', state=AddPracStatesGroup.new_url)
async def check_prac_url(message: types.Message):
    await message.answer("Отправьте ссылку!")


@dp.message_handler(state=AddPracStatesGroup.new_url)
async def load_new_prac_url(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        async with state.proxy() as data:
            url = await get_url_prac(data['id'])
            data['url'] = url
    else:
        async with state.proxy() as data:
            data['url'] = message.text
    await admin_update_prac(state, message.from_user.id)
    if data['photo'] == "":
        await message.answer(text=f"{data['desc']}\n"
                                  f"\n"
                                  f"{data['url']}")
    else:
        await message.answer_photo(photo=data['photo'],
                                   caption=f"{data['desc']}\n"
                                           f"\n"
                                           f"{data['url']}")
    await message.answer("Все верно?",
                         reply_markup=admin_confirm_add_prac_ikb(data['id']))
    await state.finish()