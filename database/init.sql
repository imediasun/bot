CREATE TABLE IF NOT EXISTS language(
                user_id INTEGER PRIMARY KEY,
                language TEXT,
                currency TEXT,
                block INTEGER,
                reason TEXT,
                ban_time TEXT,
                profile TEXT,
                amount_clicks INTEGER,
                time_log TEXT);
CREATE TABLE IF NOT EXISTS info_player(
                user_id INTEGER PRIMARY KEY,
                nickname TEXT,
                age TEXT,
                teamspeak TEXT,
                teamspeak1 TEXT,
                device TEXT,
                tournament TEXT,
                finals TEXT,
                highilights TEXT,
                description TEXT,
                contact TEXT);
                
CREATE TABLE IF NOT EXISTS young_player(
                user_id INTEGER PRIMARY KEY,
                nickname TEXT,
                age TEXT,
                teamspeak TEXT,
                teamspeak1 TEXT,
                device TEXT,
                practice_game TEXT,
                highilights TEXT,
                description TEXT,
                contact TEXT);

CREATE TABLE IF NOT EXISTS info_team(
                user_id INTEGER PRIMARY KEY,
                team_name TEXT,
                age TEXT,
                teamspeak TEXT,
                teamspeak1 TEXT,
                role TEXT,
                device TEXT,
                tournament TEXT,
                finals TEXT,
                description TEXT,
                contact TEXT);
    CREATE TABLE IF NOT EXISTS young_team(
                user_id INTEGER PRIMARY KEY,
                team_name TEXT,
                age TEXT,
                teamspeak TEXT,
                teamspeak1 TEXT,
                role TEXT,
                device TEXT,
                practice_game TEXT,
                description TEXT,
                contact TEXT);
    CREATE TABLE IF NOT EXISTS info_tour(
                tour_id TEXT PRIMARY KEY,
                user_id INTEGER,
                format TEXT,
                photo TEXT,
                desc TEXT,
                url TEXT);
    CREATE TABLE IF NOT EXISTS practice_game(
                prac_id TEXT PRIMARY KEY,
                user_id INTEGER,
                photo TEXT,
                desc TEXT,
                url TEXT);

    CREATE TABLE IF NOT EXISTS vip_slots(
                tour_id TEXT PRIMARY KEY,
                user_id INTEGER,
                stage TEXT,
                photo TEXT,
                desc TEXT,
                price INTEGER,
                tour_name TEXT,
                ds_link TEXT,
                time TEXT);
    CREATE TABLE IF NOT EXISTS available_vip_slots(
                tour_id TEXT,
                time TEXT,
                amount_busy INTEGER,
                amount INTEGER);

    CREATE TABLE IF NOT EXISTS prac_vip_slot(
                tour_id TEXT PRIMARY KEY,
                user_id INTEGER,
                time TEXT,
                photo TEXT,
                price TEXT,
                desc TEXT,
                tour_name TEXT,
                link TEXT,
                amount INTEGER,
                amount2 INTEGER);

    CREATE TABLE IF NOT EXISTS events(
                tour_id TEXT PRIMARY KEY,
                user_id INTEGER,
                time TEXT,
                photo TEXT,
                price TEXT,
                desc TEXT,
                tour_name TEXT,
                link TEXT,
                amount INTEGER,
                amount2 INTEGER);

    CREATE TABLE IF NOT EXISTS payments(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                bank TEXT,
                card TEXT,
                currency TEXT);
    CREATE TABLE IF NOT EXISTS uc_package(
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                photo TEXT,
                price TEXT,
                amount_uc TEXT);
    CREATE TABLE IF NOT EXISTS buy_vip_slot(
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                username TEXT,
                proof TEXT,
                proof_d TEXT,
                amount TEXT,
                currency TEXT,
                bank TEXT,
                pay_number TEXT,
                vip_slot_id TEXT,
                format TEXT,
                logo TEXT,
                logo_d TEXT,
                team_name TEXT,
                team_tag TEXT,
                cap TEXT,
                reason TEXT,
                time TEXT,
                buy_time TEXT);

    CREATE TABLE IF NOT EXISTS buy_uc(
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                proof TEXT,
                proof_d TEXT,
                amount TEXT,
                currency TEXT,
                amount_uc TEXT,
                bank TEXT,
                pay_number TEXT,
                user_name TEXT,
                game_id TEXT,
                nick TEXT,
                reason TEXT,
                buy_time TEXT);

    CREATE TABLE IF NOT EXISTS news(
                news_id TEXT PRIMARY KEY,
                user_id INTEGER,
                text TEXT,
                url TEXT);
    CREATE TABLE IF NOT EXISTS admin_table(
                admin_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                admin_username TEXT,
                job_title TEXT,
                type TEXT);
    CREATE TABLE IF NOT EXISTS music(
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                artist TEXT,
                music_name TEXT,
                file BLOB,
                kind TEXT);
    CREATE TABLE IF NOT EXISTS rate(
                currency TEXT PRIMARY KEY,
                amount TEXT);
    CREATE TABLE IF NOT EXISTS send_mess(
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                desc TEXT,
                photo TEXT,
                link TEXT,
                active TEXT);
    CREATE TABLE IF NOT EXISTS uc_active(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                active INTEGER,
                reason TEXT,
                photo TEXT,
                text TEXT);