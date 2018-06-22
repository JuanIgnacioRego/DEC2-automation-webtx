import time
import argparse
import os
from subprocess import call
import poormanslogging as log
from settings import environments, defaultEnvironment, defaultDriver

if __name__ == '__main__':
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument("-d", "--driver",
                            choices=["chrome", "headless_chrome"],
                            help="Test using an specific browser driver, for example '--webdriver headless_chrome'. "
                                 "Chrome is used by default.")
    argsParser.add_argument("-ts", "--testsuite",
                            help="Specify a test suite to be run, for example '--testsuite home/user/smoke_test'. "
                                 "If no file is sent as parameter, all test cases will be run.")
    argsParser.add_argument("-e", "--environment",
                            choices=["desa", "local_machine", "jenkins"],
                            help="Set an environment to run tests, for example '--environment jenkins' set baseURL, "
                            "port and browser driver to be deployed on Jenkins. "
                            "DESA environment is used by default.")
    argsParser.add_argument("-bv", "--buildversion",
                            help="Indicate a build version. It will be used to generate report file name. "
                                 "For example, '--buildversion 75' will generate '75_report.xml' report file. "
                                 "A timestamp is used by default.")

    args = argsParser.parse_args()
    if (args.environment and args.driver) or (not args.environment and args.driver):
        os.environ["DRIVER"] = args.driver
    else:
        os.environ["DRIVER"] = defaultDriver
    os.environ["ENVIRONMENT"] = args.environment if args.environment else defaultEnvironment
    os.environ["BUILDVERSION"] = args.buildversion if args.buildversion else str(int(time.time()))
    if environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["driver"] != os.getenv("DRIVER", defaultDriver):
        environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["driver"] = args.driver
    if args.testsuite:
        try:
            file = open(args.testsuite, 'r')
            testsToRun = []
            for line in [line for line in file if not line.startswith("#")]:
                testsToRun.append(line.replace("\n", ""))

        except Exception:
            print (("There was a problem trying to open --testsuite file '{}'.\n"
                   "Please, verify if:\n"
                    "- file exists there;\n"
                    "- file has a plain text format;\n"
                    "- necessary permissions were given to open that file;\n"
                    ).format(args.testsuite))
            exit()

    log.info(("You're running on {} environment").format(os.environ["ENVIRONMENT"]))
    log.info(("You're using {} driver").format(environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["driver"]))

    #This is for using a report file name with timestamp format
    reportFile = open("unittest.cfg", "w")
    reportFile.write((
        "[unittest]\n"
        "plugins = nose2.plugins.junitxml\n"
        "\n"
        "[junit-xml]\n"
        "always-on = True\n"
        "keep_restricted = False\n"
        #"path = /build/reports/test_report_{}.xml\n"
        "path = {}reports/test_report_{}.xml\n"
        "test_fullname = True\n"
    ).format("/build/" if os.getenv("ENVIRONMENT", defaultEnvironment) == "jenkins" else "",
            os.getenv("BUILDVERSION",str(int(time.time()))))
            )
    reportFile.close()

    listToCall = ["nose2"] + ["--verbose"] + ["--config"] + ["unitest.cfg"]

    if args.testsuite:
        for test in testsToRun:
            listToCall += [test]

    call(listToCall)

"""
nose2 test_St.test_CompraSimple.test_hola test_St.test_CompraSimple.test_chau test_St.test_CompraSimple.test_holaYChau    runner.run(suite())
"""