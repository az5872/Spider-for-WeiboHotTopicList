# encoding=utf-8

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import random
from io import StringIO
from PIL import Image
from math import sqrt
import ims
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains


logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人

"""
账号密码
"""
myWeiBo = [

]

PIXELS = []


def getExactly(im):
    """ 精确剪切"""
    imin = -1
    imax = -1
    jmin = -1
    jmax = -1
    row = im.size[0]
    col = im.size[1]
    for i in range(row):
        for j in range(col):
            if im.load()[i, j] != 255:
                imax = i
                break
        if imax == -1:
            imin = i

    for j in range(col):
        for i in range(row):
            if im.load()[i, j] != 255:
                jmax = j
                break
        if jmax == -1:
            jmin = j
    return (imin + 1, jmin + 1, imax + 1, jmax + 1)


def getType(browser):
    """ 识别图形路径 """
    ttype = ''
    time.sleep(3.5)
    browser.get_screenshot_as_file('picture.png')
    im0 = Image.open('picture.png')
    box = browser.find_element_by_id('patternCaptchaHolder')
    PIXELS.append((box.location['x']+ 20,box.location['y']+20))
    im = im0.crop((int(box.location['x']) + 10, int(box.location['y']) + 100,
                   int(box.location['x']) + box.size['width'] - 10,
                   int(box.location['y']) + box.size['height'] - 10)).convert('L')
    newBox = getExactly(im)
    im = im.crop(newBox)
    im.save('picture.png')
    width = im.size[0]
    height = im.size[1]
    for png in ims.ims.keys():
        isGoingOn = True
        for i in range(width):
            for j in range(height):
                if abs(im.load()[i, j]-ims.ims[png][i][j]) > 30:
                    isGoingOn = False
                    break
            if isGoingOn is False:
                break
        if isGoingOn is True:
            ttype = png
            break
    if ttype == '':
        im.show()
        ttype = input("输入顺序")
    px0_x = box.location['x'] + 40 + newBox[0]
    px1_y = box.location['y'] + 150 + newBox[1]
    PIXELS.append((px0_x, px1_y))
    PIXELS.append((px0_x + 100, px1_y))
    PIXELS.append((px0_x, px1_y + 100))
    PIXELS.append((px0_x + 100, px1_y + 100))
    return ttype


def move(browser, coordinate, coordinate0):
    """ 从坐标coordinate0，移动到坐标coordinate """
    time.sleep(0.05)
    length = sqrt((coordinate[0] - coordinate0[0]) ** 2 + (coordinate[1] - coordinate0[1]) ** 2)  # 两点直线距离
    if length < 4:  # 如果两点之间距离 小于4px，直接划过去
        ActionChains(browser).move_by_offset(coordinate[0] - coordinate0[0], coordinate[1] - coordinate0[1]).perform()
        return
    else:  # 递归，不断向着终点滑动
        step = random.randint(5,7)
        x = int(step * (coordinate[0] - coordinate0[0]) / length)  # 按比例
        y = int(step * (coordinate[1] - coordinate0[1]) / length)
        try:
            ActionChains(browser).move_by_offset(x,y).perform()
        except Exception as e:
            print(e)
        move(browser, coordinate, (coordinate0[0] + x, coordinate0[1] + y))


def draw(browser, ttype):
    """ 滑动 """
    if len(ttype) == 4:
        px0 = PIXELS[int(ttype[0])]
        login = browser.find_element_by_id('loginAction')
        ActionChains(browser).move_by_offset(px0[0],px0[1]).perform()
        ActionChains(browser).click_and_hold().perform()
        #browser.execute(Command.MOUSE_DOWN, {})
        px1 = PIXELS[int(ttype[1])]
        #move(browser,c,c0)
        #move(browser, (px1[0], px1[1]), px0)
        ActionChains(browser).move_by_offset(px1[0] - px0[0], px1[1] - px0[1]).perform()
        time.sleep(1)

        px2 = PIXELS[int(ttype[2])]
        #move(browser, (px2[0], px2[1]), px1)
        ActionChains(browser).move_by_offset(px2[0] - px1[0], px2[1] - px1[1]).perform()
        time.sleep(1)

        px3 = PIXELS[int(ttype[3])]
        #move(browser, (px3[0], px3[1]), px2)
        ActionChains(browser).move_by_offset(px3[0] - px2[0], px3[1] - px2[1]).perform()
        ActionChains(browser).release().perform()
    else:
        print('Sorry! Failed! Maybe you need to update the code.')


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        try:
            browser = webdriver.Firefox()
            browser.set_window_size(1050, 840)
            browser.get(loginURL)
            time.sleep(1)
            failure = 0
            while '登录' in browser.title and failure < 5:
                try:
                    failure += 1
                    username = browser.find_element_by_id('loginName')
                    username.send_keys("")

                    psd = browser.find_element_by_id('loginPassword')

                    username.send_keys(account)

                    psd.send_keys(password)

                    login = browser.find_element_by_id('loginAction')
                    login.click()

                    ttype = getType(browser)
                    print('Result: %s!' % ttype)
                    draw(browser, ttype)# 滑动破解
                    time.sleep(10)
                    if '登录' in browser.title:
                        ActionChains(browser).reset_actions()
                        browser.refresh()
                        time.sleep(5)
                    if '未激活微博' in browser.page_source:
                        print('账号未开通微博')
                        return {}
                except Exception as e:
                    print(e)

            cookie = {}
            if '发现新鲜事' in browser.title:
                for elem in browser.get_cookies():
                    cookie[elem["name"]] = elem["value"]
                if len(cookie) > 0:
                    logger.warning("Get Cookie Successful: %s" % account)
                    cookies.append(cookie)
                    continue
            logger.warning("Get Cookie Failed: %s!" % account)
        except Exception as e:
            logger.warning("Failed %s!" % account)
        finally:
            try:
                browser.quit()
            except Exception as e:
                pass
    return cookies


'''if __name__ == "__main__":
    myWeiBo=[{'no':'15392609851','psw':'8239876gxy'}]
    cookies,ttype = getCookies(myWeiBo)
    print(cookies)
    logger.warning("Get Cookies Finish!( Num:%d)" % len(cookies))'''
