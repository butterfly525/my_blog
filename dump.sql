--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0 (Debian 17.0-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: admin_my_blog
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO admin_my_blog;

--
-- Name: photos; Type: TABLE; Schema: public; Owner: admin_my_blog
--

CREATE TABLE public.photos (
    id integer NOT NULL,
    image character varying(255) NOT NULL,
    post_id integer NOT NULL
);


ALTER TABLE public.photos OWNER TO admin_my_blog;

--
-- Name: photos_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_my_blog
--

CREATE SEQUENCE public.photos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.photos_id_seq OWNER TO admin_my_blog;

--
-- Name: photos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_my_blog
--

ALTER SEQUENCE public.photos_id_seq OWNED BY public.photos.id;


--
-- Name: post; Type: TABLE; Schema: public; Owner: admin_my_blog
--

CREATE TABLE public.post (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    content text NOT NULL,
    author_id integer NOT NULL,
    created_at timestamp without time zone,
    edited_at timestamp without time zone
);


ALTER TABLE public.post OWNER TO admin_my_blog;

--
-- Name: post_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_my_blog
--

CREATE SEQUENCE public.post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.post_id_seq OWNER TO admin_my_blog;

--
-- Name: post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_my_blog
--

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: admin_my_blog
--

CREATE TABLE public.role (
    id integer NOT NULL,
    name character varying(15) NOT NULL
);


ALTER TABLE public.role OWNER TO admin_my_blog;

--
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_my_blog
--

CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.role_id_seq OWNER TO admin_my_blog;

--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_my_blog
--

ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: admin_my_blog
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role_id integer
);


ALTER TABLE public."user" OWNER TO admin_my_blog;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_my_blog
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO admin_my_blog;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_my_blog
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: photos id; Type: DEFAULT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.photos ALTER COLUMN id SET DEFAULT nextval('public.photos_id_seq'::regclass);


--
-- Name: post id; Type: DEFAULT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.post ALTER COLUMN id SET DEFAULT nextval('public.post_id_seq'::regclass);


--
-- Name: role id; Type: DEFAULT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: admin_my_blog
--

COPY public.alembic_version (version_num) FROM stdin;
43b7668d19e0
\.


--
-- Data for Name: photos; Type: TABLE DATA; Schema: public; Owner: admin_my_blog
--

COPY public.photos (id, image, post_id) FROM stdin;
5	static/uploads/idea.png	11
\.


--
-- Data for Name: post; Type: TABLE DATA; Schema: public; Owner: admin_my_blog
--

COPY public.post (id, title, content, author_id, created_at, edited_at) FROM stdin;
1	title	text	5	2024-11-14 15:18:11.994691	2024-11-14 15:18:11.994694
2	title	text	5	2024-11-14 15:18:28.830239	2024-11-14 15:18:28.830242
3	qwe	qwe	5	2024-11-14 15:44:37.941608	2024-11-14 15:44:37.941611
4	как сортирвоать по убыванию	Для сортировки результатов по убыванию в SQLAlchemy можно использовать метод desc(). Вот несколько способов сделать это:\r\n\r\nИспользование desc():\r\nfrom sqlalchemy import desc\r\n\r\nquery = session.query(SomeModel).order_by(desc(SomeModel.column_name)).all()\r\nИспользование атрибута desc():\r\nquery = session.query(SomeModel).order_by(SomeModel.column_name.desc()).all()\r\nДля более сложных запросов:\r\nfrom sqlalchemy import desc\r\n\r\nquery = (\r\n    session.query(SomeModel)\r\n    .join(AnotherModel)\r\n    .filter(SomeModel.some_condition)\r\n    .order_by(desc(SomeModel.column_name))\r\n    .all()\r\n)\r\nС использованием текстового выражения:\r\nfrom sqlalchemy import desc, text\r\n\r\nquery = session.query(SomeModel).order_by(text("column_name DESC")).all()\r\nКлючевые моменты:\r\n\r\ndesc() - это функция из модуля sqlalchemy, которая принимает столбец как аргумент.\r\nВы можете использовать desc() как отдельную функцию или как метод столбца.\r\nЭтот метод работает не только для числовых столбцов, но и для строковых.\r\nВыберите наиболее подходящий для вашего случая способ сортировки по убыванию. Обычно desc() является наиболее гибким и читаемым вариантом.	5	2024-11-14 15:48:01.284472	2024-11-14 15:48:01.284474
5	1233	ckjndsjknc\r\n	5	2024-11-14 16:06:07.06619	2024-11-14 16:06:07.066194
6	dcwef	efcewfc	5	2024-11-14 16:16:28.444846	2024-11-14 16:16:28.444849
7	efdewf	wefew	5	2024-11-14 16:44:58.916104	2024-11-14 16:44:58.916108
8	123	123	5	2024-11-14 16:45:35.83577	2024-11-14 16:45:35.835773
9	new	qwertyui	5	2024-11-14 16:49:08.664555	2024-11-14 16:49:08.664558
10	21	123	5	2024-11-14 16:53:15.492789	2024-11-14 16:53:15.492793
11	qdw	wdqw	5	2024-11-14 16:55:08.857316	2024-11-14 16:55:08.857319
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: admin_my_blog
--

COPY public.role (id, name) FROM stdin;
1	admin
2	user
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: admin_my_blog
--

COPY public."user" (id, username, email, password_hash, role_id) FROM stdin;
6	hroaa	ananasik1@yahoo.com	scrypt:32768:8:1$VAmQKLYqoe83Zldm$90d47d63c62244f98e57c93a567da00ebdeaf594bf8f9d8d66255e68e2007b47789f3b3c7aa0db822e609699f60cb410436d2e7974396a38f1abcd0dd9826008	2
5	Anastasia	nastya.khromykh@mail.ru	scrypt:32768:8:1$jkQtqmeMj11SnKzy$69c316b59fbcfd01e23fa59c06993e059c3c8a6701d083bb0a5cb096245260273a6dcb6736dd51d213beed28297cdb81f6078240fa90962fbaa59d82314d14e6	1
\.


--
-- Name: photos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_my_blog
--

SELECT pg_catalog.setval('public.photos_id_seq', 5, true);


--
-- Name: post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_my_blog
--

SELECT pg_catalog.setval('public.post_id_seq', 11, true);


--
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_my_blog
--

SELECT pg_catalog.setval('public.role_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_my_blog
--

SELECT pg_catalog.setval('public.user_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: photos photos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_pkey PRIMARY KEY (id);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: role role_name_key; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_name_key UNIQUE (name);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: photos photos_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.photos
    ADD CONSTRAINT photos_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.post(id);


--
-- Name: post post_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_author_id_fkey FOREIGN KEY (author_id) REFERENCES public."user"(id);


--
-- Name: user user_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_my_blog
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO admin_my_blog;


--
-- PostgreSQL database dump complete
--

