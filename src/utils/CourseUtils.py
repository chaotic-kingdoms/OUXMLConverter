import os
from os import listdir
import tarfile
import zipfile
import shutil
import stat


class CourseUtils(object):

    @staticmethod
    def compress_course(src, type='mbz'):
        filename = src.split('/')[-1]
        print src

        if type == 'mbz':
            with tarfile.open(filename + '.mbz', "w:gz") as tar:
                for file in listdir(src):
                    tar.add(os.path.join(src, file), arcname=file)
                tar.close()
        elif type == 'zip':
            with zipfile(filename + '.zip', 'w') as zip:
                for file in listdir(src):
                    zip.write(os.path.join(src, file))
                zip.close()
        else:
            print 'Error: Wrong backup extension.'
