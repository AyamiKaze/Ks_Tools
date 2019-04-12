# -*- coding:utf-8 -*-

import struct,os,fnmatch,re,zlib

#遍历文件夹，返回文件列表
def walk(adr):
    mylist=[]
    for root,dirs,files in os.walk(adr):
        for name in files:
            adrlist=os.path.join(root, name)
            mylist.append(adrlist)
    return mylist

#将4字节byte转换成整数
def byte2int(byte):
    long_tuple=struct.unpack('L',byte)
    long = long_tuple[0]
    return long

#将整数转换为4字节二进制byte
def int2byte(num):
    return struct.pack('L',num)


#将txt转换成文本列表
def makestr(lines):
    string_list = []
    num = len(lines)
    for index,line in enumerate(lines):
        if re.match('★[0-9A-Fa-f]+★', line):
            i = 1
            string = ''
            while True:
                if index+i >= num:
                    break
                if re.match('☆[0-9A-Fa-f]+☆', lines[index+i]):
                    break
                string += lines[index+i]
                i += 1
            string_list.append(string[:-1])
    return string_list

def FormatString(string, count):
    #格式说明：
    #★字符串行数★字符串
    res = ''
    flag = False
    if string != '':
        flag = True
        '''
        res = "★%08d★\n%s\n"%(count, string)
        '''
        res = "☆%08d☆\n%s★%08d★\n%s\n"%(count, string, count, string)
 
    else:
        flag = False

    return flag, res

def StringFilter(string):
    left = b'\x6a\x22'.decode('utf16')
    right = b'\x6b\x22'.decode('utf16')
    if left in string:
        string = string.replace(left, '《')
    if right in string:
        string = string.replace(right, '》')
    return string
        

f_lst = walk('TEXT')
for fn in f_lst:
    srcname = fn
    src = open(srcname,'r', encoding='utf16')
    
    dstname = fn + '.ks'
    dst = open(dstname,'w', encoding='utf16')
    
    raw = open(fn, 'r+', encoding='utf16')
    lines = src.readlines()
    string_list = makestr(lines)

    new_list = []
    raw_lines = raw.readlines()
    num = len(raw_lines)
    stringline = ''
    j = 0
    for line in lines:
        if (line[0] != ';'
            and line[0] != '*'
            and line[0] != '@'
            and line[:2] != '[f'
            and line[:2] != '[b'
            and line[:2] != '[p'
            and line[:2] != '[m'
            and line[:2] != '[j'
            and line[:2] != '[r'
            and line[:2] != '[e'
            and line[:2] != '  '
            and line[:3] != '[st'
            and line != '\n'):
            new_list.append(line)
            j += 1
        else:
             new_list.append(line)
    new_list.append(raw_lines[len(raw_lines)-1])
            
    for string in new_list:
        dst.write(string)
            
            
    print(dstname)
    src.close()
    dst.close()
    raw.close()

