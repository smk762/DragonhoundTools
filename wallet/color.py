#!/usr/bin/env python3

class ColorMsg():
    def __init__(self):
        self.colors = {
            'default':'\033[0m',
            'status':'\033[94m',
            'lightblue':'\033[94m',
            'table':'\033[37m',
            'lightgrey':'\033[37m',
            'warning':'\033[91m',
            'lightred':'\033[91m',
            'validated':'\033[92m',
            'lightgreen':'\033[92m',
            'error':'\033[31m',
            'red':'\033[31m',
            'black':'\033[30m',
            'green':'\033[32m',
            'orange':'\033[33m',
            'blue':'\033[34m',
            'purple':'\033[35m',
            'cyan':'\033[36m',
            'darkgrey':'\033[90m',
            'yellow':'\033[93m',
            'pink':'\033[95m',
            'lightcyan':'\033[96m',
        }

    def color(self, color: str) -> str:
        return self.colors[color]
        
    def colorize(self, msg: str, color: str) -> str:
        if color not in self.colors:
            return f"{msg}"
        else:
            return f"{self.color(color)}{msg}{self.color('default')}"

    def input(self, msg: str) -> str:
        return input(f'\n> {self.colorize(msg, "orange")}')

    def table(self, msg: str) -> None:
        print(self.colorize(msg, "cyan"))

    def info(self, msg: str) -> None:
        print(self.colorize(msg, "orange"))

    def status(self, msg: str) -> None:
        print(self.colorize(msg, "status"))

    def success(self, msg: str) -> None:
        print(self.colorize(msg, "green"))

    def option(self, msg: str) -> None:
        print(self.colorize(msg, "darkgrey"))

    def warning(self, msg: str) -> None:
        print(self.colorize(msg, "lightred"))

    def error(self, msg: str) -> None:
        print(self.colorize(msg, "error"))
        
    def green(self, msg: str) -> None:
        print(self.colorize(msg, "green"))

    def ltgreen(self, msg: str) -> None:
        print(self.colorize(msg, "lightgreen"))

    def ltgrey(self, msg: str) -> None:
        print(self.colorize(msg, "lightgrey"))

    def ltblue(self, msg: str) -> None:
        print(self.colorize(msg, "lightblue"))

    def ltcyan(self, msg: str) -> None:
        print(self.colorize(msg, "lightcyan"))

    def darkgrey(self, msg: str) -> None:
        print(self.colorize(msg, "darkgrey"))

    def confirm(self) -> None:
        self.input("Press [Enter] to continue...")
