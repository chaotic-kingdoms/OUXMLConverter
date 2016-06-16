import os
from os import listdir
import tarfile
import zipfile
import shutil
import stat
from datetime import datetime as DT
import settings


class CourseUtils(object):

    course_name = ""

    @staticmethod
    def compress_course(src, type='mbz'):
        print src
        backup_name = src.split('/')[-1]

        if type == 'mbz':
            backup_name += '.mbz'
            with tarfile.open(backup_name, "w:gz") as tar:
                print src
                print backup_name
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

        return backup_name

    @staticmethod
    def get_course_name():
        if CourseUtils.course_name:
            return CourseUtils.course_name
        else:
            return 'backup-moodle2-course-2-Course-' + str(DT.today().year) \
                           + str(DT.today().month) + str(DT.today().day) + '-' + str(DT.today().hour) \
                           + str(DT.today().minute) + '-nu'


def readonly_handler(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)
