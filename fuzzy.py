import os
import base64
from rich.console import Console
from rich.prompt import Prompt


class Fuzzy:
    def __init__(self):
        self.console = Console()
        self.OFFSET = 10
        self.VARIABLE_NAME = "__Nl1pR2MuIkzDocKUKk5vwoLDnMKAwpDCm8K4w7zDl8K2w63Diw__w71Kw7jChxrDpMK2JTFQwqzCjCBQaDHDgGfDg29EwqHChA" * 1000

    def obfuscate(self, content):
        index = 0
        code = f'{self.VARIABLE_NAME} = ""\n'
        b64_content = base64.b64encode(content.encode()).decode()

        for _ in range(int(len(b64_content) / self.OFFSET) + 1):
            _str = ""
            for char in b64_content[index : index + self.OFFSET]:
                byte = str(hex(ord(char)))[2:]
                if len(byte) < 2:
                    byte = "0" + byte
                _str += "\\x" + str(byte)
            code += f'{self.VARIABLE_NAME} += "{_str}"\n'
            index += self.OFFSET
        code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({self.VARIABLE_NAME}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))'
        return code

    def main(self):
        self.console.print("[bold cyan]=[/]" * 60)
        self.console.print("[b]Welcome to Fuzzy Python Obfuscator![/b]")
        path = Prompt.ask("Enter path to Python script", default="default=none")

        if not os.path.exists(path):
            self.console.print("\t[-] Invalid path/file not found!")
            exit()

        if not os.path.isfile(path) or not path.endswith(".py"):
            self.console.print("\t[-] Invalid file provided! Must be a Python script.")
            exit()

        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            file_content = file.read()

        obfuscated_content = self.obfuscate(file_content)
        with open(f"{path.split('.')[0]}-fuzzy-obfuscated.py", "w") as file:
            file.write(obfuscated_content)

        self.console.print("[b]Fuzzy obfuscation successful![/b]")
        self.console.print("[bold cyan]=[/]" * 60)


if __name__ == "__main__":
    fuzzy = Fuzzy()
    fuzzy.main()
