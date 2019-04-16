import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def total_pix(image):
    size = image.shape[0] * image.shape[1]
    return size


def histogramify(image):
    grayscale_array = []
    for w in range(0, image.size[0]):
        for h in range(0, image.size[1]):
            intensity = image.getpixel((w, h))
            grayscale_array.append(intensity)
    bins = range(0, 256)
    # img_histogram = np.histogram(grayscale_array, bins)
    grayscale_array = np.array(grayscale_array)
    plt.hist(grayscale_array, bins, normed=0, facecolor="blue", edgecolor="blue", alpha=0.7)
    plt.title("Grayscale")
    plt.show()


def get_best_threshold(img_array):
    height = img_array.shape[0]
    width = img_array.shape[1]
    count_pixel = np.zeros(256)

    for i in range(height):
        for j in range(width):
            count_pixel[int(img_array[i][j])] += 1

    max_variance = 0.0
    best_thresold = 0
    for thresold in range(256):
        n0 = count_pixel[:thresold].sum()
        n1 = count_pixel[thresold:].sum()
        w0 = n0 / (height * width)
        w1 = n1 / (height * width)
        u0 = 0.0
        u1 = 0.0

        for i in range(thresold):
            u0 += i * count_pixel[i]
        for j in range(thresold, 256):
            u1 += j * count_pixel[j]

        u = u0 * w0 + u1 * w1
        tmp_var = w0 * np.power((u - u0), 2) + w1 * np.power((u - u1), 2)

        if tmp_var > max_variance:
            best_thresold = thresold
            max_variance = tmp_var

    return best_thresold


def my_otsu(image, threshold):
    image = np.transpose(np.asarray(image))
    total = total_pix(image)
    bin_image = image < threshold
    sumT = np.sum(image)
    w0 = np.sum(bin_image)
    sum0 = np.sum(bin_image * image)
    w1 = total - w0
    if w1 == 0:
        return 0
    sum1 = sumT - sum0
    mean0 = sum0 / (w0 * 1.0)
    mean1 = sum1 / (w1 * 1.0)
    varBetween = w0 / (total * 1.0) * w1 / (total * 1.0) * (mean0 - mean1) * (
            mean0 - mean1)  # formulation form https://en.wikipedia.org/wiki/Otsu%27s_method
    # print "varBetween is:", varBetween
    return varBetween


#print(my_otsu(img_array, 116))


