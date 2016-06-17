import tarfile
import zipfile
from datetime import datetime as DT

import os
from os import listdir


class CourseUtils(object):

    course_name = ""

    @staticmethod
    def compress_course(src, type='mbz'):
        print '\n> Compressing course...',
        backup_name = src.split('/')[-1]
        backup_path = os.path.join(src, backup_name)

        if type == 'mbz':
            backup_path += '.mbz'
            with tarfile.open(backup_path, "w:gz") as tar:
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
        return backup_path

    @staticmethod
    def get_course_name(course_title):
        if CourseUtils.course_name:
            return CourseUtils.course_name
        else:
            return course_title + '-' + str(DT.today().strftime('%Y%m%d%H%M'))


