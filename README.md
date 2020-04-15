## KON-Konverter
Convert spreadsheet headers to Ennovatis in the Konstanz project.

# Usage
- Launching the program shows a file dialog. Please choose a folder.
- All .csv files in all subfolders will be found and converted.
- The converted files will be stored in a parallel folder structure.

Example folder structure:

    Outside-Folder
    	TOP-Folder                  <- Selected folder
    		Sub-Folder 1
    			file 1.csv
    			file 2.csv
    		Sub-Folder 2
    			file 3.csv

    	TOP-Folder_konvertiert      <- New folder
    		Sub-Folder 1
    			file 1.csv
    			file 2.csv
    		Sub-Folder 2
    			file 3.csv

If the folder **TOP-Folder** is selected by the user, a new folder
**TOP-Folder_converted** will be created, containing all the converted
files. If the new folder already exists, all files within are overwritten
without warning.

# Contact
Franziska Bockelmann: For the data
Joris Zimmermann: For this program