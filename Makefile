.PHONY: start build test lint fmt clean help

# Запуск проекта через Docker
start:
	docker-compose up --build

# Сборка Docker-образов
build:
	docker-compose build

# Запуск тестов
test:
	poetry run pytest -v

# Проверка кода через ruff
lint:
	poetry run ruff check .

# Форматирование кода через ruff
fmt:
	poetry run ruff format .

# Удаление контейнеров и очистка
clean:
	docker-compose down --remove-orphans
	rm -rf .pytest_cache/

# Помощь — показывает доступные команды
help:
	@echo "Доступные команды:"
	@echo "  start  - запустить проект (Docker)"
	@echo "  build  - собрать Docker-образы"
	@echo "  test   - запустить тесты"
	@echo "  lint   - проверить код"
	@echo "  fmt    - форматировать код"
	@echo "  clean  - остановить и удалить контейнеры"
	@echo "  help   - показать это сообщение"