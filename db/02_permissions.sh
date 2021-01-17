psql -U postgres $POSTGRES_DB << EOF
create user $DB_USER with password '$DB_PASS';
grant all on schema laserpiente to dev;
alter table laserpiente.verbo owner to dev;
alter table laserpiente.frase owner to dev;
alter table laserpiente.ejercicio owner to dev;
EOF
