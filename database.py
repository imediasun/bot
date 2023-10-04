import sqlite3 as sq
import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def db_start():
    global db, cur

    db = sq.connect('pubgbot.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS language("
                "user_id INTEGER PRIMARY KEY,"
                "language TEXT,"
                "currency TEXT,"
                "block INTEGER,"
                "reason TEXT,"
                "ban_time TEXT,"
                "profile TEXT,"
                "amount_clicks INTEGER,"
                "time_log TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS info_player("
                "user_id INTEGER PRIMARY KEY,"
                "nickname TEXT,"
                "age TEXT,"
                "teamspeak TEXT,"
                "teamspeak1 TEXT,"
                "device TEXT,"
                "tournament TEXT,"
                "finals TEXT,"
                "highilights TEXT,"
                "description TEXT,"
                "contact TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS young_player("
                "user_id INTEGER PRIMARY KEY,"
                "nickname TEXT,"
                "age TEXT,"
                "teamspeak TEXT,"
                "teamspeak1 TEXT,"
                "device TEXT,"
                "practice_game TEXT,"
                "highilights TEXT,"
                "description TEXT,"
                "contact TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS info_team("
                "user_id INTEGER PRIMARY KEY,"
                "team_name TEXT,"
                "age TEXT,"
                "teamspeak TEXT,"
                "teamspeak1 TEXT,"
                "role TEXT,"
                "device TEXT,"
                "tournament TEXT,"
                "finals TEXT,"
                "description TEXT,"
                "contact TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS young_team("
                "user_id INTEGER PRIMARY KEY,"
                "team_name TEXT,"
                "age TEXT,"
                "teamspeak TEXT,"
                "teamspeak1 TEXT,"
                "role TEXT,"
                "device TEXT,"
                "practice_game TEXT,"
                "description TEXT,"
                "contact TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS info_tour("
                "tour_id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "format TEXT,"
                "photo TEXT,"
                "desc TEXT,"
                "url TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS practice_game("
                "prac_id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "photo TEXT,"
                "desc TEXT,"
                "url TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS vip_slots("
                "tour_id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "stage TEXT,"
                "photo TEXT,"
                "desc TEXT,"
                "price INTEGER,"
                "tour_name TEXT,"
                "ds_link TEXT,"
                "time TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS available_vip_slots("
                "tour_id TEXT,"
                "time TEXT,"
                "amount_busy INTEGER,"
                "amount INTEGER)")

    cur.execute("CREATE TABLE IF NOT EXISTS prac_vip_slot("
                "tour_id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "time TEXT,"
                "photo TEXT,"
                "price TEXT,"
                "desc TEXT,"
                "tour_name TEXT,"
                "link TEXT,"
                "amount INTEGER,"
                "amount2 INTEGER)")

    cur.execute("CREATE TABLE IF NOT EXISTS events("
                "tour_id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "time TEXT,"
                "photo TEXT,"
                "price TEXT,"
                "desc TEXT,"
                "tour_name TEXT,"
                "link TEXT,"
                "amount INTEGER,"
                "amount2 INTEGER)")

    cur.execute("CREATE TABLE IF NOT EXISTS payments("
                "id INTEGER PRIMARY KEY,"
                "user_id INTEGER,"
                "bank TEXT,"
                "card TEXT,"
                "currency TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS uc_package("
                "id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "photo TEXT,"
                "price TEXT,"
                "amount_uc TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS buy_vip_slot("
                "id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "username TEXT,"
                "proof TEXT,"
                "proof_d TEXT,"
                "amount TEXT,"
                "currency TEXT,"
                "bank TEXT,"
                "pay_number TEXT,"
                "vip_slot_id TEXT,"
                "format TEXT,"
                "logo TEXT,"
                "logo_d TEXT,"
                "team_name TEXT,"
                "team_tag TEXT,"
                "cap TEXT,"
                "reason TEXT,"
                "time TEXT,"
                "buy_time TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS buy_uc("
                "id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "proof TEXT,"
                "proof_d TEXT,"
                "amount TEXT,"
                "currency TEXT,"
                "amount_uc TEXT,"
                "bank TEXT,"
                "pay_number TEXT,"
                "user_name TEXT,"
                "game_id TEXT,"
                "nick TEXT,"
                "reason TEXT,"
                "buy_time TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS news("
                "news_id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "text TEXT,"
                "url TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS admin_table("
                "admin_id INTEGER PRIMARY KEY,"
                "user_id INTEGER,"
                "admin_username TEXT,"
                "job_title TEXT,"
                "type TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS music("
                "id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "artist TEXT,"
                "music_name TEXT,"
                "file BLOB,"
                "kind TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS rate("
                "currency TEXT PRIMARY KEY,"
                "amount TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS send_mess("
                "id TEXT PRIMARY KEY,"
                "user_id INTEGER,"
                "desc TEXT,"
                "photo TEXT,"
                "link TEXT,"
                "active TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS uc_active("
                "id INTEGER PRIMARY KEY,"
                "user_id INTEGER,"
                "active INTEGER,"
                "reason TEXT,"
                "photo TEXT,"
                "text TEXT)")
    db.commit()


