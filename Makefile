install:
	bundler install

build:
	bundler exec jekyll build

watch:
	bundler exec jekyll serve --watch

push:
	JEKYLL_ENV=production bundle exec jekyll build
	cd _site && git add . && git commit -am 'Site update' && git push
	git add . && git commit -am 'Site update' && git push
