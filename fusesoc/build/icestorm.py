import os.path
from fusesoc import utils

from fusesoc.build.backend import Backend
class Icestorm(Backend):

    MAKEFILE_TEMPLATE = """#Auto generated by FuseSoC
include config.mk

all: $(TARGET).bin

%.blif: %.ys
	yosys -q -s $?
%.txt: $(PCF_FILE) %.blif
	arachne-pnr $(ARACHNE_PNR_OPTIONS) -q -p $? -o $@
%.bin: %.txt
	icepack $< $@

clean:
	rm -f $(TARGET).blif $(TARGET).txt $(TARGET).bin
"""

    CONFIG_MK_TEMPLATE = """#Auto generated by FuseSoC
TARGET   := {target}
PCF_FILE := {pcf_file}
ARACHNE_PNR_OPTIONS := {arachne_pnr_options}
"""

    def configure(self, args):
        super(Icestorm, self).configure(args)
        self._write_config_files()

    def _write_config_files(self):
        # Write Makefile
        with open(os.path.join(self.work_root, 'Makefile'), 'w') as makefile:
            makefile.write(self.MAKEFILE_TEMPLATE)

        # Write yosys script file
        (src_files, incdirs) = self._get_fileset_files()
        with open(os.path.join(self.work_root, self.name+'.ys'), 'w') as yosys_file:
            yosys_file.write("verilog_defaults -push\n")
            yosys_file.write("verilog_defaults -add -defer\n")
            if incdirs:
                yosys_file.write("verilog_defaults -add {}\n".format(' '.join(['-I'+d for d in incdirs])))

            pcf_files = []
            for f in src_files:
                if f.file_type in ['verilogSource']:
                    yosys_file.write("read_verilog {}\n".format(f.name))
                elif f.file_type == 'PCF':
                    pcf_files.append(f.name)
            for key, value in self.vlogparam.items():
                _s = "chparam -set {} {} $abstract\{}\n"
                yosys_file.write(_s.format(key,
                                           self._param_value_str(value, strings_in_quotes=True),
                                           self.toplevel))

            yosys_file.write("verilog_defaults -pop\n")
            yosys_file.write("synth_ice40")
            yosys_file.write(" -blif {}.blif".format(self.name))
            if self.toplevel:
                yosys_file.write(" -top " + self.toplevel)
            yosys_file.write("\n")

        if not pcf_files:
            raise RuntimeError("Icestorm backend requires a PCF file")
        elif len(pcf_files) > 1:
            raise RuntimeError("Icestorm backend supports only one PCF file. Found {}".format(', '.join(pcf_files)))
        # Write config.mk
        with open(os.path.join(self.work_root, 'config.mk'), 'w') as config_mk:
            config_mk.write(self.CONFIG_MK_TEMPLATE.format(
                target              =  self.name,
                pcf_file            = pcf_files[0],
                arachne_pnr_options = ' '.join(self.tool_options['arachne_pnr_options'])))

    def build(self, args):
        super(Icestorm, self).build(args)

        utils.Launcher('make', cwd = self.work_root).run()

        super(Icestorm, self).done()
