create schema laserpiente;
create user dev with password 'devpass';
grant all on schema laserpiente to dev;

create table laserpiente.verbo
(
	infinitivo varchar not null
		constraint v_conj_ind_pres_pk
			primary key,
	gerundio varchar,
	participio varchar,
	modo varchar,
	tiempo varchar,
	singular1 varchar,
	singular2 varchar,
	singular3 varchar,
	plural1 varchar,
	plural2 varchar,
	plural3 varchar
);

alter table laserpiente.verbo owner to dev;

create table laserpiente.frase
(
    id    bigserial
        constraint frase_pk primary key,
    texto varchar not null
);

alter table laserpiente.frase owner to dev;

create table laserpiente.ejercicio
(
    id                  bigserial
        constraint ejercicio_pk primary key,
    quiz                varchar not null,
    frase_id            bigint references laserpiente.frase (id),
    palabra_q_falta     integer not null,
    solucion_infinitivo varchar,
    solucion_sujeto     varchar
);

create index ejercicio_quiz_index
    on laserpiente.ejercicio (quiz);

alter table laserpiente.ejercicio owner to dev;


insert into laserpiente.verbo (infinitivo, gerundio, participio, modo, tiempo, singular1, singular2, singular3, plural1, plural2, plural3)
values ('comer', 'comiendo', 'comido', 'indicativo', 'presente', 'como', 'comes', 'come', 'comemos', 'coméis', 'comen'),
       ('ir', 'yendo', 'ido', 'indicativo', 'presente', 'voy', 'vas', 'va', 'vamos', 'vais', 'van'),
       ('pedir', 'pidiendo', 'pedido', 'indicativo', 'presente', 'pido', 'pides', 'pide', 'pedimos', 'pedís', 'piden');

