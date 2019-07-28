# Data Validation

The purpose of this program is to provide a general framework for testing csv files against a configuration stored in a json file.

The program can be run with `python3 main.py`

## Configuration

file\_schema.json contains a list of files to be tested.

### file\_schema.json is in the following format:
* contains "data_dir" key, value pair for the directory where the files are
* contains "report_dir" key, value pair for the directory where the reports should be written out to
* contains "files" key, value pair for the list of files to be checked
  * file contains the filename of the file to be tested
  * file contains columns with the list of columns to be checked
    * each column contans a the column name
    * each column contans a regex to be tested against
    * each column array can contain a "req" arguement to tell that that column is required
      * this factors into the report
      * a row either has all required fields matching the regex, or it does not, the number of rows with all required arguements passing the regex is reported in the reports


## Design considerations

1) It should aim to be extensible for other types of files, and other file schema
2) It should aim to be modular in design
3) It should aim to keep functions small, and only doing one thing
4) File schema config should be easy to understand and manipulate

I started out thinking I should iterate through the rows checking against regex, keeping a record of the total amount of empty rows, and empty columns, which would provide a way of checking rows which would be easy to verify

I should generate a report including the number of empty columns, empty rows, and bad values.

I should also consider keeping a record, or making a way to create a list of all the bad rows and bad values.

I ended up deciding to stick with the regex approach, because it allows for a great amount of flexibility in configuring the project, without having to change the project code. I decided to go with a json configuration file, because it's a standard format and easy to deal with, and also easy to modify in a way that allows for program extensibility.

### Room for improvement
 * this project could use unit testing
 * this project could have implimentation added for dealing with different kinds of files outside of .csv files 
 * type hints could be added
 * check_csv_file could be split up into two-three smaller functions, increasing readability and modularity
 * there could be a function to automatically generate a default configuration file, or something from an existing file
 * the numbers at the end of the column arrays in the config could be removed, since I don't use them anywhere
 * if performance is a concern, it could be parallelized 
 * this project could be changed to be an actual python module
 * could allow for command line arguement to specify the location of the configuration file to be used
 * there could be a percentage threshold field added for each file for the required fields to determine if the file is okay or not