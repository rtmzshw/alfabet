## Run
* run -> ```docker pull postgis/postgis```
* run -> ```docker build -t alfabet-app .```
* run -> ```docker-compose up```
* give it a few seconds, it might fail (but restart automatically) a few times because Postgres needs to install extensions

## Interact
For viewing api documentation, naviage to:
* user api -> http://localhost/user/docs
* event api -> http://localhost/user/docs

In order to access event api, you need to authenticate first (get the token from signup api under users).

## architecture
The entire codebase is encapsulated within a single service, using Python's FastAPI web server. \
While the current implementation houses both user and event-related api's, it has been intentionally designed as seperated fastapi apps, what eases separation into two services in the future. \
for storing data I used postgres, mainly because i know you work with it at the company and it will achive the work with no real effort.

## Test
* run  ```pip install --no-cache-dir --upgrade -r ./requirements.txt```
* insure postgres image is running (from the docker-compose)
* run  ```pytest```

### personal note
Prior to this exercise, I hadn't worked with PostgreSQL or Python, and the learning experience has been incredibly enriching. If there are any deviations from best practices in terms of language features or database queries, I appreciate your understanding and welcome any guidance or feedback. I really want to expand my knowledge in various technologies and completely enjoy the process.
