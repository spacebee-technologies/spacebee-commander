from telecommand_interface import TelecommandInterface

class set_profile_mode(TelecommandInterface):
    def __init__(self):
        self.name="Set profile mode"
        self.help=""
        self.interaction_stage=1
        self.service=1
        self.operation=3
        self.area_version=0