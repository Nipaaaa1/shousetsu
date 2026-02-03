twdev:
	pnpm tailwindcss -i ./app/static/css/input.css -o ./app/static/css/app.css --watch

twprod:
	pnpx @tailwindcss/cli -i ./app/static/css/input.css -o ./app/static/css/app.css --minify

dev:
	uv run manage.py runserver

migrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate
