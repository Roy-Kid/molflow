import os
from molflow.parser import LmpLogParser
import time
import nni

optimized_params = nni.get_next_parameter()

# start to run the task
os.system(f'lmp -in in.lj -var eps {optimized_params["eps"]} -var sig {optimized_params["sig"]}')

parser = LmpLogParser(log_name = 'lammps.log')

for output in parser.watch(keys=['TotEng']):

    if "TotEng" not in output:
        continue
    else:
        nni.report_intermediate_result(output["TotEng"][-1])

    if parser.is_finish():
        break
    else:
        time.sleep(1)

nni.report_final_result(output["TotEng"][-1])