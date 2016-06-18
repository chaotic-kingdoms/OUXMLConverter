import sys
from distutils.dir_util import remove_tree
from distutils.file_util import copy_file

import os

import settings
from CourseExporter import CourseExporter
from CourseParser import CourseParser
from utils.CourseUtils import CourseUtils


def main(argv):
    if len(argv) != 3:
        print 'Wrong number of arguments.'
        print 'Usage:'  # TODO
    else:
        CourseUtils.set_start_time()

        input_path = sys.argv[1]
        output_path = sys.argv[2]
        settings.OUTPUT_PATH = output_path

        parser = CourseParser(input_path, output_path)
        course = parser.retrieve_course()

        course_name = CourseUtils.get_course_name(course.title_full)
        course_dir = os.path.join(output_path, settings.TEMP_FOLDER, course_name)

        exporter = CourseExporter(course, output_path, course_dir)
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

