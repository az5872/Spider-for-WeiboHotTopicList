#encoding:utf-8

#import get_hotUrl
import time
import json
import requests
import get_cookies
import get_hotUrl
import re
import os
import csv
import codecs
params = []
image_content = []
image_content_unsave = []
image_url = []
myWeiBo=[{'no':'13991150938','psw':'NImabi123'}]
#cookies = get_cookies.getCookies(myWeiBo)[0]
#print(cookies)
cookies={'SUB': '_2A253pKw3DeRhGedP61MZ8CjJyT2IHXVVZjR_rDV6PUJbkdAKLU2skW1NIST94loPXLZ0HTV84m5tQqFJbdcCdgip', 'SUHB': '0IIjW1qqEg1OWW', 'SCF': 'AvijpnwBU7pBExnhVockKCQYf3RgbhGYSvnufJnTxkD1aYyUWmUPis53_drc2qYSJPLzW7_VLmZIClMcupEpDTI.', 'SSOLoginState': '1520491623', '_T_WM': '710085185823c8d735e86c632c8b1468', 'M_WEIBOCN_PARAMS': 'featurecode=20000320&oid=4215297030091333&luicode=20000061&lfid=4215309651417282&uicode=20000061&fid=4215297030091333'}
hot_class = get_hotUrl.get_hotUrl()
hot_class.get_hotUrl(cookies)
m = 'D:\\sina_data\\%s'%(time.strftime("%Y_%m_%d_%H",time.localtime()))
hot_class.store2csv(m)
q= '%s\\'%m
hot_url = []
with open('%smain.csv'%q) as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        if row==[]:
            continue
        else:
            hot_url.append(row[1])
    f.close()
