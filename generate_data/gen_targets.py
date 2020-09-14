from PIL import Image, ImageDraw
import random
import math
import json
import os

def draw_hole(drawer, x, y):
    hole_rad = 4
    
    x1 = x - hole_rad
    y1 = y - hole_rad
    x2 = x1 + hole_rad*2
    y2 = y1 + hole_rad*2

    drawer.ellipse((x1, y1, x2, y2), outline="white", width=2, fill='black')


def draw_target(file_name: str):
    image_size = 400
    circle_margin = 5
    circle_width = 3

    img = Image.new('RGB', (image_size, image_size), color = 'yellow')
    
    d = ImageDraw.Draw(img)

    d.ellipse((circle_margin, circle_margin, image_size-circle_margin,image_size-circle_margin), fill='black')

    c1 = image_size / 2.25 / 2
    d.ellipse((c1, c1, image_size-c1,image_size-c1), outline="yellow", width=circle_width, fill='black')

    c2 = image_size / 1.3 / 2
    d.ellipse((c2, c2, image_size-c2,image_size-c2), outline="yellow", width=circle_width, fill='black')

    c3 = image_size / 1.05 / 2
    d.ellipse((c3, c3, image_size-c3,image_size-c3), fill='red')

    score_limits = [int(image_size / 2 - c3), int(image_size / 2 - c2), int(image_size / 2 - c1), int(image_size / 2 - circle_margin)]
    scores_values= [10, 9, 5, 2]
    
    def compute_hole_score(x, y):
        center = image_size / 2
        a = center - x
        b = center - y
        dist = math.sqrt(a*a + b*b)
        for l, s in zip(score_limits, scores_values):
            if dist <= l:
                return s

        return 0

    target_score = 0
    for h in range(15):
        x = random.randint(1,400)
        y = random.randint(1,400)
        target_score = target_score + compute_hole_score(x,y)
        draw_hole(d, x, y)

    #print(target_score)
    img.save(file_name)
    return target_score


def generate_dataset(samples_count, dir):
    #generate training set
    scores = {}
    for num_hole in range(samples_count):
        file_name = "target_train_{}.png".format(num_hole)
        full_file_name = os.path.join(dir, file_name)
        score = draw_target(full_file_name)
        print("{} {}".format(file_name, score))
        scores[file_name] = score

    with open(os.path.join(dir, 'scores.json'), 'w') as outfile:
        json.dump(scores, outfile)


#generate_dataset("training_set", 10000)
#generate_dataset("test_set", 10)
#draw_target("pil_text.png")
