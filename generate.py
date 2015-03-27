import jinja2
from defaults import templateVars

templateLoader = jinja2.FileSystemLoader(searchpath="templates")
templateEnv = jinja2.Environment(loader=templateLoader)
static_output_loc = 'static'

TEMPLATE_FILES = ["index.html", "profile.html"]
templates = map(templateEnv.get_template, TEMPLATE_FILES)

for template in templates:
    outputText = template.render(**templateVars)
    with open("static/%s"%template.name, 'w') as f:
        f.write(outputText)
