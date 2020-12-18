# -*- coding: utf-8 -*- 
# @Time : 2020/12/18 4:21 下午 
# @Author : yl
import cv2
from utils.mouse_func import *
import numpy as np
import os
import os.path as osp


class Labeler(object):
    def __init__(self,
                 img_dir,
                 mask_out,
                 img_window='image',
                 mask_window='mask'):
        self.img_dir = img_dir
        self.mask_out = mask_out
        self.img_window = img_window
        self.mask_window = mask_window

    def buildWindow(self):
        namedWindow(self.img_window)
        namedWindow(self.mask_window)

    def selectColor(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            

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

        cv2.setMouseCallback(self.img_window, self.selectColor)
