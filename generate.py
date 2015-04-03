import jinja2
from defaults import templateVars
import csv

templateLoader = jinja2.FileSystemLoader(searchpath="templates")
templateEnv = jinja2.Environment(loader=templateLoader)
static_output_loc = 'static'

TEMPLATE_FILES = ["index.html", "profile.html"]
# TEMPLATE_FILES = ["profile.html"]
templates = map(templateEnv.get_template, TEMPLATE_FILES)

def render_static_files(**profile_data):
    print profile_data
    for template in templates:

        outputText = template.render(FirstName=profile_data['First Name'],
                                     LastName=profile_data['Last Name'],
                                     MarathonReason=  profile_data['Why do you want to run for Asha for Education'],
                                     templateVars=templateVars)
        dirname = profile_data['First Name'] + profile_data['Last Name']
        with open("static/users/%s/profile.html"%dirname, 'w') as f:
            f.write(outputText)



def load_data(filename):
    csv_file = open(filename, 'rb')
    return [row for row in csv.DictReader(csv_file, delimiter=",", quotechar='|')]


def csv_to_jinja(filename):
    all_profile_data=load_data(filename)
    for profile_data in all_profile_data:
        render_static_files(**profile_data)


if __name__ == '__main__':
    filename = "data/Team Asha 2015 Registration (Responses) - Form Responses 1.csv"
    csv_to_jinja(filename)

