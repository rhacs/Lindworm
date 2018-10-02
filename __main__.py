#!/usr/bin/python3
from os.path import dirname, realpath
from sys import argv, exit

from PyQt5.QtWidgets import QApplication
from lindworm import Lindworm

if __name__ == '__main__':
    application = QApplication(argv)

    application.setStyle("fusion")
    application.setApplicationName("Lindworm")
    application.setApplicationVersion("1.0:2018.10")
    application.setOrganizationName("rhacs")

    workdir = dirname(realpath(__file__))
    lindworm = Lindworm(workdir)

    exit(application.exec_())
