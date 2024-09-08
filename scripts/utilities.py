"""
Some useful utilities.
"""
import os
from glob import glob

__author__ = "Johnathan Lin <jagonball@g-mail.nsysu.edu.tw>"
__email__ = "jagonball@g-mail.nsysu.edu.tw"


def create_folder(folder_name, path_to_folder, verbose = False):
    """Create folder if not already exist.

    :param folder_name: The folder name.
    :type folder_name: str
    :param path_to_folder: The path to check for the folder.
    :type path_to_folder: str
    :return: The full path to inside the folder.
    :rtype: str
    """
    final_folder = path_to_folder / folder_name
    if verbose:
        print(f'Checking if folder "{folder_name}" '
              f'exists in "{path_to_folder}"...')
    if folder_name not in os.listdir(path_to_folder):
        if verbose:
            print(f'## Folder "{folder_name}" not found, creating...')
        os.mkdir(final_folder) 
    return final_folder


def search_target_files(file_list, folder_path):
    """Search files matching "file_list" in "folder_path".

    :param file_list: a list of files. (accept regular expression)
    :type file_list: list
    :param folder_path: The folder path to search for.
    :type folder_path: Path or str
    :return: A list of target files.
    :rtype: list
    """
    target_files_list = []
    for name in file_list:
        target_files = str(folder_path / name)
        target_files_list += glob(target_files)
    return target_files_list


def text_color(text, color=None, background=None):
    """Change the text and background color with ANSI escape code.
       The options are: 
       'black', 'red', 'green', 'yellow',
       'blue', 'magenta', 'cyan', 'white',
       'gray', 'bright red', 'bright green', 'bright yellow',
       'bright blue', 'bright magenta', 'bright cyan', 'bright white'

    :param text: The input text.
    :type text: str
    :param color: The text color, defaults to None
    :type color: str, optional
    :param background: The background color, defaults to None
    :type background: str, optional
    :return: The color modified text
    :rtype: str
    """
    options = ['black', 'red', 'green', 'yellow',
               'blue', 'magenta', 'cyan', 'white',
               'gray', 'bright red', 'bright green', 'bright yellow',
               'bright blue', 'bright magenta', 'bright cyan', 'bright white']
    fg_code = ['30', '31', '32', '33', '34', '35', '36', '37',
               '90', '91', '92', '93', '94', '95', '96', '97']
    bg_code = ['40', '41', '42', '43', '44', '45', '46', '47',
               '100', '101', '102', '103', '104', '105', '106', '107']
    if color in options:
        color = fg_code[options.index(color)]
    else:
        color = '39' # Default.
    if background in options:
        background = bg_code[options.index(background)]
    else:
        background = '49' # Default.
    # print(f'Color = {color}; Background = {background}')
    text = f'\033[{color}m\033[{background}m{text}\033[00m'
    return text
 

# Reference: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# black   = "\033[30m"
# red     = "\033[31m"
# green   = "\033[32m"
# yellow  = "\033[33m"
# blue 34
# magenta 35
# cyan 36
# white   = "\033[37m"
# nocolor = "\033[0m"