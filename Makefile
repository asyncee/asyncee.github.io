install:
	bundler install

build:
	bundler exec jekyll build --unpublished

serve:
	bundler exec jekyll serve --watch --unpublished

push:
	JEKYLL_ENV=production bundle exec jekyll build
	cd _site && git add . && git commit -am 'Site update' && git push
	git add . && git commit -am 'Site update' && git push
