CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    mail VARCHAR(255) UNIQUE NOT NULL,
    pass VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    delete_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    img_path TEXT UNIQUE,
    user_id INTEGER REFERENCES users(id),
    delete_flag BOOLEAN DEFAULT false,
    created_at DATE
);

CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    mail VARCHAR(255) UNIQUE,
    pass VARCHAR(255),
    salt VARCHAR(255),
    updated_at TIMESTAMP
);
