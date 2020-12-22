# -*- coding: utf-8 -*- 
# @Time : 2020/12/18 4:12 下午 
# @Author : yl
import cv2


def namedWindow(window_name, flags=cv2.WINDOW_NORMAL):
    cv2.namedWindow(window_name, flags=flags)


def setMouseCallback(window_name, onMouse):
    cv2.setMouseCallback(window_name, onMouse)


def drawCircle(img, center, radius, color=(0, 255, 0), thick=1):
    draw = cv2.circle(img, center, radius, color, thickness=thick)


def createTrackbar(trackbar_name, window_name, on_change, value=5, count=50):
    cv2.createTrackbar(trackbar_name, window_name, value, count, on_change)
