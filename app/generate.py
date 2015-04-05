import csv

import jinja2
from app.defaults import templateVars
import os


templateLoader = jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__))+"/templates")
templateEnv = jinja2.Environment(loader=templateLoader)
static_output_loc = 'static'

TEMPLATE_FILES = ["index.html", "profile.html"]
# TEMPLATE_FILES = ["profile.html"]
templates = map(templateEnv.get_template, TEMPLATE_FILES)

def render_static_files(**profile_data):
    print profile_data
    for template in templates:
        output_text = template.render(FirstName=profile_data['First Name'],
                                     LastName=profile_data['Last Name'],
                                     MarathonReason=profile_data['Why do you want to run for Asha for Education'])

        dir_name = profile_data['First Name'] + profile_data['Last Name']

        write_static_file("static/users/%s/profile.html" % dir_name, output_text)


def render_index_file(runners_data_list):
    index = templateEnv.get_template("index.html")

    outputText = index.render(runners_data_list=runners_data_list,
                              **templateVars)
    write_static_file("static/index.html", outputText)


def write_static_file(filename, outputText):
    if "profile" in filename:
        directory = filename[:-12]
        if not os.path.exists(directory):
            os.makedirs(directory)
    with open(filename, 'w') as f:
        f.write(outputText)

def load_data(filename):
    csv_file = open(filename, 'rb')
    return filter(lambda x: x['First Name'] is not None and x['Channelid'] is not None and len(x['Channelid'])>0,
                  [row for row in csv.DictReader(csv_file, delimiter=",", quotechar='|') if row is not None])



def csv_to_jinja(filename):
    all_profile_data=load_data(filename)

    if all_profile_data is not None:
        runners_data_list = [('%s %s' % (profile_data['First Name'], profile_data['Last Name']),
                          'users/%s%s/profile.html' % (profile_data['First Name'], profile_data['Last Name']))

                         for profile_data in all_profile_data]

        render_index_file(runners_data_list)

        for profile_data in all_profile_data:
            render_static_files(**profile_data)


if __name__ == '__main__':
    filename = "data/data.csv"
    csv_to_jinja(filename)

