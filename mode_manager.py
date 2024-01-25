import data.creator as db

db_creator = db.dbCreator()

modes = ['gpt-3.5-turbo', 'gpt-4', 'MIDJOURNEY-5.2', 'MIDJOURNEY-6']
mode_names = ['GPT-3.5', 'GPT-4', 'MIDJOURNEY-5.2', 'MIDJOURNEY-6']
mode_indx = [0, 1, 2, 3]


class ModeManager:
    def __init__(self, user_id, mode_index=0):
        self.modes = modes
        self.mode_names = mode_names
        self.mode_indx = mode_indx
        self.user_id = user_id
        self.mode_index = mode_index
        self.mode_name = mode_names[self.mode_index]
        self.mode = modes[mode_index]

    def get_modenames(self):
        return self.mode_names

    def get_modetypes(self):
        return self.modes

    def get_modeindexes(self):
        return self.mode_indx

    def get_index(self):
        return self.mode_index

    def get_name(self):
        return mode_names[self.mode_index]

    def get_mode(self):
        return modes[self.mode_index]

    def set_mode(self):
        db_creator.set_user_mode(self.user_id, self.mode)
        return self.mode
