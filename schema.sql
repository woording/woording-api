DROP TABLE IF EXISTS user;
CREATE TABLE user (
	id integer primary key autoincrement,
	username text not null,
	email text not null,
	email_verified boolean not null,
	password_hash text not null
);

CREATE UNIQUE INDEX user_username_unique
on user (username);

DROP TABLE IF EXISTS list;
CREATE TABLE list (
	id integer primary key autoincrement,
	user_id integer not null,
	listname text not null,
	language_1_tag text not null,
	language_2_tag text not null,
	shared integer not null,
    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE UNIQUE INDEX list_name_unique_for_user
on list (user_id, listname);

DROP TABLE IF EXISTS translation;
CREATE TABLE translation (
	id integer primary key autoincrement not null,
	list_id integer not null,
	language_1_text text not null,
	language_2_text text not null,
    FOREIGN KEY(list_id) REFERENCES list(id) ON DELETE CASCADE
);

-- TODO: make user_1_id and user_2_id a unique combo
DROP TABLE IF EXISTS friendship;
CREATE TABLE friendship (
	user_1_id integer not null,
	user_2_id integer not null,
	FOREIGN KEY(user_1_id) REFERENCES user(id) ON DELETE CASCADE,
	FOREIGN KEY(user_2_id) REFERENCES user(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS auth_tokens;
CREATE TABLE auth_tokens (
    id integer primary key autoincrement not null,
    selector text not null,
    token text not null,
    expires text not null
);
