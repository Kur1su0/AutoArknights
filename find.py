import numpy as np
import cv2

def compare(img1,img2):
    MIN_MATCH_COUNT = 34

    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)


    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    print(len(good))

    if len(good) >= MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        matchesMask = mask.ravel().tolist()

        h, w = img1.shape

        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

        dst = cv2.perspectiveTransform(pts, M)

    else:      
        matchesMask = None
        dst = None

    return dst

if __name__ == '__main__':

    src = 'finish_temp.png'
    #dest = 'chara/ct1.png'
    dest = 'finish/1.png'

    img1 = cv2.imread(src, 0)
    img2 = cv2.imread(dest, 0)
    color_img = cv2.imread(dest)
    color_img = cv2.cvtColor(color_img, cv2.COLOR_RGB2BGR)

    pts = compare(img1, img2)

