--
-- File generated with SQLiteStudio v3.4.4 on �� ��� 19 00:00:32 2024
--
-- Text encoding used: System
--
PRAGMA
foreign_keys = off;
BEGIN
TRANSACTION;

-- Table: user
CREATE TABLE IF NOT EXISTS user
(
    id
    INTEGER
    NOT
    NULL
    PRIMARY
    KEY,
    user_id
    INTEGER
    NOT
    NULL,
    nickname
    TEXT
(
    60
), time_sub NOT NULL DEFAULT
(
    0
), signup TEXT DEFAULT setnickname, subscription_type TEXT DEFAULT none, user_limit INTEGER DEFAULT
(
    50000
) NOT NULL, limit_update_date TEXT);

COMMIT TRANSACTION;
PRAGMA
foreign_keys = on;
