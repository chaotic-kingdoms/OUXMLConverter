import sys
import argparse
from distutils.dir_util import remove_tree
from distutils.file_util import copy_file

import os

import settings
from CourseExporter import CourseExporter
from CourseParser import CourseParser
from utils.CourseUtils import CourseUtils


def main(argv):
    parser = argparse.ArgumentParser(version=settings.PROJECT_VERSION)
    parser.add_argument('input_file',type=str,
                        help='.txt file containing the URLs to the Open University course sections.')

    default_output = os.path.abspath(os.path.dirname(argv[1])) if len(argv) > 1 else ""

    parser.add_argument('-o', '--output_path', type=str,
                        help='Directory where the course will be stored.', default=default_output)
    parser.add_argument('--includerefs', help='If set, the references section is added to the course. Otherwise, they are ignored.', action="store_true")
    parser.add_argument('-n', '--keepnums', help='If set, the numbering in the section and session titles (e.g. "3.6 -") is kept.', action="store_true")
    args = parser.parse_args()

    CourseUtils.set_start_time()

    input_path = args.input_file
    output_path = args.output_path
    settings.OUTPUT_PATH = output_path

    parser = CourseParser(input_path, output_path, args.includerefs, args.keepnums)
    course = parser.retrieve_course()

    course_name = CourseUtils.get_course_name(course.title_full)
    course_dir = os.path.join(output_path, settings.TEMP_FOLDER, course_name)

    exporter = CourseExporter(course, output_path, course_dir, args.keepnums)
    exporter.generate_backup()

    backup_path = CourseUtils.compress_course(course_dir)

    copy_file(backup_path, output_path)
    remove_tree(os.path.join(output_path, 'temp'))
    print ('\nCourse created successfully at path: ' + output_path)
    duration = CourseUtils.get_program_duration()
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    print ('Duration: ' + str(minutes) + 'm ' + str(seconds) + 's.')

if __name__ == "__main__":
    main(sys.argv)

