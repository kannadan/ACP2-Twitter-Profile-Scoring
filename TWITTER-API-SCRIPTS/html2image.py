import io
import time
import os.path
import JSInjection
from PIL import Image
from selenium import webdriver


class Html2Image:
    def __init__(self, url, jscode=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.set_window_size(1920, 1080)
        self.browser.get(url)
        self.jscode = jscode
        self.image = None

    def get_image(self):
        if self.jscode is not None and isinstance(self.jscode, JSInjection.JSCode) and self.jscode.get_jscode != "":
            # print(self.jsCode.getJSCode())
            self.browser.execute_script(self.jscode.get_jscode())
            for i in range(30):
                # print(self.browser.title)
                if self.jscode.finished_sign in self.browser.title:
                    break
                time.sleep(10)

        self.image = self.browser.get_screenshot_as_png()
        # self.browser.close()
        return self.image

    def get_element_image(self, css_selector):
        if self.image is None:
            self.get_image()
        element = self.browser.find_element_by_css_selector(css_selector)
        left, top = element.location['x'], element.location['y']
        right = left + element.size['width']
        bottom = top + element.size['height']
        im = Image.open(io.BytesIO(self.image))
        im = im.crop((left, top, right, bottom))
        # im.show()
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def save_image(self, image=None, filename="result.png"):
        if image is None:
            if self.image is None:
                image = self.get_image()
            else:
                image = self.image
        try:
            with open(filename, 'wb') as f:
                f.write(image)
        except IOError:
            return False
        finally:
            del image
        return True

    def __del__(self):
        self.browser.close()

profileimgsBase = 'profile_images'
def save_twitter_Profile_image(id = 12, username = 'jack'):
    if not id is None:
        if not username is None:
            filepath = os.path.join(profileimgsBase, str(id), 'profile.png')
            if not os.path.exists(os.path.join(profileimgsBase, str(id))):
                os.makedirs(os.path.join(profileimgsBase, str(id)))
            h2i = Html2Image("https://twitter.com/" + username, JSInjection.Scroll2Bottom())
            h2i.save_image(h2i.get_element_image(
                "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div > div > div:nth-child(2) > div > div > div:nth-child(1)"), filepath)

def save_tweet_image(user_id = 12, username = 'jack', tweetid = '1466238295914991616', filename = 'tweet_1.png'):
    if not tweetid is None:
        if not user_id is None:
            if not username is None:
                filepath = os.path.join(profileimgsBase, str(user_id), filename)
                if not os.path.exists(os.path.join(profileimgsBase, str(user_id))):
                    os.makedirs(os.path.join(profileimgsBase, str(user_id)))
                h2i = Html2Image("https://twitter.com/" + username + "/status/" + tweetid, JSInjection.Scroll2Bottom())
                try:
                    h2i.save_image(h2i.get_element_image(
                        "#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-jxzhtn.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > section > div > div > div:nth-child(1) > div > div:nth-child(1)"), filepath)
                except Exception as e:
                    print("Tweet not Existed anymore")

