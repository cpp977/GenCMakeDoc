# GenCMakeDoc
Generates documentation of all cmake build options for a cmake based project directly into the project's README

# Inputs

## `source_dir`

**Required** The directory where the CMakeLists.txt is located from which the options are documented. Should be set after a call to `actions/checkout`.

## `option_filter`
Specify a filter for cmake options to process. For getting options like `MYLIB_SOME_OPT`, set filter to `"MYLIB"`. If empty, no filter is applied. Default `""`.

# Example usage

```
uses: actions/GenCMakeDoc@v0
with:
    source_dir: $GITHUB_WORKSPACE
    option_filter: MYPROJECT
```
