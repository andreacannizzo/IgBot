from definitions import *
import chromedriver_autoinstaller
import os
import ssl
import sys
import getopt


def options(argv):
    arg_likes = 2
    arg_boolean = False
    arg_help = "{0} -u <username> -l <likes> -b <boolean>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hu:l:b:", ["help", "username=", "likes=", "boolean="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-u", "--username"):
            arg_user = arg
        elif opt in ("-l", "--likes"):
            arg_likes = int(arg)
        elif opt in ("-b", "--boolean"):
            if arg == "True":
                arg_boolean = True
            else:
                arg_boolean = False

    ssl._create_default_https_context = ssl._create_unverified_context
    # auto download latest chromedriver if mac then open a browser and get its handle
    # TODO fix the chromedriver_autoinstaller for Rasp
    auto_chromedriver = chromedriver_autoinstaller.install()
    browser = launch_browser(auto_chromedriver, False, arg_boolean)

    if os.path.exists("Clients_Files/" + arg_user + "/cookies_file"):
        LOAD_cookie(browser, arg_user)
    else:
        input_password = input("Enter the password: ")
        inputs_hashtags = []
        while True:
            inp = input("Enter a valid hashtag without the # prefix / Press Enter when finished: ")
            if inp == "":
                break
            inputs_hashtags.append(inp)
        SAVE_cookies(browser, arg_user, input_password)
        SAVE_hashtags(arg_user, inputs_hashtags)
        input("Press Enter when access authenticated...")

    avoid_popup(browser, "Not Now")
    put_likes(browser, arg_user, arg_likes)

    # close browser and exit
    browser.close()
    exit()


if __name__ == "__main__":
    options(sys.argv)
