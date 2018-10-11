# Copyright © 2018 Stanislav Lobanov, original plugin code by Roberto Alsina and others.

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This plugin is based on https://github.com/getnikola/plugins/tree/master/v7/sass

import codecs
import os
import sys
import subprocess

from nikola.plugin_categories import Task
from nikola import utils


class BuildSass(Task):
    """Generate CSS out of sass sources."""

    name = "build_sass"
    sources_folder = "sass"
    sources_ext = (".sass", ".scss")

    def gen_tasks(self):
        """Generate CSS out of sass sources."""
        self.logger = utils.get_logger('build_sass', utils.STDERR_HANDLER)

        kw = {
            'cache_folder': self.site.config['CACHE_FOLDER'],
            'themes': self.site.THEMES,
        }
        tasks = {}

        # Find where in the theme chain we define the Sass targets
        # There can be many *.sass/*.scss in the folder, but we only
        # will build the ones listed in sass/targets
        if os.path.isfile(os.path.join(self.sources_folder, "targets")):
            targets_path = os.path.join(self.sources_folder, "targets")
        else:
            targets_path = utils.get_asset_path(os.path.join(self.sources_folder, "targets"), self.site.THEMES)

        try:
            with codecs.open(targets_path, "rb", "utf-8") as inf:
                targets = [x.strip() for x in inf.readlines()]
        except Exception as e:
            self.logger.error('nikola_libsass: error while processing targets: %s' % e)
            targets = []

        for task in utils.copy_tree(self.sources_folder, os.path.join(kw['cache_folder'], self.sources_folder)):
            if task['name'] in tasks:
                continue
            task['basename'] = 'prepare_sass_sources'
            tasks[task['name']] = task
            yield task

        for theme_name in kw['themes']:
            src = os.path.join(utils.get_theme_path(theme_name), self.sources_folder)
            for task in utils.copy_tree(src, os.path.join(kw['cache_folder'], self.sources_folder)):
                if task['name'] in tasks:
                    continue
                task['basename'] = 'prepare_sass_sources'
                tasks[task['name']] = task
                yield task

        # Build targets and write CSS files
        dst_dir = os.path.join(self.site.config['OUTPUT_FOLDER'], 'assets', 'css')
        # Make everything depend on all sources, rough but enough
        deps = []
        for task in tasks.keys():
            for ext in self.sources_ext:
                if task.endswith(ext):
                    deps.append(task)

        def compile_target(target, dst):
            utils.makedirs(dst_dir)
            src = os.path.join(kw['cache_folder'], self.sources_folder, target)
            include_path = os.path.join(kw['cache_folder'], self.sources_folder)
            try:
                import sass
                compiled = sass.compile(
                    string=open(src).read(),
                    include_paths=[include_path]
                )
            except ImportError:
                utils.req_missing(['python-libsass'], 'build Sass files', True, False)
            with open(dst, "w+") as outf:
                outf.write(compiled)

        yield self.group_task()

        # We can have file conflicts.  This is a way to prevent them.
        # I orignally wanted to use sets and their cannot-have-duplicates
        # magic, but I decided not to do this so we can show the user
        # what files were problematic.
        # If we didn’t do this, there would be a cryptic message from doit
        # instead.
        seennames = {}
        for target in targets:
            base = os.path.splitext(target)[0]
            dst = os.path.join(dst_dir, base + ".css")

            if base in seennames:
                self.logger.error(
                    'Duplicate filenames for Sass compiled files: {0} and '
                    '{1} (both compile to {2})'.format(
                        seennames[base], target, base + ".css"))
            else:
                seennames.update({base: target})

            yield {
                'basename': self.name,
                'name': dst,
                'targets': [dst],
                'file_dep': deps,
                'task_dep': ['prepare_sass_sources'],
                'actions': ((compile_target, [target, dst]), ),
                'uptodate': [utils.config_changed(kw)],
                'clean': True
            }