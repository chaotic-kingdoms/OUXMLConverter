import os
from os import listdir
import tarfile
import zipfile
import shutil
import stat


class CourseUtils(object):

    @staticmethod
    def compress_course(src, type='mbz'):
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

        return backup_name

def readonly_handler(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)
