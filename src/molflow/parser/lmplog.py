# author: Roy Kid
# contact: lijichen365@126.com
# date: 2023-06-11
# version: 0.0.1

from collections import defaultdict

START_THERMO_STRINGS = ["Memory usage per processor", "Per MPI rank memory allocation"]
END_THERMO_STRINGS = ["Loop time", "ERROR"]

START_TIMING_STRINGS = ["MPI task timing breakdown"]
END_TIMING_STRINGS = ["Nlocal"]

class LmpLog:

    # This class can keep watch log.lammps and read the data

    def __init__(self, log_name="log.lammps"):
        # Identifiers for places in the log file
        self.log_name = log_name
        self.before_run_output = []
        self.each_run_output = {}
        self.n_run = 0
        self._is_finish = False

    @property
    def is_finish(self):
        return self._is_finish

    def read(self, keys=[]):
        """Read log file and store data in a dictionary."""
        f = open(self.log_name, "r")
        contents = f.readlines()
        thermo_section_flag = False
        self.n_run = 0
        i = 0
        n_run_output = defaultdict(list)
        while i < len(contents):
            line = contents[i]
            if not self.n_run:
                self.before_run_output.append(line)

            #--- read thermo section ---
            if thermo_section_flag:
                keywords = line.split()
                if sum([key in keywords for key in keys]):
                    # get index of keys
                    key_index = [keywords.index(key) for key in keys]
                    # start to parse data
                    i += 1
                    line = contents[i]
                    while not sum([string in line for string in END_THERMO_STRINGS]) >= 1:
                        for j, key in enumerate(keys):
                            n_run_output[key].append(float(line.split()[key_index[j]]))
                        i += 1
                        line = contents[i]

                    # end
                    self.each_run_output[self.n_run-1] = n_run_output
                thermo_section_flag = False

            # Check whether start to read thermo section
            if sum([line.startswith(string) for string in START_THERMO_STRINGS]) >= 1:
                thermo_section_flag = True
                self.n_run += 1
            i += 1

            # Check whether start to read timing section
            # if sum([line.startswith(string) for string in START_TIMING_STRINGS]) >= 1:
                

    def watch(self, keys=[]):

        f = open(self.log_name, "r")
        n_run_output = defaultdict(list)
        while line:=f.readline():

            #--- read thermo section ---
            if thermo_section_flag:
                keywords = line.split()
                if sum([key in keywords for key in keys]):
                    # get index of keys
                    key_index = [keywords.index(key) for key in keys]
                    # start to parse data
                    line = f.readline()
                    while not sum([string in line for string in END_THERMO_STRINGS]) >= 1:
                        for j, key in enumerate(keys):
                            n_run_output[key].append(float(line.split()[key_index[j]]))
                        line = f.readline()

                    # end
                    self.each_run_output[self.n_run-1] = n_run_output
                thermo_section_flag = False

            # Check whether start to read thermo section
            if sum([line.startswith(string) for string in START_THERMO_STRINGS]) >= 1:
                thermo_section_flag = True
                self.n_run += 1
            line = f.readline()

            # Check whether start to read timing section
            # if sum([line.startswith(string) for string in START_TIMING_STRINGS]) >= 1:

            if "Total wall time" in line:
                self._is_finish = True
                break

            yield n_run_output



if __name__ == '__main__':
    log = LmpLog("example/lmp_lj_pot/log.lammps")
    log.read(keys=["TotEng"])
    print(log.each_run_output[0]["TotEng"])