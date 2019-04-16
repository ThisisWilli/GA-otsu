import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from GeneticAlgorithm import GeneticAlgorithm
import otsu


def threshold(t, image):
    image_tmp = np.asarray(image)
    intensity_array = list(np.where(image_tmp < t, 0, 255).reshape(-1))
    image.putdata(intensity_array)
    #image.show()
    image.save('image/output.jpg')


def main():
    thresholds, fitnesss = [], []
    im = Image.open('image/women.jpeg')
    im.load()
    #im.show()
    im_gray = im.convert('L')
    # im_gray.show()
    # im_gray.save('image/woman_gray.jpg')
    g = GeneticAlgorithm(im_gray, 8, 100)
    # print(otsu.get_best_threshold(np.array(im_gray)))
    best_threshold, thresholds, fitnesss, cur_iteration = g.get_threshold()
    # otsu.histogramify(im_gray)#画出灰度直方图
    threshold(best_threshold, im_gray)
    plt.title("threshold(N={} iteration={})".format(g.N, g.max_interation), fontsize=12)
    plt.plot(thresholds, linewidth=1)
    plt.show()
    plt.title("fitness N=({} iteration={})".format(g.N, g.max_interation), fontsize=12)
    plt.plot(fitnesss, linewidth=1)
    plt.show()
    # print(fitnesss)


if __name__ == '__main__':
    main()
