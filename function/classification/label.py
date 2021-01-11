# -*- coding: utf-8 -*- 
# @Time : 2020/12/22 3:31 下午 
# @Author : yl

import cv2
import os.path as osp
import os
from utils import namedWindow
import shutil


class Classifier(object):
    def __init__(self,
                 img_dir,
                 out_root,
                 img_suffix='.jpg',
                 img_window='image',
                 key_class=dict(n='normal', )):
        self.img_dir = img_dir
        self.out_root = out_root
        self.img_suffix = img_suffix
        self.img_window = img_window
        self.key_class = key_class

    def prepare(self):
        if not osp.exists(self.img_dir):
            raise FileExistsError(f"The path {self.img_dir} is not existed.")

        if not osp.exists(self.out_root):
            print(f"create directory {self.out_root}")
            os.makedirs(self.out_root)
        files = os.listdir(self.img_dir)
        self.file_list = [osp.join(self.img_dir, file) for file in files]

    def run(self):
        print(f'Initialize the environment.')
        self.prepare()
        namedWindow(self.img_window)
        for file in self.file_list:
            image = cv2.imread(file)
            cv2.imshow(self.img_window, image)
            while True:
                key = cv2.waitKey() & 0xff
                if key == ord(' '):
                    key2 = cv2.waitKey() & 0xff
                    if key2 in self.key_class:
                        cls_name = self.key_class[key]
                        cls_path = osp.join(self.out_root, cls_name)
                        if not osp.exists(cls_path):
                            os.makedirs(cls_path)
                        dst_file = osp.join(cls_path, osp.basename(file).split('.')[0] + self.img_suffix)
                        if self.img_suffix in osp.basename(file):
                            shutil.copy(file, dst_file)
                        else:
                            cv2.imwrite(dst_file, image)
                        break
                    else:
                        print(f'no classes bounding to key{key2}, please press space again.')
                elif key == 27:
                    break
