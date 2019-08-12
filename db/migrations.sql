
CREATE TABLE IF NOT EXISTS online_history(
    user_id integer,
    time timestamp,
    new_status text
);

CREATE TABLE IF NOT EXISTS last_online(
    user_id integer,
    time timestamp,
    last_status text
);

CREATE TABLE IF NOT EXISTS user_info(
    user_id integer,
    first_name text,
    last_name text,
    user_name text,
    bio text,
    trackable_online boolean,
    last_modified timestamp
);
