import os
from os import listdir
import tarfile
import zipfile
import stat
from datetime import datetime as DT


class CourseUtils(object):

    course_name = ""

    @staticmethod
    def compress_course(src, type='mbz'):
        print '\n > Compressing course...',
        backup_name = src.split('/')[-1]

        if type == 'mbz':
            backup_name += '.mbz'
            with tarfile.open(backup_name, "w:gz") as tar:
                for file in listdir(src):
                    tar.add(os.path.join(src, file), arcname=file)
                tar.close()
        elif type == 'zip':
            backup_name += '.zip'
            with zipfile(backup_name, 'w') as zip:
                for file in listdir(src):
                    zip.write(os.path.join(src, file))
                zip.close()
        else:
            print 'Error: Wrong backup extension.'

        print 'Done.'
        return backup_name

    @staticmethod
    def get_course_name(course_title):
        if CourseUtils.course_name:
            return CourseUtils.course_name
        else:
            return 'backup-moodle2-course-2-' + course_title +'-' + str(DT.today().strftime('%Y%m%d-%H%M')) + '-nu'


def readonly_handler(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)
