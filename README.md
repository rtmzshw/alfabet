# alfabet

docker pull postgres
docker run --name my-pgadmin -p 5050:80 -e 'PGADMIN_DEFAULT_EMAIL=rtmzshw@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=alfabet' -d dpage/pgadmin4

docker run --net=my_network -d --name alfabet-postgres -p 5432:5432 -e POSTGRES_PASSWORD=alfabet postgis/postgis
docker run --net=my_network -d --name alfabet-app -p 8000:8000 -e db_host=localhost alfabet-app
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' alfabet-postgres 


pytest