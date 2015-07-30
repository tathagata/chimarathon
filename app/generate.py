import csv
import logging
import os
import sys
import jinja2
import openpyxl

logging.basicConfig(level=logging.DEBUG)

templateVars = { 'year':'2015', 
    'baml_logo':'https://scontent-ord.xx.fbcdn.net/hphotos-xpa1/t31.0-8/1495181_10152923331531645_4198555104746370160_o.jpg',
    'baml_marathon_headline':'Bank of America Chicago Marathon',
    'baml_marathon_blurb':"35 guaranteed spots for Asha for Education runners.<br/> 350 students in India guaranteed education.<br/>Train. Run. Educate! ",
    'asha_for_education_logo':'images/PA080234.JPG',
    'asha_for_education':'', 
    'asha_for_education_blurb':'Asha for Education is a secular organization dedicated to change in India by focusing on basic education in the belief that education is a critical requisite for socio-economic change.', 
    'sample_logo':'',
    'sample_headline':'', 
    'sample_blurb':'', 
}

print os.path.dirname(os.path.dirname(__file__))

templateLoader      = jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/templates")

templateEnv         = jinja2.Environment(loader=templateLoader)
static_output_loc   = 'static'

TEMPLATE_FILES      = ["index.html", "profile.html"]
templates           = map(templateEnv.get_template, TEMPLATE_FILES)

def render_profile_pages(**profile_data):
    for template in templates:
        print repr(profile_data['Why are you running for Asha for Education?'])

        output_text = template.render(FirstName=profile_data['First Name'],
                                     LastName=profile_data['Last Name'],
                                     MarathonReason=profile_data['Why are you running for Asha for Education?'],
                                     channelid=int(profile_data['Channelid']),
                                     donorcount=int(profile_data['DonorsCount']),
                                     totalAmount=int(profile_data['TotalAmount']))

        dir_name    = profile_data['First Name'] + profile_data['Last Name']

        write_templates_to_file("static/users/%s/profile.html" % dir_name, output_text)
        print profile_data['First Name'], "completed"

def render_index_page(runners_data_list):
    index           = templateEnv.get_template("index.html")
    runners_data_list.sort(key=lambda x:x[3], reverse=True)
    outputText      = index.render(top_runners_data_list=runners_data_list[:4],
                            runners_data_list=runners_data_list, **templateVars)
    write_templates_to_file("static/index.html", outputText)


def write_templates_to_file(filename, outputText):
    if "profile" in filename:
        directory = filename[:-12]
        if not os.path.exists(directory):
            os.makedirs(directory)
    with open(filename, 'w') as f:
        f.write(outputText)


def load_csv(filename):
    csv_file = open(filename, 'rb')
    return filter(lambda x: x['First Name'] is not None, #and x.get('Channelid') is not None and len(x['Channelid']) > 0,
                  [row for row in csv.DictReader(csv_file, delimiter=",", quotechar='|') if row is not None])


def load_xlsx(filename):
    def sanitize(value):
        if value is None:
            return 0
        if not isinstance(value, unicode):
            return value

        return value.replace("\u201c", "'").replace("\u2013", "'").replace("\u201d", "").replace("\u2015", "")

    workbook  = openpyxl.load_workbook(filename=filename, use_iterators=True)
    worksheet = workbook.get_sheet_by_name('Form Responses 1')
    rows      = worksheet.rows

    header    = [cell.value for cell in rows.next()]
    data_list = []

    for row in rows:
        data_list.append((dict(zip(header, [sanitize(cell.value) for cell in row]))))
    # return filter(lambda x: x['First Name'] is not None and x.get('Channelid') is not None, data_list)
    return filter(lambda x: x['First Name'] is not None and x['First Name'] != 0, data_list)


def csv_to_jinja(filename):
    all_profile_data = load_xlsx(filename)
    if all_profile_data is not None:
        runners_data_list = [(profile_data['First Name'],
                              profile_data['Last Name'],
                              int(profile_data['DonorsCount']),
                              int(profile_data['TotalAmount']),
                             )

                         for profile_data in all_profile_data]

        render_index_page(runners_data_list)

        for profile_data in all_profile_data:
            render_profile_pages(**profile_data)

if __name__ == '__main__':
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print "No such file"
        sys.exit(1)
    csv_to_jinja(filename)
