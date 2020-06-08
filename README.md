# Bilateral Filter
A bilateral filter is a non-linear, edge-preserving, and noise-reducing smoothing filter for images. It replaces the intensity of each pixel with a weighted average of intensity values from nearby pixels. This weight can be based on a Gaussian distribution. Crucially, the weights depend not only on Euclidean distance of pixels, but also on the radiometric differences (e.g., range differences, such as color intensity, depth distance, etc.). This preserves sharp edges. [MIT](https://en.wikipedia.org/wiki/Bilateral_filter)

The equation used for filtering is as follows:
![Image of Yaktocat](https://wikimedia.org/api/rest_v1/media/math/render/svg/2765ae591a57896fe5e802ed797ad87a99a77887)

The Gaussian function used to make up the filters is as follows:
![Image of Yaktocat](https://wikimedia.org/api/rest_v1/media/math/render/svg/8aa9ff808602c27f1d9d63d7b2c115388a34f190)

## How to Run the Program
The program requires the user to specify only one parameter, which is the image path (there is a test image called image.jpg that is good for testing).

The user can also choose to specify the spatial variance, range variance, and mask size (all masks are of form nxn).

An example of running the program is as follows:
singularize('phenomena') # returns 'phenomenon'
```bash
python3 bilateral_filter.py image.jpg 50 25 3
```
This produces a bilateral filtered version of "image.jpg" with a spatial variance of 50, range variance of 25 using a 3x3 mask.


## Useful Tips
The filter is built in python and requires python3 to run.

The filter runs rather slow, so I recommend using a low-res image such as image.jpg provides in the main directory.

Using large masks will increase the time it takes for the algorithm to run, so I suggest picking something small like 3 or 5.