CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    msg_type VARCHAR(255),
    sender_name VARCHAR(255),
    msg_dist_type VARCHAR(255),
    reply_count INT
)