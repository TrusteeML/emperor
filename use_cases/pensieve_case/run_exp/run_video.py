import os
import sys
import signal
import subprocess

# import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# from selenium.webdriver.remote.remote_connection import LOGGER

# LOGGER.setLevel(logging.INFO)

from pyvirtualdisplay import Display
from time import sleep


# TO RUN: download https://pypi.python.org/packages/source/s/selenium/selenium-2.39.0.tar.gz
# run sudo apt-get install python-setuptools
# run sudo apt-get install xvfb
# after untar, run sudo python setup.py install
# follow directions here: https://pypi.python.org/pypi/PyVirtualDisplay to install pyvirtualdisplay

# For chrome, need chrome driver: https://code.google.com/p/selenium/wiki/ChromeDriver
# chromedriver variable should be path to the chromedriver
# the default location for firefox is /usr/bin/firefox and chrome binary is /usr/bin/google-chrome
# if they are at those locations, don't need to specify


def timeout_handler(signum, frame):
    raise Exception("Timeout")


ip = sys.argv[1]
abr_algo = sys.argv[2]
run_time = int(sys.argv[3])
process_id = sys.argv[4]
trace_file = sys.argv[5]
sleep_time = sys.argv[6]

SUMMARY_DIR = "./results"
LOG_FILE = "./results/log"

if not os.path.exists(SUMMARY_DIR):
    os.makedirs(SUMMARY_DIR)

# prevent multiple process from being synchronized
sleep(int(sleep_time) + 10)  # + 10 for safety

# generate url
url = "http://" + ip + "/" + "index_" + abr_algo + ".html"


# timeout signal
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(run_time + 30)

try:
    print("RUN VIDEO")
    # copy over the chrome user dir
    default_chrome_user_dir = "../abr_browser_dir/chrome_data_dir"
    chrome_user_dir = "/tmp/chrome_user_dir_id_" + process_id
    os.system("rm -r " + chrome_user_dir)
    os.system("cp -r " + default_chrome_user_dir + " " + chrome_user_dir)

    # # start abr algorithm server
    # if abr_algo == "RL":
    #     command = (
    #         "exec /usr/bin/python ../rl_server/rl_server_no_training.py " + trace_file
    #     )
    # elif abr_algo == "fastMPC":
    #     command = "exec /usr/bin/python ../rl_server/mpc_server.py " + trace_file
    # elif abr_algo == "robustMPC":
    #     print("RUN ROBUST MPC")
    #     command = "exec /usr/bin/python ../rl_server/robust_mpc_server.py " + trace_file
    # else:
    #     print("RUN SIMPLE SERVER")
    #     command = (
    #         "exec /usr/bin/python ../rl_server/simple_server.py "
    #         + abr_algo
    #         + " "
    #         + trace_file
    #     )

    # proc = subprocess.Popen(
    #     command,
    #     # stdout=subprocess.PIPE,
    #     # stderr=subprocess.PIPE,
    #     shell=True,
    # )
    # sleep(5)

    # to not display the page in browser
    display = Display(visible=0, size=(800, 600))
    display.start()

    # initialize chrome driver
    chrome_driver = "../abr_browser_dir/chromedriver"
    # options = Options()
    # options.add_argument("--user-data-dir=" + chrome_user_dir)
    # options.add_argument("--ignore-certificate-errors")
    # driver = webdriver.Chrome(chrome_driver, chrome_options=options)

    # enable browser logging
    d = DesiredCapabilities.CHROME
    d["goog:loggingPrefs"] = {"browser": "ALL"}

    options = webdriver.ChromeOptions()
    options.add_argument("enable-automation")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--user-data-dir=" + chrome_user_dir)
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-file-access-from-files")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--allow-file-access-from-files")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--allow-cross-origin-auth-prompt")
    options.add_argument("--allow-file-access")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-features=CrossSiteDocumentBlockingIfIsolating")

    ser = Service(chrome_driver)
    driver = webdriver.Chrome(service=ser, options=options, desired_capabilities=d)

    # run chrome
    driver.set_page_load_timeout(10)
    print("REQUEST", url)
    driver.get(url)
    # print("REQUEST DONE")
    # print(driver.page_source)
    print("SLEEPING FOR {}s...".format(str(run_time + 10)))

    sleep(run_time + 10)  # + 10 for safety
    # sleep(20)  # + 10 for safety

    with open(LOG_FILE + "_" + abr_algo + "_" + trace_file, "a") as log_file:
        for entry in driver.get_log("browser"):
            # print(entry)
            if "RESULTS" in entry["message"]:
                log_file.write(entry["message"].split('"RESULTS"')[1].strip())
                log_file.write("\n")
        # so we know when the video ends
        log_file.write("\n")

    # print messages
    # with open(LOG_FILE + "_" + abr_algo + "_" + trace_file, "w") as log_file:
    #     for index in range(run_time + 10):
    #         sleep(1)  # + 10 for safety
    #         for entry in driver.get_log("browser"):
    #             print(entry)
    #             if "RESULTS" in entry["message"]:
    #                 log_file.write(entry["message"].split('"RESULTS"')[1].strip())
    #                 log_file.write("\n")

    # # so we know when the video ends
    # log_file.write("\n")

    driver.quit()
    display.stop()

    # kill abr algorithm server
    # proc.send_signal(signal.SIGINT)
    # proc.kill()

    print("done")

except Exception as e:
    print("EXCEPTION", e)
    try:
        display.stop()
    except:
        pass
    try:
        driver.quit()
    except:
        pass
    # try:
    #     proc.send_signal(signal.SIGINT)
    # except:
    #     pass

    print(e)
