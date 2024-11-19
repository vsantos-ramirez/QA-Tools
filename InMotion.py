import argparse
import os

parser = argparse.ArgumentParser(description='In motion control')
parser.add_argument('-m', '--moving', action='store_true', help='Start Moving')
parser.add_argument('-p', '--parking', action='store_true', help='Park vehicle')
args = parser.parse_args()


def in_motion():
    os.system("adb forward tcp:33452 tcp:33452")
    if args.moving:
        os.system("vhal_cli s p -p GEAR_SELECTION -i 8")
        os.system("vhal_cli s p -p PERF_VEHICLE_SPEED -f 20.0")
    elif args.parking:
        os.system("vhal_cli s p -p GEAR_SELECTION -i 4")
        os.system("vhal_cli s p -p PERF_VEHICLE_SPEED -f 0.0")
    else:
        print("Please enter a valid option '-m' to move or '-p' to park")


in_motion()



