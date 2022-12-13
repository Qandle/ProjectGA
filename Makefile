setup: requirements.txt
	pip install -r requirements.txt

run:
	python .\genetic_algorithm\__init__.py

clean:
    rm -rf .\genetic_algorithm\__pycache__
