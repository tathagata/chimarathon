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
    # print profile_data
    for template in templates:
        print profile_data['Why are you running for Asha for Education?']
        output_text = template.render(FirstName=profile_data['First Name'],
                                     LastName=profile_data['Last Name'],
                                     MarathonReason=profile_data['Why are you running for Asha for Education?'])

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


def load_csv(filename):
    csv_file = open(filename, 'rb')
    return filter(lambda x: x['First Name'] is not None and x.get('Channelid') is not None and len(x['Channelid']) > 0,
                  [row for row in csv.DictReader(csv_file, delimiter=",", quotechar='|') if row is not None])


def load_xlsx(filename):
    def sanitize(value):
        print value, type(value)
        if not isinstance(value, unicode):
            return value

        v = value.replace("\u201c", "'").replace("\u2013", "'").replace("\u201d", "").replace("\u2015", "")
        return v

    import openpyxl

    workbook = openpyxl.load_workbook(filename='data/data.xlsx', use_iterators=True)
    worksheet = workbook.get_sheet_by_name('Form Responses 1')
    rows = worksheet.rows
    header = [cell.value for cell in rows.next()]
    data_list = []
    for row in rows:
        # print [sanitize(cell.value) for cell in row]
        data_list.append((dict(zip(header, [sanitize(cell.value) for cell in row]))))
    # pp( data_list)
    return filter(lambda x: x['First Name'] is not None and x.get('Channelid') is not None, data_list)



def csv_to_jinja(filename):
    # all_profile_data=load_csv(filename)
    all_profile_data = load_xlsx(filename)
    print all_profile_data
    if all_profile_data is not None:
        runners_data_list = [('%s %s' % (profile_data['First Name'], profile_data['Last Name']),
                          'users/%s%s/profile.html' % (profile_data['First Name'], profile_data['Last Name']))

                         for profile_data in all_profile_data]

        render_index_file(runners_data_list)

        for profile_data in all_profile_data:
            render_static_files(**profile_data)


if __name__ == '__main__':
    filename = "data/data.xlsx"

    csv_to_jinja(filename)

