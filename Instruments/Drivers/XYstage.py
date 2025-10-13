from pylablib.devices import Thorlabs



class XYstage:
    

    def __init__(self):

        try:
            self.stage = Thorlabs.KinesisMotor("103514374", scale="20", is_rack_system=True)   # MLS203 X
        except:
            self.stage = None
            print("Failed to connect to XY stage")

        self.steps_per_micron = 20
        self.step_multiplier = 10
        self.piezo_step = 10.0

    def get_xy_stage_position(self, channel=None):
        """Get stage position for specified channel or both channels"""
        if channel:
            return self.stage.get_position(channel=channel)/self.steps_per_micron
        else:
            # Return both X and Y positions
            x_pos = self.stage.get_position(channel=1)
            y_pos = self.stage.get_position(channel=2)
            return {"x": x_pos/self.steps_per_micron, "y": y_pos/self.steps_per_micron}


    def up(self, steps): 
        self.stage.move_by(self.steps_per_micron*steps, channel=2)
        print(f"XY stage position = {self.get_xy_stage_position()}")
    def down(self, steps): 
        self.stage.move_by(-self.steps_per_micron*steps, channel=2)
        print(f"XY stage position = {self.get_xy_stage_position()}")
    def left(self, steps): 
        self.stage.move_by(-self.steps_per_micron*steps, channel=1)
        print(f"XY stage position = {self.get_xy_stage_position()}")
    def right(self, steps): 
        self.stage.move_by(self.steps_per_micron*steps, channel=1)
        print(f"XY stage position = {self.get_xy_stage_position()}")
    