import random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pathlib import Path
from rembg import remove
import io


#Создание фона



# Фильтры
def add_filter(image):
    im_bg = remove(image)
    im_bg.thumbnail((300, 300))
    enhancer = ImageEnhance.Contrast(im_bg)
    contrast_image = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Sharpness(contrast_image)
    sharp_image = enhancer.enhance(2.0)
    return sharp_image

# Пикселизатор
def pixelated(image):
    width, height = image.size
    block_size = 16
    width = (width // block_size) * block_size
    height = (height // block_size) * block_size
    image = image.resize((width, height))
    pixelated = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(pixelated)

    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            # Получаем цвет пикселя в блоке
            r, g, b = image.getpixel((x, y))

            # Рисуем квадратный блок с цветом пикселя
            draw.rectangle((x, y, x + block_size, y + block_size), fill=(r, g, b))
    return pixelated

# Форматирование в RGB
def check_RGB(all_spisok, spisok_for_random):
    for index, item in enumerate(all_spisok):
        input_path = Path(item)
        image = Image.open(input_path)
        if image.mode == 'P':
            image = image.convert('RGB')
        if image.mode == 'RGBA':
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3])
            image = rgb_image
        spisok_for_random.append(image)
    return spisok_for_random



# Добавление светильника
def add_ligher(pic):
    list_of_lighters = ['*.png', '*.jpg', '*jpeg']
    all_lighers = []
    lighters = []
    for lighter in list_of_lighters:
        all_lighers.extend(Path('lamps').glob(lighter))

    lighters = check_RGB(all_lighers, lighters)

    im = random.choice(lighters)
    im_bg = remove(im)
    if im_bg.size == (1280,960):
        im_bg.thumbnail((300,300))
        pic.paste(im_bg, (1450, 170), im_bg)
    else:
        im_bg.thumbnail((200,200))
        pic.paste(im_bg, (1500, 170), im_bg)

# Добавление цепи
def add_chain(pic):
    im1 = Image.open('chain.jpg')
    im1_bg = remove(im1)
    im1_new = im1_bg.resize((200,200))
    pic.paste(im1_new, (1500,0), im1_new)

# Добавление эмодзи
def add_emoji(pic):
    list_of_emojies = ['*.png', '*.jpg', '*jpeg']
    all_emojies = []
    emojies = []
    for emoji in list_of_emojies:
        all_emojies.extend(Path('Emojies').glob(emoji))

    emojies = check_RGB(all_emojies, emojies)

    a = random.choice(emojies)

    pixelated_image = pixelated(a)

    filtered = add_filter(pixelated_image)

    pic.paste(filtered, (100,100), filtered)

# Добавление поезда
def add_train(pic):
    im = Image.open('train.png')
    im_bg = remove(im)
    pic.paste(im_bg, (1500,700), im_bg)

# Добавление торта
def add_cake(pic):
    list_of_cakes = ['*.png', '*.jpg', '*jpeg']
    all_cakes = []
    images = []
    for cake in list_of_cakes:
        all_cakes.extend(Path('Cakes').glob(cake))

    images = check_RGB(all_cakes, images)

    b = random.choice(images)

    pixelated_image = pixelated(b)

    filtered = add_filter(pixelated_image)

    pic.paste(filtered, (200,700), filtered)

# Добавление текста
def add_text(name, lastname, group, pic):
    W = 1920
    H = 1080
    #Добавление текста ВИШ
    size1 = 30
    font = ImageFont.truetype('Minecraftia-Regular.ttf', size=size1)
    text1 = 'Высшая инженерная школа РУТ (МИИТ)'
    draw_text1 = ImageDraw.Draw(pic)
    w, h = font.getbbox(text1)[2], font.getbbox(text1)[3]
    draw_text1.text(((W-w)/2, 0), text1,font=font)

    #Текст поздравления
    size2 = 90
    font2 = ImageFont.truetype('vcrosdmonorusbyd.ttf', size=size2)
    text2 = 'С Днём Рождения,'
    draw_text2 = ImageDraw.Draw(pic)
    w2, h2 = font2.getbbox(text2)[2], font2.getbbox(text2)[3]
    draw_text2.text(((W-w2)/2+15, (H-h2)/2-100), text2,font=font2)

    #Именинник
    text3 = lastname+name + '!'
    draw_text3 = ImageDraw.Draw(pic)
    w3, h3 = font2.getbbox(text3)[2], font2.getbbox(text3)[3]
    draw_text3.text(((W-w3)/2+15, (H-h3)/2), text3, font=font2)

    #Группа
    size3 = 40
    text4 = group
    font3 = ImageFont.truetype('vcrosdmonorusbyd.ttf' , size=size3)
    draw_text4 = ImageDraw.Draw(pic)
    w4, h4 = font3.getbbox(text4)[2], font3.getbbox(text4)[3]
    draw_text4.text(((W-w4)/2+15,(H-h4)/2+80), text4, font=font3)






def createImage(name, lastname, group):
    picture = Image.open('Фон.png')
    add_ligher(picture)
    add_chain(picture)
    add_emoji(picture)
    add_train(picture)
    add_cake(picture)
    add_text(name, lastname, group, picture)
    bytepic = io.BytesIO()
    picture.save(bytepic, format="PNG")
    bytepic = bytepic.getvalue()
    return bytepic




#picture.save('Шаблон.png')