import numpy as np
import random
import cv2
from skimage.util import random_noise

# p is center of the mask
# q is a point in S
# variance is a constant value
def gaussian(x, x_i, variance):
    x = np.round(np.linalg.norm(x-x_i), 2)
    return (1/(variance * (2 * np.pi))) * np.exp(-0.5 * (x**2/variance**2))

def sp_noise(image,prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

img = cv2.imread("image2.jpg")
original = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
a = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# a = sp_noise(a, 0.05)

a = a.astype('float64')

mask_size = 3
cp_index = int(np.ceil(mask_size/2)) - 1     # 1

variance_s = 50
variance_r = 25

numerator = 0
denominator = 0
filtered_img = np.zeros(a.shape)

# 5->300-5
for i in range(cp_index, a.shape[0]-cp_index):
    for j in range(cp_index, a.shape[1]-cp_index):
        x = np.array([i, j])
        for k in range(i-cp_index, i-cp_index+mask_size):
            for l in range(j-cp_index, j-cp_index+mask_size):
                x_i = np.array([k,l])
                if np.array_equal(x, x_i) == False:
                    numerator += a[k,l] * gaussian(a[k, l], a[i, j], variance_r) * gaussian(x_i, x, variance_s)
                    denominator += gaussian(a[k, l], a[i, j], variance_r) * gaussian(x_i, x, variance_s)
        filtered_img[i,j] = numerator/denominator
        numerator = 0
        denominator = 0
    print(i)


filtered_img_uint = filtered_img.astype(np.uint8)

cv2.imshow("original", original)
cv2.imshow("filtered", filtered_img_uint)


cv2.waitKey(0)
cv2.destroyAllWindows()