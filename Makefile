.PHONY: run
run:
	python3 manage.py runserver

.PHONY: test
test:
	python3 manage.py test

.PHONY: coverage
coverage:
	coverage run manage.py test

.PHONY: shell
shell:
	python3 manage.py shell_plus

.PHONE: webapp_container
webapp_container:
	docker exec -it f59f097ae969 bash -l

.PHONY: sass
sass:
	sass network/static/network/css/styles.scss:network/static/network/css/styles.css

.PHONY: sass_watch
sass_watch:
	sass --watch network/static/network/css/styles.scss:network/static/network/css/styles.css
