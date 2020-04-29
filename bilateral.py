import numpy as np
import random
import cv2
from skimage.util import random_noise

# p is center of the mask
# q is a point in S
# variance is a constant value
def gaussian(p,q, variance):
    x = np.round(np.linalg.norm(p-q), 2)
    return (1/((2 * np.pi) * variance**2)) * np.exp(-0.5 * (x**2/variance**2))

def gaussian_intensity(i_p,i_q, variance):
    x = i_p- i_q
    return (1 / ((2 * np.pi) * variance ** 2)) * np.exp(-0.5 * (x ** 2 / variance ** 2))

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


img = cv2.imread("image.jpg")
a = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
a = sp_noise(a, 0.05)

b = a.size

a = a.astype('float64')

# Mask size
n = 3
n1 = int(np.ceil(n/2))
variance_s = 50
variance_r = 25

c = 0
c1 = 0
d = np.zeros(a.shape)

# 5->300-5
for i in range(n1-1,a.shape[0]-n1+1):
    for j in range(n1-1, a.shape[1]-n1+1):
        p = np.array([i,j])     # p is the center point
        for k in range(i-n1+1,i-n1+1+n):
            for l in range(j-n1+1,j-n1+1+n):
                q = np.array([k,l])
                c += gaussian(q, p, variance_s) * gaussian_intensity(a[i,j], a[k,l], variance_r) * a[i,j]
                c1 += gaussian(p, q, variance_s) * gaussian_intensity(a[i,j], a[k,l], variance_r)
        d[i,j] = c/c1
        c = 0
        c1 = 0
    print(i)


d1 = d.astype(np.uint8)

cv2.imshow("filtered", d1)


cv2.waitKey(0)
cv2.destroyAllWindows()