import cv2 as cv
import numpy as np

ans = [[],[],[],[]]

for i in range(1, 51):
    if i < 26:
        if i < 10:
            filename = f"100_0{i}.jpg"
        else:
            filename = f"100_{i}.jpg"
    else:
        if i < 35:
            filename = f"200_0{i-25}.jpg"
        else:
            filename = f"200_{i-25}.jpg"
    img_bgr = cv.imread("tlights\\" + filename)
    img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)

    img_hsv = cv.cvtColor(img_rgb, cv.COLOR_RGB2HSV)

    colors = [[170,185],[25,35],[85,100]]
    saved_pix = [0,0,0]

    wellplate = np.copy(img_rgb)
    for i in range(3): # Red, Yellow, Green
        mask_x = np.zeros(shape=wellplate.shape[0:2], dtype="bool")               # Yellow 25:35, Green 85:100 red 170:185
        mask_y = np.zeros(shape=wellplate.shape[0:2], dtype="bool")
        x = np.where( (img_hsv[:,:,0]>colors[i][0]) & (img_hsv[:,:,0]<colors[i][1]))
        y = np.where(img_hsv[:,:,1]>150)
        mask_x[x] = 1

        masked_img = np.copy(wellplate)

        masked_img[np.logical_not(mask_x)] = 0
        mask_y[y] = 1
        masked_img[np.logical_not(mask_y)] = 0

        new_arr = masked_img[:,:,0] + masked_img[:,:,1] + masked_img[:,:,2]
        colored_pixs = np.count_nonzero(new_arr)
        saved_pix[i] = colored_pixs

    first_max = max(saved_pix)
    first_ind = saved_pix.index(first_max)
    saved_pix.remove(first_max)
    second_max = max(saved_pix)

    if second_max != 0:
        if first_max/second_max > 1.5:
            ans[first_ind].append(filename)
        else:
            ans[3].append(filename)
    elif first_max != 0:
        ans[first_ind].append(filename)
    else:
        ans[3].append(filename)

print(f"RED:{ans[0]}\nYELLOW: {ans[1]} \nGREEN: {ans[2]}") # Mistakes 100_19, 100_15, 100_25, 200_19, 200_21
