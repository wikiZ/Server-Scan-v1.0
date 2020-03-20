#!/usr/bin/python
#coding:utf-8

import time
import threading
import argparse
import os
#import datatime
from colorama import *
from IPy import IP
import platform
from socket import *

init(autoreset=True)
threadLock=threading.Lock()
def banner():
	try:
		print("\033[0;32;40m\t\t\t\tServer Scan v1.0\033[0m")
		print("           _     _")	#这段图片我是真的不会搞就网上找了贴上了
		print("          (_)   | |")
		print(" _ __ ___  _ ___| |_____ ____")
		print("| '_ ` _ \| / __| __/ _ \ '__|"+"\033[0;36;40m\t\t大风起兮云飞扬\033[0m")
		print("| | | | | | \__ \ ||  __/ |")
		print("|_| |_| |_|_|___/\__\___|_|")
		print("\033[0;33;40m\t\t\t\t我只是一个服务扫描器!\033[0m")
		print("\n")

		print("用法:")
		print("	--help:帮助文档")
		print("	-H:目标IP (-h 127.0.0.1)")
		print("	-p:目标端口 (-p 445,443)不指定端口时则进行全端口扫描")
		print("	-s:存活性扫描(-s 192.168.52.0/24)")
		print("	-o:将扫描结果输出至指定文件 (-o C:/Users/asus/Desktop/a.txt)--暂未推出")
	except:
		pass


def doc():
	"""@author 风起 QQ:1402720815"""
	"""要是妹子发现这条注释就加我啊╰(●’◡’●)╮"""
	pass

def HostScan(host,port):
	print(Fore.GREEN+"["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]--"+"Scan Start")
	try:
		IP = gethostbyname(host)
	except:
		print("\033[41m[-] Cannot resolve '%s':Unknow host" % host)
		return

	try:
		name = gethostbyaddr(host)
		print(Fore.RED+"[+] Scan Results for:"+IP)       
		print(Fore.RED+"\n[+] Scan result for:"+name[0])
	except:
		print(Fore.RED+"\n[+] Scan Results for:"+IP)

	try:
		setdefaulttimeout(1)
		start_time = time.time()
		if(port==None):
			for port in range(0,65535):
				t=threading.Thread(target=AllPortScan,args=(IP,port,))
				t.start()
		else:
			for ports in port:
				print("Scan port:"+ports)
				PortScan(IP,int(ports))
		print(Fore.GREEN+'扫描端口完成，总共用时 ：%.2f' % (time.time() - start_time))
	except Exception as e:
		print(e)
		print("\033[41m[ERROR]异常错误")
		pass

def PortScan(IP,port):
	try:
		conn=socket(AF_INET,SOCK_STREAM)
		res=conn.connect_ex((IP,port))
		conn.send('Hello,World!'.encode("utf8"))
		results=conn.recv(25)
		threadLock.acquire()
		if res==0:
			print('[+]%d/tcp OPEN'%port)
			print(results.decode("utf8","ignore"))
			conn.close()
	except Exception as e:
		threadLock.acquire()
		print('[-]%d/tcp CLOSED'% port)
	finally:
		print("")
		threadLock.release()
		conn.close()

def AllPortScan(IP,port):
	try:
		conn=socket(AF_INET,SOCK_STREAM)
		res=conn.connect_ex((IP,port))
		conn.send('Hello,World!'.encode("utf8"))
		results=conn.recv(25)
		threadLock.acquire()
		if res==0:
			print('[+]%d/tcp OPEN'%port)
			conn.close()
	except:
		threadLock.acquire()
		pass
	finally:
		threadLock.release()
		conn.close()

def my_os():
	return platform.system()

def Survivability(ip):
	try:
		if my_os() == 'Windows':
			p_w = 'n'
		elif my_os() == 'Linux':
			p_w = 'c'
		else:
			print('不支持此操作系统')
			sys.exit()
		output = os.popen('ping -b -%s 1 %s'%(p_w,ip)).readlines()
		#Curtime = datetime.datetime.now()  安装模块后使用
		for w in output:
			if str(w).upper().find('TTL')>=0:
					#print(Curtime)
					print("")
					print(ip)
				
	except:
		pass

def Survivabilitys(surv):
	try:
		print(Fore.GREEN+"Survivability Scan Start")
		print("局域网主机存活性扫描")
		ip=IP(surv)
		for ips in ip:
			t=threading.Thread(target=Survivability,args=(ips,))
			t.start()
	except:
		pass
		
def main():
	try:
		banner()
		parser = argparse.ArgumentParser()
		parser.description="使用教程"
		parser.add_argument("-H","--host", help="目标主机IP")
		parser.add_argument("-p","--port", help="目标主机端口")
		parser.add_argument("-s","--Survivability", help="指定目标网段")
		print("\n")
		args = parser.parse_args()
		if args.Survivability:
			Survivabilitys(args.Survivability)
			return 0
		if(args.host==None):
			print("\033[41mIP不能为空!")
			exit(0)
		host=args.host
		port=str(args.port).split(",") if args.port!=None else None
		HostScan(host,port)
	except:
		print("\033[41m请检查语法是否存在错误!")
		pass
		
if __name__=="__main__":
	try:
		t=threading.Thread(target=main)
		t.start()
	except:
		pass

 
