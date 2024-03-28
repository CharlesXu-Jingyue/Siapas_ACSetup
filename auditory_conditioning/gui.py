from pyBehavior.interfaces.rpi.local import RPIRewardControl, PumpConfig
from pyBehavior.interfaces.socket import Position
from ratBerryPi.interfaces import RewardInterface
from pyBehavior.gui import *

class auditory_conditioning(SetupGUI):
    def __init__(self):
        super(auditory_conditioning, self).__init__(Path(__file__).parent.resolve())
        self.interface = RewardInterface(None)
        self.buildUI()

    def buildUI(self):

        self.position = Position()
        self.position.new_position.connect(self.register_pos)
        self.position.start()
        self.layout.addWidget(self.position)

        # self.pump1 = PumpConfig(self.interface, 'pump1', ['module1', 'module2'])
        self.pump1 = PumpConfig(self.interface, 'pump1', ['module1'])
        self.layout.addWidget(self.pump1)

        self.mod1 = RPIRewardControl(self.interface, 'module1')
        self.mod1.new_lick.connect(lambda x: self.register_lick('a', x))
        # self.mod2 = RPIRewardControl(self.interface, 'module2')
        # self.mod2.new_lick.connect(lambda x: self.register_lick('b', x))

        # self.reward_modules.update({'a': self.mod1, 
        #                             'b': self.mod2})
        self.reward_modules.update({'a': self.mod1})

        #format widgets
        mod_layout = QHBoxLayout()
        mod_layout.addWidget(self.mod1)
        # mod_layout.addWidget(self.mod2)
        self.layout.addLayout(mod_layout)

    def register_lick(self, arm, amt):
        if self.running:
            self.state_machine.handle_input({"type": "lick", "arm": arm, "amt":amt})
        self.log(f"{arm} {amt} licks")

    def register_pos(self, pos):
        pos = tuple(pos)
        self.pos.setText(str(pos))
        if self.running:
            self.state_machine.handle_input({"type":"pos", "pos": pos})

    def trigger_reward(self, module, small, force = True, wait = False):
        amt = float(self.reward_modules[module].amt.text())
        amt = amt * float(self.reward_modules[module].small_pulse_frac.text()) if small else amt
        self.log(f"triggering {amt:.2f} mL reward on module {module}")
        self.reward_modules[module].trigger_reward(small, force, wait)