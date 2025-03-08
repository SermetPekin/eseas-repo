import os
import platform
from dataclasses import dataclass


def check_java_version():
    JAVA_EXEC_PATH = "/usr/bin/java"
    os.system(f"{JAVA_EXEC_PATH} -version")


def get_os():
    return str(platform.system()).lower()


import subprocess
from pathlib import Path


@dataclass
class JavaEnviron:

    def __init__(self, java_bin: str = None, quick=None):
        self.java_bin = None if java_bin is None else   str(java_bin)
        self.check_exists()

        self.separator = ";" if self.windows() else ":"
        self.quick = True if quick is None else False
        if self.java_bin:
            self.quick = False

        self.process()

    def check_exists(self):
        if self.java_bin is None :
            return 
        p = Path(self.java_bin)
        if p.exists():
            return
        raise ValueError(
            f"""\n\n `java_bin` directory was given as `{self.java_bin}` but it does not exist or it is not a directory `{self.java_bin}`
                         if your java folder is already defined as `path` just remove java_bin parameter while calling Cruncher. 
                         Or give a correct folder where java executable exists. 
                         """
        )

    def process(self):
        if self.java_bin is None:
            self.show_java_version()
            self.show_cmd()
            self.check_java_folders()
        else:
            self.set_path()

            self.sleep(3)
            self.show_java_version()
            self.show_cmd()
            self.check_java_folders()

    def windows(self) -> bool:
        return get_os() == "windows"

    def find_java_paths(self) -> list[str]:
        cmd_where_which = "where" if self.windows() else "which"
        result = self.run_process([cmd_where_which, "-a", "java"])
        java_paths = result.stdout.strip().split("\n")
        return java_paths if java_paths[0] else []

    def run_process(self, cmds):
        class Result:
            stderr = "Error in subprocess while running " + " ".join(cmds)
            stdout = ""

        result = Result()
        try:
            result = subprocess.run(cmds, capture_output=True, text=True)
        except Exception as exc:
            import traceback

            traceback.print_exc()

        return result

    def sleep(self, num=2):
        if self.quick:
            return
        import time

        time.sleep(num)

    def show_java_version(self):
        print("[showing java version] ...")
        result = self.run_process(["java", "-version"])
        res = (str(result.stdout) + str(result.stderr)).strip().split("\n")
        msg = "\n".join(res)
        print("Java Version \n", msg)
        self.sleep(2)

    def check_java_folders(self):
        print("[checking Java folders] ...")
        java_executables: list = self.find_java_paths()
        folders = self.split()
        active = False
        suffix = "/java.exe" if self.windows() else "/java"
        active_java_folder = "None"
        for path in java_executables:
            p = str(path).removesuffix(suffix)
            if p in folders and active is False:
                active = True
                active_java_folder = p
        folders = self.split()
        liste = []
        for p in folders:
            bool_ = active_java_folder == p
            liste.append((bool_, p))
        self.show_folders(liste, "Current Folders in environment [Path variable]")
        self.sleep(2)

    def show_cmd(self):
        cmd = """
        To check manually :
        from Terminal type  
                echo $PATH 
                java -version 

            """
        if self.windows():
            cmd = """
        To check manually :
        from Command line 
                path
                java -version 
            """
        print(cmd)
        self.sleep(2)

    def split(self) -> tuple:
        d = os.environ.get("PATH")
        return d.split(self.separator)

    def show_folders(self, items: tuple, msg: str = None):
        if not items:
            return
        if msg is None:
            msg = "Setting path environment variable with these folders:"

        def p(bool_: bool, string: str):
            string = str(string)
            if bool_:
                return "[+]  -> " + string
            return "     -> " + string

        def show():
            template = msg
            print(template)
            for bool_, item in items:
                x = p(bool_, item)
                if item is None:
                    continue
                print(x)

        show()
        self.sleep(2)

    def set_path(self):
        folders = self.split()
        folders2 = [self.java_bin] + [x for x in folders if x != self.java_bin]

        def check(string):
            return string == str(self.java_bin)

        items2 = [(check(x), x) for x in folders2]
        self.show_folders(items2)
        print(f"[Done] {self.java_bin} was set as java folder")
        self.sleep(2)


# e = JavaEnviron("/usr/bin")
