CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    image_file VARCHAR(20) NOT NULL DEFAULT 'default.jpg',
    password VARCHAR(60) NOT NULL
);

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);

CREATE TABLE topic (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);

CREATE TABLE topic_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    topic_id INTEGER REFERENCES topic (id) NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);

CREATE TABLE legend (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL
    );
