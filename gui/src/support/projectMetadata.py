import pickle
import os


class ProjectMetadata:
    def __init__(self):
        self.file = None

    def get_projects_dict(self):
        if os.path.isfile('./.metadata'):
            self.file = open(".metadata", 'rb')
            projects = pickle.load(self.file)
            self.file.close()
            return projects
        else:
            return None

    def add_project_to_dict(self, name, date, loc):
        if os.path.isfile('./.metadata'):
            projects = pickle.load(open('./.metadata', 'rb'))
            projects[name] = (date, loc)
            self.file = open('./.metadata', 'wb+')
            pickle.dump(projects, self.file)
            self.file.close()
        else:
            projects = {name: (date, loc)}
            print(projects)
            self.file = open('./.metadata', 'wb+')
            pickle.dump(projects, self.file)
            self.file.close()
