import time
import argparse
import os
from subprocess import call
import poormanslogging as log
from settings import environments, defaultEnvironment, defaultDriver



if __name__ == '__main__':
    def selectDriver(argsDriver):
        from selenium import webdriver

        if argsDriver == "chrome":
            return webdriver.Chrome("/home/juan/Automation/chromedriver")
        if argsDriver == "headless_chrome":
            driverOptions = webdriver.chrome.options.Options()
            driverOptions.add_argument("--headless")
            return webdriver.Chrome("/home/juan/Automation/chromedriver" ,chrome_options=driverOptions)
        elif argsDriver == "remote_headless_chrome":
            return webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                           desired_capabilities=webdriver.common.desired_capabilities.DesiredCapabilities.CHROME)
        else:
            raise Exception("Driver '{}' is not handled".format(argsDriver))

    def generatePPBLink(argsDriver):
        from selenium import webdriver
        from pages.RequestBin import RequestBin

        driver = selectDriver(argsDriver)
        requestBin = RequestBin (driver)
        ppbLink = requestBin.generateMockLink()
        driver.quit()
        return ppbLink


    argsParser = argparse.ArgumentParser()
    argsParser.add_argument("-d", "--driver",
                            choices=["chrome", "headless_chrome", "remote_headless_chrome"],
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
    argsParser.add_argument("-ppb", "--ppblink",
                            help="Specify a link to make PPB (Post Por Background), for example "
                                 "'--ppblink http://marathon-lb.infrastructure.marathon.mesos:10113/reyhgpre'. "
                                 "If no link is sent as parameter, a new one will be generated using RequestBin.")
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

    os.environ["PPBLINK"] = args.ppblink if args.ppblink else generatePPBLink(os.environ["DRIVER"])

    log.info(("You're running on {} environment").format(os.environ["ENVIRONMENT"]))
    log.info(("You're using {} driver").format(environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["driver"]))
    log.info(("Post Por Background link: {}").format(os.environ["PPBLINK"]))
    log.info(("Report will be stored at path = {}reports/test_report_{}.xml".format
            ("/build/" if os.getenv("ENVIRONMENT", defaultEnvironment) == "jenkins" else "",
            os.getenv("BUILDVERSION",str(int(time.time()))))))

    #This is for using a report file name with timestamp format
    reportFile = open("unittest.cfg", "w")
    reportFile.write((
        "[unittest]\n"
        "plugins = nose2.plugins.junitxml\n"
        #"plugins = nose2.plugins.layers\n"
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

