from dataclasses import dataclass 
import subprocess
from enum import Enum, auto 
import locale

system_encoding = locale.getpreferredencoding()

class Status(Enum):
    success = auto()
    failed = auto() 
    waiting = auto() 

@dataclass
class Subprocess:
    command : tuple 
    convert : bool = True 
    status :Status = Status.waiting 
    return_code : int = -1  
    stdout : str =  "" 
    stderr :str = "" 
    
    def explode(self , command: str ):
        return [x for x in str(command).split() if x ]
        
    def __post_init__(self):
        if self.convert is False :
            return 
        if isinstance(self.command , str ): 
            self.command = self.explode(self.command)
        commands = []
        for command in self.command:
             c = self.explode(command) 
             commands.extend(c) 
        self.command =commands 
            
    def str_(self):
        t = f"""
      command       : {self.command}
      status        : {self.status} 
      return_code   : {self.return_code}
      stdout        : {self.stdout} 
      stderr        : {self.stderr}
      
        """
        return t 
    def __str__(self):
        return self.str_() 
    
        
    def run(self, verbose = False ):
        
        self.return_code , self.stdout , self.stderr = self.run_internal(self.command)
        self.status = Status.success if self.return_code == 0 else  Status.failed        
        self.evaluate()

    def evaluate(self):
        if self.return_code == 0:
            print("Command 1 executed successfully:")
            print("Stdout:\n", self.stdout)
        else:
            print("Command 1 failed.")
            print("Stderr:\n", self.stderr)

    def sleep(self, seconds :int =  1 ):
            import time 
            time.sleep(seconds)            


    def run_internal(self, command , verbose = False):
        if verbose :
            print(command) 
        try:
            result = subprocess.run(
                command,
                capture_output=True,      # Capture stdout and stderr
                text=True,                # Decode output as text (instead of bytes)
                check=True,               # Raise an exception if the return code is non-zero
                encoding=system_encoding, # "utf-8" 
            )

            return result.returncode, result.stdout, result.stderr

        except subprocess.CalledProcessError as e:
            
            print(f"Command failed with error: {e}")
            print(f"Return code: {e.returncode}")
            print(f"Stdout: {e.stdout}")
            print(f"Stderr: {e.stderr}")
            self.sleep(2) 
            return e.returncode, e.stdout, e.stderr
        except FileNotFoundError:
            print(f"Command not found: {self.command[0]}")
            return -1, "", "Command not found"  # Indicate an error
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return -1, "", str(e)
