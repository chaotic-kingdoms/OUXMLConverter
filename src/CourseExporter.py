import os

class CourseExporter:

    def __init__(self, course):
        self.generate_base_course()

    def generate_base_course(self):
        if not os.path.exists('Course'):
            os.makedirs('Course')

        self.generate_groups_file()
        self.generate_outcomes_file()
        self.generate_questions_file()
        self.generate_roles_file()

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

    def generate_roles_file(self):
        print('Generating roles.xml... ')
        f = open("Course/roles.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<roles_definition></roles_definition>')
        f.close()

    def generate_scales_file(self):
        print('Generating scales.xml... ')
        f = open("Course/scales.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<scales_definition></scales_definition>')
        f.close()