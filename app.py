from os.path import join, dirname
from dotenv import load_dotenv
import os, dotenv, shutil
from datetime import datetime
import subprocess

START_SCRIPT_DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#Please Update These Variables to Match your System Requirements
pdf_folder = r"c:\temp\pdfout"
work_folder = r"c:\temp\dwg_converter"
search_folders = [r"c:\temp"]
dp_executable_path = r"C:\Program Files (x86)\Any DWG to PDF Converter Pro\dp.exe"
dp_option_PDFColor = r"GrayScale"       #Valid Options are TrueColors, GrayScale, BlackWhite
dp_option_PDFQuality = r"High"          #Valid Options are Normal, Medium, High, Highest
dp_option_HIDE = r"flase"                #Valid Options are true or false



print(START_SCRIPT_DATE)


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

last_date = os.environ.get('LAST_DATE')
if os.path.isdir(work_folder):
    shutil.rmtree(work_folder)
os.mkdir(work_folder)

for search_folder in search_folders:
    for root, dirs, files in os.walk(search_folder): 
        for file in files:     
            if file[-3:].lower() == "dwg":                 
                try:
                    source_file = root + "\\" + file
                    mtime = os.path.getctime(source_file)
                    created_date = datetime.fromtimestamp(mtime)
                    if created_date > datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S'):
                        shutil.copyfile(source_file, os.path.join(work_folder, file))
                        
                except OSError:                    
                    mtime = 0
if dp_option_HIDE == 'true':
        subprocess.call([dp_executable_path, '/InFolder', work_folder, '/OutFolder', pdf_folder, '/ConvertType', 'DWG2PDF', '/PDFColor', dp_option_PDFColor, '/PDFQuality', dp_option_PDFQuality, '/HIDE' ])
else:
    subprocess.call([dp_executable_path, '/InFolder', work_folder, '/OutFolder', pdf_folder, '/ConvertType', 'DWG2PDF', '/PDFColor', dp_option_PDFColor, '/PDFQuality', dp_option_PDFQuality ])

shutil.rmtree(work_folder)


#dotenv.set_key(dotenv_path, "LAST_DATE", str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
dotenv.set_key(dotenv_path, "LAST_DATE", START_SCRIPT_DATE)
