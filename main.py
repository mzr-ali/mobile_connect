import os
import re
import signal
import subprocess
import time
from argparse import ArgumentParser
from datetime import datetime


class MobileConnect:
    def __init__(self, ip_address, port=5555):
        self.ip_address = ip_address
        self.port = port

    def connect(self):
        """ Connect to device """
        try:
            subprocess.check_output(["adb", "tcpip", f'{self.port}'])
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass

        result = subprocess.check_output(["adb", "connect", f"{self.ip_address}:{self.port}"], stderr=subprocess.STDOUT,
                                         timeout=20)
        if 'connected' in result.decode('utf-8'):
            return True
        else:

            return False

    def screen_locked(self):
        """ Check Screen lock status """
        try:
            result = subprocess.check_output(["adb", "shell", "dumpsys", "deviceidle"], stderr=subprocess.STDOUT,
                                             timeout=20)
            screen_pattern = re.compile('mScreenLocked=(.*?)\n', re.MULTILINE | re.DOTALL)
            is_screen_on = re.findall(screen_pattern, result.decode('utf-8'))
            return is_screen_on[0] == 'true'

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            return True

    def start_recording(self, output_path):
        """ Record and stop recording  """
        conneced = self.connect()
        if not conneced:
            print(
                'if you are connecting first time\n1- Connect device with USB cable\n2- Make sure device debug is on\n3- Try again')
            return
        is_recording = False
        result = None
        current_date_time = None
        while True:
            if not is_recording and not self.screen_locked():
                print('Recording')
                current_date_time = f'{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.mp4'
                is_recording = True
                output_file_path = os.path.join(output_path, current_date_time)

                result = subprocess.Popen(
                    ["scrcpy", f"--tcpip={self.ip_address}", "--no-display", "--record", output_file_path],
                    preexec_fn=os.setsid)
            elif is_recording and self.screen_locked():
                is_recording = False
                os.killpg(os.getpgid(result.pid), signal.SIGTERM)
                result = None
            time.sleep(2)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--ip', required=True, type=str)
    parser.add_argument('-p', '--port', type=int, default=5555)
    args = parser.parse_args()
    bot = MobileConnect(ip_address=args.ip, port=args.port)
    bot.start_recording(os.getcwd())
