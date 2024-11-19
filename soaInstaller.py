import argparse
import os
import time
from utils import prepare_device, finder, install_apk, execute_command, rro_confirm


parser = argparse.ArgumentParser(description='Tool for installing SOA apks')
parser.add_argument("version", type=str, help="Valid input: soaa-sat, soaa-mars, soab-mars, soab-sat")
parser.add_argument("path", help="path to file")
args = parser.parse_args()


version = args.version
file_path = args.path
valid = {"soaa-sat": '*fullNoHal-generic-userdebug.apk', "soaa-mars": '*full-generic-userdebug.apk',
         "soab-mars": "*full-userdebug.apk", "soab-sat": '*fullNoHal-userdebug.apk'}


def install_rro_carmedia():
    carmedia = ('*release-signed-rpi.apk', '*release-signed.apk')
    carmedia_available = []

    find_rro = finder('oemoverlay-bmw-debug.apk', file_path)
    if find_rro == "No such file or directory":
        print("Error No rro found")
        return "ERROR No rro found"
    else:
        execute_command(f"adb install -r -d {find_rro}")
        time.sleep(6)
    execute_command("adb shell rm -r /system/priv-app/CarMediaApp2")
    for new_carmedia in carmedia:
        new_carmedia = finder(new_carmedia, file_path)
        if new_carmedia == "No such file or directory":
            continue
        else:
            carmedia_available.append(new_carmedia)
            execute_command(f"adb push {new_carmedia} /system/priv-app/CarMediaApp.apk")
            print("Rebooting please wait")
            execute_command("adb reboot && adb wait-for-device")
            time.sleep(30)
            execute_command("adb root")
            execute_command("adb remount")
            time.sleep(3)
            execute_command(f"adb install {new_carmedia}")
            time.sleep(5)
            execute_command("adb shell cmd overlay enable --user 10 com.siriusxm.aaos.coreapp.soab.gen8.bmw.rro")
            execute_command("adb shell cmd overlay enable --user 0 com.siriusxm.aaos.coreapp.soab.gen8.bmw.rro")
            rro_confirm()
    if not carmedia_available:
        print("Error No carmedia found")
        return "ERROR No carmedia found"


def soab_setup(soab_to_install):
    execute_command("adb root")
    time.sleep(2)
    execute_command("adb remount")
    time.sleep(2)
    prepare_device()
    execute_command("adb shell setprop persist.vendor.sxm.satmodule.srslite true")
    install_apk(soab_to_install)
    if install_rro_carmedia() in ("ERROR No carmedia found", "ERROR No rro found"):
        print("Check your files in folder")
    else:
        print("SOAB system setup complete, Rebooting...")
        os.system("adb reboot")


def install_soab():
    time.sleep(3)
    if version == "soab-mars":
        find_mars = finder(valid.get("soab-mars"), file_path)
        if find_mars == "No such file or directory":
            return print("ERROR No SOA found")
        else:
            soab_setup(find_mars)
    elif version == "soab-sat":
        find_sat = finder(valid.get("soab-sat"), file_path)
        if find_sat == "No such file or directory":
            return print("ERROR No SOA found")
        else:
            soab_setup(find_sat)


def install_soaa():
    if version == "soaa-sat":
        if "fullNoHal-generic-userdebug.apk" in file_path:
            execute_command("adb root")
            time.sleep(2)
            prepare_device()
            install_apk(file_path)
            os.system("adb reboot")
        else:
            find_sat_a = finder(valid.get("soaa-sat"), file_path)
            if find_sat_a == "No such file or directory":
                return print("ERROR No SOA found")
            else:
                execute_command("adb root")
                time.sleep(2)
                prepare_device()
                install_apk(find_sat_a)
                os.system("adb reboot")
    elif version == "soaa-mars":
        if "emulator-full-generic-debug.apk" in file_path:
            prepare_device()
            install_apk(file_path)
            os.system("adb reboot")
        else:
            find_mars_a = finder(valid.get("soaa-mars"), file_path)
            if find_mars_a == "No such file or directory":
                return print("ERROR No SOA found")
            else:
                prepare_device()
                install_apk(find_mars_a)
                os.system("adb reboot")


def starting():
    if version in valid:
        if version == "soaa-sat" or version == "soaa-mars":
            install_soaa()
        elif version == "soab-sat" or version == "soab-mars":
            install_soab()
    else:
        print("your version does not match any of the options")


starting()

