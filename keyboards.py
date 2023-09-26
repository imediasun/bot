from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from translations import _



def choose_country_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Українська')
    btn2 = KeyboardButton('English')
    btn3 = KeyboardButton('Русский')
    btn4 = KeyboardButton('Қазақ')
    btn5 = KeyboardButton("O'zbek")
    btn6 = KeyboardButton("Türkçe")
    kb.add(btn1, btn2, btn3).add(btn4, btn5).add(btn6)

    return kb

def choose_type_akk() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('👶Young player')
    btn2 = KeyboardButton('👨PRO player')
    kb.add(btn1, btn2)

    return kb

def main_menu_kb(lang) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton('👤Free agent')
    btn2 = KeyboardButton('👥Free team')
    btn3 = KeyboardButton('👑VIP Slots')
    btn4 = KeyboardButton('📋Tournament')
    btn5 = KeyboardButton('💥Events')
    btn6 = KeyboardButton('🔥NEWS')
    btn7 = KeyboardButton(f'💬{_("Поддержка", lang)}')
    btn8 = KeyboardButton('🎶MUSIC')
    btn9 = KeyboardButton('💸UC SHOP')
    kb.add(btn4, btn3, btn5).add(btn1, btn2).add(btn9).add(btn6, btn8).add(btn7)

    return kb


def cancel_kb(lang) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton(f'❌{_("Отменить", lang)}')
    kb.add(btn1)

    return kb

def skip_kb(lang) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(_("Пропустить", lang))
    kb.add(btn1)

    return kb


def admin_skip_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Пропустить")
    kb.add(btn1)

    return kb


def photo_kb(lang) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton(_('Оставить прошлый', lang))
    btn2 = KeyboardButton(_("Пропустить", lang))
    kb.add(btn1, btn2)

    return kb



#FREE AGENT
def free_agent_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✍️{_("Оставить свою анкету", lang)}', callback_data='add_agent')
    btn2 = InlineKeyboardButton(f'🔍{_("Найти команду", lang)}', callback_data='search_team')
    btn3 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
    ikb.add(btn1, btn2, btn3)

    return ikb

def back_free_agent_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_free_agent_main')
    ikb.add(btn1)

    return ikb

def finish_agent_profile_kb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(f'✅{_("Да", lang)}', callback_data='yes_free_agent')
    btn2 = InlineKeyboardButton(f'🔁{_("Изменить", lang)}', callback_data='change_free_agent')
    btn3 = InlineKeyboardButton(f'🗑{_("Удалить", lang)}', callback_data='delete_free_agent')
    ikb.add(btn1, btn2, btn3)

    return ikb

def send_agent_profil_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🔍{_("Найти команду", lang)}', callback_data='search_team')
    btn2 = InlineKeyboardButton(f'🔙{_("Главное меню", lang)}', callback_data='back_main_menu')
    ikb.add(btn1, btn2)

    return ikb

def next_team_kb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_team')
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_free_agent_main')
    ikb.add(back, btn1)

    return ikb

def desc_agent_kb(lang) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton(_("Оставить прошлый текст", lang))
    kb.add(btn1)

    return kb

def choose_teamspeak_kb(lang) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Українська')
    btn2 = KeyboardButton('English')
    btn3 = KeyboardButton('Русский')
    btn4 = KeyboardButton('Қазақ')
    btn5 = KeyboardButton("O'zbek")
    btn6 = KeyboardButton('Türkçe')
    btn7 = KeyboardButton(_("Пропустить", lang))
    kb.add(btn1, btn2, btn3, btn4, btn5).add(btn6).add(btn7)

    return kb


#FREE TEAM
def free_team_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✍️{_("Оставить анкету о поиске игрока", lang)}', callback_data='add_team')
    btn2 = InlineKeyboardButton(f'🔍{_("Найти игрока", lang)}', callback_data='search_agent')
    btn3 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
    ikb.add(btn1, btn2).add(btn3)

    return ikb

def finish_team_profile_kb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(f'✅{_("Да", lang)}', callback_data='yes_free_team')
    btn2 = InlineKeyboardButton(f'🔁{_("Изменить", lang)}', callback_data='change_free_team')
    btn3 = InlineKeyboardButton(f'🗑{_("Удалить", lang)}', callback_data='delete_free_team')
    ikb.add(btn1, btn2, btn3)

    return ikb

