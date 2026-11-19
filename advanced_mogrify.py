#!/usr/bin/env python3

from os import scandir, path, chdir, makedirs
from time import time
from subprocess import CalledProcessError, run
from sys import exit as sexit
from sys import argv
from shutil import move

fast = False


def get_base_folder() -> list[str]:
    f: list[str] = [f.path for f in scandir("./Bilder") if f.is_dir()]
    f.sort()
    return f


def recursive_get_png_folders(base_path: str) -> list[str]:
    """Recursively finds all folders containing pngs

    Args:
        base_path (str): Path of the folder

    Returns:
        list[str]: List of all (sub)folders containing pngs
    """
    result: list[str] = []
    f: list[str] = [f.path for f in scandir(base_path) if f.is_file()]
    # print("Files in folder " + base_path + ": " + str(len(f)))
    if f:
        for file in f:
            if file.lower().endswith(".png"):
                result: list[str] = [base_path]
                break
    f: list[str] = [f.path for f in scandir(base_path) if f.is_dir()]
    for folder in f:
        if "HQ-Set" in folder:
            continue
        if "Fappening/Sorted" in folder:
            continue
        if fast and "__" in folder:
            continue
        result += recursive_get_png_folders(folder)
    return result


def process_png_folder(folder: str) -> None:
    """Processes all png files in a folder.

    Args:
        folder (str): Path of the folder
    """
    folder: str = path.abspath(folder)
    chdir(folder)
    time_before: int | float = time()
    # command = "mogrify -format jpg *.png"
    # try:
    #     run(command, shell=True, executable="/bin/bash", check=True)
    # except CalledProcessError as e:
    #     print("Error during mogrify command: " + str(e))
    #     return
    # try:
    #     run("rm *.png", shell=True, executable="/bin/bash", check=True)
    # except CalledProcessError as e:
    #     print("Error during removal: " + str(e))
    #     return
    f: list[str] = [f.path for f in scandir(".") if f.is_file()]
    counter = 0
    for file in f:
        if file.lower().endswith(".png"):
            if process_png_file(file):
                counter += 1
                print("🞓", end="", flush=True)
            chdir(folder)
    time_after: int | float = time()
    total_time: int | float = time_after - time_before
    speed: int | float = counter / total_time if total_time > 0 else 0
    print(
        "\n-->  Converted "
        + str(counter)
        + " PNG to JPG in {:.2f} seconds.".format(total_time)
        + " ({:.2f} PNG/s)".format(speed)
    )


def process_png_file(file: str) -> bool:
    """Converts a png file to jpg. Returns True if successfull.

    Args:
        file (str): The path to the png file.

    Returns:
        bool: True if the conversion was successful, False otherwise.
    """
    if not file.lower().endswith(".png"):
        return False
    filename: str = path.basename(file)
    old_path: str = path.dirname(path.abspath(file))
    # old_subfolder: str = path.basename(old_path)
    # new_subfolder: str = "PNG_CONV-" + old_subfolder.replace("__", "-")
    # new_path: str = path.join(path.dirname(old_path), new_subfolder)
    # if not path.exists(new_path):
    #    makedirs(new_path)
    # new_file: str = path.join(old_path, filename)
    # print(file)
    # print(new_file)
    # try:
    #     move(file, new_file)
    # except KeyboardInterrupt:
    #     print("Process interrupted by user.")
    #     sexit()
    # except Exception as e:
    #     print("\nError moving file: " + str(e))
    #     return False
    if path.exists(filename.replace(".png", ".jpg")):
        print("\nFile already exists: " + filename.replace(".png", ".jpg"))
        return False
    chdir(old_path)
    command: str = 'mogrify -format jpg "' + filename + '"'
    try:
        run(command, shell=True, executable="/bin/bash", check=True)
    except CalledProcessError as e:
        print("\nError during mogrify command: " + str(e))
        return False
    except KeyboardInterrupt:
        print("Process interrupted by user.")
        sexit()
    try:
        run('rm "' + filename + '"', shell=True, executable="/bin/bash", check=True)
    except CalledProcessError as e:
        print("\nError during removal: " + str(e))
        return False
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sexit()
    #print("Converted: " + filename.replace(".png", ".jpg"))
    return True


def main():
    """Main Function"""
    current_dir: str = path.dirname(path.abspath(__file__))
    # print("Processing folder: " + sub_folder)
    png_folders: list[str] = recursive_get_png_folders(current_dir)
    if png_folders:
        for folder in png_folders:
            print("-->  Processing PNG folder: " + folder)
            chdir(current_dir)
            process_png_folder(folder)
            chdir(current_dir)


if __name__ == "__main__":
    if "-f" in argv or "--fast" in argv:
        print("Fast option enabled")
        fast = True

    main()
