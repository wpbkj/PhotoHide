# -*- coding: utf-8 -*-
#
# Copyright 2018-2022 WPBKJ Network Studio
# Author WPBKJ(www.wpbkj.com)
#
# Version 1.0.2
#
# This file is main part of WPBKJ PhotoHide.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
import os

os.environ['KIVY_IMAGE'] = 'pil,sdl2'
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import cv2
import numpy as np


def linear_add(pic1, pic2):
    out = pic1 + pic2
    out[out > 255] = 255
    return out


def divide(pic1, pic2):
    pic2 = pic2.astype(np.float)
    pic2[pic2 == 0] = 1e-10
    out = (pic1 / pic2) * 255
    out[out > 255] = 255
    return out


def inversion(pic):
    return 255 - pic


def rgb2gray(pic):
    pic_shape = pic.shape
    out = np.ones((pic_shape[0], pic_shape[1], 4)) * 255
    temp = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    out[:, :, 0] = temp
    out[:, :, 1] = temp
    out[:, :, 2] = temp
    return out.astype(np.uint8)


def get_red_channel(pic):
    return pic[:, :, 2]


def add_alpha(pic, A):
    pic[:, :, 3] = A
    return pic


def change_color_level(pic, is_light):
    light_table = [120, 120, 121, 121, 122, 122, 123, 123, 124, 124, 125, 125, 126, 126, 127, 127, 128, 128,
                129, 129, 130, 130, 131, 132, 132, 133, 133, 134, 134, 135, 135, 136, 136, 137, 137, 138,
                138, 139, 139, 140, 140, 141, 142, 142, 143, 143, 144, 144, 145, 145, 146, 146, 147, 147,
                148, 148, 149, 149, 150, 150, 151, 152, 152, 153, 153, 154, 154, 155, 155, 156, 156, 157,
                157, 158, 158, 159, 159, 160, 161, 161, 162, 162, 163, 163, 164, 164, 165, 165, 166, 166,
                167, 167, 168, 168, 169, 170, 170, 171, 171, 172, 172, 173, 173, 174, 174, 175, 175, 176,
                176, 177, 177, 178, 179, 179, 180, 180, 181, 181, 182, 182, 183, 183, 184, 184, 185, 185,
                186, 186, 187, 188, 188, 189, 189, 190, 190, 191, 191, 192, 192, 193, 193, 194, 194, 195,
                195, 196, 197, 197, 198, 198, 199, 199, 200, 200, 201, 201, 202, 202, 203, 203, 204, 205,
                205, 206, 206, 207, 207, 208, 208, 209, 209, 210, 210, 211, 211, 212, 212, 213, 214, 214,
                215, 215, 216, 216, 217, 217, 218, 218, 219, 219, 220, 220, 221, 222, 222, 223, 223, 224,
                224, 225, 225, 226, 226, 227, 227, 228, 228, 229, 229, 230, 231, 231, 232, 232, 233, 233,
                234, 234, 235, 235, 236, 236, 237, 237, 238, 239, 239, 240, 240, 241, 241, 242, 242, 243,
                243, 244, 244, 245, 245, 246, 247, 247, 248, 248, 249, 249, 250, 250, 251, 251, 252, 252,
                253, 253, 254, 255]
    dark_table = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10,
                10, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20, 21,
                22, 22, 23, 23, 24, 24, 25, 25, 26, 26, 27, 27, 28, 28, 29, 29, 30, 30, 31, 32, 32,
                33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38, 39, 39, 40, 41, 41, 42, 42, 43, 43,
                44, 44, 45, 45, 46, 46, 47, 47, 48, 48, 49, 50, 50, 51, 51, 52, 52, 53, 53, 54, 54,
                55, 55, 56, 56, 57, 57, 58, 59, 59, 60, 60, 61, 61, 62, 62, 63, 63, 64, 64, 65, 65,
                66, 66, 67, 68, 68, 69, 69, 70, 70, 71, 71, 72, 72, 73, 73, 74, 74, 75, 75, 76, 77,
                77, 78, 78, 79, 79, 80, 80, 81, 81, 82, 82, 83, 83, 84, 85, 85, 86, 86, 87, 87, 88,
                88, 89, 89, 90, 90, 91, 91, 92, 92, 93, 94, 94, 95, 95, 96, 96, 97, 97, 98, 98, 99,
                99, 100, 100, 101, 102, 102, 103, 103, 104, 104, 105, 105, 106, 106, 107, 107, 108,
                108, 109, 109, 110, 111, 111, 112, 112, 113, 113, 114, 114, 115, 115, 116, 116, 117,
                117, 118, 119, 119, 120, 120, 121, 121, 122, 122, 123, 123, 124, 124, 125, 125, 126,
                127, 127, 128, 128, 129, 129, 130, 130, 131, 131, 132, 132, 133, 133, 134, 135]

    pic_shape = pic.shape
    out = np.zeros((pic_shape[0], pic_shape[1], 4), dtype=np.uint8)
    if is_light:
        out[:, :, 0] = [[light_table[y] for y in x] for x in pic[:, :, 0]]
        out[:, :, 1] = [[light_table[y] for y in x] for x in pic[:, :, 1]]
        out[:, :, 2] = [[light_table[y] for y in x] for x in pic[:, :, 2]]
        out[:, :, 3] = pic[:, :, 3]
    else:
        out[:, :, 0] = [[dark_table[y] for y in x] for x in pic[:, :, 0]]
        out[:, :, 1] = [[dark_table[y] for y in x] for x in pic[:, :, 1]]
        out[:, :, 2] = [[dark_table[y] for y in x] for x in pic[:, :, 2]]
        out[:, :, 3] = pic[:, :, 3]
    return out


