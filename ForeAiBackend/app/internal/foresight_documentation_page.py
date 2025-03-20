class ForesightDoc:
    def __init__(self, documentation_text: str, platform_version: str, documentation_part: str):
        self.documentation_text = documentation_text
        self.platform_version = platform_version
        self.documentation_part = documentation_part
    def __str__(self):
        return (f'Текст страницы: {self.documentation_text}\n'
                f'Версия платформы: {self.platform_version}\n'
                f'Название раздела: {self.documentation_part}\n')
