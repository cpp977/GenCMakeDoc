import os
import sys
import subprocess
import argparse
import tempfile

parser = argparse.ArgumentParser(description='Generate documentation for cmake builds.')
parser.add_argument('--source-dir', type=str, default='.', dest='source_dir', help='Where the CMakeLists.txt is.')
parser.add_argument('--filter', type=str, default='', dest='opt_filter', help='Specify a filter for cmake options to process. For getting options like MYLIB_SOME_OPT, set filter to MYLIB. If empty, no filter is applied.')
parser.add_argument('--outfile', type=str, default='cmake_doc.md', dest='outfile', help='Filename of the output.')
parser.add_argument('--section-title', type=str, default='Build Options', dest='section_title', help='Title of the section in the README file where the build options are in.')
parser.add_argument('--section-prefix', type=str, default='##', dest='section_prefix', help='Markdown specifier for the section. Normally ##')
parser.add_argument('--README-name', type=str, default='README.md', dest='README_name', help='Name of the README file relative to source-dir')

args = parser.parse_args()

class CMakeOption:
    def __init__(self, name_in, default_in, description_in, opt_type_in):
        self.name = name_in
        self.default = default_in
        self.description = description_in
        self.opt_type = opt_type_in
        name_parts = name.split("_")
        if name_parts[0].isupper():
            self.category = name_parts[0]
        else:
            self.category = "unknown"

    def __str__(self):
        return f"Option {self.name} with default={self.default}. Description={self.description}. Deduced category={self.category}."
    
with tempfile.TemporaryDirectory() as tmpdirname:
    process = subprocess.run(['cmake', '-LH', args.source_dir], capture_output=True, text=True, cwd=tmpdirname)
    filtered = process.stdout[process.stdout.find("// "):]
    plain_options = filtered.split("\n\n")
    options = []
    for plain_opt in plain_options:
        try:
            desc, value = plain_opt.split("\n")
        except:
            pass
        name,type_default = value.split(":")
        opt_type, default = type_default.split("=")
        opt = CMakeOption(name,default,desc[3:], opt_type)
        if args.opt_filter != '':
            if opt.category != args.opt_filter:
                continue
        options.append(opt)

    options = sorted(options, key=lambda opt: opt.category)

    strTable = """\n\n| Option | Default | Description |
| --- | --- | --- |\n"""

    for opt in options:
        strRW = f"| `{opt.name}` | `{opt.default}` | {opt.description} |\n"
        strTable = strTable+strRW
     
    with open(args.source_dir+"/"+args.README_name, 'r+') as md_file:
        data = md_file.read()
        begin = data.find(args.section_prefix + " " + args.section_title) + len(args.section_prefix + " " + args.section_title)
        end = begin+data[begin:].find(args.section_prefix)
        if end < begin:
            end = len(data)
        else:
            print(data[end:])
        data = data[:begin] + strTable + "\n" + data[end:]
        md_file.truncate(0)
        md_file.seek(0)
        md_file.write(data)