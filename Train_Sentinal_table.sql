CREATE TABLE public.platform (
	id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	"time" timestamp NULL,
	passenger_count int4 NULL,
	incident varchar NULL,
	CONSTRAINT platform_pkey PRIMARY KEY (id)
);

CREATE TABLE public.train (
	id int4 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE) NOT NULL,
	technical varchar NULL,
	medical varchar NULL,
	"time" timestamp NULL,
	expected_resolve timestamp NULL,
	remarks varchar NULL,
	CONSTRAINT train_pkey PRIMARY KEY (id)
);