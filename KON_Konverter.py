# Copyright (C) 2020 Joris Zimmermann

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

"""Convert spreadsheet headers to Ennovatis in the Konstanz project.

To be used in the following folder:
V:\MA\5_Messdaten\696_Schmidtenbühl\01_Daten-Original\01_GLT\Original

Contact for usage: Franziska Bockelmann

Author of this script: Joris Zimmermann

"""

import pandas as pd
import os
import glob
import logging
import csv

# Define the logging function
logger = logging.getLogger(__name__)

def main():
    """Run the main function on all files in a folder."""
    top_folder = folder_dialog(initialdir=os.path.expanduser("~"))

    if top_folder == None:
        logger.info('No folder selected.')
        return

    files = glob.glob(top_folder + '/**/*.csv', recursive=True)

    logger.info('Converted files:')
    for filename in files:

        df = read_and_change_file(filename)
        # print(df)

        rel_path = os.path.relpath(filename, top_folder)

        new_path = os.path.join(top_folder+'_converted', rel_path)

        if not os.path.exists(os.path.dirname(new_path)):
            os.makedirs(os.path.dirname(new_path))

        if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
            df.to_excel(new_path)
        else:  # With CSV, we need a specific format
            df.to_csv(new_path, sep=';', quoting=csv.QUOTE_ALL)

        print(new_path)  # Print the created files


def main_file():
    """Run the main function on a selection of files."""
    files = file_dialog()

    for filename in files:

        df = read_and_change_file(filename)

        splitext = os.path.splitext(filename)
        filename_new = splitext[0] + '_geändert'+splitext[1]

        if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
            df.to_excel(filename_new)
        else:  # With CSV, we need a specific format
            df.to_csv(filename_new, sep=';', quoting=csv.QUOTE_ALL)

        print(filename_new)

def read_and_change_file(filename):

    if os.path.splitext(filename)[1] in ['.xlsx', '.xls']:
        df = pd.read_excel(filename, index_col=0)
    else:
        df = pd.read_csv(filename, index_col=0, sep=';')

    rename_dict = dict()
    for col in df.columns:
        rename_dict[col] = change_column(col)

    df.rename(columns=rename_dict, inplace=True)

    return df


def change_column(col):
    """Replace and filter the column header text."""
    import re

    col = re.sub('ä', 'ae', col)  # replace
    col = re.sub('ö', 'oe', col)  # replace
    col = re.sub('ü', 'ue', col)  # replace
    col = re.sub('ß', 'ss', col)  # replace

    # Match the text right until before the second comma
    match = re.search(r'([^,]*,[^,]*).*', col)  # extract group match
    if match:
        col = match.group(1)

    return col


def file_dialog(initialdir=os.getcwd()):
    """Present a file dialog for one or more Excel files."""
    from tkinter import Tk, filedialog

    title = 'Please choose an Excel file'
    root = Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(
                initialdir=initialdir, title=title,
                filetypes=(
                    ('CSV File', '*.csv'),
                    ('Excel File', ['*.xlsx', '*.xls']),
                    )
                )
    files = list(files)

    return files


def folder_dialog(initialdir=os.getcwd()):
    """Present a folder dialog for one or more Excel files."""
    from tkinter import Tk, filedialog

    title = 'Please choose a folder. All .csv files within are converted.'
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(initialdir=initialdir, title=title)

    if len(folder) == 0:
        folder = None

    return folder


def print_readme():
    """Print contents of the readme to the screen."""
    try:
        with open('README.md') as f:
            readme = f.read()
    except Exception as e:
        logger.exception(e)
    else:
        print(readme)
        print()


def setup(log_level='INFO'):
    """Set up the logger."""
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logger.setLevel(level=log_level.upper())  # Logger for this module


if __name__ == '__main__':
    setup()
    print_readme()

    try:
        main()
        # main_file()
    except Exception as e:
        logger.exception(e)
    input('\nPress the enter key to exit.')
