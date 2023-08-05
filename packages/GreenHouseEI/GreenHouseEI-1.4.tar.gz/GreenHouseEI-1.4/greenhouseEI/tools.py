__author__ = 'plant-phenotyping'

from zipfile import ZipFile
from pathlib import Path
import os
import cv2
import numpy as np
import sys
import argparse


# output the types of images that are available in the folder
def info(plant_ID, date, input_path):
    try:
        if plant_ID == "" or date == "" or input_path == "":
            print("please inout correct plant_ID or date or input path")
            return 0

        image_type = set()
        path = input_path
        files = os.listdir(path)
        for file in files:
            if plant_ID in file and "zip" in file:
                file_name = file
                break
        # old data structure
        if "Schnable" in file_name:
            with ZipFile(path + '/' + file_name, 'r') as zip:
                for file in zip.namelist():
                    image_type.add(file.split('/')[1].split("_")[0])

            print("available image types:")
            for t in image_type:
                if t in ["Fluo", "IR", "Hyp", "Vis", "Nir"]:
                    print(t)

            return 1

        # new data structure
        else:
            date_formatted = date[:4] + date[5:7] + date[8:10]
            if len(date_formatted) != 8:
                print("please input correct date format")
                return 0

            with ZipFile(path + '/' + file_name, 'r') as zip:
                for file in zip.namelist():
                    if date_formatted in file and "RAW" not in file:
                        image_type.add(file.split('/')[-1].split("__")[2])

            print("available image types:")
            for t in image_type:
                if t in ["Fluo", "IR", "Hyp", "Vis", "Nir"]:
                    print(t)
            return 1

    except BaseException:
        print("please input correct date or plant name")
        return 0



# unzip the folder of images that matches specified plant ID, date, and image type
def unzip(plant_ID, date, image_type, input_path):
    if plant_ID == "" or date == "" or input_path == "":
        print("please input correct plant_ID or date or input path")
        return 0

    if image_type not in ["Fluo", "IR", "Hyp", "Vis", "Nir"]:
        print("please input correct image type")
        return 0
    else:
        path = input_path
        try:
            files = os.listdir(path)
            for file in files:
                if "Schnable" in file:
                    if plant_ID in file and date in file and "zip" in file:
                        file_name = file
                        break
                else:
                    if plant_ID in file and "zip" in file:
                        file_name = file
                        break
            # old data structure
            if "Schnable" in file_name:
                i = 0
                folder_name = file_name[0:-4]

                with ZipFile(path + '/' + file_name, 'r') as zip:
                    for file in zip.namelist():
                        if file.startswith(folder_name + '/' + image_type):
                            zip.extract(file)
                            i += 1
                if i == 0:
                    print("image type not available")
                    return 0

            # new data structure
            else:
                i = 0
                folder_name = file_name[0:-4]

                date_formatted = date[:4] + date[5:7] + date[8:10]
                if len(date_formatted) != 8:
                    print("please input correct date format")
                    return 0

                with ZipFile(path + '/' + file_name, 'r') as zip:
                    for file in zip.namelist():
                        if date_formatted in file:
                            if image_type in file and "RAW" not in file:
                                zip.extract(file)
                                i += 1
                if i == 0:
                    print("image type not available")
                    return 0

        except BaseException:
            print("please input correct date or plant name")
            return 0

        else:
            print("successfully extracted " + image_type + " images from " + folder_name + ".zip")
            return 1



