.PHONY: run
run:
	python3 manage.py runserver

.PHONY: run-sqlite
run-sqlite: export DB_ENV=sqlite
run-sqlite:
	python3 manage.py runserver

.PHONY: test
test:
	docker-compose exec webapp python manage.py test

.PHONY: coverage
coverage:
	docker-compose exec webapp coverage run manage.py test

.PHONY: shell
shell:
	python3 manage.py shell_plus
# docker-compose exec webapp python manage.py shell_plus

.PHONE: webapp_container
webapp_container:
	docker exec -it f59f097ae969 bash -l

.PHONY: sass
sass:
	sass apps/core/static/core/css/styles.scss:apps/core/static/core/css/styles.css

.PHONY: sass_watch
sass_watch:
	sass --watch apps/core/static/core/css/styles.scss:apps/core/static/core/css/styles.css
