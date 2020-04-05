create schema laserpiente;
create user dev with password 'devpass';
grant all on schema laserpiente to dev;

create table laserpiente.v_conj_ind_pres
(
	infinitivo varchar not null
		constraint v_conj_ind_pres_pk
			primary key,
	singular1 varchar not null,
	singular2 varchar not null,
	singular3 varchar not null,
	plural1 varchar not null,
	plural2 varchar not null,
	plural3 varchar not null
);

grant select on laserpiente.v_conj_ind_pres to dev;

insert into laserpiente.v_conj_ind_pres (infinitivo, singular1, singular2, singular3, plural1, plural2, plural3)
values ('comer', 'como', 'comes', 'come', 'comemos', 'coméis', 'comen'),
       ('ir', 'voy', 'vas', 'va', 'vamos', 'vais', 'van'),
       ('pedir', 'pido', 'pides', 'pide', 'pedimos', 'pedís', 'piden');
