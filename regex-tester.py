#!/usr/bin/env python3
"""
show differences between headers
of all files matching regex
"""

import re
import os
import json
import argparse
from argparse import RawTextHelpFormatter as rawtxt
from stringcolor import cs, bold
from columnar import columnar


def head_n_1(filename, encoding):
    """return the first line of filename"""
    with open(filename, mode="r", encoding=encoding) as f:
        first_line = f.readline()
    return first_line.rstrip("\n")


def diff_regex_headers():
    """
    show differences between headers
    of all files matching regex
    """
    version = "0.0.0"
    parser = argparse.ArgumentParser(
        description='regex tester',
        prog='regex-tester',
        formatter_class=rawtxt
    )
    parser.add_argument("regex", nargs="?", help="regular expression (use quotes!)")
    parser.add_argument("--encoding", "-e", help="optional: include file encoding.\ndefaults to utf-8", default="utf-8")
    parser.add_argument("--workdir", "-w", help="optional: use a working dir other than the current dir", default="./")
    parser.add_argument("--delimiter", "-d", help="define a delimiter other than `,`", default=",")
    parser.add_argument("--json", "-j", action="store_true", help="print json object")
    parser.add_argument("--table", "-t", action="store_true", help="print table")
    parser.add_argument("--files", "-f", action="store_true", help="only show matching files")
    args = parser.parse_args()
    regex = args.regex
    encoding = args.encoding
    working_dir = args.workdir
    do_json = args.json
    do_table = args.table
    do_files = args.files
    delim = args.delimiter
    if delim == "\\t":
        delim = "\t"
    _, _, all_filenames = next(os.walk(working_dir))
    regex = re.compile(regex)
    matching_filenames = []
    # find all matching files
    for filename in all_filenames:
        if regex.match(filename):
            matching_filenames.append(filename)
    if len(matching_filenames) < 2:
        print(cs("Please use a pattern matching at least 2 files", "yellow", "red"))
        exit()
    if do_files:
        for filename in matching_filenames:
            print(cs(filename, "Chartreuse"))
        exit()
    headers = {}
    columns = []
    # get headers from file and build list of all headers
    for matched_file in matching_filenames:
        first_line = head_n_1(os.path.join(working_dir, matched_file), encoding)
        first_line = first_line.split(delim)
        header_dict = [{"value": x, "position": first_line.index(x)} for x in first_line]
        for header in first_line:
            if header not in columns:
                columns.append(header)
        headers[matched_file] = header_dict
    if do_json:
        print(json.dumps(headers))
    elif do_table:
        # show diff
        columnar_headers = [""]
        for column in columns:
            columnar_headers.append(column)
        columnar_rows = []
        for key, value in headers.items():
            colored_key = cs(key, "Cornsilk")
            this_row = [colored_key]
            for column in columns:
                found =False
                for val_pos in value:
                    if val_pos["value"] == column:
                        this_row.append(val_pos["position"] + 1)
                        found = True
                if not found:
                    this_row.append(cs("0", "red"))

            columnar_rows.append(this_row)
        table = columnar(columnar_rows, columnar_headers)
        print(table)
    else:
        # basic output
        for matched_file in matching_filenames:
            print(cs(matched_file, "yellow"))
            first_line = head_n_1(os.path.join(working_dir, matched_file), encoding)
            first_line = first_line.split(delim)
            print(first_line)
            # print missing
            missing = ""
            for column in columns:
                if column not in first_line:
                    missing += f"\'{column}\', "
            if missing:
                print("Missing:", cs(missing[:-2], "red"))
            else:
                print(cs("Nothing missing", "green"))

if __name__ == "__main__":
    diff_regex_headers()
