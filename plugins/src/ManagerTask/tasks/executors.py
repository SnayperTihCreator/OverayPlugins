import subprocess
import io

from attrs import define, field

from .baseExecutor import BaseExecutor


@define
class RunCommandExecutor(BaseExecutor):
    command: str = field(default="")
    
    def execute(self, *args, **kwargs) -> bool:
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = subprocess.run(self.command, stdout=stdout, stderr=stderr)
        if code.returncode != 0:
            raise RuntimeError(stderr.getvalue())
        self.result_execute = stdout.getvalue()
        return True
    
    @classmethod
    def restore(cls, data):
        return cls(None, data["command"])
    
    def save(self):
        return {
            "command": self.command
        }


__all__ = ["RunCommandExecutor"]
