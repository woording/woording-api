CREATE TABLE auth_tokens (
    id integer primary key autoincrement not null,
    selector text not null,
    token text not null,
    user_id integer not null,
    expires text not null
);
