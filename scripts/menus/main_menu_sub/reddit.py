from scripts import common as c
import pygame
import requests
import io
from datetime import datetime
from random import randint

from _thread import start_new_thread
from scripts.utility.size_element import size_element
from scripts.utility.scale_image import scale_image
from scripts.editor_objects.scrollbar import Scrollbar


def get_ending(n):
    # Get 'th', 'nd', 'st' etc from date number
    output = "th"
    if n == 1:
        output = "st"
    elif n == 2:
        output = "nd"
    elif n == 3:
        output = "rd"
    return output


class Reddit:
    def __init__(self):
        self.title = c.editor_font_large.render("Reddit", True, (250, 250, 255))
        self.loading_text = c.editor_font.render("Loading posts, please wait...", True, (150, 150, 155))
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        self.create_template_images()
        self.kill_thread = False
        start_new_thread(self.get_reddit_posts, ())
        self.posts, self.post_ids = [],[]
        self.scrollbar = Scrollbar(height=c.height - 20)

    def __del__(self):
        self.kill_thread = True

    def create_template_images(self):
        self.box = size_element('assets/editor_gui/main_menu/news.png', (c.width - 325, 200), (10, 10, 10, 10))
        self.cutout = pygame.image.load('assets/editor_gui/main_menu/news_cutout.png').convert_alpha()
        self.remove = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.remove.fill((255, 255, 255, 255))
        fade = pygame.image.load('assets/editor_gui/gradient.png').convert_alpha()
        fade = pygame.transform.scale(fade, (30, 200))
        self.fade = pygame.transform.flip(fade, True, False)

    def redraw_posts(self):
        self.create_template_images()
        for num, post in enumerate(self.post_data):
            self.render_post(post[0], post[1], post[2], post[3], replace=num)

    def get_reddit_posts(self):
        self.post_ids = []
        self.posts = []
        self.post_data = []
        # [id, title, author, date, image]

        try:
            from psaw import PushshiftAPI
            api = PushshiftAPI()
            submissions = api.search_submissions(subreddit='ClashOfClans', title='Concept|Concepts',
                                                 limit=60, sort_type="created_utc", sort="desc")
        except UserWarning:
            print("Reddit PushShift User Warning (probably due to no internet)")
            self.loading_text = c.editor_font.render("Couldn't connect.", True, (255, 150, 150))
            return None

        num = 0
        # https://github.com/pushshift/api
        for submission in submissions:

            if self.kill_thread:
                break
            if hasattr(submission, "media_metadata"):
                date_org = datetime.fromtimestamp(submission.created_utc)
                ending = get_ending(date_org.day)
                date = date_org.strftime("%d{th} %b %Y")
                date = date.replace("{th}", ending)

                image_item = list(submission.media_metadata.values())[-1]
                image_url = image_item['s']['u']
                # Some strange encoding stuff
                # https://old.reddit.com/r/redditdev/comments/9ncg2r/deleted_by_user/
                image_url = image_url.replace("&amp;", "&")
                self.post_data.append((image_url, submission.title, date, submission.author))
                self.render_post(image_url, submission.title, date, submission.author)

                # Save surface
                self.post_ids.append(submission.id)
                num += 1

    def render_post(self, image_url, title, date, author, replace=None):

        surf = self.box.copy()

        response = requests.get(image_url)
        img = pygame.Surface((200, 200), pygame.SRCALPHA)
        img2 = io.BytesIO(response.content)
        img2 = pygame.image.load(img2).convert_alpha()
        scale = img2.get_height() / 200
        img2 = pygame.transform.smoothscale(img2, (img2.get_width() / scale, 200))
        img.blit(img2, (100 - img2.get_width() // 2, 0))
        surf.blit(self.remove, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        img.blit(self.cutout, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        surf.blit(img, (0, 0))
        surf.blit(self.fade, (200, 0))
        text_x = 215

        max_width = c.width - 325 - text_x - 20
        if c.editor_font.size(title)[0] > max_width:
            text = title
            text_index = 0
            need_more_text = True
            text_y = 10
            while need_more_text:
                test_index = 0
                # Find the max number of words that fit on the line
                while need_more_text:  # Loop through each word, break when it's too long
                    last_word_index = test_index
                    # Find the next space
                    while True:
                        test_index += 1
                        # Stop finding lines if we're at the end of the text
                        if test_index > len(text) - 1:
                            need_more_text = False
                            break
                        # We've found a word!
                        if text[test_index] == " ":
                            break

                    # Remove the space at the start of the line

                    if c.editor_font.size(text[text_index:test_index])[0] > max_width:
                        test_index = last_word_index
                        if not need_more_text:
                            need_more_text = True
                        break

                line = text[text_index:test_index]
                if len(line) > 0:
                    if line[0] == " ":
                        line = line[1:]
                text_surf = c.editor_font.render(line, True, (255, 255, 255))
                surf.blit(text_surf, (text_x + 10, text_y))
                text_index = test_index
                text_y += 30
                if text_y > 100: # 4 lines max
                    need_more_text = False
                    text_surf = c.editor_font.render("...", True, (255, 255, 255))
                    surf.blit(text_surf, (text_x + 10, text_y))
        else:
            title_surf = c.editor_font.render(title, True, (255, 255, 255))
            surf.blit(title_surf, (text_x + 10, 10))

        author_surf = c.editor_font_small.render(author, True, (150, 150, 155))
        surf.blit(author_surf, (text_x + 10, 170))
        date_surf = c.editor_font_small.render(date, True, (150, 150, 155))
        surf.blit(date_surf, (c.width - 335 - date_surf.get_width(), 170))
        if replace is None:
            self.posts.append(surf)
        else:
            self.posts[replace] = surf

    def render(self):
        self.surf = pygame.Surface((c.width - 250, c.height), pygame.SRCALPHA)
        centre = c.width // 2 - 125

        self.surf.blit(self.title, (centre - self.title.get_width() // 2, 15-self.scrollbar.scroll))
        if len(self.posts) == 0:
            self.surf.blit(self.loading_text, (centre - self.loading_text.get_width() // 2, 70 - self.scrollbar.scroll))
        y = 70-self.scrollbar.scroll
        for post in self.posts:
            self.surf.blit(post, (25, y))
            y += 225

        self.scrollbar.set_height(c.height-20,y+self.scrollbar.scroll)

        self.scrollbar.render(self.surf,(c.width-275,10))

        c.display.blit(self.surf, (250, 0))

    def event(self, event, pos):
        if event.type == pygame.VIDEORESIZE:
            start_new_thread(self.redraw_posts, ())
        self.scrollbar.event(event,pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                y = 70 - self.scrollbar.scroll
                for id in self.post_ids:
                    rect = pygame.Rect(25,y,c.width-325,200)
                    if rect.collidepoint(pos):
                        import webbrowser
                        webbrowser.open('https://reddit.com/r/ClashOfClans/comments/'+id)
                    y += 225
