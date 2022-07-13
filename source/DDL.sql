BEGIN;

CREATE TABLE IF NOT EXISTS public."hotel-room" (
    id SERIAL PRIMARY KEY,
    bedrooms smallint NOT NULL,
    beds smallint NOT NULL,
    bathrooms smallint NOT NULL,
    luxury boolean,
    images varchar,
    breakfast boolean,
    desk boolean,
    baby_chair boolean,
    crib boolean,
    tv boolean,
    shampoo boolean,
    corridor boolean,
    disabled boolean,
    smoke boolean,
    pet boolean,
    guest boolean,
    stars smallint NOT NULL
);

CREATE TABLE IF NOT EXISTS public.comment (
    id SERIAL PRIMARY KEY,
    hotel_room_id bigint NOT NULL,
    user_name varchar NOT NULL,
    comment_date date DEFAULT now(),
    text varchar NOT NULL,
    rating smallint NOT NULL
);

CREATE TABLE IF NOT EXISTS public.availability (
    id SERIAL PRIMARY KEY,
    hotel_room_id bigint NOT NULL,
    date date NOT NULL,
    price bigint NOT NULL,
    reservation_id bigint
);

CREATE TABLE IF NOT EXISTS public.user (
    id SERIAL PRIMARY KEY,
    name varchar NOT NULL,
    surname varchar NOT NULL,
    gender smallint NOT NULL,
    birthday date NOT NULL,
    email varchar NOT NULL,
    password varchar NOT NULL,
    subscription boolean
);

CREATE TABLE IF NOT EXISTS public.reservation (
    id SERIAL PRIMARY KEY,
    user_id bigint NOT NULL,
    hotel_room_id bigint NOT NULL,
    date_in date NOT NULL,
    date_out date NOT NULL,
    total_price integer NOT NULL
);

ALTER TABLE IF EXISTS public.comment
    ADD FOREIGN KEY (hotel_room_id)
    REFERENCES public."hotel-room" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.availability
    ADD FOREIGN KEY (hotel_room_id)
    REFERENCES public."hotel-room" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.availability
    ADD FOREIGN KEY (reservation_id)
    REFERENCES public.reservation (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.reservation
    ADD FOREIGN KEY (user_id)
    REFERENCES public.user (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.reservation
    ADD FOREIGN KEY (hotel_room_id)
    REFERENCES public."hotel-room" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;