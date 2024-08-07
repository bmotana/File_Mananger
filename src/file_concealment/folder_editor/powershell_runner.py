from typing import Tuple
import subprocess


class PowerShellRunner:
    """A class to run PowerShell scripts."""

    def __init__(self, script_path: str):
        self.script_path = script_path

    def run_script(self) -> Tuple[str, str, int]:
        """
        Run the PowerShell script.

        Returns:
            Tuple[str, str, int]: A tuple containing (stdout, stderr, return_code)
        """
        try:
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", self.script_path],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr, e.returncode