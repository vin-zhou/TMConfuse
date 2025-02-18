#!/usr/bin/python3
# -*- Also compatible with Python2 -*- coding: utf-8 -*-
# 
from __future__ import unicode_literals
import os
import re
import sys
import random
from datetime import datetime

isPython2 = sys.version_info < (3, 0)
if isPython2:
    from io import open


class ConfuseBiz(object):
    # save configs
    @staticmethod
    def save_configs(configs):
        ConfuseBiz.configs = configs

    # 扫描某个目录，返回以特定后缀结尾的所有文件
    @staticmethod
    def scan_path(input_dirs, exclusive_dirs, suffixs):
        filelist = []
        for input_dir in input_dirs:
            log_info("Start scanning system direction {0}".format(input_dir), 0, True)
            if not os.path.isdir(input_dir):
                log_info("System direction {0} doesn't exist.".format(input_dir), 0, True)
                exit(-1)
            if suffixs:
                re_str = '.*\.[' + ''.join(suffixs) + ']$'
            pattern_suffix = re.compile(r'' + re_str)
            for filename in os.listdir(input_dir):
                path = os.path.join(input_dir, filename)
                if os.path.isdir(path):
                    shouldExclude = False
                    if exclusive_dirs:
                        for exclusive_dir in exclusive_dirs:
                            if path.startswith(exclusive_dir):
                                log_info('Skipping system direction {0}'.format(path), 2,
                                         True)
                                shouldExclude = True
                                break
                    if not shouldExclude:
                        filelist.extend(ConfuseBiz.scan_path([path], exclusive_dirs, suffixs))
                else:
                    matches = re.match(pattern_suffix, filename)
                    if matches:
                        filelist.append(path)
        return filelist

    @staticmethod
    def pre_format_file(file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path):
            file = open(file_path, 'r', encoding='utf-8', errors='ignore')
            try:
                file_content = file.read()
            except Exception as e:
                try:
                    file = open(file_path, 'r', encoding='ascii', errors='ignore')
                    file_content = file.read()
                except Exception as e:
                    try:
                        file = open(file_path, 'r', encoding='ISO-8859-1', errors='ignore')
                        file_content = file.read()
                    except Exception as e:
                        try:
                            file = open(file_path, 'r', encoding='gbk', errors='ignore')
                            file_content = file.read()
                        except Exception as e:
                            try:
                                file = open(file_path, 'r', encoding='Windows-1252', errors='ignore')
                                file_content = file.read()
                            except Exception as e:
                                log_file('no compatible encoding with ascii, utf-8, ISO-8859-1, gbk and Windows-1252, please have a self-check. {0}'.e, 3, True)
                            finally:
                                file.close()
                        finally:
                            file.close()
                    finally:
                        file.close()
                finally:
                    file.close()
            finally:
                file.close()

            # 去除注释
            file_content = ConfuseBiz.filter_useless_chars(file_content)

            # 去除空白行
            cleaned_lines = ConfuseBiz.clean_blank_lines(file_content)
            return cleaned_lines
        else:
            return []

    @staticmethod
    def clean_blank_lines(file_content):
        lines = file_content.split('\n')
        cleaned_lines = []
        for line in lines:
            if len(line.strip()) != 0:
                cleaned_lines.append(line)

        return cleaned_lines

    # 过滤无用字符
    @staticmethod
    def filter_useless_chars(file_content):
        # 移除单行注释和多行注释
        def _remove_comments(string):
            pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
            regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

            def _replacer(match):
                if match.group(2) is not None:
                    return ""
                else:
                    return match.group(1)

            return regex.sub(_replacer, string)

        file_str = _remove_comments(file_content)
        return file_str

    # 生成2个随机单词拼接成的字符串
    @staticmethod
    def confuse_text(text):
        firstArray = ['send', 'check', 'upload', 'refresh', 'has','rest', 'change', 'add', 'remove', 'is']
        secondArray = ['Item', 'UserInfo', 'MediaInfo', 'Route', 'Common', 'Chat', 'Commis']
        thirdArray = ['By', 'Of', 'With', 'And', 'From', 'To', 'In']
        forthArray = ['Home', 'DrawMap', 'MediaID', 'Message', 'Loaction', 'Username', 'My']
        fifthArray = ['Info', 'Count', 'Name', 'SystemId', 'Title', 'Topic', 'Action']
        word = random.choice(firstArray) + random.choice(secondArray) + random.choice(thirdArray) + random.choice(forthArray) + random.choice(fifthArray)
        return word
    #        word_file = "/usr/share/dict/words"
    #        WORDS = open(word_file).read().splitlines()
    #        word = random.choice(WORDS).lower()
    #        word += random.choice(WORDS).capitalize()

    # 生成唯一的字符串
    #        seeds = 'abcdefghijklmnopqrst'
    #        uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, text))
    #        uid = "".join(uid.split('-'))
    #        result = ""
    #        for c in uid:
    #            try:
    #                num = int(c)
    #                result += seeds[num]
    #            except Exception as e:
    #                result += c
    #        return result.upper()

    # 生成混淆文件
    @staticmethod
    def create_confuse_file(output_file, confused_dict):
        log_info("Start creating confuse file, file fullpath is {0}".format(os.path.realpath(output_file)), 2, True)
        f = open(output_file, 'wb')
        if isPython2:
            f.write(bytes('#ifndef NEED_CONFUSE_h\n').encode('utf-8'))
            f.write(bytes('#define NEED_CONFUSE_h\n').encode('utf-8'))
            f.write(bytes('// create time: {0}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))).encode('utf-8'))
            for (key, value) in confused_dict.items():
                f.write(bytes('#define {0} {1}\n'.format(key, value)).encode('utf-8'))
            f.write(bytes('#endif').encode('utf-8'))
        else:
            f.write(bytes('#ifndef NEED_CONFUSE_h\n', encoding='utf-8'))
            f.write(bytes('#define NEED_CONFUSE_h\n', encoding='utf-8'))
            f.write(bytes('// 生成时间： {0}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), encoding='utf-8'))
            for (key, value) in confused_dict.items():
                f.write(bytes('#define {0} {1}\n'.format(key, value), encoding='utf-8'))
            f.write(bytes('#endif', encoding='utf-8'))
        f.close()
        log_info("Complete create confuse file", 2, True)


class DealUserFile(object):
    """
    整理 Input Source codes
    """
    
    def __init__(self, input_dirs, exclusive_dirs):
        self.input_dirs = input_dirs
        self.exclusive_dirs = exclusive_dirs

    # 挑选需要关键字
    def parse_user_identifiers(self):
        user_file_paths = ConfuseBiz.scan_path(self.input_dirs, self.exclusive_dirs, ['h', 'm'])
        user_identifiers = []
        user_properties = []
        user_actions = []
        for file_full_path in user_file_paths:
            (identifiers, properties, actions) = self.__parse_user_file_content(file_full_path)
            user_identifiers += identifiers
            user_properties += properties
            user_actions += actions

        # 对字典去重
        user_identifiers = list(set(user_identifiers).difference(set(user_properties)))
        user_identifiers = list(set(user_identifiers).difference(set(user_actions)))
        return sorted(user_identifiers)

    # 挑选用户文件中的关键字, 去掉IBAction, init, property, 更严格些
    def __parse_user_file_content(self, file_full_path):
        file_local = file_full_path
        file_lines = ConfuseBiz.pre_format_file(file_local)
        # 读取文件行
        identifier_array = []
        user_property = []
        user_action = []
        # 一行一行的读取文件
        log_info("Start extracting confusing identifiers {0} ".format(file_local), 0, True)
        for line in file_lines:
            # 宏定义内容不用管
            if line.startswith('#'):
                continue
            # xib连线
            if 'IBAction' in line:
                func_regex = '\s*(\w+)\s*:\s*\(\s*\w*\s*\s*\w+\s*\*?\s*\)\s*\w+\s*'
                matches = re.findall(func_regex, line)
                if matches:
                    user_action += matches
                continue
            # init开头的方法不用管
            if 'init' in line:
                continue
            # 去掉property, 防止懒加载
            if line.startswith('@property'):
                pattern_search = re.compile(r'[\s+|*](\w*);.*$')
                matches = re.findall(pattern_search, line)
                if matches:
                    user_property += matches
                continue
            # 方法名
            if '+' in line or '-' in line:
                func_regex = '\s*(\w+)\s*:\s*\(\s*\w*\s*\s*\w+\s*\*?\s*\)\s*\w+\s*'
                #不带参数
                func_simple_regex = '\s*[-\+]\s*\(\s*\w+\s*\*?\)\s*(\w+)\s*;*'
                matches = re.findall(func_regex, line)
                if len(re.findall(func_simple_regex, line)) >= 1:
                    matches += re.findall(func_simple_regex, line)
                if matches:
                    for match in matches:
                        # set、get、_开头的方法不用管
                        if re.match(r'^set|^get|^_', match):
                            continue
                        # 去除中文
                        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
                        if zh_pattern.search(match):
                            continue
                        # 去除纯数字
                        if match.isdigit():
                            continue

                        identifier_array.append(match)
        return (identifier_array, user_property, user_action)


class DealSystemIdentifiers(object):
    """
    整理系统关键字
    """

    def __init__(self, system_file_dirs):
        self.system_file_dirs = system_file_dirs

    def parse_system_identifiers(self):
        system_file_paths = ConfuseBiz.scan_path(self.system_file_dirs, None, ['h'])
        system_identifiers = []
        for file_full_path in system_file_paths:
            identifier_array = self.__parse_system_file_content(file_full_path)
            if len(identifier_array):
                system_identifiers += identifier_array

        # 对字典去重并排序
        return sorted(list(set(system_identifiers)))

    # 挑选系统文件中的关键字
    def __parse_system_file_content(self, file_full_path):
        file_local = file_full_path
        file_lines = ConfuseBiz.pre_format_file(file_local)
        identifier_array = []
        # 读取文件行
        pattern_split = re.compile(r'\W')
        pattern_clean = re.compile(r'[\s+\W*\d+]')
        log_info("Start extracting system identifiers {0} ".format(file_local), 0, True)
        for line in file_lines:
            matches = re.split(pattern_split, line)
            if len(matches):
                # 遍历结果集，去除无用结果
                for res in matches:
                    # 去除None
                    if not res:
                        continue
                    # 去除空白字符，非单词字符，b\，纯数字
                    if not re.match(pattern_clean, str(res)):
                        identifier_array.append(str(res))
        return identifier_array


class DealCleanIdentifers(object):
    """
    整理需要清除的关键字
    """

    def __init__(self, clean_file_dirs):
        self.clean_file_dirs = clean_file_dirs

    def parse_clean_identifiers(self):
        clean_file_paths = ConfuseBiz.scan_path(self.clean_file_dirs, None, ['h', 'm'])
        clean_identifiers = []
        for file_full_path in clean_file_paths:
            identifier_array = self.__parse_clean_file_content(file_full_path)
            if len(identifier_array):
                clean_identifiers += identifier_array

        # 对字典去重并排序
        return sorted(list(set(clean_identifiers)))

    # 挑选需要排除的文件中的关键字, 包含了property, _变量，block，方法, 方法参数等，更广泛些
    def __parse_clean_file_content(self, file_full_path):
        file_local = file_full_path
        file_lines = ConfuseBiz.pre_format_file(file_local)
        # 读取文件行
        identifier_array = []
        for line in file_lines:
            # @property
            if line.startswith('@property'):
                pattern_search = re.compile(r'[\s+|*](\w*);.*$')
                matches = re.findall(pattern_search, line)
                if matches:
                    identifier_array += matches
            # 以_开头的变量名
            if '_' in line:
                pattern_search = re.compile(r'.*?_(\w*)[. =\)].*')
                matches = re.findall(pattern_search, line)
                if matches:
                    identifier_array += matches
            # void (^block)(void);
            if '^' in line:
                pattern_search = re.compile(r'\(\^(\w*)\).*')
                matches = re.findall(pattern_search, line)
                if matches:
                    identifier_array += matches
            # 方法名，参数等
            if '+' in line or '-' in line:
                # 判断参数个数
                parameter_pattern = re.compile(r'.*?(\(.*?\)).*?')
                if len(re.findall(parameter_pattern, line)) <= 1:
                    # 检测'- (NSInteger)tableView {'
                    pattern_search = re.compile(r'[)\s+](\w+):?.*?')
                else:
                    pattern_search = re.compile(r'[)\s+](\w+):.*?')
                matches = re.findall(pattern_search, line)
                if matches:
                    for match in matches:
                        # set、get、_开头的方法不用管
                        if re.match(r'^set|^get|^_', match):
                            continue
                        # 去除中文
                        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
                        if zh_pattern.search(match):
                            continue
                        # 去除纯数字
                        if match.isdigit():
                            continue
                        identifier_array.append(match)
        return identifier_array


class DealIgnoreKey(object):
    """
    整理忽略的特殊关键字
    """

    def __init__(self, ignore_key_dir):
        self.ignore_key_dir = ignore_key_dir

    # 挑选需要关键字
    def ignore_key(self):
        file = open(self.ignore_key_dir)
        keys = []
        for line in file:
            keys.append(line.strip('\n'))
        file.close()

        return keys


# 打印方法
log_file = None


def log_info(info, level=1, to_log_file=False):
    """
    打印到控制台
    0 不打印
    1 info
    2 warning
    3 error
    """
    print_infos = info
    if level == 1:
        print(print_infos)
    elif level == 2:
        print('\033[0;32m{0}\033[0m'.format(print_infos))
    elif level == 3:
        print('\033[0;31m╔═════════════════════════════════ ERROR ═════════════════════════════════╗\033[0m')
        print('\033[0;31m║\033[0m')
        print('\033[0;31m║ {0}\033[0m'.format(print_infos))
        print('\033[0;31m║\033[0m')
        print('\033[0;31m╚═════════════════════════════════════════════════════════════════════════╝\033[0m')
    if to_log_file:
        # 写入文件
        if isPython2:
            log_file.write('{0}\n'.format(print_infos))
        else:
            log_file.write('{0}\n'.format(print_infos))


def usage():
    help_info = """
-i\t必须，项目需要处理的主要文件所在的目录
-s\t可选，配置系统Framework文件的目录，一般用于做排除字典，避免替换系统关键字，iOS SDK path /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks
-e\t可选，用于存放不扫描处理的文件的目录，比如Swift文件目录
-c\t可选，用于存放排除关键字的文件的目录，例如Pods下的目录，或者静态库（头文件修改后会出错）
-k\t可选，用于存放需要过滤的key
-o\t必须，输出文件的目录，用于输出关键字、日志以及最后生成的混淆头文件的目录

Example:

python /Users/wuaming/Desktop/TMConfuse/CodeConfuse/Confuse.py \
-i /Users/wuaming/Desktop/TMConfuse/TMConfuse \
-s /Users/wuaming/Desktop/TMConfuse/System_Frameworks_iOS \
-k /Users/wuaming/Desktop/TMConfuse/CodeConfuse/ignoreKey.txt \
-o /Users/wuaming/Desktop/TMConfuse/CodeConfuse
"""
    print(help_info)

def scanSystemIdentifiers(system_dirs):
    log_info("Start scanning System identifiers...", 2, True)
    system_identifiers = DealSystemIdentifiers(system_dirs).parse_system_identifiers()
    log_info("Complete scan System identifiers...", 2, True)
    return system_identifiers

if __name__ == '__main__':
    
    # use relative path to set the config since it will be auto runed by Xcode.
    cwd = os.getcwd() # for XCode, it's ${SRCROOT}, i.e. Zoom; for Python console, it's Zoom/Scripts.
    workDir = cwd # for Xcode, use it directly.
#    workDir = os.path.dirname(cwd) # for terminal, we should use it's parent folder.

    # 获取参数
    input_dirs = [os.path.join(workDir, "TMConfuse")]  # 项目需要处理的主要文件所在的目录
    system_dirs = [os.path.join(workDir, "System_Frameworks_iOS")]  # 配置系统Framework文件的目录，一般用于做排除字典，避免替换系统关键字
    # system_dirs = ["/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks"]
    exclusive_dirs = None  # 用于存放不扫描处理的文件的目录，比如Swift文件目录
    clean_dirs = None  # 用于存放排除关键字的文件的目录，例如Pods下的目录，或者静态库（头文件修改后会出错）
    ignore_key_dir = os.path.join(workDir, "CodeConfuse/ignoreKey.txt")  #用于存放需要过滤的key
    output_dir = os.path.join(workDir, "CodeConfuse")  # 输出文件的目录，用于输出关键字、日志以及最后生成的混淆头文件的目录

    # 保存配置信息
    configs = {
        'input_dirs': input_dirs,
        'system_dirs': system_dirs,
        'exclusive_dirs': exclusive_dirs,
        'clean_dirs': clean_dirs,
        'ignore_key_dir': ignore_key_dir,
        'output_dir': output_dir
    }
    ConfuseBiz.save_configs(configs)

    # 初始化日志打印文件
    log_file = open(os.path.join(output_dir, 'confuse_log.log'), 'w')

    # 获取系统文件关键字并写入文件
    system_identifiers = []
    system_identifiers_fileName = os.path.join(output_dir, 'system_identifiers.txt')
    if os.path.getsize(system_identifiers_fileName): # file not empty, read directly
        with open(system_identifiers_fileName, 'r') as f:
            log_info("Read System identifiers directly from {0}".format(system_identifiers_fileName), 1, True)
            for line in f:
                system_identifiers.append(line.strip())
    else:  # scan system_dirs and save values to file
        system_identifiers = scanSystemIdentifiers(system_dirs)
        log_info("Start writing System identifiers into Dict File, File fullpath is {0}".format(system_identifiers_fileName), 1, True)
        system_identifiers_record_file = open(system_identifiers_fileName, 'wb')
        if isPython2:
            for item in system_identifiers:
                system_identifiers_record_file.write(bytes(item).encode('utf-8'))
                system_identifiers_record_file.write(bytes('\n').encode('utf-8'))
        else:
            for item in system_identifiers:
                system_identifiers_record_file.write(bytes(item, encoding='utf-8'))
                system_identifiers_record_file.write(bytes('\n', encoding='utf-8'))
        # 关闭文件读写
        system_identifiers_record_file.close()
        log_info("Complete write System identifiers into Dict File", 1, True)

    # 遍历用户指定目录，提取关键字，主要提取方法名
    log_info("Start scanning assign need deal files' identifiers...", 2, True)
    user_identifiers = DealUserFile(input_dirs, exclusive_dirs).parse_user_identifiers()

    # 将系统关键字去除
    log_info("Start excluding system identifiers...", 2, True)
    system_intersect_identifiers = list(set(system_identifiers).intersection(set(user_identifiers)))
    diff_identifiers = list(set(user_identifiers).difference(set(system_intersect_identifiers)))

    # 将排除目录的关键字去除
    if clean_dirs:
        # 遍历排除关键字的文件目录，提取关键字，并写入文件
        log_info("Start scanning assign Clean identifiers...", 2, True)
        clean_identifiers = DealCleanIdentifers(clean_dirs).parse_clean_identifiers()
        log_info("Start writing Clean identifiers into Dict File, File fullpath is {0}".format(
            os.path.join(output_dir, 'clean_identifiers.txt')), 1, True)
        clean_identifiers_record_file = open(os.path.join(output_dir, 'clean_identifiers.txt'), 'wb')
        if isPython2:
            for item in clean_identifiers:
                clean_identifiers_record_file.write(bytes(item).encode('utf-8'))
                clean_identifiers_record_file.write(bytes('\n').encode('utf-8'))
        else:
            for item in clean_identifiers:
                clean_identifiers_record_file.write(bytes(item, encoding='utf-8'))
                clean_identifiers_record_file.write(bytes('\n', encoding='utf-8'))
        # 关闭文件读写
        clean_identifiers_record_file.close()
        log_info("Complete write Clean identifiers into Dict File", 1, True)
        
        log_info("Start excluding clean identifiers...", 2, True)
        clean_intersect_identifiers = list(set(clean_identifiers).intersection(set(user_identifiers)))
        diff_identifiers = list(set(diff_identifiers).difference(set(clean_intersect_identifiers)))

    # 将特殊字段去除
    log_info("Start excluding ignore keys...", 2, True)
    ignore_keys = DealIgnoreKey(ignore_key_dir).ignore_key()
    diff_identifiers = list(set(diff_identifiers).difference(set(ignore_keys)))
    # 重新去重排序
    diff_identifiers = sorted(list(set(diff_identifiers)))

    # 写入文件
    log_info("Start writing need deal files' identifiers into Dict File, File fullpath is {0}".format(
        os.path.join(output_dir, 'user_identifiers.txt')), 2, True)
    user_identifiers_file = open(os.path.join(output_dir, 'user_identifiers.txt'), 'wb')
    for item in diff_identifiers:
        if isPython2:
            user_identifiers_file.write(bytes(item).encode('utf-8'))
            user_identifiers_file.write(bytes('\n').encode('utf-8'))
        else:
            user_identifiers_file.write(bytes(item, encoding='utf-8'))
            user_identifiers_file.write(bytes('\n', encoding='utf-8'))
    user_identifiers_file.close()
    log_info("Complete write need deal files' identifiers into Dict File", 1, True)

    # 生成混淆文件
    confused_dict = {}
    diff_dic = []
    for item in diff_identifiers:
        randomNum = random.randint(0,4)
        if randomNum == 0:
            confused_dict[item] = random.choice(['zndy_', 'tim_']) + item
        else:
            confused_word = ConfuseBiz.confuse_text(item)
            while confused_word in diff_dic:
                confused_word = ConfuseBiz.confuse_text(item)
            diff_dic.append(confused_word)
            confused_dict[item] = confused_word
    ConfuseBiz.create_confuse_file(os.path.join(output_dir, 'Confuse.h'), confused_dict)
    log_info("You can browse run logs in file {0}".format(os.path.join(output_dir, 'confuse_log.log')), 1, True)
    log_file.close()
