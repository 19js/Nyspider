# -*- coding: utf-8 -*-
#

from ctypes import *

ocrpasswd = "868197D30CC624FD3C2E2EE66494DA5F"
#VcodeInit 初始换引擎函数 只有一个参数 为引擎初始化密码 失败返回-1 此函数只需调用一次 切勿多次调用 。
dll = windll.LoadLibrary('CaptchaOCR.dll')
load_ocr = dll.VcodeInit
load_ocr.argtypes = [c_char_p]
load_ocr.restypes = c_int
index = load_ocr(ocrpasswd.encode('utf-8'))
img_string = open(imgname, "rb").read()
img_buffer = create_string_buffer(img_string)
#申请接收识别结果的缓冲区  一定要申请
ret_buffer = create_string_buffer(15)
#调用此函数之前，如果已经初始化成功过识别引擎函数 那么无需再调用初始化函数
#GetVcode 识别函数 参数1为 VcodeInit 返回值 index 参数2为图片数据 参数3为图片大小 参数4为接收识别结果 需要给变量申请内存 如 ret_buffer = create_string_buffer(10)
get_code_from_buffer = dll.GetVcode
get_code_from_buffer(index, byref(img_buffer), len(img_buffer), byref(ret_buffer))
print (ret_buffer.value.decode('utf-8'))
