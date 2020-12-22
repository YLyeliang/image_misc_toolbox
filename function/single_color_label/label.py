# -*- coding: utf-8 -*- 
# @Time : 2020/12/18 4:21 下午 
# @Author : yl
import cv2
from utils.mouse_func import *
import numpy as np
import os
import os.path as osp
import shutil


class Labeler(object):
    def __init__(self,
                 img_dir,
                 img_out,
                 mask_out,
                 img_suffix='.jpg',
                 mask_suffix='.png',
                 img_window='image',
                 mask_window='mask'):
        self.img_dir = img_dir
        self.img_out = img_out
        self.mask_out = mask_out
        self.img_suffix = img_suffix
        self.mask_suffix = mask_suffix
        self.img_window = img_window
        self.mask_window = mask_window
        self.radius = 5

    def buildWindow(self):
        namedWindow(self.img_window)
        namedWindow(self.mask_window)

    def change_radius(self, x):
        self.radius = x

    def selectColor(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.val = self.img[y, x]
            indices = self.img[:, :, ] == self.val
            indices = np.sum(indices, axis=2)
            indices = np.where(indices == 3)
            self.mask[indices] = 255

    def removeRegion(self, event, x, y, flags, param):
        if event == cv2.EVENT_RBUTTONDOWN:
            drawCircle(self.mask, (x, y), self.radius, color=0, thick=-1)

    def prepare(self):
        """
        check the path, create necessary path.
        Read images as list
        Returns:

        """
        if not osp.exists(self.img_dir):
            raise FileExistsError(f"Path {self.img_dir} is not found.")
        if not osp.exists(self.mask_out):
            os.makedirs(self.mask_out)
        file_list = os.listdir(self.img_dir)
        self.file_list = [osp.join(self.img_dir, file) for file in file_list]

    def run(self):
        self.prepare()
        self.buildWindow()
        for file in self.file_list:
            self.img = cv2.imread(file)
            self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            setMouseCallback(self.img_window, self.selectColor)
            setMouseCallback(self.mask_window, self.removeRegion)
            createTrackbar('radius', self.mask_window, self.change_radius, 5, 50)
            while True:
                cv2.imshow(self.img_window, self.img)
                cv2.imshow(self.mask_window, self.mask)
                key = cv2.waitKey(1)
                if key == ord('s'):  # preserve the result.
                    seg_map = np.where(self.mask == 255, 1, 0)
                    if self.img_suffix in osp.basename(file):
                        shutil.copy(file, osp.join(self.img_out, osp.basename(file)))
                    else:
                        cv2.imwrite(osp.join(self.img_out, osp.basename(file).split('.')[0] + self.img_suffix),
                                    self.img)
                    cv2.imwrite(
                        osp.join(self.mask_out, osp.basename(file).split('.')[0] + self.mask_suffix), seg_map)
                    break
                elif key == ord('d'):  # reset mask to zero
                    self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
                elif key == ord('n'):  # next image
                    break


root = "/Users/fiberhome/Downloads/paint_data/image"
out = "/Users/fiberhome/Downloads/paint_data/label_debug"
labelr = Labeler(root, root, out)
labelr.run()
