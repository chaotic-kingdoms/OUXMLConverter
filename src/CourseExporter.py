import os
from os import listdir
from os import walk
import re
import pystache
import settings
import hashlib
import shutil
import time
from datetime import datetime as DT
import sys
import tarfile
import zipfile
import stat
from distutils.dir_util import copy_tree

class CourseExporter:

    section_values = []
    session_values = []
    files_values = []

    def __init__(self, course, output_path):
        self.export_course(course, output_path)
        self.coursename = ""

    def export_course(self, course, output_path):
        print('\nExporting course to Oppia format...')

        self.coursename = 'backup-moodle2-course-2-Course-' + str(DT.today().year) \
                          + str(DT.today().month) + str(DT.today().day) + '-' + str(DT.today().hour) + str(
            DT.today().minute) + '-nu'

        self.course_dir = os.path.join(os.path.join(output_path, 'temp'), self.coursename)

        self.copy_base_course(output_path)

        self.generate_files_dir(output_path)
        self.generate_sessions(course.sections)
        self.generate_sections(course)
        self.generate_files_file()
        self.generate_moodle_backup_info(course)

        filename = self.compress_course(course.title)
        shutil.move(os.path.join(settings.PROJECT_ROOT, filename), os.path.join(output_path, filename))

    def copy_base_course(self, output_path):
        """ Create all the base files needed to restore the course. """
        print('\nCopying course base files...')

        if not os.path.exists(self.course_dir):
            os.makedirs(self.course_dir)
        copy_tree(settings.TEMP_COURSE, self.course_dir)

    def generate_files_dir(self, output_path):
        files_dir = os.path.join(self.course_dir, 'files')
        if os.path.exists(files_dir):
            try:
                os.remove(os.path(files_dir))
            except Exception as e:
                print e

        os.makedirs('Course/files')

        images_dir = os.path.join(os.path.join(output_path, 'temp'), 'images')
        i = 1
        for image_file in listdir(images_dir):
            new_filename = hashlib.sha1(image_file).hexdigest()
            self.files_values.append({'fileid': str(i), 'filename': image_file, 'file_hash': new_filename, 'timecreated': int(time.time())})

            os.rename(os.path.join(images_dir, image_file), os.path.join(images_dir, new_filename))
            filepath = os.path.join('Course/files', new_filename[:2])
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            shutil.move(os.path.join(images_dir, new_filename), os.path.join(settings.PROJECT_ROOT, filepath, new_filename))
            i += 1

        shutil.rmtree("images", onerror=self.readonly_handler)

    def generate_sections(self, course):
        """ Generate all the files that include information about the sections"""
        print('\nGenerating sections...')

        renderer = pystache.Renderer()

        # Create section.xml files within the "sections" directory
        i = 1
        for section in course.sections:
            progress = str(i * 100 / len(course.sections)) + '%'
            print '\r  > Generating sections (' + progress + ')',
            sys.stdout.flush()
            #Information of sections for "moodle_backup.xml" file
            self.section_values.append({'sectionid': str(i), 'section_directory': 'sections/section_' + str(i)})

            if not os.path.exists('Course/sections/section_' + str(i)):
                os.makedirs("Course/sections/section_" + str(i))

            section_file = open("Course/sections/section_" + str(i) + "/section.xml", "wb+")
            section_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'section.mustache'),
                                                    {'id': str(i), 'number': str(i), 'name': section.title}))
            section_file.close()
            i += 1
        print '\r  > Generating sections (100%). Done.'

        # Add sections count to file course.xml within "course" directory
        course_info_file = open("Course/course/course.xml", "wb+")
        course_info_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'course_info.mustache'),
                                                    {'sections_count': len(course.sections), 'course_title': course.title}))

    def generate_sessions(self, sections):
        print('\nGenerating sessions...')
        renderer = pystache.Renderer()
        i = 1
        j = 1
        for section in sections:
            print("Section " + str(i) + ":")
            for session in section.sessions:
                progress = str(j * 100 / len(section.sessions)) + '%'
                print '\r  > Generating sessions (' + progress + ')',
                sys.stdout.flush()
                self.session_values.append({'sessionid': str(j), 'sectionid': str(i), 'title': session.title.rstrip(),
                                            'session_directory': 'activities/page_' + str(j)})
                if not os.path.exists('Course/activities/page_' + str(j)):
                    os.makedirs("Course/activities/page_" + str(j))

                self.generate_session_base_files(j)

                # Create "module.xml" file
                module_file = open("Course/activities/page_" + str(j) + "/module.xml", "wb+")
                module_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'activity_module.mustache'),
                                                       {'id': str(j), 'sectionid': str(i)}))
                module_file.close()


                # Create "page.xml" file
                regex = re.compile(r'(?:<img src=\")(?:\\[^"]+)\\([^"]+)\"')
                new_content = regex.sub(r'<img src="@@PLUGINFILE@@/\g<1>"', session.content)
                for image in regex.finditer(session.content):
                    filename = image.group(1)
                    item = (item for item in self.files_values if item['filename'] == filename).next()
                    item['contextid'] = j
                    #self.files_values.append({'filename': filename, 'contextid':contextid})

                page_file = open("Course/activities/page_" + str(j) + "/page.xml", "wb+")
                page_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'activity_page.mustache'),
                                                     {'id': str(j), 'title': session.title, 'content': new_content}))
                page_file.close()

                # Create "inforef.xml" file
                files = []
                for file in self.files_values:
                    if file.get('contextid', -1) == j:
                        files.append(file)

                inforef_file = open('Course/activities/page_' + str(j) + '/inforef.xml', "wb+")
                inforef_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'inforef.mustache'),
                                                        {'files': files, 'fileid': str(j)}))
                inforef_file.close()
                j += 1
            print '\r  > Generating sessions (100%). Done.'
            i += 1

    def generate_moodle_backup_info(self, course):
        """ Generate the file moodle_backup.xml"""
        print('\nCreating moodle_backup.xml... '),
        sys.stdout.flush()
        renderer = pystache.Renderer()

        moodle_backup_file = open("Course/moodle_backup.xml", "wb+")
        moodle_backup_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'moodle_backup.mustache'),
                                                      {'sessions': self.session_values, 'sections': self.section_values, 'course_title': course.title}))
        print 'Done.'

    def generate_session_base_files(self, sessionid):

        # Create grade_history.xml file
        grade_history_file = open('Course/activities/page_' + str(sessionid) + '/grade_history.xml', "wb+")
        grade_history_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<grade_history>\n<grade_grades></grade_grades>\n</grade_history>')
        grade_history_file.close()

        # Create grades.xml file
        grades_file = open('Course/activities/page_' + str(sessionid) + '/grades.xml', "wb+")
        grades_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<activity_gradebook>\n<grade_items></grade_items>\n<grade_letters></grade_letters>\n</activity_gradebook>')
        grade_history_file.close()

        # Create roles.xml file
        roles_file = open('Course/activities/page_' + str(sessionid) + '/roles.xml', "wb+")
        roles_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<roles>\n<role_overrides></role_overrides>\n<role_assignments></role_assignments>\n</roles>')
        roles_file.close()


    def generate_files_file(self):
        """ Generate the file files.xml"""
        renderer = pystache.Renderer()

        files_file = open("Course/files.xml", "wb+")
        files_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'files.mustache'),
                                              {'files': self.files_values}))

    def compress_course(self, course_title, type='mbz'):
        source_path = os.path.join(settings.PROJECT_ROOT, "Course")

        if type == 'mbz':
            with tarfile.open(self.coursename + '.mbz', "w:gz") as tar:
                for file in listdir(source_path):
                    tar.add(os.path.join("Course", file), arcname=file)
                tar.close()
        elif type == 'zip':
            with zipfile(self.coursename + '.zip', 'w') as zip:
                for file in listdir(source_path):
                    zip.write(os.path.join("Course", file))
                zip.close()
        else:
            print 'Error: Wrong backup extension.'

        shutil.rmtree("Course", onerror=self.readonly_handler)

    def readonly_handler(func, path, execinfo, extra):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    #def export_course(self, filename, output_path):
    #    if not os.path.exists(output_path):
    #        os.makedirs(output_path)
    #    shutil.move(os.path.join(settings.PROJECT_ROOT, filename), os.path.join(output_path, filename))
