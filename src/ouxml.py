import sys
from CourseParser import ParseXML
from CourseExporter import CourseExporter
from utils.CourseUtils import CourseUtils
import settings
import os
from distutils.file_util import copy_file
from distutils.dir_util import remove_tree


def main(argv):
    if len(argv) != 3:
        print 'Wrong number of arguments.'
        print 'Usage:'  # TODO
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        settings.OUTPUT_PATH = output_path

        parser = ParseXML(input_path, output_path)
        course = parser.retrieve_course()

        course_name = CourseUtils.get_course_name(course.title_full)
        settings.COURSE_DIR = os.path.join(output_path, 'temp', course_name)

        exporter = CourseExporter(course)
        exporter.generate_backup()

        backup_name = CourseUtils.compress_course(settings.COURSE_DIR)
        copy_file(os.path.join(settings.COURSE_DIR, backup_name), output_path)
        remove_tree(os.path.join(output_path, 'temp'))
        print ('\nCourse created successfully at path: ' + output_path)


if __name__ == "__main__":
    main(sys.argv)

