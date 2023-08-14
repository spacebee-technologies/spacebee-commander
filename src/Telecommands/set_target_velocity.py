from telecommand_interface import TelecommandInterface

class set_target_velocity(TelecommandInterface):
    def __init__(self):
        self.name="Set target velocity"
        self.help=""
        self.interaction_stage=1
        self.service=1
        self.operation=4
        self.area_version=0