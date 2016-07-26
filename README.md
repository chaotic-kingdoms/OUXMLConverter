# OUXMLConverter
Standalone script to process courses in OUXML (Open University XML) format

## Introduction
Document describing the OpenLearn XML format: http://www.open.edu/openlearnworks/pluginfile.php/129492/mod_resource/content/1/Hints_and_tips_for_using_OpenLearn_XML_1318799738.pdf



Currently, there is only one export format implemented: Moodle. The script is able to replicate a full Moodle backup package, so the course can be imported in Moodle via the "Restore course" admin option.
It creates the course with a structure optimized for the OppiaMobile platform (https://github.com/DigitalCampus/oppia-mobile-android), so for example, the Glossary section of a course is created as a group of page module activities instead of a glossary module.

## Installation

If you use pip, a `requirements.txt` file is included, so:
```
pip install -r requirements.txt
```
Otherwise, you can use the `setup.py` script included.

## Usage
```
ouxml.py [optional arguments] input_file
```

Arguments:
* `input_file`: **mandatory**. Path to a plain text file containing the URLs to the Open University course sections. The URLs should not to contain the content format parameter (e.g. `?content=scxml`)

* `-h`, `--help`: show the usage help message

* `-v`: show the current version of the script

* `-o OUTPUT_PATH`: the path where the course will be stored. If not set, the path used is the one from where the script is executed.

* `--includerefs`: if set, the references section is added to the course. Otherwise, they are ignored.

* `-n`, `--keepnums`: If set, the numbering in section and session titles (e.g. "3.6.1 -") is kept. Otherwise, they are removed.

#### Troubleshooting

**Debian**: if you find problems trying to install the required libraries, try to install first the related packages from apt:
```
sudo apt-get install libxml2-dev libxslt1-dev zlib1g-dev
```

If you have the glossary thumbnails option enabled and the script throws an error saying `_imagingft C module is not installed`, the problem is that the Pillow library was compiled without `libfreetype`. To solve it, install the library and compile again PIL:
```
sudo apt-get install libfreetype6-dev
pip uninstall pillow
pip install pillow
```

## Contributing

If you want to contribute to the project just follow this steps:

1. Fork the repository.
2. Clone your fork to your local machine.
3. Create your feature branch.
4. Commit your changes, push to your fork and submit a pull request.

### Issues

if you encounter any bug in the app or have a feature request, feel free to [open an issue](https://github.com/chaotic-kingdoms/OUXMLConverter/issues/new)!!
