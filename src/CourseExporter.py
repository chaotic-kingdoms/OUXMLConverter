import os
import pystache
import settings

class CourseExporter:

    section_values = []
    session_values = []

    def __init__(self, course):
        print('\nExporting course to Oppia format...')
        self.generate_base_course(course)

    def generate_base_course(self, course):
        """ Create all the base files needed to restore the course. """
        print('\nGenerating course base files...')

        if not os.path.exists('Course'):
            os.makedirs('Course')

        self.generate_roles_files()
        self.generate_groups_file()
        self.generate_outcomes_file()
        self.generate_questions_file()
        self.generate_scales_file()

        self.generate_sections(course.sections)
        self.generate_sessions(course.sections)
        self.generate_moodle_backup_info()

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
        if not os.path.exists('Course/course'):
            os.makedirs("Course/course")

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

                self.generate_session_base_files(j)

                self.session_values.append({'sessionid': str(j), 'sectionid': str(i), 'title': session.title.rstrip(),
                                            'session_directory': 'activities/page_' + str(j)})
                if not os.path.exists('Course/activities/page_' + str(j)):
                    os.makedirs("Course/activities/page_" + str(j))

                # Create "module.xml" file
                module_file = open("Course/activities/page_" + str(j) + "/module.xml", "wb+")
                module_file.write(renderer.render_path(os.path.join(settings.TEMPLATES_ROOT, 'activity_module.mustache'),
                                                       {'id': str(j), 'sectionid': str(i)}))
                module_file.close()
                print('File module.xml for session ' + str(j) + ' created successfully!')

                # Create "page.xml" file
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

        # Create inforef.xml file
        inforef_file = open('Course/activities/page_' + str(sessionid) + '/inforef.xml', "wb+")
        inforef_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<inforef></inforef>')
        inforef_file.close()

        # Create roles.xml file
        roles_file = open('Course/activities/page_' + str(sessionid) + '/roles.xml', "wb+")
        roles_file.write('<?xml version="1.0" encoding="UTF-8"?>\n<roles>\n<role_overrides></role_overrides>\n<role_assignments></role_assignments>\n</roles>')
        roles_file.close()
