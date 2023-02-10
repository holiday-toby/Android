import subprocess
import os
import shutil
import hashlib


# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:

    @staticmethod
    def header(text):
        Logger._print(Colors.HEADER, text)

    @staticmethod
    def info(text):
        Logger._print(Colors.OKBLUE, text)

    @staticmethod
    def success(text):
        Logger._print(Colors.OKGREEN, text)

    @staticmethod
    def _print(color, text):
        Logger._println(f"{color}{text}{Colors.ENDC}")

    @staticmethod
    def _println(text):
        print(text, end="\n\n")


gradle = "../gradlew -p ../"

version = subprocess.getoutput(f"{gradle} -q printVersion")
Logger.header(f"Package version: {version}")

sdk_version_name = version.split("_")[1]
Logger.header(f"SDK version name: {sdk_version_name}")

output_path = os.path.abspath(f"../release/msdk_{version}")
output_zip_filename = f"MSDK-Android-{sdk_version_name}"
output_temp_path = f"{output_path}/temp"

source_codes_filename = f"msdk_{version}_source_codes.zip"
source_codes_temp_path = f"{output_temp_path}/{source_codes_filename}"

sample_apk_name = f"msdk_demo_{version}-google-iap-release.apk"
sample_apk_path = f"googleIap/release/{sample_apk_name}"

git_current_branch = subprocess.getoutput("git rev-parse --abbrev-ref HEAD")
Logger.header(f"Current branch: {git_current_branch}")


def init():
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_temp_path)


def output_source_codes():
    Logger.info("Output source codes...")
    os.system(
        f"cd .. && git archive --format zip --output '{source_codes_temp_path}' '{git_current_branch}' ")


def generate_apk():
    Logger.info("Clean project...")
    os.system(f"{gradle} clean")

    Logger.info("Generate Apk...")
    os.system(f"{gradle} assembleGoogleIapRelease")

    Logger.info("Copy Apk...")
    shutil.copy(os.path.abspath(f"../sample/build/outputs/apk/{sample_apk_path}"),
                output_temp_path)


def package_output():
    Logger.info("Package output...")

    os.chdir(output_path)
    shutil.make_archive(output_zip_filename, 'zip', output_temp_path)

    if os.path.exists(output_temp_path):
        shutil.rmtree(output_temp_path)


def calculate_md5():
    with open(f"{output_path}/{output_zip_filename}.zip", "rb") as f:
        Logger.info(f"Package md5: {hashlib.new('md5', f.read()).hexdigest()}")


init()
output_source_codes()
generate_apk()
package_output()
calculate_md5()

Logger.success(f"Please find files here: {output_path}")
