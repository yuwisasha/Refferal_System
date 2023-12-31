## RUN
* Create and run containers for django and postgres
```
docker-compose up --build
```

*From 2nd terminal*

* Apply migrations
```
docker-compose run app python manage.py migrate
```

*From 3rd terminal*

* Check db data
```
docker-compose exec db bash
sudo psql -U postgres
```

## Endpoints

|Endpoint|HTTP Method|Result|Data|
| ------ | --------- | ---- | --- |
|```api/v1/login/```|POST|send sms code, code stores int db|phone_number(regex=9\d{9})|
|```api/v1/auth/```|POST|authenticate via csrf, code autodeleting from db|phone_number and code(regex=\d{4})|
|```api/v1/users/profile```|GET|profile details(with X-CSRFToken header)|None|
|```api/v1/users/profile/```|POST|profile list with invite refferal token sent|invite_refferal_token(regex=\d{6})|
