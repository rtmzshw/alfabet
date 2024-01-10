# alfabet

docker pull postgres
docker run --name alfabet-postgres -p 5432:5432 -e POSTGRES_PASSWORD=alfabet -d postgres
docker run --name my-pgadmin -p 5050:80 -e 'PGADMIN_DEFAULT_EMAIL=rtmzshw@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=alfabet' -d dpage/pgadmin4

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' alfabet-postgres 

docker run --name alfabet-postgres -p 5432:5432 -e POSTGRES_PASSWORD=alfabet -d postgis/postgis