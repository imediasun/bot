from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards import tour_cb
from translations import _

def main_young_menu_ikb(lang) -> ReplyKeyboardMarkup:
    ikb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton('📋Practice game')
    btn4 = KeyboardButton('👑VIP Slotsㅤ')
    btn2 = KeyboardButton('👤Free agentㅤ')
    btn3 = KeyboardButton('👥Free teamㅤ')
    btn5 = KeyboardButton('Pablic chats')
    btn6 = KeyboardButton('🔥NEWS')
    btn7 = KeyboardButton(f'💬{_("Поддержка", lang)}')
    btn8 = KeyboardButton('🎶MUSIC')
    btn9 = KeyboardButton('💸UC SHOP')
    ikb.add(btn1, btn4).add(btn2, btn3).add(btn9).add(btn6, btn8).add(btn7)

    return ikb

def info_from_bd(info) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = KeyboardButton(info)
    kb.add(btn)

    return kb


# YOUNG PRACTICE
def next_prac(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_prac')
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
    ikb.add(back, btn1)

    return ikb

def back_young_main_kb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'🔙{_("Главное меню", lang)}', callback_data='back_young_main')
    ikb.add(btn1)

    return ikb

# VIP SLOT PRAC
def vip_prac_time_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(f'🕒{_("15:00", lang)}', callback_data='prac_vip_15')
    btn2 = InlineKeyboardButton(f'🕕{_("18:00", lang)}', callback_data='prac_vip_18')
    btn3 = InlineKeyboardButton(f'🕘{_("21:00", lang)}', callback_data='prac_vip_21')
    btn4 = InlineKeyboardButton(f'🕛{_("00:00", lang)}', callback_data='prac_vip_00')
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
    ikb.add(btn1, btn2, btn3, btn4, back)

    return ikb


