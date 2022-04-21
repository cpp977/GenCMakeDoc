# GenCMakeDoc
Generates documentation of all cmake build options for a cmake based project directly into the project's README

# Use case
This action is for projects which provide a [cmake](https://cmake.org/) build.
Usually, the cmake build can be controlled by several options which are passed to the cmake command.
The options are specified in the `CMakeLists.txt` file using cmake's [option](https://cmake.org/cmake/help/latest/command/option.html) or cmake's [set](https://cmake.org/cmake/help/latest/command/set.html) as for example:
```
option(MYLIB_BUILD_TESTS "Whether to build the tests for the project." OFF)
option(MYLIB_SOME_OTHER_OPT "This controls some other stuff." ON)
```
When these options are defined, the name, the default value and the description are already given.
Documenting these options in the project's README would lead to duplication and superfluous work.
This action will scan the `CMakeLists.txt` of the project using `cmake -LH` and generate a markdown table of all options containing the name, the default value and the description.
Then the action puts this table directly to the project's README site in a specified section.
For the examples above, the table will look like this:

| Option | Default | Description |
| --- | --- | --- |
| `MYLIB_BUILD_TESTS` | `OFF` | Whether to build the tests for the project. |
| `MYLIB_SOME_OTHER_OPT` | `ON` | This controls some other stuff. |

# Inputs
## `source_dir`
**Required** The directory where the CMakeLists.txt is located from which the options are documented. Should be set after a call to `actions/checkout`.

## `option_filter`
Specify a filter for cmake options to process. For getting options like `MYLIB_SOME_OPT`, set filter to `"MYLIB"`. If empty, no filter is applied. Default `""`.

## `heading_marker`
Markdown specifier for the heading of the section which contains the documentation of cmake build options. Default `"#"`.

## `heading_title`
Title of the section which contains the documentation of cmake build options. Default `"Build Options"`.
The action will replace the complete content in this section so that **only** the table of options should be present in this section.

## `readme_name`
Filename of the README file relative to source_dir. Default: `"README.md"`

## `configure_opts`
Options which are passed to the cmake configure call. Format: `OPT1=VAL1 OPT2=VAL2 ...` Default: `""`

# Notes
Normally, the usage consists of three steps:
- You have to checkout the repository first by using for example [actions/checkout](https://github.com/marketplace/actions/checkout).
- The you can generate the cmake options documentation with this action.
- Finally, you have to commit and push the changes. Here, you can use [EndBug/add-and-commit](https://github.com/marketplace/actions/add-commit).

You must ensure that the configure step of the `cmake` command does succeed. Possible dependencies need to be installed.

# Example usage
```
uses: actions/checkout@v3

#Optionally install dependencies for the project so that cmake's configure step will run successfully.

uses: cpp977/GenCMakeDoc@v1
with:
    source_dir: $GITHUB_WORKSPACE
    option_filter: MYLIB
    
uses: EndBug/add-and-commit@v8
with:
    message: 'Updated documentation for cmake build parameters.'
    committer_name: GitHub Actions
    committer_email: actions@github.com
```
