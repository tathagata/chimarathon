Asha Chicago Chapter's site for Bank of America 2015's marathon

How to generate static pages
- Download the spreadsheet from google docs as .xlsx
- copy the file to data/ folder and name it as data.xlsx
- run `python app/generate.py` from the command line
- this will create the static pages under static directory
- use the commands in the deploy.sh(ask me for it) to upload the static files to the directory them to the server

Things to make sure
- each runner's firstname and lastname put together makes his directory
- it has 2 file called profile.html and profile.jpg. both should have 755 attributes (chmod a+r *)