def buy_vip_prac_ikb(tour_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(f'💳{_("Купить", lang)}', callback_data=tour_cb.new(tour_id, 'buy_vip_prac'))
    ikb.add(btn)

    return ikb

def next_vip_prac_ikb(time, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data=tour_cb.new(time, 'next_vip_prac'))
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
    ikb.add(back, btn1)

    return ikb

def pay_vip_prac_ikb(pay_id, event_id, lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🧾{_("Отправить чек", lang)}', callback_data=tour_cb.new(pay_id, 'send_check_vip_slot'))
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data=tour_cb.new(event_id, 'back_payment_prac_vip'))
    ikb.add(btn1, back)

    return ikb


def back_vip_prac_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_vip_prac')
    ikb.add(back)

    return ikb

# FREE AGENT
def prac_agent_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✍️{_("Оставить свою анкету", lang)}', callback_data='add_agent_prac')
    btn2 = InlineKeyboardButton(f'🔍{_("Найти команду", lang)}', callback_data='search_prac_team')
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
    ikb.add(btn1, btn2, back)

    return ikb

def finish_prac_agent_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(f'✅{_("Да", lang)}', callback_data='yes_prac_agent')
    btn2 = InlineKeyboardButton(f'🔁{_("Изменить", lang)}', callback_data='change_prac_agent')
    btn3 = InlineKeyboardButton(f'🗑{_("Удалить", lang)}', callback_data='delete_prac_agent')
    ikb.add(btn1, btn2, btn3)

    return ikb

def send_prac_agent_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🔍{_("Найти команду", lang)}', callback_data='search_prac_team')
    back = InlineKeyboardButton(f'🔙{_("Главное меню", lang)}', callback_data='back_young_main')
    ikb.add(btn1, back)

    return ikb

def next_prac_team(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_prac_team')
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
    ikb.add(back, btn1)

    return ikb


# FREE TEAM
def prac_team_main_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'✍️{_("Оставить анкету о поиске игрока", lang)}', callback_data='add_team_prac')
    btn2 = InlineKeyboardButton(f'🔍{_("Найти игрока", lang)}', callback_data='search_prac_agent')
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
    ikb.add(btn1, btn2, back)

    return ikb

def finish_prac_team_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(f'✅{_("Да", lang)}', callback_data='yes_prac_team')
    btn2 = InlineKeyboardButton(f'🔁{_("Изменить", lang)}', callback_data='change_prac_team')
    btn3 = InlineKeyboardButton(f'🗑{_("Удалить", lang)}', callback_data='delete_prac_team')
    ikb.add(btn1, btn2, btn3)

    return ikb

def send_prac_team_ikb(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(f'🔍{_("Найти игрока", lang)}', callback_data='search_prac_agent')
    back = InlineKeyboardButton(f'🔙{_("Главное меню", lang)}', callback_data='back_young_main')
    ikb.add(btn1, back)

    return ikb

def next_prac_agent(lang) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{_("Далее", lang)}➡️', callback_data='next_prac_agent')
    back = InlineKeyboardButton(f'🔙{_("Назад", lang)}', callback_data='back_young_main')
    ikb.add(back, btn1)

    return ikb


# ADMIN PRACTICE GAME
def admin_prac_game_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Добавить праки', callback_data='add_prac')
    btn2 = InlineKeyboardButton('Просмотреть все праки', callback_data='check_all_pracs')
    ikb.add(btn1, btn2)

    return ikb

def admin_edit_prac_kb(prac_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Редактировать', callback_data=tour_cb.new(prac_id, 'edit_young_prac'))
    btn2 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(prac_id, 'delete_young_prac'))
    ikb.add(btn1, btn2)

    return ikb

def admin_confirm_add_prac_ikb(prac_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('✅Да', callback_data=tour_cb.new(prac_id, 'confirm_add_prac'))
    btn2 = InlineKeyboardButton('🔁Изменить', callback_data=tour_cb.new(prac_id, 'edit_young_prac'))
    btn3 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(prac_id, 'delete_young_prac'))
    ikb.add(btn1, btn2, btn3)

    return ikb

def admin_edit_post_prac_ikb(prac_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(prac_id, 'delete_tour'))
    btn2 = InlineKeyboardButton('Редактировать', callback_data=tour_cb.new(prac_id, 'edit_tour'))
    btn3 = InlineKeyboardButton('Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2, btn3)

    return ikb


# ADMIN VIP PRAC
def admin_check_vip_prac_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Добавить слот', callback_data='add_vip_prac')
    btn2 = InlineKeyboardButton('Просмотреть все слоты', callback_data='check_all_vip_pracs')
    ikb.add(btn1, btn2)

    return ikb

def admin_edit_vip_prac_kb(prac_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🔁Редактировать', callback_data=tour_cb.new(prac_id, 'edit_vip_prac'))
    btn2 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(prac_id, 'delete_vip_prac'))
    ikb.add(btn1, btn2)

    return ikb

def conf_add_vip_prac_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('✅Подтвердить', callback_data=tour_cb.new(tour_id, 'conf_add_vip_prac'))
    btn2 = InlineKeyboardButton('🔁Изменить', callback_data=tour_cb.new(tour_id, 'edit_vip_prac'))
    btn3 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_vip_prac'))
    ikb.add(btn1, btn2, btn3)

    return ikb

def admin_edit_post_vip_prac_ikb(tour_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🗑Удалить', callback_data=tour_cb.new(tour_id, 'delete_vip_prac'))
    btn2 = InlineKeyboardButton('🔁Редактировать', callback_data=tour_cb.new(tour_id, 'edit_vip_prac'))
    btn3 = InlineKeyboardButton('🛑Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2, btn3)

    return ikb

def admin_time_vip_prac_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton('🕒15:00', callback_data='admin_prac_vip_15')
    btn2 = InlineKeyboardButton('🕕18:00', callback_data='admin_prac_vip_18')
    btn3 = InlineKeyboardButton('🕘21:00', callback_data='admin_prac_vip_21')
    btn4 = InlineKeyboardButton('🕛00:00', callback_data='admin_prac_vip_00')
    back = InlineKeyboardButton('🔙Назад', callback_data='delete')
    ikb.add(btn1, btn2, btn3, btn4, back)

    return ikb

# ADMIN BAN
def admin_next_prac_agent() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Далее➡️', callback_data='admin_next_prac_agent')
    ikb.add(btn1)

    return ikb

def admin_next_prac_team() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Далее➡️', callback_data='admin_next_prac_team')
    ikb.add(btn1)

    return ikb

def admin_prac_edit_user(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(user_id, 'admin_prac_delete_user'))
    btn2 = InlineKeyboardButton('Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2)

    return ikb

def confirm_delete_prac_user(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data=tour_cb.new(user_id, 'confirm_delete_prac_user'))
    btn2 = InlineKeyboardButton('❌', callback_data='no_delete_user')
    ikb.add(btn1, btn2)

    return ikb

def admin_edit_prac_user_team(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('Удалить', callback_data=tour_cb.new(user_id, 'admin_delete_prac_user_team'))
    btn2 = InlineKeyboardButton('Заблокировать', callback_data='admin_ban_user')
    ikb.add(btn1, btn2)

    return ikb

def confirm_delete_prac_team(user_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('✅', callback_data=tour_cb.new(user_id, 'confirm_delete_prac_team'))
    btn2 = InlineKeyboardButton('❌', callback_data='no_delete_user')
    ikb.add(btn1, btn2)

    return ikb