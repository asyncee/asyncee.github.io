bootstrap:
	rm -rf ./env
	virtualenv -p python3 env
	env/bin/pip install -U pip
	env/bin/pip install -r requirements.txt

build:
	env/bin/nikola build -a

clean:
	env/bin/nikola check --clean-files
	env/bin/nikola build

serve:
	env/bin/nikola auto --browser

deploy:
	env/bin/nikola github_deploy
