import argparse
from utils import push_xml, push_json, remove_file, execute_script

parser = argparse.ArgumentParser(description='tool to run SXM .bat files')
parser.add_argument("files", help="insert the name of your file")
parser.add_argument("-r", "--remove", action='store_true', help="remove the file")
args = parser.parse_args()
files = args.files
remove = args.remove


def file_identifier(bat_xml):
    if remove:
        remove_file(files)
    else:
        if ".bat" in bat_xml:
            run_bat = execute_script(bat_xml)
            return run_bat
        elif ".xml" in bat_xml:
            run_xml = push_xml(bat_xml)
            return run_xml
        elif "json" in bat_xml:
            run_json = push_json(bat_xml)
            return run_json


file_identifier(files)

