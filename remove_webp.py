#!/usr/bin/env python3

from os import scandir, remove, path
from subprocess import CalledProcessError, run
from multiprocessing import Process

success_count: int = 0
error_count: int = 0


def work_on_folder(folder: str) -> list[str]:
    """Works on an entire folder recursively and starts work_on_file on all found files

    Args:
        folder (str): The folder to be searched
    """
    file_paths: list[str] = []
    entries = scandir(folder)
    for entry in entries:
        if entry.is_dir():
            file_paths.extend(work_on_folder(entry.path))
        elif entry.is_symlink():
            # print("Symlink found, skipping: " + entry.path)
            continue
        elif entry.is_file() and entry.name.lower().endswith(".webp"):
            print("WebP file found, converting: " + entry.path)
            convertable: bool = check_file(entry.path)
            if convertable:
                file_paths.append(entry.path)
    return file_paths


def check_file(file_path: str) -> bool:
    """Checks if the file can be converted.

    Args:
        file_path (str): Path of the file

    Returns:
        bool: Add file to Todo
    """
    new_file_path: str = file_path.replace(".webp", ".png")
    if new_file_path == file_path:
        print(f"Error: File {file_path} does not have a .webp extension.")
        global error_count
        error_count += 1
        return False
    if path.exists(new_file_path):
        print(
            f"Warning: Target file {new_file_path} already exists. Skipping conversion for {file_path}."
        )
        return False
    global success_count
    success_count += 1
    return True

def convert(file_path: str) -> bool:
    """Converts a webp file to png and removes the original webp file.

    Args:
        file_path (str): Path of the webp file

    Returns:
        bool: True if conversion was successful, False otherwise
    """
    command: str = f'dwebp "{file_path}" -o "{file_path.replace(".webp", ".png")}"'
    try:
        run(command, shell=True, executable="/bin/bash", check=True)
    except CalledProcessError as e:
        print(f"Error during conversion of {file_path}: {e}")
        return False
    try:
        remove(file_path)
    except OSError as e:
        print(f"Error during removal of {file_path}: {e}")
        return False
    return True


if __name__ == "__main__":
    base_folder = "."
    file_paths: list[str] = work_on_folder(base_folder)
    processes: list[Process] = []
    for file_path in file_paths:
        p = Process(target=convert, args=(file_path,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print(f"Conversion completed. Successes: {success_count}, Errors: {error_count}")