# LANGUAGE
async def create_lang(user_id):
    time_log = datetime.datetime.now()
    user = cur.execute("SELECT 1 FROM language WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO language VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, '', '', 0, 0, 0, '', 1, time_log))
    db.commit()


async def edit_lang(state, currency, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE language SET language = ?, currency = ? WHERE user_id = ?",
                    (data['language'], currency, user_id))
    db.commit()


async def update_profile(profile, user_id):
    cur.execute("UPDATE language SET profile = ? WHERE user_id = ?", (profile, user_id))
    db.commit()


async def get_user_lang(user_id):
    lang = cur.execute("SELECT language FROM language WHERE user_id = ?", (user_id,)).fetchone()
    if not lang:
        return None
    else:
        return lang[0]


async def get_lang_name(user_id):
    lang = cur.execute("SELECT language FROM language WHERE user_id = ?", (user_id,)).fetchone()[0]
    if lang == 'uk':
        return "🇺🇦Українська"
    elif lang == 'en':
        return "🇬🇧English"
    elif lang == 'ru':
        return "Русский"
    elif lang == 'uz':
        return "🇺🇿O'zbek"
    elif lang == 'kz':
        return "🇰🇿Қазақ"


async def get_region_currency(lang):
    return cur.execute("SELECT currency FROM language WHERE language = ?", (lang,)).fetchone()[0]


async def get_profile(user_id):
    return cur.execute("SELECT profile FROM language WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_user_ids():
    results = cur.execute("SELECT user_id FROM language").fetchall()
    user_ids = [result[0] for result in results]  # Генератор списков для извлечения значений
    return user_ids


async def get_amount_all_users():
    users = cur.execute("SELECT COUNT(DISTINCT user_id) FROM language").fetchall()[0]
    for data in users:
        return data


async def get_amount_free_teams():
    teams = cur.execute("SELECT COUNT(DISTINCT user_id) FROM info_team").fetchall()[0]
    for data in teams:
        return data


async def get_amount_free_agents():
    agents = cur.execute("SELECT COUNT(DISTINCT user_id) FROM info_player").fetchall()[0]
    for data in agents:
        return data


async def get_random_users(sum, table):
    return cur.execute(f"SELECT * FROM {table} ORDER BY RANDOM() LIMIT {sum}").fetchall()


async def get_amount_free_teams_p():
    agents = cur.execute("SELECT COUNT(DISTINCT user_id) FROM young_team").fetchall()[0]
    for data in agents:
        return data


async def get_amount_free_agents_p():
    agents = cur.execute("SELECT COUNT(DISTINCT user_id) FROM young_player").fetchall()[0]
    for data in agents:
        return data


# CLICKS
async def get_amount_click(user_id):
    return cur.execute("SELECT amount_clicks FROM language WHERE user_id = ?", (user_id,)).fetchone()[0]


async def update_click(amount_click, user_id):
    cur.execute("UPDATE language SET amount_clicks = ? WHERE user_id = ?", (amount_click, user_id,))
    db.commit()


async def get_sum_click_users():
    return cur.execute("SELECT SUM(amount_clicks) FROM language").fetchone()[0]


async def get_top_clickers(sum):
    return cur.execute(f"SELECT * FROM language ORDER BY amount_clicks DESC LIMIT {sum}").fetchall()


# LOG TIME
async def insert_time_log(user_id):
    time_now = datetime.datetime.now()
    time_log = cur.execute("SELECT time_log FROM language WHERE user_id = ?", (user_id,)).fetchone()[0]
    if not time_log:
        cur.execute("UPDATE language SET time_log = ? WHERE user_id = ?", (time_now, user_id,))


async def get_time_log():
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_week = datetime.datetime.now().strftime("%W")
    now_day = datetime.datetime.now().day
    year = cur.execute("SELECT COUNT(DISTINCT time_log) FROM language WHERE strftime('%Y', time_log) = ?",
                       (str(now_year),)).fetchone()[0]
    month = cur.execute("SELECT COUNT(DISTINCT time_log) FROM language WHERE strftime('%Y-%m', time_log) = ?",
                        (str(f"{now_year}-{now_month:02}"),)).fetchone()[0]
    week = cur.execute("SELECT COUNT(DISTINCT time_log) FROM language WHERE strftime('%W', time_log) = ?",
                       (str(now_week),)).fetchone()[0]
    day = cur.execute("SELECT COUNT(DISTINCT time_log) FROM language WHERE strftime('%Y-%m-%d', time_log) = ?",
                       (str(f"{now_year}-{now_month:02}-{now_day:02}"),)).fetchone()[0]
    return [year, month, week, day]

# STATISTIC BUY VIP SLOTS/EVENTS
async def update_buy_time(tour_id):
    time = datetime.datetime.now()
    cur.execute("UPDATE buy_vip_slot SET buy_time = ? WHERE id = ?", (time, tour_id))
    db.commit()

async def get_all_payment_vip_slots():
    return cur.execute("SELECT COUNT(DISTINCT team_name) FROM buy_vip_slot").fetchone()[0]

async def get_payment_vip_slot(format):
    return cur.execute("SELECT COUNT(DISTINCT team_name) FROM buy_vip_slot WHERE format = ?", (format,)).fetchone()[0]

async def get_time_payment_vip_slot(format):
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_week = datetime.datetime.now().strftime("%W")
    now_day = datetime.datetime.now().day

    periods = [now_year, f"{now_year}-{now_month:02}", now_week, f"{now_year}-{now_month:02}-{now_day:02}"]
    times = ["%Y", "%Y-%m", "%W", "%Y-%m-%d"]
    counts = []

    for period, time in zip(periods, times):
        amount = cur.execute(f"SELECT COUNT(DISTINCT buy_time) FROM buy_vip_slot "
                             f"WHERE strftime('{time}', buy_time) = '{period}'"
                             "AND team_name IS NOT NULL AND format = ?",
                             (format,)).fetchone()
        if not amount:
            amount = "Нету"
        counts.append(amount[0])
    for period, time in zip(periods, times):
        peak_time = cur.execute(f"SELECT time FROM buy_vip_slot "
                                f"WHERE strftime('{time}', buy_time) = '{period}' "
                                f"AND format = ? AND team_name IS NOT NULL "
                                f"GROUP BY time "
                                f"ORDER BY COUNT(*) DESC "
                                f"LIMIT 1",
                                (format,)).fetchone()
        if not peak_time:
            peak_time = "Нету"
        counts.append(peak_time[0])
    return counts

# STATISTIC UC SHOP
async def update_buy_time_uc(uc_id):
    time = datetime.datetime.now()
    cur.execute("UPDATE buy_uc SET buy_time = ? WHERE id = ?", (time, uc_id))
    db.commit()

async def get_all_payment_uc_shop():
    return cur.execute("SELECT COUNT(DISTINCT game_id) FROM buy_uc").fetchone()[0]

async def get_time_payment_uc_shop():
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    now_week = datetime.datetime.now().strftime("%W")
    now_day = datetime.datetime.now().day

    periods = [now_year, f"{now_year}-{now_month:02}", now_week, f"{now_year}-{now_month:02}-{now_day:02}"]
    times = ["%Y", "%Y-%m", "%W", "%Y-%m-%d"]
    counts = []

    for period, time in zip(periods, times):
        amount = cur.execute(f"SELECT COUNT(DISTINCT buy_time) FROM buy_uc "
                             f"WHERE strftime('{time}', buy_time) = '{period}' AND game_id IS NOT NULL").fetchone()
        if not amount:
            amount = "Нету"
        counts.append(amount[0])
    peak_time = cur.execute("SELECT strftime('%H:%M', buy_time) "
                            "FROM buy_uc "
                            "WHERE strftime('%Y-%m-%d', buy_time) = ? "
                            "GROUP BY buy_time "
                            "LIMIT 1", (now_day,)).fetchone()
    print(peak_time)
    # for period, time in zip(periods, times):
    #     peak_time = cur.execute(f"SELECT strftime('{time}', buy_time) FROM buy_uc "
    #                             f"WHERE strftime('{time}', buy_time) = '{period}'").fetchone()
    #     if not peak_time:
    #         peak_time = "Нету"
    #     counts.append(peak_time[0])
    return counts


# ADMIN PAY
async def create_pay(card_id, user_id):
    cur.execute("INSERT INTO payments(id, user_id, bank, card, currency) VALUES(?, ?, ?, ?, ?)",
                (card_id, user_id, '', '', ''))
    db.commit()


async def update_pay(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE payments SET user_id = ?, bank = ?, card = ?, currency = ? WHERE id = ?",
                    (user_id, data['bank'], data['card'], data['currency'], data['card_id']))
    db.commit()


async def check_pay():
    return cur.execute("SELECT * FROM payments").fetchall()


async def delete_pay(tour_id):
    cur.execute("DELETE FROM payments WHERE id = ?", (tour_id,))
    db.commit()


# FREE AGENT
async def create_agent(user_id):
    user = cur.execute("SELECT 1 FROM info_player WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO info_player VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (user_id, '', '', '', '', '', '', '', '', '', ''))
    db.commit()


async def edit_agent(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            """UPDATE info_player SET nickname = ?, age = ?, teamspeak = ?, teamspeak1 = ?, device = ?, tournament = ?, finals = ?, highilights = ?, description = ?, contact = ? WHERE user_id = ?""",
            (data['nickname'], data['age'], data["teamspeak"], data["teamspeak1"], data['device'], data['tournament'],
             data['finals'], data['highilights'], data['description'], data['contact'], user_id))
        db.commit()


index = 0


async def search_agent():
    return cur.execute("SELECT * FROM info_player").fetchall()


async def delete_profile(user_id):
    cur.execute("DELETE FROM info_player WHERE user_id = ?", (user_id,))
    db.commit()


async def get_agent_profile(user_id):
    return cur.execute("SELECT * FROM info_player WHERE user_id = ?", (user_id,)).fetchall()


async def get_nickname_agent(user_id):
    return cur.execute("SELECT nickname FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_age_agent(user_id):
    return cur.execute("SELECT age FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_role_agent(user_id):
    return cur.execute("SELECT role FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_device_agent(user_id):
    return cur.execute("SELECT device FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_tournament_agent(user_id):
    return cur.execute("SELECT tournament FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_finals_agent(user_id):
    return cur.execute("SELECT finals FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_hl_agent(user_id):
    return cur.execute("SELECT highilights FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_desc_agent(user_id):
    return cur.execute("SELECT description FROM info_player WHERE user_id = ?", (user_id,)).fetchone()[0]


# FREE TEAM
async def create_team_profile(user_id):
    team = cur.execute("SELECT 1 FROM info_team WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not team:
        cur.execute("INSERT INTO info_team VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, '', '', '', '', '', '', '', '', '', ''))
    db.commit()


async def update_team_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            """UPDATE info_team SET team_name = ?, age = ?, teamspeak = ?, teamspeak = ?, role = ?, device = ?, tournament = ?, finals = ?, description = ?, contact = ? WHERE user_id = ?""",
            (data['team_name'], data['age'], data["teamspeak"], data["teamspeak1"], data['role'], data['device'],
             data['tournament'], data['finals'], data['description'], data['contact'], user_id))
    db.commit()


async def delete_team_profile(user_id):
    cur.execute("DELETE FROM info_team WHERE user_id = ?", (user_id,))
    db.commit()


async def select_team_profile():
    return cur.execute("SELECT * FROM info_team").fetchall()


async def get_team_profile(user_id):
    return cur.execute("SELECT * FROM info_team WHERE user_id = ?", (user_id,)).fetchall()


async def get_team_name(user_id):
    return cur.execute("SELECT team_name FROM info_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_age_team(user_id):
    return cur.execute("SELECT age FROM info_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_role_team(user_id):
    return cur.execute("SELECT role FROM info_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_device_team(user_id):
    return cur.execute("SELECT device FROM info_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_tournament_team(user_id):
    return cur.execute("SELECT tournament FROM info_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_finals_team(user_id):
    return cur.execute("SELECT finals FROM info_team WHERE user_id = ?", (user_id,)).fetchone()[0]


# TOURNAMENT
async def create_tour(state, user_id, tour_id):
    async with state.proxy() as data:
        cur.execute("INSERT INTO info_tour (tour_id, user_id, format, photo, desc, url) VALUES(?, ?, ?, ?, ?, ?)",
                    (tour_id, user_id, data['format'], data['photo'], data['desc'], data['url']))
    db.commit()


async def get_tours(format):
    return cur.execute("SELECT * FROM info_tour WHERE format = ?", (format,)).fetchall()


async def admin_read_tour():
    return cur.execute("SELECT * FROM info_tour").fetchall()


async def delete_tour(tour_id: int):
    cur.execute("DELETE FROM info_tour WHERE tour_id = ?", (tour_id,))
    db.commit()


async def get_banner_tour(tour_id):
    return cur.execute("SELECT photo FROM info_tour WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_tour_desc(tour_id):
    return cur.execute("SELECT desc FROM info_tour WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_tour_url(tour_id):
    return cur.execute("SELECT url FROM info_tour WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def admin_update_tour(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE info_tour SET user_id = ?, format = ?, photo = ?, desc = ?, url = ? WHERE tour_id = ?",
                    (user_id, data['format'], data['photo'], data['desc'], data['url'], data['tour_id'],))
    db.commit()


async def admin_get_tour(tour_id):
    return cur.execute("SELECT * FROM info_tour WHERE tour_id = ?", (tour_id,)).fetchall()


# ADMIN VIP SLOTS
async def create_vip_slots(state, user_id, tour_id, times, amounts):
    number = 0
    async with state.proxy() as data:
        cur.execute("INSERT INTO vip_slots (tour_id, user_id, stage, photo, desc, price, tour_name, ds_link)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (tour_id, user_id, data['stage'], data['photo'], data['desc'], data['price'], data['tour_name'],
                     data['link']))
    for time in times:
        cur.execute("INSERT INTO available_vip_slots(tour_id, time, amount_busy, amount) VALUES(?, ?, ?, ?)",
                    (tour_id, time, amounts[number], amounts[number]))
        number +=1
    db.commit()

async def update_vip_slots(state, user_id, times, amounts):
    number = 0
    async with state.proxy() as data:
        cur.execute("UPDATE vip_slots SET user_id = ?, stage = ?, photo = ?, desc = ?, price = ?, tour_name = ?"
                    "WHERE tour_id = ?",
                    (user_id, data['stage'], data['photo'], data['desc'], data['price'], data['tour_name'],
                     data['tour_id']))
        cur.execute("DELETE FROM available_vip_slots WHERE tour_id = ?", (data['tour_id'],))
    for time in times:
        cur.execute("INSERT INTO available_vip_slots(tour_id, time, amount_busy, amount) VALUES(?, ?, ?, ?)",
                    (data['tour_id'], time, amounts[number], amounts[number]))
        number +=1
    db.commit()

async def update_amount_vip_slot(tour_id, time, amount):
    cur.execute("UPDATE available_vip_slots SET amount_busy = ? WHERE tour_id = ? AND time = ?",
                (amount, tour_id, time))
    db.commit()


async def update_amount2_vip_slot(tour_id, time, amount):
    cur.execute("UPDATE available_vip_slots SET amount = ? WHERE tour_id = ? AND time = ?", (amount, tour_id, time))
    db.commit()


async def get_vip_slot(tour_id):
    return cur.execute("SELECT * FROM vip_slots WHERE tour_id = ?", (tour_id,)).fetchall()

async def get_vip_slots(stage):
    vip_slots = cur.execute("SELECT * FROM vip_slots WHERE stage = ?", (stage,)).fetchall()
    slots = []
    for data in vip_slots:
        amount_slots = cur.execute("SELECT amount_busy FROM available_vip_slots WHERE tour_id = ?",
                                   (data[0],)).fetchall()
        total_amount_slots = sum(amount[0] for amount in amount_slots)
        if total_amount_slots != 0:
            slots.append(data)
    return slots


async def get_price_vip_slot(tour_id):
    return cur.execute("SELECT price FROM vip_slots WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_name_tour_vip_slot(tour_id):
    return cur.execute("SELECT tour_name FROM vip_slots WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_stage_vip_slot(tour_id):
    return cur.execute("SELECT stage FROM vip_slots WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_desc_vip_slot(tour_id):
    return cur.execute("SELECT desc FROM vip_slots WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_link_vip_slot(tour_id):
    return cur.execute("SELECT ds_link FROM vip_slots WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_time_vip_slot_str(tour_id):
    tuple_time = cur.execute('SELECT time FROM available_vip_slots WHERE tour_id = ?', (tour_id,)).fetchall()
    list_time = [str(num[0]) for num in tuple_time]
    time_str = '/'.join(list_time)
    return time_str

async def get_amount_vip_slots_str(tour_id):
    tuples_amount = cur.execute("SELECT amount_busy FROM available_vip_slots WHERE tour_id = ?", (tour_id,)).fetchall()
    list_amount = [str(num[0]) for num in tuples_amount]
    amount_str = '/'.join(list_amount)
    return amount_str

async def get_amount_vip_slot(tour_id):
    return cur.execute("SELECT amount_busy FROM available_vip_slots WHERE tour_id = ?", (tour_id,)).fetchall()

async def get_amount_vip_slot_time(tour_id, time):
    return cur.execute("SELECT amount_busy FROM available_vip_slots WHERE tour_id = ? AND time = ?",
                       (tour_id, time)).fetchone()[0]

async def get_times_vip_slot(tour_id):
    return cur.execute("SELECT time FROM available_vip_slots WHERE tour_id = ? AND amount_busy != 0",
                       (tour_id,)).fetchall()

async def get_amount2_vip_slot(tour_id):
    return cur.execute("SELECT amount FROM available_vip_slots WHERE tour_id = ?", (tour_id,)).fetchall()

async def get_amount2_vip_slot_time(tour_id, time):
    return cur.execute("SELECT amount FROM available_vip_slots WHERE tour_id = ? AND time = ?",
                       (tour_id, time)).fetchone()[0]

async def get_photo_vip_slot(tour_id):
    return cur.execute("SELECT photo FROM vip_slots WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def delete_all_vip_slot():
    cur.execute("UPDATE available_vip_slots SET amount_busy = 0")
    cur.execute("UPDATE events SET amount = 0")
    cur.execute("UPDATE prac_vip_slot SET amount = 0")
    db.commit()


# PAY VIP SLOT
async def create_pay_vip_slot(pay_id, user_id, format, username):
    cur.execute("INSERT INTO buy_vip_slot(id, user_id, format, username) VALUES(?, ?, ?, ?)",
                (pay_id, user_id, format, username))
    db.commit()


async def update_pay_vip_slot(pay_id, pay_number, tour_id, bank, amount, currency, time):
    cur.execute("UPDATE buy_vip_slot SET amount = ?, currency = ?, bank = ?, pay_number = ?, vip_slot_id = ?, "
                "time = ? WHERE id = ?",
        (amount, currency, bank, pay_number, tour_id, time, pay_id))
    db.commit()


async def update_pay_proof_vip_slot(proof, tour_id):
    cur.execute("UPDATE buy_vip_slot SET proof = ? WHERE id = ?", (proof, tour_id))
    db.commit()


async def update_pay_proof_d_vip_slot(proof_d, tour_id):
    cur.execute("UPDATE buy_vip_slot SET proof_d = ? WHERE id = ?", (proof_d, tour_id))
    db.commit()


async def get_check_vip_slot(check_id):
    return cur.execute("SELECT * FROM buy_vip_slot WHERE id = ?", (check_id,)).fetchall()


async def update_text_info_vip_slot(state):
    async with state.proxy() as data:
        cur.execute("UPDATE buy_vip_slot SET team_name = ?, team_tag = ?, cap = ? WHERE id = ?",
                    (data['team_name'], data['team_tag'], data['cap'], data['check_id']))
        db.commit()


async def update_info_for_vip_slot(state):
    async with state.proxy() as data:
        cur.execute("UPDATE buy_vip_slot SET logo = ?, team_name = ?, team_tag = ?, cap = ? WHERE id = ?",
                    (data['logo'], data['team_name'], data['team_tag'], data['cap'], data['check_id']))
    db.commit()


async def update_info_d_for_vip_slot(state):
    async with state.proxy() as data:
        cur.execute("UPDATE buy_vip_slot SET logo_d = ?, team_name = ?, team_tag = ?, cap = ? WHERE id = ?",
                    (data['logo'], data['team_name'], data['team_tag'], data['cap'], data['check_id']))
    db.commit()


async def update_reason_vip_slot(state):
    async with state.proxy() as data:
        cur.execute("UPDATE buy_vip_slot SET reason = ? WHERE id = ?", (data['reason'], data['check_id']))
    db.commit()


async def delete_vip_slot(tour_id):
    cur.execute("DELETE FROM vip_slots WHERE tour_id = ?", (tour_id,))
    cur.execute("DELETE FROM available_vip_slots WHERE tour_id = ?", (tour_id,))
    db.commit()


# EVENTS
async def create_pay_event(pay_id, user_id, format, username):
    cur.execute("INSERT INTO buy_vip_slot(id, user_id, format,  username) VALUES(?, ?, ?, ?)",
                (pay_id, user_id, format, username))
    db.commit()


async def get_format_check(check_id):
    return cur.execute("SELECT format FROM buy_vip_slot WHERE id = ?", (check_id,)).fetchone()[0]


async def get_events(time):
    return cur.execute("SELECT * FROM events WHERE time = ? AND amount != 0", (time,)).fetchall()


async def get_price_event(tour_id):
    return cur.execute("SELECT price FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_event_name(tour_id):
    return cur.execute("SELECT tour_name FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_time_event(tour_id):
    return cur.execute("SELECT time FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_desc_event(tour_id):
    return cur.execute("SELECT desc FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_link_event(tour_id):
    return cur.execute("SELECT link FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_photo_event(tour_id):
    return cur.execute("SELECT photo FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


# ADMIN EVENTS
async def create_events(state, tour_id, user_id):
    async with state.proxy() as data:
        cur.execute(
            "INSERT INTO events (tour_id, user_id, time, photo, price, desc, tour_name, link, amount, amount2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
            tour_id, user_id, data['time'], data['photo'], data['price'], data['desc'], data['tour_name'], data['link'],
            data['amount'], data['amount']))
    db.commit()


async def update_event(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            "UPDATE events SET user_id = ?, time = ?, photo = ?, price = ?, desc = ?, tour_name = ?, link = ?, amount = ?, amount2 = ? WHERE tour_id = ?",
            (user_id, data['time'], data['photo'], data['price'], data['desc'], data['tour_name'], data['link'],
             data['amount'], data['amount'], data['tour_id']))
    db.commit()


async def get_all_events():
    return cur.execute("SELECT * FROM events WHERE amount != 0").fetchall()


async def get_event(tour_id):
    return cur.execute("SELECT * FROM events WHERE tour_id = ?", (tour_id,)).fetchall()


async def get_amount_events(tour_id):
    return cur.execute("SELECT amount FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_amount2_events(tour_id):
    return cur.execute("SELECT amount2 FROM events WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def update_amount_event(tour_id, amount):
    cur.execute("UPDATE events SET amount = ? WHERE tour_id = ?", (amount, tour_id))
    db.commit()


async def update_amount2_event(tour_id, amount):
    cur.execute("UPDATE events SET amount2 = ? WHERE tour_id = ?", (amount, tour_id))
    db.commit()


async def delete_event(tour_id: int):
    cur.execute("DELETE FROM events WHERE tour_id = ?", (tour_id,))
    db.commit()


# BUY UC
async def create_payment(id, user_id, user_name):
    cur.execute(
        "INSERT INTO buy_uc(id, user_id, user_name, proof, proof_d, amount, currency, amount_uc, bank, pay_number) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (id, user_id, user_name, '', '', '', '', '', '', ''))
    db.commit()


async def update_payment_info(amount, currency, amount_uc, id, bank, pay_number):
    cur.execute("UPDATE buy_uc SET amount = ?, currency = ?, amount_uc = ?, bank = ?, pay_number = ? WHERE id = ?",
                (amount, currency, amount_uc, bank, pay_number, id))
    db.commit()


async def update_payment_d(proof, id):
    cur.execute("UPDATE buy_uc SET proof_d = ? WHERE id = ?", (proof, id))
    db.commit()


async def update_payment(proof, id):
    cur.execute("UPDATE buy_uc SET proof = ? WHERE id = ?", (proof, id))
    db.commit()


async def get_check_uc(id):
    return cur.execute("SELECT * FROM buy_uc WHERE id = ?", (id,)).fetchall()


async def update_pay_info(state):
    async with state.proxy() as data:
        cur.execute("UPDATE buy_uc SET game_id = ?, nick = ? WHERE id = ?",
                    (data['game_id'], data['nick'], data['uc_id']))
    db.commit()


async def update_reason_uc(reason, check_id):
    cur.execute("UPDATE buy_uc SET reason = ? WHERE id = ?", (reason, check_id))
    db.commit()


# UC SHOP
async def select_uc():
    return cur.execute("SELECT * FROM uc_package").fetchall()


async def get_payment():
    return cur.execute("SELECT * FROM payments").fetchall()


async def get_card(id):
    return cur.execute("SELECT * FROM payments WHERE id = ?", (id,)).fetchall()


async def get_uc_pack(id):
    return cur.execute("SELECT * FROM uc_package WHERE id = ?", (id,)).fetchall()


async def get_price_uc(id):
    return cur.execute("SELECT price FROM uc_package WHERE id = ?", (id,)).fetchone()[0]


async def get_amount_uc(id):
    return cur.execute("SELECT amount_uc FROM uc_package WHERE id = ?", (id,)).fetchone()[0]


async def get_bank_curr(id):
    return cur.execute("SELECT currency FROM payments WHERE id = ?", (id,)).fetchone()[0]


# RATE
async def create_rate(currency, amount):
    cur.execute("INSERT INTO rate(currency, amount) VALUES(?, ?)", (currency, amount))
    db.commit()


async def get_all_currency():
    return cur.execute("SELECT * FROM rate").fetchall()


async def check_currency(currency):
    curr = cur.execute("SELECT currency FROM rate WHERE currency = ?", (currency,)).fetchone()
    if not curr:
        return None
    else:
        return curr[0]


async def get_amount_curr(currency):
    return cur.execute("SELECT amount FROM rate WHERE currency = ?", (currency,)).fetchone()[0]


async def delete_currency(currency):
    cur.execute("DELETE FROM rate WHERE currency = ?", (currency,))
    db.commit()


# ADD UC
async def create_uc_pack(state, uc_id, user_id):
    async with state.proxy() as data:
        cur.execute("INSERT INTO uc_package(id, user_id, price, amount_uc) VALUES (?, ?, ?, ?)",
                    (uc_id, user_id, data['price'], data['amount_uc']))
    db.commit()


async def update_uc_pack(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE uc_package SET user_id = ?, price = ? amount_uc = ? WHERE id = ?",
                    (user_id, data['price'], data['amount_uc'], data['uc_id']))
    db.commit()


async def admin_select_uc():
    return cur.execute("SELECT * FROM uc_package").fetchall()


async def delete_uc(tour_id: int):
    cur.execute("DELETE FROM uc_package WHERE id = ?", (tour_id,))
    db.commit()


# UC ACTIVE
async def set_active(uc_id):
    id = cur.execute("SELECT id FROM uc_active").fetchone()
    if not id:
        cur.execute("INSERT INTO uc_active(id) VALUES(?)", (uc_id,))
    db.commit()


async def update_uc_active(uc_id, user_id, active):
    cur.execute("UPDATE uc_active SET user_id = ?, active = ? WHERE id = ?",
                (user_id, active, uc_id))
    db.commit()


async def update_info_uc_active(uc_id, user_id, active, photo, text):
    cur.execute("UPDATE uc_active SET user_id = ?, active = ?, photo = ?, text = ? WHERE id = ?",
                (user_id, active, photo, text, uc_id))
    db.commit()


async def update_uc_rsn_active(uc_id, reason):
    cur.execute("UPDATE uc_active SET reason = ? WHERE id = ?",
                (reason, uc_id))
    db.commit()


async def get_active_uc(uc_id):
    return cur.execute("SELECT active FROM uc_active WHERE id = ?", (uc_id,)).fetchone()[0]


async def get_rsn_active_uc(uc_id):
    return cur.execute("SELECT reason FROM uc_active WHERE id = ?", (uc_id,)).fetchone()[0]


async def get_all_info_uc_active(uc_id):
    return cur.execute("SELECT * FROM uc_active WHERE id = ?", (uc_id,)).fetchall()


# ADD ADMIN
async def add_admin(state, user_id):
    async with state.proxy() as data:
        cur.execute("INSERT INTO admin_table(admin_id, user_id, admin_username, job_title, type) VALUES(?, ?, ?, ?, ?)",
                    (data['admin_id'], user_id, data['username'], data['job_title'], data['type_admin']))
    db.commit()


async def update_admin(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            "UPDATE admin_table SET admin_id = ?, user_id = ?, admin_username = ?, job_title = ?, type = ? WHERE admin_id = ?",
            (data['admin_id'], user_id, data['username'], data['job_title'], data['type'], data['a_id']))
    db.commit()


async def get_admin_list():
    return cur.execute("SELECT * FROM admin_table").fetchall()


async def delete_admin(tour_id: int):
    cur.execute("DELETE FROM admin_table WHERE admin_id = ?", (tour_id,))
    db.commit()


async def get_admin_id(admin_id):
    admin = cur.execute("SELECT admin_id FROM admin_table WHERE type = 'ADMIN' AND admin_id = ?",
                        (admin_id,)).fetchone()
    if not admin:
        return []
    else:
        return admin


async def get_moder_id(admin_id):
    moder = cur.execute("SELECT admin_id FROM admin_table WHERE type = 'Moderator' AND admin_id = ?",
                        (admin_id,)).fetchone()
    if not moder:
        return []
    else:
        return moder


# async def get_admin_id(admin_id):
#     admin = cur.execute("SELECT admin_id FROM admin_table WHERE admin_id = ?", (admin_id,)).fetchone()
#     if not admin:
#         return None
#     else:
#         return admin[0]

async def get_admin_profile(admin_id):
    return cur.execute("SELECT * FROM admin_table WHERE admin_id = ?", (admin_id,)).fetchall()


# ADMIN DELETE AGENT/TEAM
async def get_user_agent(user_id):
    return cur.execute("SELECT * FROM info_player WHERE user_id = ?", (user_id,)).fetchall()


async def get_user_team(user_id):
    return cur.execute("SELECT * FROM info_team WHERE user_id = ?", (user_id,)).fetchall()


async def get_prac_agent(user_id):
    return cur.execute("SELECT * FROM young_player WHERE user_id = ?", (user_id,)).fetchall()


async def get_prac_team(user_id):
    return cur.execute("SELECT * FROM young_team WHERE user_id = ?", (user_id,)).fetchall()


async def admin_delete_user(user_id):
    cur.execute("DELETE FROM info_player WHERE user_id = ?", (user_id,))
    db.commit()


async def admin_delete_user_team(user_id):
    cur.execute("DELETE FROM info_team WHERE user_id = ?", (user_id,))
    db.commit()


async def get_all_users_agent():
    return cur.execute("SELECT * FROM info_player").fetchall()


async def get_all_users_team():
    return cur.execute("SELECT * FROM info_team").fetchall()


async def admin_get_all_prac_agent():
    return cur.execute("SELECT * FROM young_player").fetchall()


async def admin_get_all_prac_team():
    return cur.execute("SELECT * FROM young_team").fetchall()


async def admin_delete_prac_user(user_id):
    cur.execute("DELETE FROM young_player WHERE user_id = ?", (user_id,))
    db.commit()


async def admin_delete_prac_team(user_id):
    cur.execute("DELETE FROM young_team WHERE user_id = ?", (user_id,))
    db.commit()


# ADMIN NEWS
async def create_news(state, user_id, news_id):
    async with state.proxy() as data:
        cur.execute("INSERT INTO news(news_id, user_id, text, url) VALUES(?, ?, ?, ?)",
                    (news_id, user_id, data['text'], data['url']))
    db.commit()


async def get_all_news():
    return cur.execute("SELECT * FROM news").fetchall()


async def delete_news(news_id):
    cur.execute("DELETE FROM news WHERE news_id = ?", (news_id,))
    db.commit()


# ADMIN BAN
async def check_id_for_ban(user_id):
    ban_user_id = cur.execute("SELECT user_id FROM language WHERE user_id = ?", (user_id,)).fetchone()
    if not ban_user_id:
        return None
    else:
        return ban_user_id[0]


async def get_block_user(user_id):
    block = cur.execute("SELECT block FROM language WHERE user_id = ?", (user_id,)).fetchone()
    if not block:
        return None
    else:
        return block[0]


async def get_reason_user(user_id):
    reason = cur.execute("SELECT reason FROM language WHERE user_id = ?", (user_id,)).fetchone()
    if not reason:
        return None
    else:
        return reason[0]


async def get_ban_time_user(user_id):
    time = cur.execute("SELECT ban_time FROM language WHERE user_id = ?", (user_id,)).fetchone()
    if not time:
        return None
    else:
        return time[0]


async def get_ban_user(user_id):
    cur.execute("UPDATE language SET block = 1 WHERE user_id = ?", (user_id,))
    db.commit()


async def get_unban_user(user_id):
    cur.execute("UPDATE language SET block = 0, reason = 0, ban_time = 0 WHERE user_id = ?", (user_id,))
    db.commit()


async def load_ban_info(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE language SET reason = ?, ban_time = ? WHERE user_id = ?",
                    (data['reason'], data['ban_time'], user_id))
    db.commit()


async def close_supp_chat(user_id):
    cur.execute("UPDATE language SET block = 2 WHERE user_id = ?", (user_id,))
    db.commit()


async def open_supp_chat(user_id):
    cur.execute("UPDATE language SET block = 0 WHERE user_id = ?", (user_id,))
    db.commit()


# MUSIC
prev_index = -1
music_nuber = 1


async def create_all_music(user_id, music_id, state):
    async with state.proxy() as data:
        cur.execute("""INSERT INTO music(id, user_id, artist, music_name, file, kind) VALUES(?, ?, ?, ?, ?, ?)""",
                    (music_id, user_id, data['artist'], data['name'], data['music_file'], data['kind']))
    db.commit()


async def update_popular_music(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE music SET user_id = ?, artist = ?, music_name = ?, file = ?, kind = ? WHERE id = ?",
                    (user_id, data['artist'], data['name'], data['music_file'], data['kind'], data['music_id']))
    db.commit()


async def get_all_music(text, message):
    global index, prev_index, music_nuber
    music = cur.execute("SELECT * FROM music WHERE artist = ? OR music_name = ?", (text, text,)).fetchall()
    all_music = list(music)[index: index + 9]
    ikb = InlineKeyboardMarkup()
    for data in all_music:
        btn1 = InlineKeyboardButton(f"{music_nuber}. {data[3]} - {data[2]}", callback_data=f'get_music_{data[0]}')
        ikb.add(btn1)
    next = InlineKeyboardButton('Далее➡️', callback_data='next_all_music')
    back_btn = InlineKeyboardButton('🔙Назад', callback_data='back_all_music')
    if prev_index >= 0:
        ikb.add(back_btn, next)
    elif len(all_music) >= 9:
        ikb.add(next)
    await message.answer(f"Результаты по запросу:'{text}'",
                         reply_markup=ikb)


async def get_next_all_music():
    global index, prev_index
    prev_index = index
    index += 9
    await get_all_music()


async def get_back_all_music():
    global index, prev_index, music_nuber
    index = prev_index
    prev_index -= 9
    music_nuber -= 1
    await get_all_music()


async def get_popular_music():
    return cur.execute("SELECT * FROM music WHERE kind = '🔥Популярная'").fetchall()


async def get_music_for_delete():
    return cur.execute("SELECT * FROM music WHERE kind = '🔥Популярная'").fetchall()


async def get_next_popular_music():
    global index, prev_index
    prev_index = index
    index += 9
    await get_popular_music()


async def get_back_popular_music():
    global prev_index, index
    index = prev_index
    prev_index -= 9
    await get_popular_music()


async def delete_all_music(kind):
    cur.execute("DELETE FROM music WHERE kind = ?", (kind,))
    db.commit()


async def delete_music(id):
    cur.execute("DELETE FROM music WHERE id = ?", (id,))
    db.commit()


async def get_music_file(id):
    return cur.execute("SELECT file FROM music WHERE id = ?", (id,)).fetchone()[0]


async def get_music(id):
    return cur.execute("SELECT * FROM music WHERE id = ?", (id,)).fetchall()


# YOUNG
async def get_prac():
    return cur.execute("SELECT * FROM practice_game").fetchall()


async def get_photo_prac(prac_id):
    return cur.execute("SELECT photo FROM practice_game WHERE prac_id = ?", (prac_id,)).fetchone()[0]


async def get_desc_prac(prac_id):
    return cur.execute("SELECT desc FROM practice_game WHERE prac_id = ?", (prac_id,)).fetchone()[0]


async def get_url_prac(prac_id):
    return cur.execute("SELECT url FROM practice_game WHERE prac_id = ?", (prac_id,)).fetchone()[0]


# ADMIN PRAC YOUNG
async def create_prac(state, user_id, prac_id):
    async with state.proxy() as data:
        cur.execute("INSERT INTO practice_game(prac_id, user_id, photo, desc, url) VALUES( ?, ?, ?, ?, ?)",
                    (prac_id, user_id, data['photo'], data['desc'], data['url']))
    db.commit()


async def admin_update_prac(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE practice_game SET user_id = ?, photo = ?, desc = ?, url = ? WHERE prac_id = ?",
                    (user_id, data['photo'], data['desc'], data['url'], data['id']))
    db.commit()


async def admin_get_prac(prac_id):
    return cur.execute("SELECT * FROM practice_game WHERE prac_id = ?", (prac_id,)).fetchall()


async def admin_get_pracs():
    return cur.execute("SELECT * FROM practice_game").fetchall()


async def admin_delete_prac(prac_id):
    cur.execute("DELETE FROM practice_game WHERE prac_id = ?", (prac_id,))
    db.commit()


# VIP PRAC
async def get_vip_prac(prac_id):
    return cur.execute("SELECT * FROM prac_vip_slot WHERE tour_id = ?", (prac_id,)).fetchall()


async def get_vip_pracs(time):
    return cur.execute("SELECT * FROM prac_vip_slot WHERE time = ? AND amount != 0", (time,)).fetchall()


async def get_price_vip_prac(tour_id):
    return cur.execute("SELECT price FROM prac_vip_slot WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_vip_prac_name(tour_id):
    return cur.execute("SELECT tour_name FROM prac_vip_slot WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_desc_prac_vip(tour_id):
    return cur.execute("SELECT desc FROM prac_vip_slot WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_time_prac_vip(tour_id):
    return cur.execute("SELECT time FROM prac_vip_slot WHERE tour_id = ?", (tour_id,)).fetchone()[0]


async def get_link_prac_vip(tour_id):
    return cur.execute("SELECT link FROM prac_vip_slot WHERE tour_id = ?", (tour_id,)).fetchone()[0]



# ADMIN VIP PRACTICE
async def create_vip_prac(state, tour_id, user_id):
    async with state.proxy() as data:
        cur.execute(
            "INSERT INTO prac_vip_slot(tour_id, user_id, time, photo, desc, tour_name, price, link, amount, amount2) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
            tour_id, user_id, data['time'], data['photo'], data['desc'], data['tour_name'], data['price'], data['link'],
            data['amount'], data['amount']))
        db.commit()


async def update_vip_prac(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            "UPDATE prac_vip_slot SET user_id = ?, time = ?, photo = ?, desc = ?, tour_name = ?, price = ?, link = ?, amount = ?, amount2 = ? WHERE tour_id = ?",
            (user_id, data['time'], data['photo'], data['desc'], data['tour_name'], data['price'], data['link'],
             data['amount'], data['amount'], data['tour_id']))
    db.commit()


async def update_amount_vip_prac(prac_id, amount):
    cur.execute("UPDATE prac_vip_slot SET amount = ? WHERE tour_id = ?", (amount, prac_id))
    db.commit()


async def update_amount2_vip_prac(prac_id, amount):
    cur.execute("UPDATE prac_vip_slot SET amount2 = ? WHERE tour_id = ?", (amount, prac_id))
    db.commit()


async def get_amount_vip_prac(prac_id):
    return cur.execute("SELECT amount FROM prac_vip_slot WHERE tour_id = ?", (prac_id,)).fetchone()[0]


async def get_amount2_vip_prac(prac_id):
    return cur.execute("SELECT amount2 FROM prac_vip_slot WHERE tour_id = ?", (prac_id,)).fetchone()[0]


async def admin_get_vip_pracs():
    return cur.execute("SELECT * FROM prac_vip_slot").fetchall()


async def get_photo_prac_vip(prac_id):
    return cur.execute("SELECT photo FROM prac_vip_slot WHERE tour_id = ?", (prac_id,)).fetchone()[0]


async def admin_delete_vip_prac(prac_id):
    cur.execute("DELETE FROM prac_vip_slot WHERE tour_id = ?", (prac_id,))
    db.commit()


# PRAC FREE AGENT
async def create_prac_agent(user_id):
    user = cur.execute("SELECT 1 FROM young_player WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO young_player VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (user_id, '', '', '', '', '', '', '', '', ''))
    db.commit()


async def edit_prac_agent(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            """UPDATE young_player SET nickname = ?, age = ?, teamspeak = ?, teamspeak1 = ?, device = ?, practice_game = ?, highilights = ?, description = ?, contact = ? WHERE user_id = ?""",
            (data['nickname'], data['age'], data["teamspeak"], data["teamspeak1"], data['device'],
             data['practice_games'], data['highilights'], data['description'], data['contact'], user_id))
        db.commit()


async def get_prac_agent_profile(user_id):
    return cur.execute("SELECT * FROM young_player WHERE user_id = ?", (user_id,)).fetchall()


async def get_nickname_prac_agent(user_id):
    return cur.execute("SELECT nickname FROM young_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_age_prac_agent(user_id):
    return cur.execute("SELECT age FROM young_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_role_prac_agent(user_id):
    return cur.execute("SELECT role FROM young_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_device_prac_agent(user_id):
    return cur.execute("SELECT device FROM young_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_amount_prac_agent(user_id):
    return cur.execute("SELECT practice_game FROM young_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_hl_prac_agent(user_id):
    return cur.execute("SELECT highilights FROM young_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_desc_prac_agent(user_id):
    return cur.execute("SELECT description FROM young_player WHERE user_id = ?", (user_id,)).fetchone()[0]


async def delete_prac_agent_profile(user_id):
    cur.execute("DELETE FROM young_player WHERE user_id = ?", (user_id,))
    db.commit()


async def get_all_prac_agent():
    return cur.execute("SELECT * FROM young_player").fetchall()


# YOUNG FREE TEAM
async def create_prac_team(user_id):
    user = cur.execute("SELECT 1 FROM young_team WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO young_team VALUES(?,?,?,?,?,?,?,?,?,?)", (user_id, '', '', '', '', '', '', '', '', ''))
    db.commit()


async def edit_prac_team(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            """UPDATE young_team SET team_name = ?, age = ?, teamspeak = ?, teamspeak1 = ?, role = ?, device = ?, practice_game = ?, description = ?, contact = ? WHERE user_id = ?""",
            (data['team_name'], data['age'], data["teamspeak"], data["teamspeak1"], data['role'], data['device'],
             data['practice_games'], data['description'], data['contact'], user_id))
        db.commit()


async def get_prac_team_profile(user_id):
    return cur.execute("SELECT * FROM young_team WHERE user_id = ?", (user_id,)).fetchall()


async def delete_prac_team(user_id):
    cur.execute("DELETE FROM young_team WHERE user_id = ?", (user_id,))
    db.commit()


async def get_prac_team_name(user_id):
    return cur.execute("SELECT team_name FROM young_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_prac_age_team(user_id):
    return cur.execute("SELECT age FROM young_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_prac_role_team(user_id):
    return cur.execute("SELECT role FROM young_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_prac_device_team(user_id):
    return cur.execute("SELECT device FROM young_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_prac_game_team(user_id):
    return cur.execute("SELECT practice_game FROM young_team WHERE user_id = ?", (user_id,)).fetchone()[0]


async def get_all_prac_team():
    return cur.execute("SELECT * FROM young_team").fetchall()


# ADMIN SEND MESS
async def create_send_mess(state, post_id, user_id):
    async with state.proxy() as data:
        cur.execute("INSERT INTO send_mess (id, user_id, desc, photo, link) VALUES(?, ?, ?, ?, ?)",
                    (post_id, user_id, data['desc'], data['photo'], data['link']))
    db.commit()


async def get_send_mess(post_id):
    return cur.execute("SELECT * FROM send_mess WHERE id = ?", (post_id,)).fetchall()


async def admin_delete_send_mess(post_id):
    cur.execute("DELETE FROM send_mess WHERE id = ?", (post_id,))
    db.commit()
