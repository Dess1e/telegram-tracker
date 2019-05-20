
CREATE TABLE online_history(
    user_id integer,
    time timestamp,
    new_status text
);

CREATE TABLE last_online(
    user_id integer,
    time timestamp,
    last_status text
);

CREATE TABLE user_info(
    user_id integer,
    first_name text,
    last_name text, 
    bio text,
    trackable_online boolean,
    last_modified timestamp
);
