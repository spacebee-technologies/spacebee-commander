from telecommand_interface import TelecommandInterface

class set_mode(TelecommandInterface):
    def __init__(self):
        self.name="Set mode"
        self.help=""
        self.interaction_stage=1
        self.service=1
        self.operation=2
        self.area_version=0