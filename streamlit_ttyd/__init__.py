"""
	This module provides a way to use a terminal under streamlit framework
"""
__version__ = "0.2.0"

import platform
import subprocess

import psutil
from port_for import get_port
from streamlit.components.v1 import iframe
from importlib import resources


def is64bit():
    return "64" in platform.machine()


def isARM():
    return "aarch" in platform.machine() or "arm" in platform.machine()


def get_ttyd():

    if psutil.WINDOWS:
        ttyd = None

    if psutil.MACOS or psutil.LINUX:
        if isARM():
            if is64bit():
                ttyd = "./binary/ttyd.aarch64"
            else:
                ttyd = "./binary/ttyd.arm"

        else:  # x86
            # we dont care here if 64bit
            ttyd = "./binary/ttyd.x86_64"

    ttyd = resources.files("streamlit_ttyd").joinpath(ttyd)
    # print(ttyd)
    return ttyd


def terminal(
    cmd: str = "echo terminal-speaking... && sleep 99999",
    readonly: bool = False,
    host: str = "http://localhost",
    port: int = 0,
    exit_on_disconnect: bool = True,
    height: int = 400,
    ttyd = ""
):
    assert type(port) == int

    if port == 0:
        port = get_port((5000, 7000))

    flags = f"--port {port} "
    if exit_on_disconnect:
        flags += "--once "
    if readonly:
        flags += "--readonly"
    
    # check if user provided path to ttyd
    ttyd = get_ttyd() if ttyd=="" else ttyd
    # print(ttyd)    
    ttydproc = subprocess.Popen(
        f"{ttyd} {flags} {cmd}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    iframe(f"{host}:{port}", height=height)

    return ttydproc, port