insert into laserpiente.frase (id, texto)
values (1, E'Probablemente esté de mal humor.'),
       (2, E'Ya está listo con sus tareas probablemente.'),
       (3, E'Posiblemente nadie lo haya visto.'),
       (4, E'No nos reconocen, posiblemente.'),
       (5, E'Es posible que le haga falta.'),
       (6, E'A lo mejor vamos a Sevilla.'),
       (7, E'Es probable que visitemos a Álvaro.'),
       (8, E'Es dudoso que sus problemas sean graves.'),
       (9, E'Puede que sea su coche.'),
       (10, E'Quizás no cerréis la puerta principal.'),
       (11, E'Vamos en la tarde, quizás.'),
       (12, E'Lo mismo te llevas un libro.'),
       (13, E'Igual os quedáis'),
       (14, E'Tal vez puedas quedarte con un amigo de ti.'),
       (15, E'Hace mucho frío, tal vez'),
       (16, E'Nos molesta que haya gatos en el parque infantil.'),
       (17, E'Me enfada que tengamos que trabajar el fin de semana.'),
       (18, E'Lamento que veáis esto.'),
       (19, E'Lamento que no te comprendo.'),
       (20, E'Cómo puedes aguantar que te manden?'),
       (21, E'Tengo miedo de que pierdas tu trabajo.'),
       (22, E'Tiene miedo de que no tiene bastante dinero.'),
       (23, E'Tememos que nos hayan engañado en la agencia turistica.'),
       (24, E'Temo que estropee mi carro.'),
       (25, E'Temo que no puedo hacerlo.'),
       (26, E'Me gusta que tu mujer te deje ir al partido de fútbol.'),
       (27, E'Nos encanta que nuestra hija suela ordenar su habitación.'),
       (28, E'Le alegra que lo protejáis.'),
       (29, E'Te sorprende que viva aquí?'),
       (30, E'Os duele que salga.'),
       (31, E'Le entristece a tu madre que no laves los dientes.'),
       (32, E'Te pone nervioso que conduzca rápido?'),
       (33, E'Me da asco que coman empanadas con azúcar.'),
       (34, E'No supongo que viajen este año al extranjero.'),
       (35, E'No siento que esté cansado.'),
       (36, E'No veo que hagas la tarea.'),
       (37, E'No pienso que esté lluviendo.'),
       (38, E'No digas que ya no hay harina.'),
       (39, E'¿No notan que el cargador no está enchufado?'),
       (40, E'No creas que no veo lo que haces.'),
       (41, E'El maestro no comunica cuándo sea la prueba.'),
       (42, E'No digáis que no tenéis ganas de ir al cine.'),
       (43, E'No suponga que quiere robar.'),
       (44, E'¿No ves que está lluviendo?'),
       (45, E'No pienses que no sé la verdad.'),
       (46, E'No creemos que compremos un nuevo carro.'),
       (47, E'¿No escucháis que os están llamando?'),
       (48, E'Cuando vengas a Budapest, tienes que visitarme.'),
       (49, E'Cuando trabajo contigo, soy feliz. (generalmente)'),
       (50, E'En cuanto llega a su trabajo, bebe un café. (generalmente)'),
       (51, E'En cuanto mi novia nos vea, me echa de casa.'),
       (52, E'Tan pronto como bebes leche, corres al baño. (generalmente)'),
       (53, E'Tan pronto como lleguemos al pueblo, vamos a la playa.'),
       (54, E'Mientras te duches, prepararé la cena.'),
       (55, E'No entrenaré, hasta que esté enfermo.'),
       (56, E'Hasta que me paguen no me quejo.'),
       (57, E'Antes de que llegue mi novia, lavaré los platos.'),
       (58, E'Antes de que vuelvas a casa, envia un email a la jefa.'),
       (59, E'Después de que terminemos me ducharé.'),
       (60, E'Como sigas llegando tarde, no te ascenderán.'),
       (61, E'Desde ahora, siempre que vayas de compras, llevate la bolsa.'),
       (62, E'Siempre que viajo al lago Balaton, recuerdo mi juventud.'),
       (63, E'A partir de ahora, cada vez que pidas pizza, dale propina al correo.'),
       (64, E'Desde que vivo aquí, no puedo dormir.'),
       (65, E'–Puedo descansar un poco más?
–Descanses cuanto quieras.'),
       (66, E'–Dónde vamos por nuestro aniversario?
–Vamos donde quieras.'),
       (67, E'–Qué tomamos?
–Tomamos lo que te guste más.'),
       (68, E'–Por dónde caminamos?
–Caminamos por donde prefieras'),
       (69, E'Es mejor que esperemos un poco más.'),
       (70, E'Es un error que no le dé una oportunidad.'),
       (71, E'Parece fantástico que dejes fumar.'),
       (72, E'Lo más importante es que desayunes cada día.'),
       (73, E'Parece cierto que pone azúcar en su café.'),
       (74, E'Lo evidente es que la humanidad causa el cambio climático.'),
       (75, E'Está claro que este verano es muy caliente.'),
       (76, E'No parece seguro que esté soltera.'),
       (77, E'No está claro que le guste el regalo.'),
       (78, E'Es ridículo que no me creáis.'),
       (79, E'Es una pena que no gane más dinero.'),
       (80, E'Es verdad que no trabaje duro.'),
       (81, E'Lo obvio es que sabéis mucho.'),
       (82, E'Está visto que ella está inocente.'),
       (83, E'No es verdad que sea inútil.'),
       (84, E'No está demonstrado que los celulares causen problemas de salud.'),
       (85, E'Necesito que me des un lápiz.'),
       (86, E'Él la pide que reduzca el volumen de la tele.'),
       (87, E'El director quiere que le devolváis la llave de su carro.'),
       (88, E'Te ruego que conduzcas más lento.'),
       (89, E'Mi madre me ha ordenado que barra el suelo.'),
       (90, E'Me dejan que vuelva tarde esta noche.'),
       (91, E'No te han prohibido que bebas cerveza durante el trabajo?'),
       (92, E'Hagas lo que hagas, hazlo con pasión.'),
       (93, E'Igual me quedo en casa esta noche.');

insert into laserpiente.ejercicio (quiz, frase_id, palabra_q_falta, solucion_infinitivo, solucion_sujeto)
values ('subjuntivo-probabilidad', 1, 2, 'estar', 'singular3'),
       ('subjuntivo-probabilidad', 2, 2, 'estar', 'singular3'),
       ('subjuntivo-probabilidad', 3, 4, 'haber', 'singular3'),
       ('subjuntivo-probabilidad', 4, 3, 'reconocer', 'plural3'),
       ('subjuntivo-probabilidad', 5, 5, 'hacer', 'singular3'),
       ('subjuntivo-probabilidad', 6, 4, 'ir', 'plural1'),
       ('subjuntivo-probabilidad', 7, 4, 'visitar', 'plural1'),
       ('subjuntivo-probabilidad', 8, 6, 'ser', 'plural3'),
       ('subjuntivo-probabilidad', 9, 3, 'ser', 'singular3'),
       ('subjuntivo-probabilidad', 10, 3, 'cerrar', 'plural2'),
       ('subjuntivo-probabilidad', 11, 1, 'ir', 'plural1'),
       ('subjuntivo-probabilidad', 12, 4, 'llevar', 'singular2'),
       ('subjuntivo-probabilidad', 13, 3, 'quedarse', 'plural2'),
       ('subjuntivo-probabilidad', 14, 3, 'poder', 'singular2'),
       ('subjuntivo-probabilidad', 15, 1, 'hacer', 'singular3'),
       ('subjuntivo-verbos_del_corazon', 16, 4, 'haber', 'singular3'),
       ('subjuntivo-verbos_del_corazon', 17, 4, 'tener', 'plural1'),
       ('subjuntivo-verbos_del_corazon', 18, 3, 'ver', 'plural2'),
       ('subjuntivo-verbos_del_corazon', 19, 5, 'comprender', 'singular1'),
       ('subjuntivo-verbos_del_corazon', 20, 6, 'mandar', 'plural3'),
       ('subjuntivo-verbos_del_corazon', 21, 5, 'perder', 'singular2'),
       ('subjuntivo-verbos_del_corazon', 22, 6, 'tener', 'singular3'),
       ('subjuntivo-verbos_del_corazon', 23, 4, 'haber', 'plural3'),
       ('subjuntivo-verbos_del_corazon', 24, 3, 'estropear', 'singular3'),
       ('subjuntivo-verbos_del_corazon', 25, 4, 'poder', 'singular1'),
       ('subjuntivo-verbos_del_corazon', 26, 7, 'dejar', 'singular3'),
       ('subjuntivo-verbos_del_corazon', 27, 6, 'soler', 'singular3'),
       ('subjuntivo-verbos_del_corazon', 28, 5, 'proteger', 'plural2'),
       ('subjuntivo-verbos_del_corazon', 29, 4, 'vivir', 'singular1'),
       ('subjuntivo-verbos_del_corazon', 30, 4, 'salir', 'singular1'),
       ('subjuntivo-verbos_del_corazon', 31, 8, 'lavar', 'singular2'),
       ('subjuntivo-verbos_del_corazon', 32, 5, 'conducir', 'singular1'),
       ('subjuntivo-verbos_del_corazon', 33, 5, 'comer', 'plural3'),
       ('subjuntivo-verbos_de_la_cabeza', 34, 4, 'viajar', 'plural3'),
       ('subjuntivo-verbos_de_la_cabeza', 35, 4, 'estar', 'singular1'),
       ('subjuntivo-verbos_de_la_cabeza', 36, 4, 'hacer', 'singular2'),
       ('subjuntivo-verbos_de_la_cabeza', 37, 4, 'estar', 'singular3'),
       ('subjuntivo-verbos_de_la_cabeza', 38, 6, 'haber', 'singular3'),
       ('subjuntivo-verbos_de_la_cabeza', 39, 7, 'estar', 'singular3'),
       ('subjuntivo-verbos_de_la_cabeza', 40, 8, 'hacer', 'singular2'),
       ('subjuntivo-verbos_de_la_cabeza', 41, 6, 'ser', 'singular3'),
       ('subjuntivo-verbos_de_la_cabeza', 42, 5, 'tener', 'plural2'),
       ('subjuntivo-verbos_de_la_cabeza', 43, 4, 'querer', 'singular3'),
       ('subjuntivo-verbos_de_la_cabeza', 44, 4, 'estar', 'singular3'),
       ('subjuntivo-verbos_de_la_cabeza', 45, 5, 'saber', 'singular1'),
       ('subjuntivo-verbos_de_la_cabeza', 46, 4, 'comprar', 'plural1'),
       ('subjuntivo-verbos_de_la_cabeza', 47, 5, 'estar', 'plural3'),
       ('subjuntivo-frases_temporales', 48, 2, 'ir', 'singular2'),
       ('subjuntivo-frases_temporales', 49, 2, 'trabajar', 'singular1'),
       ('subjuntivo-frases_temporales', 50, 3, 'llegar', 'singular3'),
       ('subjuntivo-frases_temporales', 51, 6, 'ver', 'singular3'),
       ('subjuntivo-frases_temporales', 52, 4, 'beber', 'singular2'),
       ('subjuntivo-frases_temporales', 53, 4, 'llegar', 'plural1'),
       ('subjuntivo-frases_temporales', 54, 3, 'duchar', 'singular2'),
       ('subjuntivo-frases_temporales', 55, 5, 'estar', 'singular1'),
       ('subjuntivo-frases_temporales', 56, 4, 'pagar', 'plural3'),
       ('subjuntivo-frases_temporales', 57, 4, 'llegar', 'singular3'),
       ('subjuntivo-frases_temporales', 58, 4, 'volver', 'singular2'),
       ('subjuntivo-frases_temporales', 59, 4, 'terminar', 'plural1'),
       ('subjuntivo-frases_temporales', 60, 2, 'seguir', 'singular2'),
       ('subjuntivo-frases_temporales', 61, 5, 'ir', 'singular2'),
       ('subjuntivo-frases_temporales', 62, 3, 'viajar', 'singular1'),
       ('subjuntivo-frases_temporales', 63, 8, 'pedir', 'singular2'),
       ('subjuntivo-frases_temporales', 64, 3, 'vivir', 'singular1'),
       ('subjuntivo-estructuras_fijas', 65, 6, 'descansar', 'singular2'),
       ('subjuntivo-estructuras_fijas', 66, 8, 'querer', 'singular2'),
       ('subjuntivo-estructuras_fijas', 67, 7, 'gustar', 'singular3'),
       ('subjuntivo-estructuras_fijas', 68, 7, 'preferir', 'singular2'),
       ('subjuntivo-expresiones_para_valorar', 69, 4, 'esperar', 'plural1'),
       ('subjuntivo-expresiones_para_valorar', 70, 7, 'dar', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 71, 4, 'dejar', 'singular2'),
       ('subjuntivo-expresiones_para_valorar', 72, 6, 'desayunar', 'singular2'),
       ('subjuntivo-expresiones_para_valorar', 73, 4, 'poner', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 74, 7, 'causar', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 75, 6, 'ser', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 76, 5, 'estar', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 77, 6, 'gustar', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 78, 6, 'creer', 'plural2'),
       ('subjuntivo-expresiones_para_valorar', 79, 6, 'ganar', 'singular1'),
       ('subjuntivo-expresiones_para_valorar', 80, 5, 'trabajar', 'singular1'),
       ('subjuntivo-expresiones_para_valorar', 81, 5, 'saber', 'plural2'),
       ('subjuntivo-expresiones_para_valorar', 82, 5, 'estar', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 83, 5, 'ser', 'singular3'),
       ('subjuntivo-expresiones_para_valorar', 84, 7, 'causar', 'plural3'),
       ('subjuntivo-peticion_prohibicion_etc', 85, 4, 'dar', 'singular2'),
       ('subjuntivo-peticion_prohibicion_etc', 86, 5, 'reducir', 'singular3'),
       ('subjuntivo-peticion_prohibicion_etc', 87, 6, 'devolver', 'plural2'),
       ('subjuntivo-peticion_prohibicion_etc', 88, 4, 'conducir', 'singular2'),
       ('subjuntivo-peticion_prohibicion_etc', 89, 7, 'barrer', 'singular1'),
       ('subjuntivo-peticion_prohibicion_etc', 90, 4, 'volver', 'singular1'),
       ('subjuntivo-peticion_prohibicion_etc', 91, 6, 'beber', 'singular2'),
       ('subjuntivo-estructuras_fijas', 92, 1, 'hacer', 'singular2'),
       ('subjuntivo-estructuras_fijas', 92, 4, 'hacer', 'singular2'),
       ('subjuntivo-probabilidad', 93, 2, null, null),
       ('subjuntivo-probabilidad', 93, 3, 'quedarse', 'singular1'),
       ('subjuntivo-probabilidad', 13, 2, null, null);
