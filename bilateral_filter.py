import numpy as np
import random
import cv2
import sys

# Gaussian function used for calculating the filterered pixels.
def gaussian(x, x_i, variance):
  x = np.round(np.linalg.norm(x-x_i), 2)
  return (1/(variance * (2 * np.pi))) * np.exp(-0.5 * (x**2/variance**2))

# calculations of bilateral filter.
def bilateral_filter(a, mask_size, variance_r, variance_s, cp_index):
  # Initialization variables.
  numerator = 0
  denominator = 0
  filtered_img = np.zeros(a.shape)

  # Loops i and j must take into considertaion the mask size
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

  # Final image needs to have uint types for pixel values.
  filtered_img_uint = filtered_img.astype(np.uint8)

  return filtered_img_uint


# The user must specify the image.  If not the program exits and gives error message.
try:
  img = cv2.imread(sys.argv[1])
except:
  print("Please restart the program and enter an image as an arguement.")
  exit() 

print("You can specify values for variance and mask size (e.g. python3 image spatial_variance range_variance mask_size)")


# Convert the original image to grayscale and all the pixel itensities to floats.
original = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
a = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
a = a.astype('float64')


# Mask size is at default 3x3 unless the user specifies.
try:
  mask_size = int(sys.argv[4])
except:
  mask_size = 3

cp_index = int(np.ceil(mask_size/2)) - 1


# Varaiance types can be set by the user, but if not they have decent defaults.
try:
  variance_s = int(sys.argv[2])
except:
  variance_s = 50

try:
  variance_r = int(sys.argv[3])
except:
  variance_r = 25

f_uint = bilateral_filter(a, mask_size, variance_r, variance_s, cp_index)

print("Image filtered successfully")
print("Mask Size: " + str(mask_size))
print("Spatial Variance: " + str(variance_s))
print("Range Variance: " + str(variance_r))
print("(close all the image windows to continue)")

cv2.imshow("original", original)
cv2.imshow("filtered", f_uint)

cv2.waitKey(0)
cv2.destroyAllWindows()