def send_team_profile_kb(lang) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🔍{_("Найти игрока", lang)}', callback_data='search_agent')
    btn2 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_team_main')
    kb.add(btn1, btn2)

    return kb

def back_free_team_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_team_main')
    ikb.add(back)

    return ikb

def next_agent_kb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_agent')
    back = InlineKeyboardButton(f'🔙{_("Далее", lang)}', callback_data='back_team_main')
    ikb.add(back, btn1)

    return ikb

#VIP SLOTS
def vip_slot_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Qualification', callback_data='vip_slot_Qualification')
    btn2 = InlineKeyboardButton('1/4 STAGE', callback_data='vip_slot_1/4 STAGE')
    btn3 = InlineKeyboardButton('1/2 STAGE', callback_data='vip_slot_1/2 STAGE')
    btn4 = InlineKeyboardButton('FINAL STAGE', callback_data='vip_slot_FINAL STAGE')
    btn5 = InlineKeyboardButton('GRAND-FINAL STAGE', callback_data='vip_slot_GRAND-FINAL STAGE')
    btn6 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
    ikb.add(btn1, btn2, btn3).add(btn4, btn5).add(btn6)

    return ikb

def buy_vip_slot_ikb(tour_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'💳{_("Купить", lang)}', callback_data=tour_cb.new(tour_id, 'buy_vip_slot'))
    ikb.add(btn1)

    return ikb

def next_vip_slot_ikb(stage, lang):
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data=tour_cb.new(stage, 'next_vip_slot'))
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_vip_slots')
    ikb.add(back, btn1)

    return ikb

def back_vip_slot_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_vip_slots')
    ikb.add(back)

    return ikb

def back_pro_main(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'🔙{_("Главное меню", lang)}', callback_data='back_main_menu')
    ikb.add(btn1)

    return ikb

def back_pro_main_kb(lang) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(row_width=1)
    btn1 = KeyboardButton(f'🔙{_("Главное меню", lang)}')
    kb.add(btn1)

    return kb

def pay_vip_slot_ikb(pay_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🧾{_("Отправить чек", lang)}', callback_data=tour_cb.new(pay_id, 'send_check_vip_slot'))
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data=tour_cb.new(pay_id, 'back_payment_vip_slot'))
    ikb.add(btn1, back)

    return ikb

