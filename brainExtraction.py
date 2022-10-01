import os
import cv2 as cv
import numpy as np


def reader(dir):
    os.chdir(dir)
    l = os.listdir()
    l = [i for i in l if
         i[0] == 'I' and i.split('.')[-1] == 'png' and len(i.split('_')) == 3 and i.split('.')[0].split('_')[
             2] == 'thresh']
    return l


def extraction(curr_dir, test_dir, slice_dir_i, bound_dir_i, i):
    img = cv.imread(os.path.join(test_dir, i))
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    template = cv.imread(os.path.join(curr_dir, 'template.png'), 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    y = loc[::-1][1]
    x = loc[::-1][0]
    ptx = sorted(list(set(x)))
    pty = sorted(list(set(y)))
    x_dist = ptx[1] - ptx[0]
    for i in range(1, len(ptx)):
        if ptx[i] - ptx[i - 1] != x_dist: print('error')
    y_dist = pty[1] - pty[0]
    for i in range(1, len(pty)):
        if pty[i] - pty[i - 1] != y_dist: print('error')
    counter = 1
    for pt in zip(*loc[::-1]):
        p = pt[0] + w, pt[1] + h
        crop_img = img[p[1]:p[1] + y_dist - h, p[0]:p[0] + x_dist - w]
        gray_crop = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
        if cv.countNonZero(gray_crop) != 0:
            cv.imwrite(os.path.join(slice_dir_i, 'slice_img_'+str(counter)+'.png'), crop_img)
            _, thresh = cv.threshold(gray_crop, 0, 225, cv.THRESH_BINARY)
            contours, hierarchies = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2:]
            cv.drawContours(crop_img, contours, -1, (0, 0, 255), 1)
            cv.imwrite(os.path.join(bound_dir_i, 'bound_img_'+str(counter)+'.png'), crop_img)
        counter += 1