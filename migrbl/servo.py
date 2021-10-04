#!/usr/bin/env python 

import sys

from gcodetools import Gcodetools
import gcodetools
import time
import os

stdout = sys.stdout.buffer


class PenGcodetools(Gcodetools):
    def export_gcode(self, gcode, no_headers=False):
        if self.options.postprocessor != "" or self.options.postprocessor_custom != "":
            postprocessor = gcodetools.Postprocessor(self.error)
            postprocessor.gcode = gcode
            if self.options.postprocessor != "":
                postprocessor.process(self.options.postprocessor)
            if self.options.postprocessor_custom != "":
                postprocessor.process(self.options.postprocessor_custom)

            gcode = postprocessor.gcode

        if not no_headers:
            gcode = self.header + gcode + self.footer

        with open(os.path.join(self.options.directory, self.options.file), "w") as f:
            f.write(gcode)

    def effect(self):
        start_time = time.time()

        gcodetools.options = self.options
        gcodetools.options.self = self
        gcodetools.options.doc_root = self.document.getroot()

        # define print_ function
        if self.options.log_create_log:
            try:
                if os.path.isfile(self.options.log_filename):
                    os.remove(self.options.log_filename)
                with open(self.options.log_filename, "a") as fhl:
                    fhl.write("""Gcodetools log file.
        Started at {}.
        {}
        """.format(time.strftime("%d.%m.%Y %H:%M:%S"), self.options.log_filename))
            except:
                gcodetools.print_ = lambda *x: None
        else:
            gcodetools.print_ = lambda *x: None

        self.default_tool.update({
            "name": "Laser Engraver",
            "id": "Laser Engraver",
            "diameter": "0.1",
            "depth step": 1,
            "penetration feed": self.options.laser_speed,
            "feed": self.options.laser_speed,
            "gcode before path": (self.options.laser_command + " S" + str(
                self.options.laser_power) + "\nG4 P" + str(self.options.power_delay)),
            "gcode after path": (
                    self.options.laser_off_command + "\nG4 P" + str(self.options.power_delay) + "\n" + "G1 F" + str(self.options.travel_speed)),
        })

        self.options.path_to_gcode_depth_function = "d"

        self.tab_path_to_gcode()

        gcodetools.print_("------------------------------------------")
        gcodetools.print_("Done in {:f} seconds".format(time.time() - start_time))
        gcodetools.print_("End at {}.".format(time.strftime("%d.%m.%Y %H:%M:%S")))

    def add_arguments(self, pars):
        super(PenGcodetools, self).add_arguments(pars)

        add_argument = pars.add_argument
        add_argument("--laser-speed", dest="laser_speed", type=float, default="3000", help="Feed rate in unit/min")
        add_argument("--travel-speed", dest="travel_speed", type=float, default="3000", help="Feed rate in unit/min")
        add_argument("--laser-power", dest="laser_power", type=float, default="30", help="Feed rate in unit/min")
        add_argument("--power-delay", dest="power_delay", type=float, default="0.1", help="Feed rate in unit/min")
        add_argument("--laser-command", dest="laser_command", default="M3", help="Comment Gcode")
        add_argument("--laser-off-command", dest="laser_off_command", default="M5", help="Comment Gcode")


if __name__ == '__main__':
    gkt = PenGcodetools()
    gkt.run()
