import os
from os import listdir
from os import walk
import re
import pystache
import settings
import hashlib
from shutil import move

class CourseExporter:

    section_values = []
    session_values = []
    files_values = []
    images = {} # Key:filename, value:contextid

    def __init__(self, course, images):
        print('\nExporting course to Oppia format...')
        self.images = images
        print images
        self.generate_base_course(course)
        self.generate_files_folder()
        self.generate_files_file()
        self.generate_sections(course.sections)
        self.generate_sessions(course.sections)
        self.generate_moodle_backup_info()

    def generate_base_course(self, course):
        """ Create all the base files needed to restore the course. """
        print('\nGenerating course base files...')

        if not os.path.exists('Course/course'):
            os.makedirs('Course/course')

        self.generate_roles_files()
        self.generate_groups_file()
        self.generate_outcomes_file()
        self.generate_questions_file()
        self.generate_scales_file()


    def generate_roles_files(self):
        f = open("Course/course/roles.xml", "wb+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<roles><role_overrides>'
                '</role_overrides><role_assignments></role_assignments></roles>')
        f.close()
        print('Course/course/roles.xml created.')

        f = open("Course/roles.xml", "wb+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<roles_definition></roles_definition>')
        f.close()
        print('Course/roles.xml created. ')

    def generate_groups_file(self):
        f = open("Course/groups.xml", "wb+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<groups></groups>')
        f.close()
        print('goups.xml created.')

    def generate_outcomes_file(self):
        f = open("Course/outcomes.xml", "wb+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<outcomes_definition></outcomes_definition>')
        f.close()
        print('outcomes.xml created.')

    def generate_questions_file(self):
        f = open("Course/questions.xml", "wb+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<question_categories></question_categories>')
        f.close()
        print('questions.xml created.')

    def generate_scales_file(self):
        f = open("Course/scales.xml", "wb+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<scales_definition></scales_definition>')
        f.close()
        print('scales.xml created.')

    def generate_sections(self, sections):
        """ Generate all the files that include information about the sections"""
        print('\nGenerating sections...')

        renderer = pystache.Renderer()

        # Create section.xml files within the "sections" directory
        i = 1
        for section in sections:
            #Information of sections for "moodle_backup.xml" file
            self.section_values.append({'sectionid': str(i), 'section_directory': 'sections/section_' + str(i)})

            if not os.path.exists('Course/sections/section_' + str(i)):
                os.makedirs("Course/sections/section_" + str(i))

            section_file = open("Course/sections/section_" + str(i) + "/section.xml", "wb+")
            section_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'section.mustache'),
                                                    {'id': str(i), 'number': str(i), 'name': section.title}))
            section_file.close()
            print('File section.xml for section ' + str(i) + ' created successfully!')
            i += 1

        # Add sections count to file course.xml within "course" directory
        course_info_file = open("Course/course/course.xml", "wb+")
        course_info_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'course_info.mustache'),
                                                    {'sections_count': len(sections)}))

    def generate_sessions(self, sections):
        print('\nGenerating sessions...')
        renderer = pystache.Renderer()
        i = 1
        j = 1
        for section in sections:
            for session in section.sessions:

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
                print('File module.xml for session ' + str(j) + ' created successfully!')

                # Create "inforef.xml" file
                files = []
                for file in self.files_values:
                    if file['contextid'] == j:
                        files.append(file)

                inforef_file = open('Course/activities/page_' + str(j) + '/inforef.xml', "wb+")
                inforef_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'inforef.mustache'),
                                                        {'files': files, 'fileid': str(j)}))
                inforef_file.close()

                # Create "page.xml" file
                if files:
                    print files
                    print files[0]
                    session.content = session.content.replace("<img src=\"\"", "<img src=\"@@PLUGINFILE@@/" + files[0]['filename'] + "\"")
                page_file = open("Course/activities/page_" + str(j) + "/page.xml", "wb+")
                page_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'activity_page.mustache'),
                                                     {'id': str(j), 'title': session.title, 'content': session.content}))
                page_file.close()
                print('File page.xml for session ' + str(j) + ' created successfully!\n')

                j += 1
            i += 1

    def generate_moodle_backup_info(self):
        """ Generate the file moodle_backup.xml"""
        renderer = pystache.Renderer()

        moodle_backup_file = open("Course/moodle_backup.xml", "wb+")
        moodle_backup_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'moodle_backup.mustache'),
                                                      {'sessions': self.session_values, 'sections': self.section_values}))
        print('moodle_backup.xml created.')

    def generate_session_base_files(self, sessionid):
        print('Generating session ' + str(sessionid) + ' base files... ')

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

    def generate_files_folder(self):
        if os.path.exists('Course/files'):
            try:
                os.remove(os.path('Course/files'))
            except Exception as e:
                print e
        else:
            os.makedirs('Course/files')

        images_folder = os.path.join(settings.PROJECT_ROOT, 'images')
        i = 1
        for image_file in listdir(images_folder):
            new_filename = hashlib.sha1(image_file).hexdigest()
            contextid = self.images[image_file]
            self.files_values.append({'fileid': str(i), 'file_hash': new_filename, 'contextid': contextid,
                                        'filename': image_file})

            os.rename(os.path.join(images_folder, image_file), os.path.join(images_folder, new_filename))
            filepath = os.path.join('Course/files', new_filename[:2])
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            move(os.path.join(images_folder, new_filename), os.path.join(settings.PROJECT_ROOT, filepath, new_filename))
            i += 1

    def generate_files_file(self):
        """ Generate the file files.xml"""
        renderer = pystache.Renderer()

        files_file = open("Course/files.xml", "wb+")
        files_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'files.mustache'),
                                              {'files': self.files_values}))
