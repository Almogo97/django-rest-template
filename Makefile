delete-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete