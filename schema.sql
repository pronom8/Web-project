CREATE TABLE "user" (
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


CREATE TABLE topic_post_comments (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    topic_post_id INTEGER REFERENCES topic_posts (id) ON DELETE CASCADE NOT NULL,
    topic_id INTEGER REFERENCES topic (id) NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);



CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    post_id INTEGER REFERENCES post (id) NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);




CREATE TABLE private_area (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);

CREATE TABLE private_area_user (
    id SERIAL PRIMARY KEY,
    private_area_id INTEGER REFERENCES private_area(id) NOT NULL,
    user_id INTEGER REFERENCES "user"(id),
    UNIQUE(private_area_id, user_id)  
);

CREATE TABLE private_area_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    private_area_id INTEGER REFERENCES private_area (id) NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);

CREATE TABLE private_area_post_comments (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    private_area_post_id INTEGER REFERENCES private_area_posts (id) ON DELETE CASCADE NOT NULL,
    private_area_id INTEGER REFERENCES private_area (id) NOT NULL,
    user_id INTEGER REFERENCES "user" (id) NOT NULL
);
