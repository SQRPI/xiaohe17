# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 09:41:17 2017

@author: Sqrpi/Ning Shangyi


"""
import re
import sys


class method(object):
    '''
        Save Main Code
    '''
    def __init__(self):
        self.word = {}
        self.oriCode = []
        self.startNum = 0

    def add(self, code, character):
        '''
            增加一条编码
            code:       str
            character:  str
            character 是 code 对应的汉字
        '''
        self.word[code] = [character] if not self.word.get(code)\
            else self.word.get(code) + [character]

    def readFromText(self, text):
        '''
            从搜狗输入法的码表文件中读取代码, 读取后通过 splitOri 添加到 method 中
            text:       .txt文档 格式: a,1=啊\n
        '''
        f = open(text)
        for line in f:
            line = line
            self.oriCode.append(line)
        f.close

    def splitOri(self):
        for item in self.oriCode:
            item = re.split(',|=|\n', item)
            self.add(item[0], item[2])

    def changeKeyBoard(self, newMethod, keyboard):
        '''
            通过键盘映射 keyboard 批量生成新的码表
            制作异型键盘的码表
        '''
        for key in self.word.keys():
            newKey = [] + list(key)
            for i in range(len(newKey)):
                letter = newKey[i]
                newKey[i] = keyboard.get(letter) if keyboard.get(letter)\
                    else letter
            for item in self.word[key]:
                newMethod.add(''.join(newKey), item)

    def sortCharacters(self, startNum=0):
        size = len(self.word.keys()) - startNum
        if size < 0:
            print 'Error readOriCode-sorting 064:\t StartNum > Size'
            return
        for i in range(size):
            code = self.word.keys()[startNum + i]
            character = self.word[code]
            if len(character) == 1:
                continue
            sys.stdout.write('\r编码:%s\t' % (code))
            for j in range(len(character)):
                sys.stdout.write('%d:%s\t' % (j+1, character[j]))
            content = list(raw_input("\r输入排序, 输入非法值退出, 直接按回车跳过此项:".decode('utf-8').encode('gbk')))
            if content == []:
                continue
            try:
                1/(sorted(content) == [str(j)for j in range(1, len(character)+1)])
            except:
                print '输入错误, 示例:', int(''.join([str(j)for j in range(len(character), 0, -1)])),\
                    '进度已保存', startNum + i, '/', len(self.word.keys()), '已完成'
                self.startNum = startNum + i
                return
            newCharacter = character
            for j in range(len(character)):
                newCharacter[int(content[j])-1] = character[j]
            self.word[code] = newCharacter
    pass


xiaoheOri = method()
xiaohe17 = method()

xiaoheOri.readFromText('oriCode1.txt')
xiaoheOri.oriCode[0] = u'a,1=\u554a\n'
xiaoheOri.splitOri()

xiaoheOri.changeKeyBoard(xiaohe17, {'w': 'e'})
xiaohe17.sortCharacters()
