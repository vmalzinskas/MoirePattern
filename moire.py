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
                rotated_image[i + int(ii*break_width): i + int(ii*break_width + band_width)] = [0, 0, 0, 0]
            ic(r"Output\pattern" + str(ii) + "png")
            cv.imwrite(r"Output\pattern_" + str(ii) + ".png", rotated_image)
            ic(rotated_image)
            cv.imshow("ss", rotated_image)
            cv.waitKey(0)
            cv.destroyAllWindows()


    def overlay_images(self, array_images, width, height, frames):  # image.shape[0] = width, image.shape[1] = height
        overlayed_image = np.zeros([int(height), int(width/frames), 4], dtype=np.uint8)
        # ic(overlayed_image.shape)
        # self.show_image(overlayed_image)
        image = array_images[0]
        # ic(image.shape[0])
        # self.show_image(image)
        M = int(height)
        N = int(width / frames)
        tiles = [image[x:x + M, y:y + N] for x in range(0, image.shape[0], M) for y in range(0, image.shape[1], N)]
        for tile in tiles:
            # self.show_image(tile)
            # ic(image.shape)
            # for i in range(0, len(image)):
            #     row = image[i]
            #     for ii in range(0, len(row)):
            #         col = row[ii]
            #         if col[3] != 0:
            #             # ic(col)
            #             overlayed_image[ii][i] = col

            for i in range(0, tile.shape[0]):
                for ii in range(0, tile.shape[1]):
                    # ic(tile[i][ii][3])
                    if tile[i][ii][3] != 0:
                        overlayed_image[i][ii] = tile[i][ii]
                        # overlayed_image[i, ii] = col
        # self.show_image(overlayed_image)
        self.save_image(r"Output\overlayed.png", overlayed_image)


    def show_image(self, image):
        cv.imshow("image", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def save_image(self, name, file):
        cv.imwrite(name, file)

    @staticmethod
    def convert_cm_to_pxl(cm):
        return cm / 0.02645

    @staticmethod
    def convert_pxl_to_cm(pxl):
        return pxl * 0.02645



if __name__ == "__main__":

    # mask = Moire(width=20, height=29, cm=True)
    # mask.genertate_mask(4, 0.5, True)
    # # mask.show_mask()
    # mask.save_mask(r"Output\mask.png")

    image = cv.imread(r"Images\blinkingIcon.png", cv.IMREAD_UNCHANGED)  # Sprite sheets work just like arrays it seems
    # ic(image)
    img_arr = [image, image, image, image]
    # cv.imshow("ss", img_arr[0])
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    animation = Moire_animation()
    animation.cut_frames(4, 0.5, True, img_arr)


    a = cv.imread(r"Output\pattern_0.png", cv.IMREAD_UNCHANGED)
    b = cv.imread(r"Output\pattern_1.png", cv.IMREAD_UNCHANGED)
    c = cv.imread(r"Output\pattern_2.png", cv.IMREAD_UNCHANGED)
    d = cv.imread(r"Output\pattern_3.png", cv.IMREAD_UNCHANGED)

    arrays = [a, b, c, d]
    animation.overlay_images(arrays, 4536, 756, 6)

