from scripts import common as c
import pygame
from sys import version as python_version
from scripts.editor_objects.button import Button

class About:
    def __init__(self):
        self.title = c.editor_font_large.render("About", True, (250, 250, 255))
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.text = []
        text = ["CCC Version: "+c.VERSION,
                "Version release date: 2nd Sep 2022",
                "Supported project versions: "+", ".join(c.settings["supported_versions"]),
                "",
                "Python Version: "+python_version.split(" ")[0],
                "Pygame Version: "+pygame.version.ver,
                "SDL Version: "+str(pygame.get_sdl_version()),
                "",
                "Created by Smarf1. Some images fetched from Clash of Clans Wiki.",
                "",
                "This material is unofficial and is not endorsed by Supercell.",
                "For more information see Supercell's Fan Content Policy",
                "at 'www.supercell.com/fan-content-policy' or click the link below."
                ]
        for line in text:
            text_surf = c.editor_font_small.render(line,True,(150,150,155))
            self.text.append(text_surf)

        self.content_policy = Button("Supercell Fan Content Policy",width=300)
        self.project_download = Button("CCC Download Page", width=300)
        self.discord_button = Button("",width=150,file="discord")

    def render(self):
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        centre = c.width // 2 - 125

        self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15))
        y = 80
        for line in self.text:
            self.surf.blit(line, (centre - line.get_width()//2, y))
            y += 25

        self.content_policy.render(self.surf, (centre - 150, y + 50))
        self.project_download.render(self.surf, (centre - 150, y + 90))
        self.discord_button.render(self.surf,(centre-65, y+130))

        c.display.blit(self.surf, (250, 0))

    def event(self,event,pos):
        if self.discord_button.click(event,pos):
            from webbrowser import open
            open(c.DISCORD_LINK)

        if self.content_policy.click(event,pos):
            from webbrowser import open
            open("https://www.supercell.com/fan-content-policy")

        if self.project_download.click(event,pos):
            from webbrowser import open
            open("https://smarf1.itch.io/ccc")
