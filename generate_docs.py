#! /usr/bin/env python3
from pdoc import cli
import os

class PdocArgs(object):

    def __init__(self, modules):
        self.template_dir = None
        self.html = True
        self.http = None
        self.filter = None
        self.external_links = None
        self.overwrite = True
        self.html_dir = 'docs'
        self.modules = modules
        self.link_prefix = ''
        self.html_no_source = False



cli.main(PdocArgs(['acsploit']))
os.rename('docs/acsploit.html', 'docs/index.html')

modules = ['exploits', 'input', 'output', 'options']
for module in modules:
    cli.main(PdocArgs([module]))

toc_end = """</ul>\n</li>\n</ul>\n</li>"""

# Generate the Sub-module table of contents
sub_module_entries = """\n<li><h3><a href="">Sub-modules</a></h3>\n<ul>"""

for module in modules:
    sub_module_entries += '<li><h4><code><a title="{}" href="{}/index.html">{}</a></code></h4></li>\n'.format(module, module, module)

sub_module_entries += """</ul>\n</li>"""
doc_path = "docs/index.html"

with open(doc_path) as f:
    newText=f.read()
    pos = newText.find(toc_end)
    if pos > 0:
        pos += len(toc_end)
        newText = newText[:pos] + sub_module_entries + newText[pos:]

with open(doc_path, "w") as f:
    f.write(newText)

