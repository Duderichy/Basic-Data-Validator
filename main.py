#!/bin/usr/env python3

import csv
import json
import re
import os

# runs the file check, based on the configuration, and then generate the reports after the checks are finished
# creates the report directory if it does not already exist
def main(config_path="./file_schema.json"):
    with open(config_path) as schema_file:
        schema_dict = json.load(schema_file)
    report_dir = schema_dict["report_dir"]
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    for file_check_results in files_check(schema_dict):
        generate_report(file_check_results, report_dir)
    return None

def files_check(schema_dict):
    return [check_csv_file(file["filename"], file["columns"], schema_dict["data_dir"])
            for file in schema_dict["files"]]

# checks the csv file against the configuraiton, and returns a list of important values
# the return could be improved to use a named tuple, or object, so there is less abiguity
# (also so if the order of return values is changed, you don't end up with a bug)
def check_csv_file(file, columns, root="."):
    all_required_total = 0
    fullmatch_totals = [[0, col[0]] for col in columns]
    empty_rows = 0
    data_row_count = 0
    with open(os.path.join(root, file)) as csv_file:
        csv_reader = csv.reader(csv_file)
        compiled_rexprs = compile_re_list([column[1] for column in columns])
        for i, row in enumerate(csv_reader):
            # checks to see if all headers are what they're supposed to be
            if i == 0:
                for header, header_match in zip(row, [col[0] for col in columns]):
                    if not header == header_match:
                        print("[WARNING] " + header + \
                            " does not match file_schema header of " + \
                            header_match)
            else: # if it's not the first row, it iterates through checking each column of the row for correct values
                data_row_count += 1
                if empty_row(row):
                    empty_rows += 1
                all_required_vals = True
                for j, (val, rexpr, col) in enumerate(zip(row, compiled_rexprs, columns)):
                    if rexpr.fullmatch(val):
                        fullmatch_totals[j][0] += 1
                    elif col[2] == "req":
                        all_required_vals = False
                if all_required_vals:
                    all_required_total += 1
    return (file, columns, all_required_total, empty_rows, fullmatch_totals, data_row_count)

# generates a report to the report directory passed to it
def generate_report(file_check_results, report_path):
    file, columns, required_count, empty_rows, fullmatch_total, data_row_count \
        = file_check_results
    report_file_name = os.path.splitext(file)[0] + "_report.txt"
    report_file_path = os.path.join(report_path, report_file_name)
    required_fraction = required_count / data_row_count
    with open(report_file_path, "w") as report:
        report.write("Report for {}\n".format(file))
        report.write("There were {} rows of data\n".format(data_row_count))
        report.write("There were {} empty lines\n".format(empty_rows))
        for (col_name, regex, required, num), fullmatch_totals in zip(columns, fullmatch_total):
            report.write("Column {} matched regex on {} out of {} or {:3.2f}% of lines\n"\
                .format(col_name, fullmatch_totals[0], data_row_count, fullmatch_totals[0] / data_row_count * 100))
        report.write("Total number of data rows with all required fields matching regex was {} or {:3.2f}%\n"\
            .format(required_count, required_fraction * 100))
        if required_fraction >= .95:
            report.write("Based on the percentage of rows with all required fields present, the data is okay")
        else:
            report.write("Based on the percentage of required fields present too much data is missing")

# checks for empty rows
def empty_row(row):
    if row:
        for s in row:
            if s == '':
                pass
            else: return False
        else: return True

# compiles regexs
def compile_re_list(re_list):
    return [re.compile(expr) for expr in re_list]

# runs the project, but could be changed, to be an actual python module
if __name__ == "__main__":
    print(main())
