import cv2 as cv
import numpy as np
from icecream import ic
import math
from sklearn.cluster import MiniBatchKMeans
import numpy as np



class Moire:


    def __init__(self, width, height, cm):  # in pixels
        if cm:
            self.cm = True
            self.width = self.convert_cm_to_pxl(width)
            self.height = self.convert_cm_to_pxl(height)
        else:
            self.cm = False
            self.width = width
            self.height = height
        self.moire_mask = np.ndarray


    def genertate_mask(self, number_of_frames, mask_bands_width, cm):
        if cm:
            band_width = self.convert_cm_to_pxl(mask_bands_width)
        else:
            band_width = mask_bands_width

        break_width = band_width / (number_of_frames - 1)

        # ic(band_width)
        # ic(break_width)
        self.moire_mask = np.zeros([int(self.height), int(self.width), 4], dtype=np.uint8)  # The number 4 is channels
        # ic(self.moire_mask)
        for i in range(0, self.moire_mask.shape[0]-int(break_width), int(band_width + break_width)):
            self.moire_mask[i : i + int(band_width)] = [0, 0, 0, 255]
            self.moire_mask[i + int(band_width): i + int(band_width + break_width)] = [255, 255, 255, 0]

    def show_mask(self):
        cv.imshow("Display", self.moire_mask)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def save_mask(self, name):
        cv.imwrite(name, self.moire_mask)

    @staticmethod
    def convert_cm_to_pxl(cm):
        return cm / 0.02645

    @staticmethod
    def convert_pxl_to_cm(pxl):
        return pxl * 0.02645



class Moire_animation:


    def cut_frames(self, number_of_frames, mask_bands_width, cm, image_array):
        if cm:
            band_width = self.convert_cm_to_pxl(mask_bands_width)
        else:
            band_width = mask_bands_width

        break_width = band_width / (number_of_frames - 1)
        for ii in range(len(image_array)):
            ic(image)
            rotated_image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)

            for i in range(0, rotated_image.shape[0]-int(break_width + ii*break_width), int(band_width + break_width)):
            # for i in range(0, 10):
            #     rotated_image[i] = [0, 0, 0]
                rotated_image[i + int(ii*break_width): i + int(ii*break_width + band_width)] = [0, 0, 0, 0]
                # self.moire_mask[i + int(band_width): i + int(band_width + break_width)] = [255, 255, 255, 0]
            ic(rotated_image)
            cv.imshow("ss", rotated_image)
            cv.waitKey(0)
            cv.destroyAllWindows()

    @staticmethod
    def convert_cm_to_pxl(cm):
        return cm / 0.02645

    @staticmethod
    def convert_pxl_to_cm(pxl):
        return pxl * 0.02645



if __name__ == "__main__":

    # mask = Moire(width=5, height=5, cm=True)
    # mask.genertate_mask(3, 0.5, True)
    # # mask.show_mask()
    # mask.save_mask(r"C:\Users\vmalzinskas\OneDrive - Optalert\Pictures\mask.png")

    image = cv.imread(r"C:\Users\vmalzinskas\OneDrive - Optalert\Pictures\mask.png", cv.IMREAD_UNCHANGED)
    # ic(image)
    img_arr = [image, image, image, image]
    # cv.imshow("ss", img_arr[0])
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    animation = Moire_animation()
    animation.cut_frames(4, 0.5, True, img_arr)

