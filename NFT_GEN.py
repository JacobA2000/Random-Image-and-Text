import bs4
import requests
import random
import os
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps

save_path = f"{os.path.dirname(os.path.abspath(__file__))}\\images"

# GET RANDOM IMAGES OF VEGETABLES FROM GOOGLE IMAGE SEARCH VIA BEAUTIFUL SOUP
def get_image():
    image_picked = False
    url = "https://www.google.com/search?q=vegetable%20single&tbm=isch&hl=en&tbs=ic:trans&sa=X&ved=0CAMQpwVqFwoTCJD6ut_Z1fUCFQAAAAAdAAAAABAC&biw=1903&bih=933"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')

    while image_picked == False:
        image_url = random.choice(images).get('src')
        if ("https://" in image_url) or ("http://" in image_url):
            return image_url

#save the image to the current directory
def save_image(image_url, image_index):
    global save_path
    response = requests.get(image_url)
    image_name = str(image_index) + ".jpg"

    path = os.path.join(save_path, image_name)

    with open(path, 'wb') as f:
        f.write(response.content)

# add random word to image using pillow
def add_border_and_word(image_name, word):
    global save_path
    path = os.path.join(save_path, image_name)
    old_im = Image.open(path)
    old_size = old_im.size

    new_size = (400, 400)
    new_im = Image.new("RGB", new_size)   ## luckily, this is already black!
    new_im.paste(
        old_im, (
            (new_size[0]-old_size[0])//2,
            (new_size[1]-old_size[1])//2
        )
    )

    draw = ImageDraw.Draw(new_im)
    # draw the text in the bottom center of the image
    font = ImageFont.truetype("impact.ttf", new_im.size[1]//10)
    draw.text((new_im.size[0]/2, new_im.size[1]-50), word, (255, 255, 255), font=font, anchor="ms")
    new_im.save(path)

def add_border(input_image, border, colour):
    global save_path
    path = os.path.join(save_path, input_image)

    img = Image.open(path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=border, fill=colour)
    else:
        raise RuntimeError('Border is not an integer or tuple!')

    bimg.save(path)

def add_word(input_image):
    global save_path
    path = os.path.join(save_path, input_image)

    img = Image.open(path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", img.size[1]//10)
    draw.text((img.size[0]/2, img.size[1]-25), get_word(), (255, 255, 255), font=font, anchor="ms")

    img.save(path)

# get a random word from the vegetables.json file
def get_word():
    with open("json\\vegetables.json") as f:
        vegetables_file = json.load(f)
        vegetables_list = vegetables_file["vegetables"]
    return random.choice(vegetables_list)


if __name__ == '__main__':
    for i in range(20):
        image_url = get_image()
        save_image(image_url, i)
        add_border(str(i) + ".jpg", (50, 50), "black")
        add_word(str(i) + ".jpg")

        #add_border_and_word(str(i) + ".jpg", get_word())