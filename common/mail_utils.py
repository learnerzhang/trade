#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 4:57 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : mail_utils.py
# @Software: PyCharm
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 设置服务器所需信息
# 163邮箱服务器地址
mail_host = 'smtp.163.com'
# 163用户名
mail_user = '18518067686'
# 密码(部分邮箱为授权码)
mail_pass = 'OKFEFHUHXIQRLMJL'
# 邮件发送方邮箱地址
sender = 'learnerzhang@163.com'
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['215454560@qq.com', ]

# 设置email信息
# 邮件内容设置
message = MIMEText('content', 'plain', 'utf-8')


def gen_html(result, extra, period):
	tr_html = ""

	def get_head_tr(records, marks, mark='zxb'):
		field = "Null"
		if mark == 'zxb':
			field = '中小板'
		if mark == 'hsb':
			field = '沪A'
		if mark == 'ssb':
			field = '深A'
		record = records[0]
		bgcolor = '#FFFFF'
		if record.code in marks:
			bgcolor = 'yellow'
		return """ <tr>
		<td rowspan=""" + str(len(records)) + """> """ + field + """</td>
		<td bgcolor='""" + bgcolor + """'>""" + record.code + """</td>
		<td bgcolor='""" + bgcolor + """'>""" + record.name + """</td>
		<td bgcolor='""" + bgcolor + """'>""" + str(round(record.change, 3)) + """</td></tr>"""

	def get_tr(record, marks):
		bgcolor = '#FFFFF'
		if record.code in marks:
			bgcolor = 'yellow'
		return """ <tr> 
		<td bgcolor='""" + bgcolor + """'>""" + record.code + """</td> 
		<td bgcolor='""" + bgcolor + """'>""" + record.name + """</td> 
		<td bgcolor='""" + bgcolor + """'>""" + str(round(record.change, 3)) + """</td> </tr>	"""

	mark_codes = [ele[0][0] for ele in extra['best']][:10]  # codes
	period_rs = result[period]
	# print(period_rs)
	if period_rs:
		hsb = period_rs['hsb']  # list<record>
		ssb = period_rs['ssb']  # list<record>
		zxb = period_rs['zxb']  # list<record>

		tr_html = get_head_tr(hsb, mark_codes, mark='hsb')
		for ele in hsb[1:]:
			tr_html += get_tr(ele, mark_codes)

		tr_html += get_head_tr(ssb, mark_codes, mark='ssb')
		for ele in ssb[1:]:
			tr_html += get_tr(ele, mark_codes)

		tr_html += get_head_tr(zxb, mark_codes, mark='zxb')
		for ele in zxb[1:]:
			tr_html += get_tr(ele, mark_codes)

	# print(tr_html)
	return tr_html


def new_change_html(records):
	tr_html = ""
	if records:
		bgcolor = '#FFFFF'
		for r in records[:15]:
			bgcolor ='#99FFFF'
			tr_html += """ <tr>
			<td bgcolor='""" + bgcolor + """'>""" + r.code + """</td>
			<td bgcolor='""" + bgcolor + """'>""" + r.name + """</td>
			<td bgcolor='""" + bgcolor + """'>""" + str(round(r.change, 3)) + """</td></tr>"""

		if len(records) > 30:
			_records = records[-15:]
		else:
			_records = records[15:]

		for r in _records:
			bgcolor = '#FFFFF'
			tr_html += """ <tr>
			<td bgcolor='""" + bgcolor + """'>""" + r.code + """</td>
			<td bgcolor='""" + bgcolor + """'>""" + r.name + """</td>
			<td bgcolor='""" + bgcolor + """'>""" + str(round(r.change, 3)) + """</td></tr>"""

	return tr_html


def big_change_html(elements, top=10):
	text = ""
	if elements:
		for elem in elements[:top]:
			code = elem[0][0]
			name = elem[0][1]
			num = elem[1]
			text += name+"(" + code + ", " + str(num) + ")、"
	return text[:-1]


