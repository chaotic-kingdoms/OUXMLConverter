import sys
from CourseParser import ParseXML
import CourseExporter


def main(argv):
    if len(argv) != 3:
        print 'Wrong number of arguments.'
        print 'Usage: TO-DO'
    else:
        parser = ParseXML(str(sys.argv[1]), str(sys.argv[2]))
        course = parser.retrieve_course()
        export_course(course, str(sys.argv[2]))


def export_course(course, output_path):
    """ Export all the course contents to an output path"""
    CourseExporter.CourseExporter(course, output_path)
    print ('\nCourse created successfully at path: ' + output_path)

if __name__ == "__main__":
    main(sys.argv)