img_path = 'D:\\sina_data\\image.csv'
for hot_sub in range(len(hot_url)):
    content_type = []  # 类型  ： 热门微博，实时热议。。
    content_author = []
    content_urls = []
    content_time = []
    content_text = []
    content_zhuanfa = []
    content_zan = []
    content_pinglun = []
    file_num = 0
    hot_sub = hot_sub
    html =hot_url[hot_sub]
    #创建文件夹
    file_name = '%s%s' % (q, hot_sub + 1)
    isExists = os.path.exists(file_name)
    if not isExists:
        os.makedirs(file_name)
    ifExists = os.path.exists(img_path)
    '''f_image = open(img_path, 'a+')
    if not isExists:
        f_image_csv_writer = csv.writer(f_image)
        image_headers = ['content', 'url']
        f_image_csv_writer.writerow(image_headers)
        image_content=[]
    else:
        f_image_csv_reader = csv.reader(f_image)
        image_headers = next(f_image_csv_reader)
        for row in f_image_csv_reader:
            image_content.append(row[0])'''
    #设置参数params
    del params
    params = html.split('&')
    params[0] = params[0].split('?')[1]
    params = '\',\''.join(params)
    params ='[\''+params+'\']'
    params = params.replace('=','\':\'').replace('[','{').replace(']','}')
    params = eval(params)
    for k in range(2):
        #设置page参数 使爬虫可以爬第二页的数据
        params['page']=k+1
        r = requests.get('https://m.weibo.cn/api/container/getIndex',params = params,cookies=cookies)
        #r=re.sub('\'','\"',r)
        main_content = json.loads(r.content)
        main_content = main_content['data']
        for i in range(len(main_content['cards'])):
            if main_content['cards'][i]['card_type'] == 11:
                if main_content['cards'][i]['card_group'][0]['card_type']==10:
                    content_type.append('热搜人物')
                    content_author.append( main_content['cards'][i]['card_group'][0]['user']['screen_name'])
                    content_urls.append(main_content['cards'][i]['card_group'][0]['user']['profile_url'])
                    content_time.append('--')
                    content_text.append('--')
                    content_zhuanfa.append('--')
                    content_zan.append('--')
                    content_pinglun.append('--')
                elif main_content['cards'][i]['card_group'][0]['card_type']==9:
                    for j in range(len(main_content['cards'][i]['card_group'])):
                        if main_content['cards'][i]['card_group'][j]['card_type']==9:
                            zhuanfa_name = []
                            zhuanfa_urls = []
                            zhuanfa_time = []
                            zhuanfa_text = []
                            pinglun_name = []
                            pinglun_urls = []
                            pinglun_time = []
                            pinglun_text = []
                            pinglun_reply = []
                            zan_name = []
                            zan_urls = []
                            zan_time = []
                            file_num += 1
                            content_type.append('微博')
                            content_time.append(main_content['cards'][i]['card_group'][j]['mblog']['created_at']+' now '+time.strftime("%H:%M",time.localtime()))
                            content_author.append(main_content['cards'][i]['card_group'][j]['mblog']['user']['screen_name'])
                            content_urls.append(main_content['cards'][i]['card_group'][j]['mblog']['user']['profile_url'])
                            content_zhuanfa.append(main_content['cards'][i]['card_group'][j]['mblog']['reposts_count'])
                            content_pinglun.append(main_content['cards'][i]['card_group'][j]['mblog']['comments_count'])
                            content_zan.append(main_content['cards'][i]['card_group'][j]['mblog']['attitudes_count'])
                            if main_content['cards'][i]['card_group'][j]['mblog']['isLongText']:
                                content_text.append(main_content['cards'][i]['card_group'][j]['mblog']['longText']['longTextContent'])
                            else:
                                content_text.append(main_content['cards'][i]['card_group'][j]['mblog']['text'])
                            index_html_pinglun = 'https://m.weibo.cn/api/comments/show'
                            index_html_zan = 'https://m.weibo.cn/api/attitudes/show'
                            index_html_zhuanfa = 'https://m.weibo.cn/api/statuses/repostTimeline'
                            params_common = {}
                            #爬取的评论，转发，赞
                            a=int(int(main_content['cards'][i]['card_group'][j]['mblog']['reposts_count'])/10)+1
                            b=int(int(main_content['cards'][i]['card_group'][j]['mblog']['comments_count'])/10)+1
                            c=int(int(main_content['cards'][i]['card_group'][j]['mblog']['attitudes_count'])/50)+1
                            for page_common in range(a):
                                params_common['id']=main_content['cards'][i]['card_group'][j]['mblog']['id']
                                params_common['page'] = page_common+1
                                r_zhuanfa = requests.get(index_html_zhuanfa,params=params_common,cookies=cookies)
                                zhuanfa = json.loads(r_zhuanfa.content)
                                if 'data' in zhuanfa.keys() and zhuanfa['data']!=[]:
                                    zhuanfa = zhuanfa['data']
                                    for num in range(len(zhuanfa['data'])):
                                        zhuanfa_name.append(zhuanfa['data'][num]['user']['screen_name'])
                                        zhuanfa_urls.append(zhuanfa['data'][num]['user']['profile_url'])
                                        zhuanfa_time.append(zhuanfa['data'][num]['created_at']+' now '+time.strftime("%H:%M", time.localtime()))
                                        zhuanfa_text.append(zhuanfa['data'][num]['raw_text'])
                            for page_common in range(b):
                                params_common['id']=main_content['cards'][i]['card_group'][j]['mblog']['id']
                                params_common['page'] = page_common+1
                                r_pinglun= requests.get(index_html_pinglun, params=params_common,cookies=cookies)
                                pinglun = json.loads(r_pinglun.content)
                                if 'data' in pinglun.keys() and pinglun['data']!=[]:
                                    pinglun = pinglun['data']
                                    for num in range(len(pinglun['data'])):
                                        pinglun_name.append(pinglun['data'][num]['user']['screen_name'])
                                        pinglun_urls.append(pinglun['data'][num]['user']['profile_url'])
                                        pinglun_time.append(pinglun['data'][num]['created_at'] + ' now ' + time.strftime("%H:%M",time.localtime()))
                                        text= re.split(re.compile(r'<.?span.*?>'),pinglun['data'][num]['text'])
                                        for text_num in range(len(text)):
                                            if '回复' in text[text_num] or '@' in text[text_num] or '#' in text[text_num]:
                                                d = re.split(re.compile(r'<.?a.*?>'),text[text_num])
                                                text[text_num] = ''.join(d)
                                            if 'img' in text[text_num]:
                                                d = re.findall(re.compile(r'alt=\"(.*?)\"'),text[text_num])
                                                url = re.findall(re.compile(r'src=\"(.*?)\"'),text[text_num])
                                                '''for d_num in range(len(d)):
                                                    flag = 0
                                                    for image_c in image_content:
                                                        if d[d_num] in image_c:
                                                            flag = 1
                                                            break
                                                    if flag==0:
                                                        image_content_unsave.append(d[d_num])
                                                        image_url.append(url[d_num])'''
                                                text[text_num] = ''.join(d)
                                        text = ''.join(text)
                                        pinglun_text.append(text)
                                        if 'reply_text' in pinglun['data'][num].keys():
                                            text = re.split(re.compile(r'<.?span.*?>'),
                                                            pinglun['data'][num]['reply_text'])
                                            for text_num in range(len(text)):
                                                if '回复' in text[text_num] or '@' in text[text_num] or '#' in text[text_num]:
                                                    d = re.split(re.compile(r'<.?a.*?>'), text[text_num])
                                                    text[text_num] = ''.join(d)
                                                if 'img' in text[text_num]:
                                                    d = re.findall(re.compile(r'alt=\"(.*?)\"'), text[text_num])
                                                    url = re.findall(re.compile(r'src=\"(.*?)\"'), text[text_num])
                                                    '''for d_num in range(len(d)):
                                                        flag = 0
                                                        for image_c in image_content:
                                                            if d[d_num] in image_c:
                                                                flag = 1
                                                                break
                                                        if flag == 0:
                                                            image_content_unsave.append(d[d_num])
                                                            image_url.append(url[d_num])'''
                                                    text[text_num] = ''.join(d)
                                            text = ''.join(text)
                                            pinglun_reply.append(text)
                                        else:
                                            pinglun_reply.append('')
                                if 'hot_data' in pinglun.keys():
                                    for num in range(len(pinglun['hot_data'])):
                                        pinglun_name.append(pinglun['hot_data'][num]['user']['screen_name'])
                                        pinglun_urls.append(pinglun['hot_data'][num]['user']['profile_url'])
                                        pinglun_time.append(pinglun['hot_data'][num]['created_at'] + ' now ' + time.strftime("%H:%M", time.localtime()))
                                        text = re.split(re.compile(r'<.?span.*?>'), pinglun['hot_data'][num]['text'])
                                        for text_num in range(len(text)):
                                            if '回复' in text[text_num] or '@' in text[text_num]:
                                                d = re.split(re.compile(r'<.?a.*?>'), text[text_num])
                                                text[text_num] = ''.join(d)
                                            if 'img' in text[text_num]:
                                                d = re.findall(re.compile(r'alt=\"(.*?)\"'), text[text_num])
                                                url = re.findall(re.compile(r'src=\"(.*?)\"'), text[text_num])
                                                '''for d_num in range(len(d)):
                                                    flag = 0
                                                    for image_c in image_content:
                                                        if d[d_num] in image_c:
                                                            flag = 1
                                                            break
                                                    if flag == 0:
                                                        image_content_unsave.append(d[d_num])
                                                        image_url.append(url[d_num])'''
                                                text[text_num] = ''.join(d)
                                        text = ''.join(text)
                                        pinglun_text.append(text)
                                        if 'reply_text' in pinglun['hot_data'][num].keys():
                                            text = re.split(re.compile(r'<.?span.*?>'), pinglun['hot_data'][num]['reply_text'])
                                            for text_num in range(len(text)):
                                                if '回复' in text[text_num] or '@' in text[text_num]:
                                                    d = re.split(re.compile(r'<.?a.*?>'), text[text_num])
                                                    text[text_num] = ''.join(d)
                                                if 'img' in text[text_num]:
                                                    d = re.findall(re.compile(r'alt=\"(.*?)\"'), text[text_num])
                                                    url = re.findall(re.compile(r'src=\"(.*?)\"'), text[text_num])
                                                    '''for d_num in range(len(d)):
                                                        flag = 0
                                                        for image_c in image_content:
                                                            if d[d_num] in image_c:
                                                                flag = 1
                                                                break
                                                        if flag == 0:
                                                            image_content_unsave.append(d[d_num])
                                                            image_url.append(url[d_num])'''
                                                    text[text_num] = ''.join(d)
                                            text = ''.join(text)
                                            pinglun_reply.append(text)
                                        else:
                                            pinglun_reply.append('')
                            for page_common in range(c):
                                params_common['id']=main_content['cards'][i]['card_group'][j]['mblog']['id']
                                params_common['page'] = page_common+1
                                r_zan =requests.get(index_html_zan,params = params_common,cookies=cookies)
                                zan = json.loads(r_zan.content)
                                if 'data' in zan.keys() and zan['data']!=[]:
                                    zan = zan['data']
                                    for num in range(len(zan['data'])):
                                        zan_name.append(zan['data'][num]['user']['screen_name'])
                                        zan_urls.append(zan['data'][num]['user']['profile_url'])
                                        zan_time.append(zan['data'][num]['created_at']+ ' now ' + time.strftime("%H:%M", time.localtime()))
                            zhuanfa_header = ['name','url','time','text']
                            pinglun_header = ['name','url','time','text','reply_text']
                            zan_header = ['name','url','time']
                            row_zhuanfa = zip(zhuanfa_name,zhuanfa_urls,zhuanfa_time,zhuanfa_text)
                            row_pinglun_1 = list(zip(pinglun_name,pinglun_urls,pinglun_time))
                            row_pinglun_2 = list(zip(pinglun_text,pinglun_reply))
                            row_pinglun = []
                            for num_row in range(len(pinglun_name)):
                                row_pinglun.append(row_pinglun_1[num_row] + row_pinglun_2[num_row])
                            row_zan = zip(zan_name,zan_urls,zan_time)
                            fout = codecs.open('%s\\%s_zhuanfa.csv' % (file_name, file_num), 'w', encoding='utf-8')
                            f_csv = csv.writer(fout)
                            f_csv.writerow(zhuanfa_header)
                            f_csv.writerows(row_zhuanfa)
                            fout.close()
                            fout = codecs.open('%s\\%s_pinglun.csv' % (file_name, file_num), 'w', encoding='utf-8')
                            f_csv = csv.writer(fout)
                            f_csv.writerow(pinglun_header)
                            f_csv.writerows(row_pinglun)
                            fout.close()
                            fout = codecs.open('%s\\%s_zan.csv' % (file_name, file_num), 'w', encoding='utf-8')
                            f_csv = csv.writer(fout)
                            f_csv.writerow(zan_header)
                            f_csv.writerows(row_zan)
                            fout.close()
                            print("%s_%s已经存储完成" %(hot_sub+1,file_num))
                            time.sleep(10)

    for content_num in range(len(content_text)):
        text = re.split(re.compile(r'<.?span.*?>'), content_text[content_num])
        for text_num in range(len(text)):
            if '回复' in text[text_num] or '@' in text[text_num] or '#' in text[text_num]:
                d = re.split(re.compile(r'<.?a.*?>'), text[text_num])
                text[text_num] = ''.join(d)
            if 'img' in text[text_num]:
                d = re.findall(re.compile(r'alt=\"(.*?)\"'), text[text_num])
                url = re.findall(re.compile(r'src=\"(.*?)\"'), text[text_num])
                text[text_num] = ''.join(d)
            d = re.split(re.compile(r'<.?[aib].*?>'),text[text_num])
            text[text_num] = ''.join(d)
        text = ''.join(text)
        content_text[content_num] =text
    headers = ['type','author','urls','time','text','zhuanfa','zan','pinglun']
    rows_1 = list(zip(content_type,content_author,content_urls,content_time))
    rows_2 = list(zip(content_text,content_zhuanfa,content_zan,content_pinglun))
    rows = []
    for i in range(len(content_type)):
        rows.append(rows_1[i]+rows_2[i])
    #存储1_main.csv文件
    fout = codecs.open('%s\\comment.csv'%file_name, 'w', encoding='utf-8')
    f_csv = csv.writer(fout)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
    fout.close()
    #f_image.close()
    print("%s_comment.csv存储成功"%(hot_sub+1))
    time.sleep(3)


