# General testing and feedback

Unified tester for any language, for any exam

## Currently supported languages

 - Python
 - C++

# How to run

run the feedback module with the name of the tested file, and the appropriate configuration

## Examples

Python:
```
python -m feedback "tests/fixtures/integration/py/tested.py" "tests/fixtures/integration/py/py_config.json"
```

C++:
```
python -m feedback "tests/fixtures/integration/cpp/tested.cpp" "tests/fixtures/integration/cpp/cpp_config.json"
```

## Config file arhitecture

The config file uses JSON to serialise data.

### Tests

Specify a list of tests that should be ran, under the `"tests"` key, with each test name as a key and with a set of key-value pairs under that.

Every test requires the `"weight"` key, and some tests may require other parameters

#### Currently supported tests and parameters

 - C++
    - compile
        - weight
        - (optional) type: "o"
        - (optional) warning_penalty: [0.0, 1.0]
    - functionality
        - weight
    - functionality_executable
        - weight
    - comments
        - weight
    - static
        - weight
        - (optional) error_penalty: [0.0, 1.0]
    - style
        - style
        - weight
 - Python
    - syntax
        - weight
    - functionality
        - weight
    - comments
        - weight

### Execution

Under the `"execution"` you must specify the `"tester_file"` key and a value pointed to a file that runs the test, if you want to use the `"functionality"` test.

You can also specify a list of aditional files that need to be included in testing under `"additional_files"`.

### Example config

```
{
    "tests": {
        "compile": {
            "weight": 0.1
        },
        "functionality": {
            "weight": 0.6
        },
        "comments": {
            "weight": 0.1
        },
        "static": {
            "weight": 0.1
        },
        "style": {
            "weight": 0.1,
            "style": "google"
        }
    },
    "execution":{
        "tester_file": "run_code.cpp",
        "additional_files": [
            "test.h"
        ]
    }
}
```