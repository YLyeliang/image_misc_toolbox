# -*- coding: utf-8 -*- 
# @Time : 2020/12/18 4:12 下午 
# @Author : yl
import cv2


def namedWindow(window_name, flags=cv2.WINDOW_NORMAL):
    cv2.namedWindow(window_name, flags=flags)


def setMouseCallback(window_name, onMouse):
    cv2.setMouseCallback(window_name, onMouse)


def selectColor(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