def make(file1, file2, savePath):
    surface_pic = cv2.imread(file1)
    hidden_pic = cv2.imread(file2)
    sur_shape = surface_pic.shape
    hid_shape = hidden_pic.shape
    out_shape = (min(sur_shape[1], hid_shape[1]), min(sur_shape[0], hid_shape[0]))
    surface_pic = cv2.resize(surface_pic, out_shape)
    hidden_pic = cv2.resize(hidden_pic, out_shape)

    surface_pic = rgb2gray(surface_pic)
    surface_pic = change_color_level(surface_pic, True)
    surface_pic = inversion(surface_pic)

    hidden_pic = rgb2gray(hidden_pic)
    hidden_pic = change_color_level(hidden_pic, False)

    out_pic = linear_add(surface_pic, hidden_pic)
    A = get_red_channel(out_pic)
    out_pic = divide(hidden_pic, out_pic)
    out_pic = add_alpha(out_pic, A)
    cv2.imwrite(savePath, out_pic)

def MakePhoto(top_image, bottom_image, output_image):
    try:
        make(top_image, bottom_image, output_image)
        return '构建成功,保存在'+str(output_image)
    except:
        return '构建错误,请重试'


class PhotoHideWidget(BoxLayout):
    global root
    top_image = ''
    bottom_image = ''
    output_image = ''
    output_msg = '输入后单击提交开始构建'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.UpdateAlertMsg, 0)
    def BeginMake(self):
        self.top_image = self.ids.top_image.text
        self.bottom_image = self.ids.bottom_image.text
        self.output_image = self.ids.output_image.text
        self.output_msg = MakePhoto(self.top_image, self.bottom_image, self.output_image)
        # print(self.top_image+self.bottom_image+self.output_image)

    def changeState(self):
        self.output_msg = '正在构建,请稍候'

    def UpdateAlertMsg(self, *args):
        self.ids.alert_msg.text = self.output_msg

    def ResetInput(self):
        self.ids.top_image.text = ''
        self.ids.bottom_image.text = ''
        self.ids.output_image.text = 'output.png'
        self.output_msg = '输入后单击提交开始构建'

    @staticmethod
    def openGitee():
        webbrowser.open_new_tab("https://gitee.com/wpbkj/PhotoHide/")

    @staticmethod
    def openGitHub():
        webbrowser.open_new_tab("https://github.com/wpbkj/PhotoHide/")

    Builder.load_string('''
<DefaultTextInput@TextInput>:
    background_color: 2, 2, 2, 1
    size_hint: (.7, .35)
    pos_hint: {'center_y':.5}
    multiline: False
    font_name: 'data/fonts/Leefont.ttf'
<DefaultLabel@Label>:
    font_size: 15
    color: (0, 0, 0, 1)
    size_hint: (.3, 1)
    font_name: 'data/fonts/Leefont.ttf'
<PhotoHideWidget>:
    padding: (10, 10, 10, 10)
    orientation: 'vertical'
    spacing: 20
    canvas:
        Color:
            rgba: (2, 2, 2, 1)
        Rectangle:
            size: self.size
            pos: self.pos
    BoxLayout:
        orientation: 'vertical'
        size_hint: (1, .15)
        canvas:
            Color:
                rgba: (0,0,255,0.5)
            Rectangle:
                size: self.size
                pos: self.pos
        Label:
            text: '[size=30]WPBKJ图片隐藏工具(QQ缩略图与大图不同)[/size]\\n[size=15]图片文件应与本程序在同一目录下,输出图片也在同一目录,请手动输入图片名称\\n构建出的图片大于1MB时,请不要使用图片形式发送,否则会被QQ压缩,可使用文件形式发送[/size]'
            markup: True
            halign: 'center'
            font_name: 'data/fonts/Leefont.ttf'
        Label:
            size_hint: (1, .3)
            id: alert_msg
            text: '输入后单击提交开始构建'
            font_size: 18
            halign: 'center'
            font_name: 'data/fonts/Leefont.ttf'
    BoxLayout:
        size_hint: (1, .1)
        DefaultLabel:
            text: '上层图片(白色背景显示)'
        DefaultTextInput:
            id: top_image
    BoxLayout:
        size_hint: (1, .1)
        DefaultLabel:
            text: '下层图片(黑色背景显示)'
        DefaultTextInput:
            id: bottom_image
    BoxLayout:
        size_hint: (1, .1)
        DefaultLabel:
            text: '输出文件名(务必为png后缀)'
        DefaultTextInput:
            id: output_image
            text: 'output.png'
            
    BoxLayout:
        spacing: 30
        size_hint: (1, .05)
        Button:
            text: '提交'
            on_press: root.changeState()
            on_release: root.BeginMake()
            background_color: (0,0,255,0.45)
            font_name: 'data/fonts/Leefont.ttf'
        Button:
            text: '重置'
            on_press: root.ResetInput()
            background_color: (0,0,255,0.45)
            font_name: 'data/fonts/Leefont.ttf'
    BoxLayout:
        size_hint: (1, .05)
        padding: (200, 0 , 200, 0)
        Button:
            text: 'Gitee开源'
            on_press: root.openGitee()
            background_color: 0, 0, 0, 0
            color: (0, 0, 0, 1)
            font_name: 'data/fonts/Leefont.ttf'
        Button:
            text: 'GitHub开源'
            on_press: root.openGitHub()
            background_color: 0, 0, 0, 0
            color: (0, 0, 0, 1)
            font_name: 'data/fonts/Leefont.ttf'
''')


class PhotoHideApp(App):
    def build(self):
        self.title = 'WPBKJ图片隐藏v1.0.2'
        return PhotoHideWidget()

if __name__ == '__main__':
    PhotoHideApp().run()