def confirm_buy_vip_slot(check_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✅{_("Подтвердить", lang)}', callback_data=tour_cb.new(check_id, 'confirm_buy_vip_slot'))
    btn2 = InlineKeyboardButton(f'🔄{_("Изменить чек", lang)}', callback_data=tour_cb.new(check_id, 'change_check_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb

def go_server_for_slot(link, check_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🔗{_("Ссылка", lang)}', url=link)
    btn2 = InlineKeyboardButton(f'✅{_("Перешел", lang)}', callback_data=tour_cb.new(check_id, 'send_info_for_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb

def confirm_info_pay_vip_slot_ikb(check_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✅{_("Подтвердить", lang)}', callback_data=tour_cb.new(check_id, 'confirm_info_vip_slot'))
    btn2 = InlineKeyboardButton(f'🔄{_("Изменить", lang)}', callback_data=tour_cb.new(check_id, 'change_info_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb


# TOURNAMENT
def tour_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=3)
    btn1 = InlineKeyboardButton('Squad', callback_data='tour_Squad')
    btn2 = InlineKeyboardButton('Duo', callback_data='tour_Duo')
    btn3 = InlineKeyboardButton('TDM', callback_data='tour_TDM')
    btn4 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
    ikb.add(btn1, btn2, btn3, btn4)

    return ikb

def text_url_ikb(text, url) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text=text, url=url)
    ikb.add(btn)

    return ikb

def next_tour_ikb(tour_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data=tour_cb.new(tour_id, 'next_tour'))
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_tour_main')
    ikb.add(back, btn1)

    return ikb

def back_tour_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_tour_main')
    ikb.add(back)

    return ikb



#EVENTS
def kb_event() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    btn1 = KeyboardButton('🕒15:00')
    btn2 = KeyboardButton('🕕18:00')
    btn3 = KeyboardButton('🕘21:00')
    btn4 = KeyboardButton('🕛00:00')
    btn5 = KeyboardButton('🔙Вернутся в главное меню')
    kb.add(btn1, btn2, btn3, btn4, btn5)

    return kb

def buy_event_ikb(event_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'💳{_("Купить", lang)}', callback_data=tour_cb.new(event_id, "buy_slot_event"))
    ikb.add(btn1)

    return ikb

def pay_event_ikb(pay_id, event_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🧾{_("Отправить чек", lang)}', callback_data=tour_cb.new(pay_id, 'send_check_vip_slot'))
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data=tour_cb.new(event_id, 'back_payment_event'))
    ikb.add(btn1, back)

    return ikb


def next_event_ikb(time, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data=tour_cb.new(time, "next_event"))
    btn2 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
    ikb.add(btn2, btn1)

    return ikb

def next_events_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data="next_event")
    btn2 = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_main_menu')
    ikb.add(btn2, btn1)

    return ikb


# UC SHOP
def buy_uc_kb(uc_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'💳{_("Купить", lang)}', callback_data=tour_cb.new(uc_id,'buy_uc'))
    ikb.add(btn1)

    return ikb

def pay_uc_ikb(pay_id, uc_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🧾{_("Отправить чек", lang)}', callback_data=tour_cb.new(pay_id, 'send_check_uc'))
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data=tour_cb.new(uc_id, 'back_payment'))
    ikb.add(btn1, back)

    return ikb

def confirm_payment_uc(check, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✅{_("Подтвердить", lang)}', callback_data=tour_cb.new(check, 'confirm_payment_uc'))
    btn2 = InlineKeyboardButton(f'🔄{_("Изменить чек", lang)}', callback_data=tour_cb.new(check, 'change_check_uc'))
    ikb.add(btn1, btn2)

    return ikb

def send_info_for_uc_ikb(pay_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Отправить", lang)}', callback_data=tour_cb.new(pay_id, 'send_info_for_uc'))
    ikb.add(btn1)

    return ikb

def confirm_info_pay_uc_ikb(uc_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✅{_("Да", lang)}', callback_data=tour_cb.new(uc_id, 'confirm_info_pay_uc'))
    btn2 = InlineKeyboardButton(f'🔄{_("Изменить", lang)}', callback_data=tour_cb.new(uc_id, 'change_pay_info_uc'))
    ikb.add(btn1, btn2)

    return ikb


# HELP
def ques_kb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'{_("Задать вопрос", lang)}❓', callback_data='ques')
    ikb.add(btn1)

    return ikb


# MUSIC
def music_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton('🔍Поиск')
    btn3 = KeyboardButton('🔥Популярная')
    kb.add(btn1, btn3)

    return kb


# ADMIN
def admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('EVENT')
    btn2 = KeyboardButton('VIP SLOTS')
    btn3 = KeyboardButton('TOURNAMENT')
    btn4 = KeyboardButton('PRACTICE GAME')
    btn5 = KeyboardButton('VIP SLOT PRAC')
    btn6 = KeyboardButton('MUSIC')
    btn7 = KeyboardButton('◀️YOUNG')
    btn8 = KeyboardButton('PRO▶️')
    kb.add(btn3, btn2, btn1).add(btn4, btn5).add(btn6).add(btn7, btn8)

    return kb

# ADMIN UC SHOP
def admin_add_uc() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('💸Добавить UC пак', callback_data='add_uc')
    btn2 = InlineKeyboardButton('🔍Просмотреть все актуальные UC паки', callback_data='check_uc')
    btn3 = InlineKeyboardButton('✅Активировать', callback_data='active_uc')
    btn4 = InlineKeyboardButton('❌Деактивировать', callback_data='deactive_uc')
    close = InlineKeyboardButton("Закрыть", callback_data="statistic_count")
    ikb.add(btn1, btn2, btn3, btn4, close)

    return ikb

def admin_edit_uc(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🔄Редактировать', callback_data=tour_cb.new(tour_id, 'edit_uc'))
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_uc'))
    ikb.add(btn1, btn2)

    return ikb

def admin_conf_add_uc_ikb(uc_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(uc_id, 'admin_conf_add_uc'))
    btn2 = InlineKeyboardButton('🔄Изменить', callback_data=tour_cb.new(uc_id, 'edit_uc'))
    btn3 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(uc_id, 'delete_uc'))
    ikb.add(btn1, btn2, btn3)

    return ikb

def control_add_uc_ikb(uc_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(uc_id, 'delete_uc'))
    btn2 = InlineKeyboardButton('🔄Редактировать', callback_data=tour_cb.new(uc_id, 'edit_uc'))
    btn3 = InlineKeyboardButton('🛑Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2, btn3)

    return ikb


def check_pay_uc(check_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(check_id, 'yes_pay_uc'))
    btn2 = InlineKeyboardButton('❌Отклонить', callback_data=tour_cb.new(check_id, 'no_pay_uc'))
    ikb.add(btn1, btn2)

    return ikb

def admin_sent_uc_ikb(pay_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅UC отправлены', callback_data=tour_cb.new(pay_id, 'uc_sent'))
    btn2 = InlineKeyboardButton('❌UC не отправлены', callback_data=tour_cb.new(pay_id, 'no_uc_sent'))
    ikb.add(btn1, btn2)

    return ikb

def admin_confirm_no_send_uc_ikb(uc_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(uc_id, 'confirm_no_send_uc'))
    btn2 = InlineKeyboardButton('❌Отклонить', callback_data=tour_cb.new(uc_id, 'reject_no_send_uc'))
    ikb.add(btn1, btn2)

    return ikb

def admin_rsn_no_send_uc_ikb(uc_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(uc_id, 'send_rsn_uc'))
    btn2 = InlineKeyboardButton('❌Отклонить', callback_data=tour_cb.new(uc_id, 'no_send_rsn_uc'))
    ikb.add(btn1, btn2)

    return ikb

def conf_rsn_active_uc_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data='conf_deactive_uc')
    btn2 = InlineKeyboardButton('❌Отклонить', callback_data='no_deactive_uc')
    ikb.add(btn1, btn2)

    return ikb

def conf_active_uc() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data='conf_active_uc')
    btn2 = InlineKeyboardButton('🔄Изменить', callback_data='change_active_uc')
    ikb.add(btn1, btn2)

    return ikb


# ADMIN PAY
def admin_add_pay() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('💳Добавить способ оплаты', callback_data='add_pay')
    btn2 = InlineKeyboardButton('🔍Просмотреть все способы оплаты', callback_data='check_pay')
    btn3 = InlineKeyboardButton('🚀Обновить курс валют', callback_data='update_currency')
    btn4 = InlineKeyboardButton('🔍Просмотреть все валюты', callback_data='check_currency')
    btn5 = InlineKeyboardButton('💲Добавить валюту', callback_data='add_currency')
    close = InlineKeyboardButton("❌Закрыть", callback_data="statistic_count")
    kb.add(btn1, btn2, btn3, btn4, btn5, close)

    return kb

def delete_currency_ikb(id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(id, 'delete_currency'))
    ikb.add(btn1)

    return ikb

def confirm_add_currency(id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data='confirm_add_currency')
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(id, 'delete_currency'))
    ikb.add(btn1, btn2)

    return ikb

def admin_card_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('🇺🇦Monobank')
    btn2 = KeyboardButton('🇺🇦ПриватБанк')
    btn3 = KeyboardButton('CберБанк')
    btn4 = KeyboardButton('QIWI')
    btn5 = KeyboardButton('🇰🇿Kaspi')
    btn6 = KeyboardButton('🇺🇿UZBCARD')
    cancel = KeyboardButton('Отменить')
    kb.add(btn1, btn2).add(btn3, btn4).add(btn5).add(btn6).add(cancel)

    return kb

def edit_pay_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🔄Изменить', callback_data=tour_cb.new(tour_id, 'edit_card'))
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_card'))
    ikb.add(btn1, btn2)

    return ikb

def confirm_add_card_ikb(card_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data='confirm_add_card')
    btn2 = InlineKeyboardButton('🗑Удалить карту', callback_data=tour_cb.new(card_id, 'delete_card'))
    ikb.add(btn1, btn2)

    return ikb


# ADMIN TOURNAMENT
def admin_tour_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton('Добавить турнир')
    btn2 = KeyboardButton('Просмотреть все турниры')
    back = KeyboardButton('🔙Вернутся в меню админа')
    kb.add(btn1, btn2, back)

    return kb

def admin_format_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = KeyboardButton('Squad')
    btn2 = KeyboardButton('Duo')
    btn3 = KeyboardButton('TDM')
    back = KeyboardButton('❌Отменить')
    kb.add(btn1,btn2,btn3, back)

    return kb

def confirm_add_tour_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('✅Да', callback_data=tour_cb.new(tour_id, 'confirm_add_tour'))
    btn2 = InlineKeyboardButton('🔁Изменить', callback_data=tour_cb.new(tour_id, 'edit_tour'))
    btn3 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_tour'))
    ikb.add(btn1, btn2, btn3)

    return ikb

def admin_edit_post_tour_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_tour'))
    btn2 = InlineKeyboardButton('🔁Редактировать', callback_data=tour_cb.new(tour_id, 'edit_tour'))
    btn3 = InlineKeyboardButton('🛑Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2, btn3)

    return ikb

tour_cb = CallbackData('data', 'id', 'action')

def admin_edit_kb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🔁Редактировать', callback_data=tour_cb.new(tour_id, 'edit_tour'))
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_tour'))
    ikb.add(btn1, btn2)

    return ikb

def admin_next_tour_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Далее➡️', callback_data='admin_next_tour')
    ikb.add(btn1)

    return ikb


# ADMIN VIP SLOTS
def admin_vip_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton('Добавить слот')
    btn2 = KeyboardButton('Просмотреть все слоты')
    btn3 = KeyboardButton("Удалить все слоты")
    back = KeyboardButton('🔙Вернутся в меню админа')
    kb.add(btn1,btn2, btn3, back)

    return kb

def admin_delete_all_vs_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data='delete_all_vip_slot')
    btn2 = InlineKeyboardButton('❌', callback_data='no_delete_all_vip_slot')
    ikb.add(btn1, btn2)

    return ikb

def admin_chek_vip_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Qualificationㅤ')
    btn2 = KeyboardButton('1/4 STAGEㅤ')
    btn3 = KeyboardButton('1/2 STAGEㅤ')
    btn4 = KeyboardButton('FINAL STAGEㅤ')
    btn5 = KeyboardButton('GRAND-FINAL STAGEㅤ')
    back = KeyboardButton('🔙Вернутся в меню админа')
    kb.add(btn1, btn2, btn3).add(btn4, btn5).add(back)

    return kb

def set_time_vip_slot_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = InlineKeyboardButton('15')
    btn2 = InlineKeyboardButton('18')
    btn3 = InlineKeyboardButton('21')
    btn4 = InlineKeyboardButton('18/21')
    kb.add(btn1, btn2, btn3, btn4)

    return kb

def admin_stage_vip_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton('Qualification')
    btn2 = KeyboardButton('1/4 STAGE')
    btn3 = KeyboardButton('1/2 STAGE')
    btn4 = KeyboardButton('FINAL STAGE')
    btn5 = KeyboardButton('GRAND-FINAL STAGE')
    back = KeyboardButton('❌Отменить')
    kb.add(btn1, btn2, btn3).add(btn4, btn5).add(back)

    return kb

def admin_edit_vip_slot_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🔁Редактировать', callback_data=tour_cb.new(tour_id, 'admin_edit_vip_slot'))
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_vip_slot'))
    btn3 = InlineKeyboardButton('🎬Дублировать', callback_data=tour_cb.new(tour_id, 'double_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb

def admin_confirm_vip_slot_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(tour_id, 'confirm_add_vip_slot'))
    btn2 = InlineKeyboardButton('🔁Изменить', callback_data=tour_cb.new(tour_id, 'admin_edit_vip_slot'))
    btn3 = InlineKeyboardButton('🎬Дублировать', callback_data=tour_cb.new(tour_id, 'double_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb

def admin_edit_post_vip_slot_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_vip_slot'))
    btn2 = InlineKeyboardButton('🔁Редактировать', callback_data=tour_cb.new(tour_id, 'admin_edit_vip_slot'))
    btn3 = InlineKeyboardButton('🛑Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2, btn3)

    return ikb

def admin_next_vip_slot_ikb(stage) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Далее➡️', callback_data=tour_cb.new(stage, 'admin_next_vip_slot'))
    ikb.add(btn1)

    return ikb

def admin_check_pay_vip_slot(check_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(check_id, 'yes_pay_vip_slot'))
    btn2 = InlineKeyboardButton('❌Отклонить', callback_data=tour_cb.new(check_id, 'no_pay_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb

def admin_get_cap_chat_ikb(check_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅CAP CHAT', callback_data=tour_cb.new(check_id, 'get_cap_chat'))
    btn2 = InlineKeyboardButton('❌CAP CHAT', callback_data=tour_cb.new(check_id, 'no_get_cap_chat'))
    ikb.add(btn1, btn2)

    return ikb

def admin_send_reason_vip_ikb(check_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(check_id, 'send_reason_vip_slot'))
    btn2 = InlineKeyboardButton('❌Отменить', callback_data=tour_cb.new(check_id, 'no_send_rsn_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb

def admin_conf_reason_vip_ikb(check_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(check_id, 'conf_send_rsn_vip_slot'))
    btn2 = InlineKeyboardButton('❌Отменить', callback_data=tour_cb.new(check_id, 'no_send_rsn_vip_slot'))
    ikb.add(btn1, btn2)

    return ikb



# ADMIN EVENTS
def admin_menu_event_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton('Добавить ивент')
    btn2 = KeyboardButton('Просмотреть все ивенты')
    back = KeyboardButton('🔙Вернутся в меню админа')
    kb.add(btn1, btn2, back)

    return kb

def admin_next_event_ikb(time) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Далее➡️', callback_data=tour_cb.new(time, "admin_next_event"))
    ikb.add(btn1)

    return ikb

def admin_search_time() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton('🕒15:00ㅤ')
    btn2 = KeyboardButton('🕕18:00ㅤ')
    btn3 = KeyboardButton('🕘21:00ㅤ')
    btn4 = KeyboardButton('🕛00:00ㅤ')
    btn5 = KeyboardButton('🔙Вернутся в меню админа')
    kb.add(btn1, btn2, btn3, btn4, btn5)

    return kb

def admin_put_time() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton('15:00')
    btn2 = KeyboardButton('18:00')
    btn3 = KeyboardButton('21:00')
    btn4 = KeyboardButton('00:00')
    back = KeyboardButton('❌Отменить')
    kb.add(btn1, btn2, btn3, btn4, back)

    return kb

def admin_edit_event_kb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🔁Редактировать', callback_data=tour_cb.new(tour_id, 'edit_event'))
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_event'))
    ikb.add(btn1, btn2)

    return ikb

def conf_add_event_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(tour_id, 'conf_add_event'))
    btn2 = InlineKeyboardButton('🔁Изменить', callback_data=tour_cb.new(tour_id, 'edit_event'))
    ikb.add(btn1, btn2)

    return ikb

def admin_check_pay_event_ikb(check_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(check_id, 'yes_pay_event'))
    btn2 = InlineKeyboardButton('❌Отклонить', callback_data=tour_cb.new(check_id, 'no_pay_event'))
    ikb.add(btn1, btn2)

    return ikb


# ADMIN HELP
def admin_help_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Ответить на вопрос', callback_data='answer')
    btn2 = InlineKeyboardButton('Проигнорировать вопрос', callback_data='ignore')
    ikb.add(btn1, btn2)

    return ikb

def admin_send_ans_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✍️Написать', callback_data='admin_send_ans')
    ikb.add(btn1)

    return ikb


# GENERAL ADMIN
def general_admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('💸UC SHOPㅤ')
    btn2 = KeyboardButton('💳PAYMENTS')
    btn3 = KeyboardButton('🤴ADD ADMIN')
    btn4 = KeyboardButton('🛑BAN/UNBAN')
    btn5 = KeyboardButton('🔍Просмотреть анкеты')
    btn6 = KeyboardButton('ADD 🔥NEWS')
    btn7 = KeyboardButton('📊Статистика')
    btn8 = KeyboardButton('⬆️Сделать рассылку')
    back = KeyboardButton('🔙Вернутся в меню админа')
    kb.add(btn1, btn2, btn3).add(btn4, btn6).add(btn5).add(btn7).add(btn8).add(back)


    return kb


def admin_statistic_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Общая статистика", callback_data="all_statistic")
    btn2 = InlineKeyboardButton("Click user", callback_data="user_click_stat")
    btn3 = InlineKeyboardButton("UC SHOP", callback_data="admin_uc_shop_stat")
    btn4 = InlineKeyboardButton("Free agent", callback_data="free_agent_stat")
    btn5 = InlineKeyboardButton("Free team", callback_data="free_team_stat")
    btn6 = InlineKeyboardButton("Free young agent", callback_data="young_free_agent_stat")
    btn7 = InlineKeyboardButton("Free young team", callback_data="young_free_team_stat")
    close = InlineKeyboardButton("❌Закрыть", callback_data="statistic_count")
    ikb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, close)

    return ikb

def admin_all_click_stat_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ввести число", callback_data="get_random_clickers")
    back = InlineKeyboardButton("Назад", callback_data="back_stat_menu")
    ikb.add(btn1, back)

    return ikb

def admin_free_agent_stat_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ввести число", callback_data="get_random_fa")
    back = InlineKeyboardButton("Назад", callback_data="back_stat_menu")
    ikb.add(btn1, back)

    return ikb


def admin_free_team_stat_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ввести число", callback_data="get_random_ft")
    back = InlineKeyboardButton("Назад", callback_data="back_stat_menu")
    ikb.add(btn1, back)

    return ikb


def admin_young_fa_stat_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ввести число", callback_data="get_random_youngfa")
    back = InlineKeyboardButton("Назад", callback_data="back_stat_menu")
    ikb.add(btn1, back)

    return ikb


def admin_young_ft_stat_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Ввести число", callback_data="get_random_youngft")
    back = InlineKeyboardButton("Назад", callback_data="back_stat_menu")
    ikb.add(btn1, back)

    return ikb

def admin_back_stat_menu_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    back = InlineKeyboardButton("Назад", callback_data="back_stat_menu")
    ikb.add(back)

    return ikb

# AMOUNT USERS

def statistic_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("❌Закрыть", callback_data="statistic_count")
    ikb.add(btn1)

    return ikb



# ADMIN SEND MESS
def conf_add_send_mess_ikb(post_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(post_id, 'conf_add_send_mess'))
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(post_id, 'delete_send_mess'))
    ikb.add(btn1, btn2)

    return ikb

def admin_send_mess() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = InlineKeyboardButton('Пропустить')
    btn2 = InlineKeyboardButton('❌Отменить')
    kb.add(btn1, btn2)

    return kb



# ADD ADMIN
def add_admin_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🤴Добавить админа', callback_data='add_admin')
    btn2 = InlineKeyboardButton('🔍Просмотреть список админов', callback_data='check_admin_list')
    close = InlineKeyboardButton("❌Закрыть", callback_data="statistic_count")
    ikb.add(btn1, btn2, close)

    return ikb

def check_add_admin_ikb(admin_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🔍Просмотреть админ профиль', callback_data=tour_cb.new(admin_id, 'check_admin_profile'))
    back = InlineKeyboardButton('🔙Назад', callback_data='back_general_admin')
    ikb.add(btn1, back)

    return ikb

def type_admin_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton('Moderator')
    btn2 = KeyboardButton('ADMIN')
    back = KeyboardButton('❌Отменить')
    kb.add(btn1, btn2, back)

    return kb

def confirm_add_admin(admin_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅Да', callback_data=tour_cb.new(admin_id, 'yes_add_admin'))
    btn2 = InlineKeyboardButton('🔁Изменить', callback_data=tour_cb.new(admin_id, 'edit_admin_profile'))
    ikb.add(btn1, btn2)

    return ikb


def check_admins(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Редактировать', callback_data=tour_cb.new(tour_id, 'edit_admin_profile'))
    btn2 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(tour_id, 'delete_admin_profile'))
    ikb.add(btn1, btn2)

    return ikb

# BAN
def admin_ban_menu() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('BAN', callback_data='admin_ban_user')
    btn2 = InlineKeyboardButton('UNBAN', callback_data='admin_unban_user')
    close = InlineKeyboardButton("❌Закрыть", callback_data="statistic_count")
    ikb.add(btn1, btn2, close)

    return ikb

def confirm_ban_user(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data=tour_cb.new(user_id, 'confirm_ban_user'))
    btn2 = InlineKeyboardButton('❌', callback_data=tour_cb.new(user_id, 'no_ban_user'))
    ikb.add(btn1, btn2)

    return ikb

def confirm_unban_user_kb(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data=tour_cb.new(user_id, 'confirm_unban_user'))
    btn2 = InlineKeyboardButton('❌', callback_data=tour_cb.new(user_id, 'no_unban_user'))
    ikb.add(btn1, btn2)

    return ikb

def check_users_profile() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Просмотреть анкету по ID', callback_data='select_user')
    btn2 = InlineKeyboardButton('Просмотреть все актуальные анкеты', callback_data='check_all_users')
    close = InlineKeyboardButton("❌Закрыть", callback_data="statistic_count")
    ikb.add(btn1, btn2, close)

    return ikb

def admin_choose_user() -> InlineKeyboardMarkup:
    ikb =InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Free agent', callback_data='admin_choose_agent')
    btn2 = InlineKeyboardButton('Free team', callback_data='admin_choose_team')
    btn3 = InlineKeyboardButton('Prac free agent', callback_data='admin_check_prac_agent')
    btn4 = InlineKeyboardButton('Prac free team', callback_data='admin_check_prac_team')
    ikb.add(btn1, btn2, btn3, btn4)

    return ikb

def admin_next_agent() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Далее➡️', callback_data='admin_next_agent')
    ikb.add(btn1)

    return ikb

def admin_next_team() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Далее➡️', callback_data='admin_next_team')
    ikb.add(btn1)

    return ikb


def admin_edit_user(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(user_id, 'admin_delete_user'))
    btn2 = InlineKeyboardButton('Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2)

    return ikb

def confirm_delete_user(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data=tour_cb.new(user_id, 'confirm_delete_user'))
    btn2 = InlineKeyboardButton('❌', callback_data='no_delete_user')
    ikb.add(btn1, btn2)

    return ikb

def admin_edit_user_team(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(user_id, 'admin_delete_user_team'))
    btn2 = InlineKeyboardButton('Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2)

    return ikb

def confirm_delete_team(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data=tour_cb.new(user_id, 'confirm_delete_team'))
    btn2 = InlineKeyboardButton('❌', callback_data='no_delete_user')
    ikb.add(btn1, btn2)

    return ikb

# ADD NEWS
def admin_news_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Добавить 🔥NEWS', callback_data='admin_add_news')
    btn2 = InlineKeyboardButton('Просмотреть каналы', callback_data='check_news')
    close = InlineKeyboardButton("❌Закрыть", callback_data="statistic_count")
    ikb.add(btn1, btn2, close)

    return ikb

def confirm_add_news(news_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data='confirm_add_news')
    btn2 = InlineKeyboardButton('❌', callback_data=tour_cb.new(news_id, 'delete_news'))
    ikb.add(btn1, btn2)

    return ikb

def delete_news_ikb(news_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(news_id, 'delete_news'))
    ikb.add(btn1)

    return ikb

# ADMIN MUSIC
def admin_music_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Обновить')
    btn2 = KeyboardButton('Загрузить')
    btn3 = KeyboardButton('Просмотреть треки')
    back = KeyboardButton('🔙Вернутся в меню админа')
    kb.add(btn1, btn2).add(btn3).add(back)

    return kb

def admin_kind_music_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton('🔍Вся музыка')
    btn2 = KeyboardButton('🔥Популярная')
    back = KeyboardButton('❌Отменить')
    kb.add(btn2, back)

    return kb

def admin_edit_music_ikb(music_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Редактировать', callback_data=tour_cb.new(music_id, 'edit_music'))
    btn2 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(music_id, 'delete_music'))
    ikb.add(btn1, btn2)

    return ikb

def admin_confirm_music_ikb(music_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(music_id, 'confirm_add_music'))
    btn2 = InlineKeyboardButton('🔁Изменить', callback_data=tour_cb.new(music_id, 'edit_music'))
    btn3 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(music_id, 'delete_music'))
    ikb.add(btn1, btn2, btn3)

    return ikb