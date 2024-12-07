class HelpMenu:
    def __init__(self, file: str) -> None:
        self.filename = file
        self.command_dict = {}
        self.command_info = ""

    def add(
        self,
        command: str,
        parameters: str = None,
        description: str = None,
        example: str = None,
        note: str = None,
    ):
        self.command_dict[command] = {
            "command": command,
            "parameters": parameters,
            "description": description,
            "example": example,
            "note": note,
        }
        return self

    def info(self, command_info: str):
        self.command_info = command_info
        return self

    def get_menu(self) -> str:
        result = f"**Plugin File:** `{self.filename}`"
        if self.command_info:
            result += f"\n**Plugin Info:** __{self.command_info}__"
        result += "\n\n"
        for command in self.command_dict.values():
            result += f"**Command:** `/{command['command']}"
            if command["parameters"]:
                result += f" {command['parameters']}`\n"
            else:
                result += "`\n"
            if command["description"]:
                result += f"**Description:** __{command['description']}__\n"
            if command["example"]:
                result += f"**Example:** `/{command['example']}`\n"
            if command["note"]:
                result += f"**Note:** __{command['note']}__\n"

            result += "\n"

        return result

    def done(self) -> None:
        # Placeholder for future functionality
        pass


class BotHelp:
    def __init__(self, file: str) -> None:
        self.category = file
        self.command_dict = {}
        self.command_info = ""

    def add(self, command: str, description: str):
        self.command_dict[command] = {"command": command, "description": description}
        return self

    def info(self, command_info: str):
        self.command_info = command_info
        return self

    def get_menu(self) -> str:
        result = f"**Plugin Category:** `{self.category}`"
        if self.command_info:
            result += f"\n**Plugin Info:** __{self.command_info}__"
        result += "\n\n"
        for command in self.command_dict.values():
            result += f"**Command:** `/{command['command']}`\n"
            if command["description"]:
                result += f"**Description:** __{command['description']}__\n"

            result += "\n"

        return result

    def done(self) -> None:
        # Placeholder for future functionality
        pass


# Example usage of HelpMenu class
"""
HelpMenu("example").add(
    "example", "<text>", "description of command", "example of command", "note of command"
).info(
    "information of plugin"
).done()
"""

# Example usage of BotHelp class
"""
BotHelp("example").add(
    "example", "description of command"
).info(
    "information of category"
).done()
"""