# output numpy arrays of Hyperspectral images
def preprocess(plant_ID, date, input_path):
    if plant_ID == "" or date == "" or input_path == "":
        print("please inout correct plant_ID or date or input path")
        return 0
    flag = 0
    path = input_path
    try:
        files = os.listdir(path)
        for file in files:
            if "Schnable" in file:
                if (plant_ID in file) and (date in file) and "npy" not in file and plant_ID != "" and date != "" and ".zip" not in file:
                    hyp_dir_name = file
                    print(hyp_dir_name)
                    flag = 1
                    break
            else:
                if (plant_ID in file) and "npy" not in file and plant_ID != "" and date != "" and ".zip" not in file:
                    hyp_dir_name = file
                    flag2 = 0
                    folders = os.listdir(path + '/' + hyp_dir_name)
                    date_formatted = date[:4] + date[5:7] + date[8:10]
                    if len(date_formatted) != 8:
                        print("please input correct date format")
                        return 0

                    for folder in folders:
                        if date_formatted in folder:
                            flag = 2
                            flag2 = 1
                            break

                    if flag2 == 1:
                        break

        if flag == 0:
            print('please input correct date or plant name')
            return 0

        # old data structure
        if flag == 1:
            output_name = hyp_dir_name.split("_")[2] + "_" + hyp_dir_name.split("_")[3]
            hyp_dir = hyp_dir_name
            out_fn = output_name

            discard_imgs = ['0_0_0.png', '1_0_0.png']
            dir_path = Path(hyp_dir)
            dir_path = dir_path / 'Hyp_SV_90'
            if not dir_path.exists():
                sys.exit('Hyp images are compressed, please unzip it first')
                return 0
            imgs = list(dir_path.glob('*.png'))
            imgs = sorted(imgs, key=lambda x: int(x.name.split('_')[0]))
            num_imgs = len(imgs)
            print('%s images found.' % num_imgs)
            img_arrs = []
            for i in imgs:
                if not i.name in discard_imgs:
                    arr = cv2.imread(str(i), cv2.IMREAD_GRAYSCALE)
                    img_arrs.append(arr)
            img_array = np.stack(img_arrs, axis=2)
            print(img_array.shape)
            np.save(out_fn, img_array)
            print("numpy array successfully reconstructed!")
            return 1

        # new data structure
        if flag == 2:
            output_name = hyp_dir_name + "_" + date
            hyp_dir = hyp_dir_name
            out_fn = output_name
            dir_path = Path(hyp_dir)
            dir_path = dir_path / date_formatted
            if not dir_path.exists():
                sys.exit('Hyp images are compressed, please unzip it first')
                return 0
            imgs = list(dir_path.glob('*.png'))
            imgs = sorted(imgs, key=lambda x: x.name.split('_')[-1])
            num_imgs = len(imgs)
            print('%s images found.' % num_imgs)
            img_arrs = []
            for i in imgs:
                arr = cv2.imread(str(i), cv2.IMREAD_GRAYSCALE)
                if arr.shape != (480, 640):
                    img_arrs.append(arr)
            img_array = np.stack(img_arrs, axis=2)
            print(img_array.shape)
            np.save(out_fn, img_array)
            print("numpy array successfully reconstructed!")
            return 1

    except BaseException:
        print("please input correct path")
        return 0



# convert zip file of the Hyp images to numpy array
def zip2np(plant_ID, date, input_path):
    path = os.getcwd()
    flag = unzip(plant_ID, date, "Hyp", input_path)
    if flag == 0:
        return 0
    flag = preprocess(plant_ID, date, path)
    if flag == 0:
        return 0
    else:
        return 1


def main():
    ap = argparse.ArgumentParser()
    subparsers = ap.add_subparsers(dest='command')

    reconstruct = subparsers.add_parser('unzip', help='reconstruct specified images')
    reconstruct.add_argument("-n", "--name", required=True, help="plant ID")
    reconstruct.add_argument("-d", "--date", required=True, help="date")
    reconstruct.add_argument("-t", "--type", required=True, help="image type")
    reconstruct.add_argument("-p", "--path", required=True, help="path")

    hyp2arr = subparsers.add_parser('preprocess', help='convert hyp images to numpy array')
    hyp2arr.add_argument("-n", "--name", required=True, help="plant ID")
    hyp2arr.add_argument("-d", "--date", required=True, help="date")
    hyp2arr.add_argument("-p", "--path", required=True, help="path")

    information = subparsers.add_parser('info', help='show available image types for specified plant name and date')
    information.add_argument("-n", "--name", required=True, help="plant ID")
    information.add_argument("-d", "--date", required=True, help="date")
    information.add_argument("-p", "--path", required=True, help="path")

    zip2arr = subparsers.add_parser('zip2np', help='convert zip file of the Hyp images to numpy array')
    zip2arr.add_argument("-n", "--name", required=True, help="plant ID")
    zip2arr.add_argument("-d", "--date", required=True, help="date")
    zip2arr.add_argument("-p", "--path", required=True, help="path")

    args = ap.parse_args()
    if args.command == 'unzip':
        plant_ID = args.name
        date = args.date
        image_type = args.type
        path = args.path
        unzip(plant_ID, date, image_type, path)
    elif args.command == 'preprocess':
        plant_ID = args.name
        date = args.date
        path = args.path
        preprocess(plant_ID, date, path)
    elif args.command == 'info':
        plant_ID = args.name
        date = args.date
        path = args.path
        info(plant_ID, date, path)
    elif args.command == 'zip2np':
        plant_ID = args.name
        date = args.date
        path = args.path
        zip2np(plant_ID, date, path)


if __name__ == '__main__':
    main()
