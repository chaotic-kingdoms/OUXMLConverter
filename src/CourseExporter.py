import os
import pystache

class CourseExporter:

    def __init__(self, course):
        self.generate_base_course(course)

    def generate_base_course(self, course):
        if not os.path.exists('Course'):
            os.makedirs('Course')

        self.generate_roles_files()
        self.generate_groups_file()
        self.generate_outcomes_file()
        self.generate_questions_file()
        self.generate_scales_file()

        self.generate_sections(course.sections)

    def generate_roles_files(self):
        print('Generating Course/course/roles.xml... ')
        f = open("Course/course/roles.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<roles><role_overrides>'
                '</role_overrides><role_assignments></role_assignments></roles>')
        f.close()

        print('Generating Course/roles.xml... ')
        f = open("Course/roles.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<roles_definition></roles_definition>')
        f.close()

    def generate_groups_file(self):
        print('Generating goups.xml... ')
        f = open("Course/groups.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<groups></groups>')
        f.close()

    def generate_outcomes_file(self):
        print('Generating outcomes.xml... ')
        f = open("Course/outcomes.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<outcomes_definition></outcomes_definition>')
        f.close()

    def generate_questions_file(self):
        print('Generating questions.xml... ')
        f = open("Course/questions.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<question_categories></question_categories>')
        f.close()

    def generate_scales_file(self):
        print('Generating scales.xml... ')
        f = open("Course/scales.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<scales_definition></scales_definition>')
        f.close()

    def generate_sections(self, sections):
        """ Generate all the files that include information about the sections"""
        print('Generating sections... ')
        section_values = []

        renderer = pystache.Renderer()
        i = 1

        # Create section.xml files within the "sections" directory
        for section in sections:
            section_values.append({'id': str(i), 'directory': 'sections/section_' + str(i)})
            if not os.path.exists('Course/sections/section_' + str(i)):
                os.makedirs("Course/sections/section_" + str(i))

            section_file = open("Course/sections/section_" + str(i) + "/section.xml", "wb+")
            section_file.write(renderer.render_path('section.mustache', {'id': str(i), 'number': str(i), 'name': section.title}))
            section_file.close()
            i += 1
            print('File section.xml for section ' + str(i) + ' created successfully!')

        # Add sections references to moodle_backup.xml file
        moodle_backup_file = open("Course/moodle_backup.xml", "wb+")
        moodle_backup_file.write(renderer.render_path('moodle_backup.mustache', {'sections': section_values}))

        # Add sections count to file course.xml within "course" directory
        if not os.path.exists('Course/course'):
            os.makedirs("Course/course")

        course_info_file = open("Course/course/course.xml", "wb+")
        course_info_file.write(renderer.render_path('course_info.mustache', {'sections_count': len(sections)}))

