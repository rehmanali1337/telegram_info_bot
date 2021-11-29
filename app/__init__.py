import logging
import colorama
colorama.init(autoreset=True)


logging_format = logging.Formatter(
    "%(levelname)s:[%(filename)s:%(lineno)s]:%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging_format)
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(logging_format)

logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


class Console:

    @staticmethod
    def error(message: str):
        print(colorama.Fore.RED + colorama.Style.BRIGHT + f"[-] {message}")

    @staticmethod
    def warn(message: str):
        print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"[*] {message}")

    @staticmethod
    def info(message: str):
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT + f"[+] {message}")
