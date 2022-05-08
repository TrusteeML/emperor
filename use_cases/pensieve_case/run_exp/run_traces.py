import sys
import os
import subprocess
import numpy as np


RUN_SCRIPT = "run_video.py"
RANDOM_SEED = 42
RUN_TIME = 320  # sec
MM_DELAY = 40  # millisec


def main():
    trace_path = sys.argv[1]
    abr_algo = sys.argv[2]
    process_id = sys.argv[3]
    ip = sys.argv[4]

    sleep_vec = list(range(1, 15))  # random sleep second

    files = os.listdir(trace_path)
    for f in files:
        print("RUN TRACE", trace_path, abr_algo)

        while True:

            np.random.shuffle(sleep_vec)
            sleep_time = sleep_vec[int(process_id)]

            command = (
                "mm-delay "
                + str(MM_DELAY)
                + " mm-link 12mbps "
                + trace_path
                + f
                + " "
                + "/usr/bin/python "
                + RUN_SCRIPT
                + " "
                + ip
                + " "
                + abr_algo
                + " "
                + str(RUN_TIME)
                + " "
                + process_id
                + " "
                + f
                + " "
                + str(sleep_time)
            )

            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )

            (out, err) = proc.communicate()

            print(out)
            if "done" in str(out):
                break
            else:
                with open("./chrome_retry_log", "ab") as log:
                    log.write((abr_algo + "_" + f + "\n").encode())
                    log.write((str(out) + "\n").encode())
                    log.write((str(err) + "\n").encode())
                    log.flush()


if __name__ == "__main__":
    main()
