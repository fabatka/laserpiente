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

create table laserpiente.sentences
(
	quiz varchar not null,
	frase varchar not null,
	palabra_q_falta integer not null,
	solucion_infinitivo varchar not null,
	solucion_sujeto varchar not null
);

create index sentences_quiz_index
	on laserpiente.sentences (quiz);

grant select on laserpiente.sentences to dev;


insert into laserpiente.v_conj_ind_pres (infinitivo, singular1, singular2, singular3, plural1, plural2, plural3)
values ('comer', 'como', 'comes', 'come', 'comemos', 'coméis', 'comen'),
       ('ir', 'voy', 'vas', 'va', 'vamos', 'vais', 'van'),
       ('pedir', 'pido', 'pides', 'pide', 'pedimos', 'pedís', 'piden');

insert into laserpiente.sentences (quiz, frase, palabra_q_falta, solucion_infinitivo, solucion_sujeto)
values ('subjuntivo-probabilidad', 'Probablemente esté de mal humor.', 2, 'estar', 'singular3'),
       ('subjuntivo-probabilidad', 'Posiblemente nadie lo haya visto.', 4, 'haber', 'singular3'),
       ('subjuntivo-probabilidad', 'Es posible que le haga falta.', 5, 'hacer', 'singular3'),
       ('subjuntivo-probabilidad', 'Ya está listo con sus tareas probablemente.', 2, 'estar', 'singular3'),
       ('subjuntivo-probabilidad', 'Nos molesta que haya gatos en el parque infantil.', 4, 'haber', 'singular3')