DROP TABLE IF EXISTS session_entry;
CREATE TABLE session_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_uid TEXT NOT NULL,
    entry_time TIMESTAMP NOT NULL,
    member_uid INTEGER NOT NULL,
    member_name TEXT,
    card_uid TEXT NOT NULL,
    active_session BOOLEAN NOT NULL,
    action_description TEXT NOT NULL,
    device_uid TEXT NOT NULL,
    device_name TEXT NOT NULL
);