def send_hot_share_mail(contentResult, extraResult):

	# 邮件主题
	today = str(datetime.date.today())
	message = MIMEMultipart()
	message['Subject'] = '[MoneyShare] {}/强势股'.format(today)
	# 发送方信息
	message['From'] = sender
	# 接受方信息
	message['To'] = ';'.join(receivers)
	html = """
	<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
			<style type="text/css">
				table, td, th{
  					border:1px solid black;
  				}
				th{
  					background-color:grey;
  					color:white;
  				}
			</style>
		</head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>沪、深、中小版块近期强势股票 #""" + today + """#</title>
  		<body>
			<div id="container">
				<p><strong>加特林榜</strong></p>
  				<div> 
  					""" + big_change_html(extraResult['best'], ) + """
  				<div>
  				
  				<p><strong>周新高榜</strong></p>
  				<div> 
  					""" + big_change_html(extraResult['week_best'], top=20) + """
  				<div>
  				<p><strong>2年新高股</strong></p>
  				<div>
  					<table width="500" border="1" cellspacing="2" bgcolor="#FFFFF">
  						<tr>
    						<td><strong>代码</strong></td>
    						<td><strong>名称</strong></td>
    						<td><strong>涨幅</strong></td>
  						</tr>
  						""" + new_change_html(extraResult['high']) + """
  					</table>
  				<div>
  				<p><strong>2年新低股</strong></p>
  				<div>
  					<table width="500" border="1" cellspacing="2" bgcolor="#FFFFF">
  						<tr>
    						<td><strong>代码</strong></td>
    						<td><strong>名称</strong></td>
    						<td><strong>涨幅</strong></td>
  						</tr>
  						""" + new_change_html(extraResult['low']) + """
  					</table>
  				<div>
  				<p><strong>5D强势股票</strong></p>
  				<div>
   					<table width="500" border="1" cellspacing="2" bgcolor="#FFFFF">
  						<tr>
    						<td><strong>版块</strong></td>
    						<td><strong>代码</strong></td>
    						<td><strong>名称</strong></td>
    						<td><strong>累计涨幅</strong></td>
  						</tr>
  						""" + gen_html(contentResult, extraResult, 'd5') + """
  					</table>
  				<div>
  				<p><strong>10D强势股票</strong></p>
  				<div>
   					<table width="500" border="1" cellspacing="2" bgcolor="#FFFFF">
  						<tr>
    						<td><strong>版块</strong></td>
    						<td><strong>代码</strong></td>
    						<td><strong>名称</strong></td>
    						<td><strong>累计涨幅</strong></td>
  						</tr>
  						""" + gen_html(contentResult, extraResult, 'd10') + """
  					</table>
  				<div>
  				<p><strong>20D强势股票</strong></p>
  				<div>
   					<table width="500" border="1" cellspacing="2" bgcolor="#FFFFF">
  						<tr>
    						<td><strong>版块</strong></td>
    						<td><strong>代码</strong></td>
    						<td><strong>名称</strong></td>
    						<td><strong>累计涨幅</strong></td>
  						</tr>
  						""" + gen_html(contentResult, extraResult, 'd20') + """
  					</table>
  				<div>
  				
  				<p><strong>60D强势股票</strong></p>
  				<div>
   					<table width="500" border="1" cellspacing="2" bgcolor="#FFFFF">
  						<tr>
    						<td><strong>版块</strong></td>
    						<td><strong>代码</strong></td>
    						<td><strong>名称</strong></td>
    						<td><strong>累计涨幅</strong></td>
  						</tr>
  						""" + gen_html(contentResult, extraResult, 'd60') + """
  					</table>
  				<div>
  			<div>
  		<body>
	</html>
	"""
	# 登录并发送邮件
	try:
		smtpObj = smtplib.SMTP()
		# 连接到服务器
		smtpObj.connect(mail_host, 25)
		# 登录到服务器
		smtpObj.login(mail_user, mail_pass)
		# 发送
		context = MIMEText(html, _subtype='html', _charset='utf-8')  # 解决乱码
		message.attach(context)
		smtpObj.sendmail(sender, receivers, message.as_string())
		# 退出
		smtpObj.quit()
		print('success')
	except smtplib.SMTPException as e:
		print('error', e)  # 打印错误


if __name__ == '__main__':
	pass
