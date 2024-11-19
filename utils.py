import fnmatch
import os
import time
import socket
from subprocess import check_output




def prepare_device():
    execute_command("adb uninstall com.siriusxm.aaos.uiapp")
    time.sleep(2)
    execute_command("adb uninstall com.siriusxm.aaos.coreapp.soab.gen8.bmw.rro")
    time.sleep(2)
    execute_command("adb uninstall com.siriusxm.aaos.coreapp.soab.gen8")
    time.sleep(2)


def finder(pattern, path):
    result = []
    try:
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result[0]
    except IndexError:
        return "No such file or directory"


def install_apk(file):
    execute_command("adb shell rm -r /data/misc/logd/logcat*")
    execute_command(f"adb install {file}")


def setup_to_push():
    execute_command("adb shell am force-stop com.siriusxm.aaos.uiapp")
    execute_command("adb shell setenforce 0")
  # execute_command("adb reboot")


def push_xml(xml_file):
    file_found = finder(xml_file, 'C:')
    execute_command("adb root && adb shell rm -r /data/siriusxm/soa/external_config.xml")
    if execute_command(f"adb push {file_found} /data/siriusxm/soa/external_config.xml") == "Pass":
        setup_to_push()
    else:
        print("PLEASE CHECK THE NAME OF THE FILE")


def push_json(json_file):
    file_found = finder(json_file, 'C:')
    execute_command("adb root && adb shell rm -r /data/system/car")
    if execute_command(f"adb push {file_found} /data/system/car/ux_restrictions_prod_config.json") == "Pass":
        setup_to_push()
    else:
        print("PLEASE CHECK THE NAME OF THE FILE")


def execute_command(command):
    try:
        cmd_output = check_output(command, shell=True)
        new_cmd_output = cmd_output.decode("utf-8")
        print(f"executing command: {command}")
        print(new_cmd_output)
        return "Pass"
    except Exception as e:
        print(e.output.decode("utf-8"))
        print(e)
        return "Fail"


def remove_file(file):
    os.system("adb root")
    if "xml" in file:
        if execute_command("adb shell rm -r /data/siriusxm/soa/external_config.xml") == "Pass":
            setup_to_push()
            print("XML FILE ERASED SUCCESSFULLY")
        else:
            print("RPI DOES NOT HAVE ANY XML FILE AT THE MOMENT")
    elif "json" in file:
        if execute_command("adb shell rm -r /data/system/car") == "Pass":
            setup_to_push()
            print("JSON FILE ERASED SUCCESSFULLY")
        else:
            print("RPI DOES NOT HAVE ANY JSON FILE AT THE MOMENT")
    else:
        print("file not found")


def rro_confirm():
    for user in [0, 10]:
        execute_command(f"adb shell cmd overlay list --user {user} > overlay_{user}.txt")
        with open(f'overlay_{user}.txt') as  user_num:
            for line in user_num.readlines():
                if "com.siriusxm.aaos.coreapp.soab.gen8.bmw.rro" in line:
                    print(f"RRO confirmation for user {user}")
                    print(line)
        os.system(f"del {finder(f'overlay_{user}.txt', "C:")}")

def mars_starter():
    os.system('cd "C:\\Program Files (x86)\\Sirius XM Radio\\MARS" && start MARS')


# def read_data(read):
#     with open('userdata.txt') as reader:
#         for line in reader:
#             if read in line:
#                 read = line.replace("user_path:", "").replace("path_to_patterns:", "")
#                 read = read.strip()
#                 return str(read)


def execute_script(file):
    try:
        print("Executing {}".format(file))
        bat_path = finder(file, "C:")
        bat_file = os.system(bat_path)
        return bat_file
    except TypeError:
        print("no file to execute")


def get_ip_address():
    hostname=socket.gethostname()
    ip_address=socket.gethostbyname(hostname)
    return ip_address
