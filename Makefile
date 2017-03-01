install:
	bundler install

serve:
	bundler exec jekyll serve --watch --drafts

push:
	JEKYLL_ENV=production bundle exec jekyll build
	cd _site && git add . && git commit -am 'Site update' && git push
	git add . && git commit -am 'Site update' && git push
