import hashlib
import sys
import time
from distutils.dir_util import copy_tree
from distutils.dir_util import remove_tree
from distutils.file_util import copy_file

import os
import pystache
import re

import settings

renderer = pystache.Renderer()

class CourseExporter:

    def __init__(self, course):
        self.course = course
        self.section_values = []
        self.session_values = []
        self.files_values = []

    def generate_backup(self):
        print '\n========== COURSE EXPORT =================\n'
        print 'Creating moodle backup:'
        self.copy_base_course()
        self.generate_files_folder()
        self.generate_sessions()
        self.generate_sections()
        self.generate_files_file()
        self.generate_moodle_backup_info(self.course)

    def copy_base_course(self):
        """ Create all the base files needed to restore the course. """
        print '  > Creating course base files... ',
        if not os.path.exists(settings.COURSE_DIR):
            os.makedirs(settings.COURSE_DIR)
        copy_tree(settings.BASE_COURSE, settings.COURSE_DIR)
        print 'Done.'

    def generate_files_folder(self):
        """ Create 'files' directory where the course images are located"""
        print '  > Creating files directory...',
        files_dir = os.path.join(settings.COURSE_DIR, 'files')
        if os.path.exists(files_dir):
            try:
                os.remove(os.path.abspath(files_dir))
            except Exception as e:
                print e

        os.makedirs(files_dir)

        images_dir = os.path.join(settings.OUTPUT_PATH, 'temp', 'images')
        image_files = os.listdir(images_dir)

        for i, image_file in enumerate(image_files, start=1):
            progress = str(i * 100 / len(image_files)) + '%'
            print '\r  > Creating files directory... (' + progress + ')',

            file_sha1 = hashlib.sha1(image_file).hexdigest()
            self.files_values.append({
                'fileid': str(i),
                'filename': image_file,
                'file_hash': file_sha1,
                'timecreated': int(time.time())})

            source_path = os.path.join(images_dir, image_file)
            image_rename = os.path.join(images_dir, file_sha1)
            file_dirpath = os.path.join(files_dir, file_sha1[:2])

            os.rename(source_path, image_rename)

            if not os.path.exists(file_dirpath):
                os.makedirs(file_dirpath)

            copy_file(image_rename, file_dirpath)

        print '\r  > Creating files directory. (100%) Done.'
        remove_tree(images_dir)

    @staticmethod
    def get_template(template_name):
        return os.path.join(settings.TEMPLATES_ROOT, template_name + '.mustache')

    def generate_sections(self):
        """ Generate all the files that include information about the sections"""

        sections_dir = os.path.join(settings.COURSE_DIR, "sections")
        num_sections = len(self.course.sections)

        # Create section.xml files within the "sections" directory

        for sectionid, section in enumerate(self.course.sections, start=1):
            progress = str(sectionid * 100 / num_sections) + '%'
            print '\r  > Generating sections (' + progress + ')',
            sys.stdout.flush()
            # Information of sections for "moodle_backup.xml" file
            self.section_values.append({
                'sectionid': sectionid,
                'section_directory': 'sections/section_' + str(sectionid)})

            section_dir = os.path.join(sections_dir, 'section_' + str(sectionid))
            if not os.path.exists(section_dir):
                os.makedirs(section_dir)

            section_file = open(section_dir + "/section.xml", "wb+")
            section_file.write(renderer.render_path(self.get_template('section'),
                                                {'id': sectionid, 'number': sectionid, 'name': section.title}))
            section_file.close()

        print '\r  > Generating sections (100%). Done.'

        # Add sections count to file course.xml within "course" directory
        course_info_file = open(os.path.join(settings.COURSE_DIR, "course", "course.xml"), "wb+")
        course_info_file.write(renderer.render_path(self.get_template('course_info'), {
                                    'sections_count': num_sections,
                                    'course_title_full': self.course.title_full,
                                    'course_title_short': self.course.title_short}))

    def generate_sessions(self):
        """ Generate all the files that include information about the sessions"""

        activities_dir = os.path.join(settings.COURSE_DIR, "activities")
        if not os.path.exists(activities_dir):
            os.makedirs(activities_dir)
        num_sections = len(self.course.sections)

        for sectionid, section in enumerate(self.course.sections, start=1):
            progress = str(sectionid * 100 / num_sections) + '%'
            print '\r  > Generating sessions (' + progress + ')',
            sys.stdout.flush()

            for sessionid, session in enumerate(section.sessions, start=1):
                self.session_values.append({'sessionid': sessionid, 'sectionid': sectionid, 'title': session.title.rstrip(),
                                            'session_directory': 'activities/page_' + str(sessionid)})
                page_dir = os.path.join(activities_dir, 'page_' + str(sessionid))
                if not os.path.exists(page_dir):
                    os.makedirs(page_dir)

                self.generate_session_base_files(sessionid)

                # Create "module.xml" file
                module_file = open(page_dir + "/module.xml", "wb+")
                module_file.write(renderer.render_path(self.get_template('activity_module'),
                                       {'id': sessionid, 'sectionid': sectionid }))
                module_file.close()

                # Create "page.xml" file
                regex = re.compile(r'(?:<img src=\")(?:\\[^"]+)\\([^"]+)\"')
                new_content = regex.sub(r'<img src="@@PLUGINFILE@@/\g<1>"', session.content)
                for image in regex.finditer(session.content):
                    filename = image.group(1)
                    item = (item for item in self.files_values if item['filename'] == filename).next()
                    item['contextid'] = sessionid
                    # self.files_values.append({'filename': filename, 'contextid':contextid})

                page_file = open(page_dir + "/page.xml", "wb+")
                page_file.write(renderer.render_path(self.get_template('activity_page'),
                                     {'id': sessionid, 'title': session.title, 'content': new_content}))
                page_file.close()

                # Create "inforef.xml" file
                files = []
                for f in self.files_values:
                    if f.get('contextid', -1) == sessionid:
                        files.append(f)

                inforef_file = open(page_dir + '/inforef.xml', "wb+")
                inforef_file.write(renderer.render_path(self.get_template('inforef'),
                                        { 'files': files, 'fileid': sessionid }))
                inforef_file.close()

        print '\r  > Generating sessions (100%). Done.'

    def generate_moodle_backup_info(self, course):
        """ Generate the file 'moodle_backup.xml'"""
        print('  > Creating moodle_backup.xml... '),
        sys.stdout.flush()

        moodle_backup_file = open(os.path.join(settings.COURSE_DIR, "moodle_backup.xml"), "wb+")
        moodle_backup_file.write(renderer.render_path(self.get_template('moodle_backup'), {
                                            'sessions': self.session_values,
                                            'sections': self.section_values,
                                            'course_title_full': course.title_full,
                                            'course_title_short':course.title_short
                                          }))
        print 'Done.'

    def generate_session_base_files(self, sessionid):
        page_dir = os.path.join(settings.COURSE_DIR, "activities", "page_" + str(sessionid))
        copy_tree(settings.BASE_SESSION, page_dir)

    def generate_files_file(self):
        """ Generate the file files.xml"""
        print '  > Creating files.xml... ',

        files_file = open(os.path.join(settings.COURSE_DIR, "files.xml"), "wb+")
        files_file.write(renderer.render_path(self.get_template('files'),
                                              {'files': self.files_values}))
        print 'Done.'
