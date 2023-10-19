from pathlib import Path
import shutil
import sys
import re


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")


TRANS = {}


for c , i  in  zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = i
    TRANS[ord(c.upper())] = i.upper()


def normalize(name):
    translate_name = re.sub(r'[^\w.]+', '_', name.translate(TRANS))
    return translate_name

def handle_media(file_name, target_folder):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))


def handle_archive(file_name, target_folder):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder):
    scan(folder)
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / "JPEG")
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / "SVG")
   
    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / "AVI")
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / "MP4")
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / "MOV")
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / "MKV")
    
    for file in DOC_DOCUMENTS:
        handle_media(file, folder / "documents" / "DOC")
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / "documents" / "DOCX")
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / "documents" / "TXT")
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / "documents" / "PDF")
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / "documents" / "XLSX")
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / "documents" / "PPTX")
   
    for file in MP3_AUDIO:
        handle_media(file, folder / "audio" / "MP3")
    for file in OGG_AUDIO:
        handle_media(file, folder / "audio" / "OGG")
    for file in WAV_AUDIO:
        handle_media(file, folder / "audio" / "WAV")
    for file in AMR_AUDIO:
        handle_media(file, folder / "audio" / "AMR")
    
    for file in ZIP_ARH:
        handle_archive(file, folder / "archives" / "ZIP")
    for file in GZ_ARH:
        handle_archive(file, folder / "archives" / "GZ")
    for file in TAR_ARH:
        handle_archive(file, folder / "archives" / "TAR")
    
    for file in ANY_OTHER:
        handle_media(file,folder / "other")
    
    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []
#
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
#
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
#
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
#
ZIP_ARH = []
GZ_ARH = []
TAR_ARH = []
#
ANY_OTHER = []

REGISTER_EXTENSION = {
    "JPEG": JPEG_IMAGES,
    "PNG": PNG_IMAGES,
    "JPG": JPG_IMAGES,
    "SVG": SVG_IMAGES,
    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "DOC": DOC_DOCUMENTS,
    "DOCX": DOCX_DOCUMENTS,
    "TXT": TXT_DOCUMENTS,
    "PDF": PDF_DOCUMENTS,
    "XLSX": XLSX_DOCUMENTS,
    "PPTX": PPTX_DOCUMENTS,
    "MP3": MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    "ZIP": ZIP_ARH,
    "GZ": GZ_ARH,
    "TAR": TAR_ARH,
}

FOLDERS = []
UNKNOWN = set()
EXTENSIONS = set()


def get_extensions(name):
    return Path(name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue
        extension = get_extensions(item.name)
        full_name = folder / item.name
        if not extension:
            ANY_OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                ANY_OTHER.append(full_name)


if __name__ == '__main__':
    folder_process = sys.argv[1]
    scan(Path(folder_process))

    categories = [
        ('Images jpeg', JPEG_IMAGES),
        ('Images jpg', JPG_IMAGES),
        ('Images png', PNG_IMAGES),
        ('Images svg', SVG_IMAGES),
        ('Video avi', AVI_VIDEO),
        ('Video mp4', MP4_VIDEO),
        ('Video mov', MOV_VIDEO),
        ('Video mkv', MKV_VIDEO),
        ('Documents doc', DOC_DOCUMENTS),
        ('Documents docx', DOCX_DOCUMENTS),
        ('Documents txt', TXT_DOCUMENTS),
        ('Documents pdf', PDF_DOCUMENTS),
        ('Documents xlsx', XLSX_DOCUMENTS),
        ('Documents pptx', PPTX_DOCUMENTS),
        ('AUDIO mp3', MP3_AUDIO),
        ('AUDIO ogg', OGG_AUDIO),
        ('AUDIO wav', WAV_AUDIO),
        ('AUDIO amr', AMR_AUDIO),
        ('Archives zip', ZIP_ARH),
        ('Archives gz', GZ_ARH),
        ('Archive tar', TAR_ARH),
        ('UNKNOWN', UNKNOWN),
        ('EXTENSIONS', EXTENSIONS),
        ('Other', ANY_OTHER),
    ]

    for category, files in categories:
        print(f'{category}:')
        for file in files:
            print(f'  {file}')

def start():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)



if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())