from aiogram.dispatcher.filters.state import State, StatesGroup


class LanguageStateGroup(StatesGroup):
    language = State()
    profile = State()


# PRO

# FREE AGENT
class FreeagentStateGroup(StatesGroup):
    nickname = State()
    age = State()
    teamspeak = State()
    teamspeak1 = State()
    device = State()
    tournament = State()
    finals = State()
    highilights = State()
    description = State()
    contact = State()

    new_nickname = State()
    new_age = State()
    new_teamspeak = State()
    new_teamspeak1 = State()
    new_device = State()
    new_tournament = State()
    new_finals = State()
    new_highilights = State()
    new_description = State()
    new_contact = State()


# FREE TEAM
class FreeteamStateGroup(StatesGroup):
    team_name = State()
    age = State()
    teamspeak = State()
    teamspeak1 = State()
    role = State()
    device = State()
    tournament = State()
    finals = State()
    description = State()
    contact = State()

    new_team_name = State()
    new_age = State()
    new_teamspeak = State()
    new_teamspeak1 = State()
    new_role = State()
    new_device = State()
    new_tournament = State()
    new_finals = State()
    new_description = State()
    new_contact = State()


# BUY VIP SLOT/EVENT/PRAC
class BuyVipSlotStatesGroup(StatesGroup):
    proof = State()
    team_name = State()
    team_tag = State()
    cap = State()
    logo = State()
    reason = State()


# BUY UC
class BuyUCStatesGroup(StatesGroup):

    proof = State()
    game_id = State()
    nick = State()
    reason = State()


# SEARCH MUSIC
class MusicStatesGroup(StatesGroup):
    text = State()


# ADMIN TOURNAMENT
class TourStateGroup(StatesGroup):
    format = State()
    photo = State()
    desc = State()
    url = State()

    new_format = State()
    new_photo = State()
    new_desc = State()
    new_url = State()


# ADMIN VIP SLOTS
class VIPslotStateGroup(StatesGroup):
    stage = State()
    time = State()
    photo = State()
    tour_name = State()
    price = State()
    desc = State()
    amount = State()
    link = State()

    new_stage = State()
    new_time = State()
    new_photo = State()
    new_tour_name = State()
    new_price = State()
    new_desc = State()
    new_amount = State()
    new_link = State()

    double_time = State()
    double_amount = State()


# ADMIN EVENT
class EventStateGroup(StatesGroup):
    time = State()
    photo = State()
    desc = State()
    price = State()
    tour_name = State()
    amount = State()
    link = State()

    new_time = State()
    new_photo = State()
    new_desc = State()
    new_price = State()
    new_tour_name = State()
    new_amount = State()
    new_link = State()


# HELP
class HelpStatesGroup(StatesGroup):
    first_ques = State()
    second_ques = State()
    finish_ques = State()


# ADMIN ANSWER
class AnswerStatesGroup(StatesGroup):
    first_answer = State()
    second_answer = State()


# ADMIN NEWS
class AddNewsStatesGroup(StatesGroup):
    text = State()
    url = State()


# ADD PAY
class AdminPayStatesGroup(StatesGroup):
    bank = State()
    currency = State()
    card = State()

class AddCurrencyStatesGroup(StatesGroup):
    currency = State()
    amount = State()


# ADD UC
class UCStatesGroup(StatesGroup):
    photo = State()
    price = State()
    amount_uc = State()

    new_photo = State()
    new_price = State()
    new_amount_uc = State()

    reason = State()

    text = State()


# ADD ADMIN
class AddadminStatesGroup(StatesGroup):
    admin_id = State()
    type_admin = State()
    username = State()
    job_title = State()

    new_admin_id = State()
    new_type_admin = State()
    new_username = State()
    new_job_title = State()


# ADMIN BAN
class BanStatesGroup(StatesGroup):
    user_id = State()
    ban_user_id = State()
    reason = State()
    ban_time = State()
    unban = State()


# ADMIN MUSIC
class AdminMusicStatesGroup(StatesGroup):
    kind = State()
    load_kind = State()
    music_file = State()
    name = State()
    artist = State()

    new_load_kind = State()
    new_music_file = State()
    new_name = State()
    new_artist = State()


# ADMIN SENDING MESSAGES
class AdminSendMessagesStatesGroup(StatesGroup):

    photo = State()
    desc = State()
    link = State()


# YOUNG


# YOUNG PRAC AGENT
class PracAgentStateGroup(StatesGroup):
    nickname = State()
    age = State()
    teamspeak = State()
    teamspeak1 = State()
    device = State()
    practice_games = State()
    highilights = State()
    description = State()
    contact = State()

    new_nickname = State()
    new_age = State()
    new_teamspeak = State()
    new_teamspeak1 = State()
    new_device = State()
    new_practice_games = State()
    new_highilights = State()
    new_description = State()
    new_contact = State()


# YOUNG FREE TEAM
class PracTeamStateGroup(StatesGroup):
    team_name = State()
    age = State()
    teamspeak = State()
    teamspeak1 = State()
    role = State()
    device = State()
    practice_games = State()
    description = State()
    contact = State()

    new_team_name = State()
    new_age = State()
    new_teamspeak = State()
    new_teamspeak1 = State()
    new_role = State()
    new_device = State()
    new_practice_games = State()
    new_description = State()
    new_contact = State()


# ADMIN PRACTICE GAMES
class AddPracStatesGroup(StatesGroup):
    photo = State()
    desc = State()
    url = State()

    new_photo = State()
    new_desc = State()
    new_url = State()


# ADD VIP PRAC
class AddPracVIPStatesGroup(StatesGroup):
    time = State()
    photo = State()
    desc = State()
    price = State()
    tour_name = State()
    amount = State()
    link = State()

    new_time = State()
    new_photo = State()
    new_desc = State()
    new_price = State()
    new_tour_name = State()
    new_amount = State()
    new_link = State()


# CHECK USER
class CheckUserStatesGroup(StatesGroup):
    user_id = State()


# STATISTIC
class GetRandomUserStatesGroup(StatesGroup):

    amount = State()