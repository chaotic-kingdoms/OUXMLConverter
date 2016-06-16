import os
from os import listdir
import re
import pystache
import settings
import hashlib
import time
import sys
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from distutils.dir_util import remove_tree


class CourseExporter:

    def __init__(self, course):
        self.course = course
        self.section_values = []
        self.session_values = []
        self.files_values = []

    def generate_backup(self):
        print('\nCreating moodle backup...')
        self.copy_base_course()
        self.generate_files_folder()
        self.generate_sessions(self.course.sections)
        self.generate_sections(self.course)
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
                os.remove(os.path(files_dir))
            except Exception as e:
                print e

        os.makedirs(files_dir)

        images_dir = os.path.join(settings.OUTPUT_PATH, 'temp', 'images')
        i = 1
        progress = 0
        for image_file in listdir(images_dir):
            progress = str(i * 100 / len(listdir(images_dir))) + '%'
            print '\r  > Creating files directory... (' + progress + ')',
            file_sha1 = hashlib.sha1(image_file).hexdigest()
            self.files_values.append({'fileid': str(i), 'filename': image_file, 'file_hash': file_sha1, 'timecreated': int(time.time())})

            source_path = os.path.join(images_dir, image_file)
            image_rename = os.path.join(images_dir, file_sha1)
            file_dirpath = os.path.join(files_dir, file_sha1[:2])

            os.rename(source_path, image_rename)

            if not os.path.exists(file_dirpath):
                os.makedirs(file_dirpath)

            copy_file(image_rename, file_dirpath)
            i += 1

        print '\r  > Creating files directory. (' + progress + ') Done.'
        remove_tree(images_dir)

    def generate_sections(self, course):
        """ Generate all the files that include information about the sections"""

        sections_dir = os.path.join(settings.COURSE_DIR, "sections")

        renderer = pystache.Renderer()

        # Create section.xml files within the "sections" directory
        i = 1
        for section in course.sections:
            progress = str(i * 100 / len(course.sections)) + '%'
            print '\r  > Generating sections (' + progress + ')',
            sys.stdout.flush()
            #Information of sections for "moodle_backup.xml" file
            self.section_values.append({'sectionid': str(i), 'section_directory': 'sections/section_' + str(i)})

            section_dir = os.path.join(sections_dir, 'section_' + str(i))
            if not os.path.exists(section_dir):
                os.makedirs(section_dir)

            section_file = open(section_dir + "/section.xml", "wb+")
            section_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'section.mustache'),
                                                    {'id': str(i), 'number': str(i), 'name': section.title}))
            section_file.close()
            i += 1
        print '\r  > Generating sections (100%). Done.'

        # Add sections count to file course.xml within "course" directory
        course_info_file = open(os.path.join(settings.COURSE_DIR, "course", "course.xml"), "wb+")
        course_info_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'course_info.mustache'),
                                                    {'sections_count': len(course.sections),
                                                     'course_title_full': course.title_full,
                                                     'course_title_short': course.title_short}))

    def generate_sessions(self, sections):
        """ Generate all the files that include information about the sessions"""

        activities_dir = os.path.join(settings.COURSE_DIR, "activities")
        if not os.path.exists(activities_dir):
            os.makedirs(activities_dir)

        renderer = pystache.Renderer()
        i = 1
        j = 1
        for section in sections:
            progress = str(i * 100 / len(sections)) + '%'
            print '\r  > Generating sessions (' + progress + ')',
            sys.stdout.flush()
            for session in section.sessions:
                self.session_values.append({'sessionid': str(j), 'sectionid': str(i), 'title': session.title.rstrip(),
                                            'session_directory': 'activities/page_' + str(j)})
                page_dir = os.path.join(activities_dir, 'page_' + str(j))
                if not os.path.exists(page_dir):
                    os.makedirs(page_dir)

                self.generate_session_base_files(j)

                # Create "module.xml" file
                module_file = open(page_dir + "/module.xml", "wb+")
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

                page_file = open(page_dir + "/page.xml", "wb+")
                page_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'activity_page.mustache'),
                                                     {'id': str(j), 'title': session.title, 'content': new_content}))
                page_file.close()

                # Create "inforef.xml" file
                files = []
                for file in self.files_values:
                    if file.get('contextid', -1) == j:
                        files.append(file)

                inforef_file = open(page_dir + '/inforef.xml', "wb+")
                inforef_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'inforef.mustache'),
                                                        {'files': files, 'fileid': str(j)}))
                inforef_file.close()
                j += 1
            i += 1
        print '\r  > Generating sessions (100%). Done.'

    def generate_moodle_backup_info(self, course):
        """ Generate the file 'moodle_backup.xml'"""
        print('  > Creating moodle_backup.xml... '),
        sys.stdout.flush()
        renderer = pystache.Renderer()

        moodle_backup_file = open(os.path.join(settings.COURSE_DIR, "moodle_backup.xml"), "wb+")
        moodle_backup_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'moodle_backup.mustache'),
                                                      {'sessions': self.session_values, 'sections': self.section_values,
                                                       'course_title_full': course.title_full, 'course_title_short':course.title_short}))
        print 'Done.'

    def generate_session_base_files(self, sessionid):
        page_dir = os.path.join(settings.COURSE_DIR, "activities", "page_" + str(sessionid))
        copy_tree(settings.BASE_SESSION, page_dir)

    def generate_files_file(self):
        """ Generate the file files.xml"""
        print '  > Creating files.xml... ',
        renderer = pystache.Renderer()

        files_file = open(os.path.join(settings.COURSE_DIR, "files.xml"), "wb+")
        files_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'files.mustache'),
                                              {'files': self.files_values}))
        print 'Done.'
