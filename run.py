# -*- coding: utf-8 -*- 
# @Time : 2020/12/24 10:45 上午 
# @Author : yl
from function.single_color_label import Labeler

root = "/Users/fiberhome/Downloads/paint_data/image"
out = "/Users/fiberhome/Downloads/paint_data/label_debug"
labelr = Labeler(root, root, out)
labelr.run()
