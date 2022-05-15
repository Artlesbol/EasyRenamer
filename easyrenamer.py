# -*- coding: utf-8 -*-
import argparse
import os
import sys
import re


def replace(str, rules, case):
    """工具函数-替换

    Parameters
    ----------
    str : string
        待处理字符串
    rules : list
        正则表达式和目标字符串的列表
    case : bool
        忽略大小写标记

    Returns
    -------
    string
        处理结果
    """
    # 解析规则
    [srouce_rule, target_rule] = rules
    if case:
        # 忽略大小写
        return re.sub(srouce_rule, target_rule, str, flags=re.IGNORECASE)
    else:
        # 正则表达式匹配并替换
        return re.sub(srouce_rule, target_rule, str)


def delate(str, des, case):
    """工具函数-删除

    Parameters
    ----------
    str : string
        待处理字符串
    des : string
        被删除函数-正则表达式
    case : bool
        忽略大小写标记

    Returns
    -------
    string
        处理结果
    """
    srouce_rule = des
    target_rule = ""
    rules = [srouce_rule, target_rule]
    return replace(str, rules, case)


def insert(str, index, des):
    """工具函数-插入

    Parameters
    ----------
    str : string
        待处理字符串
    index : int
        插入位置下标
    des : string
        插入的字符串

    Returns
    -------
    string
        处理结果
    """
    return str[0:index]+des+str[index:]


def insert_head(str, des):
    """工具函数-在头部插入

    Parameters
    ----------
    str : string
        待处理字符串
    des : string
        插入的字符串

    Returns
    -------
    string
        处理结果
    """
    str = insert(str, 0, des)
    return str


def insert_tail(str, des):
    """工具函数-在尾部插入

    Parameters
    ----------
    str : string
        待处理字符串
    des : string
        插入的字符串

    Returns
    -------
    string
        处理结果
    """
    str = insert(str, len(str), des)
    return str


def insert_after(str, src, des, case):
    """工具函数-在匹配位置后插入

    Parameters
    ----------
    str : string
        待处理字符串
    src : string
        匹配的正则表达式
    des : string
        插入的字符串
    case : bool
        忽略大小写标记

    Returns
    -------
    string
        处理结果
    """
    srouce_rule = src
    target_rule = src + des
    rules = [srouce_rule, target_rule]
    str = replace(str, rules, case)
    return str


def get_suffix(filename):
    """获取文件后缀名

    Parameters
    ----------
    filename : string
        文件名

    Returns
    -------
    string
        后缀名（包含.）
    """
    rule = re.compile(r"\.([^\.]*)?$")
    suffix = rule.search(filename)
    if suffix is None:
        suffix = ""
    else:
        suffix = suffix[0]
    return suffix


special_character = ['\\', '^', '$', '*', '?', '+', '[', ']', '(', ')']


# 处理函数
def replace_handle(args, parser):
    """替换命令处理流程

    Parameters
    ----------
    args : Namespace
        参数的Namespace
    parser : parser对象
        解析器的parser对象
    """
    source = args.source
    regular = args.regular
    if source and not regular:
        for c in special_character:
            source = source.replace(c, "\\"+c)

    destination = args.destination
    path = args.directory
    if not os.path.isabs(path):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        path = os.path.join(dirname, path)
        
    suffix_set = args.S
    withsuffix = args.withsuffix
    case = args.case

    change_flag = False
    for file in os.listdir(path):
        if len(suffix_set) > 0:
            if get_suffix(file)[1:] not in suffix_set:
                continue
        name = file
        suffix = get_suffix(file)
        if not withsuffix:
            if len(suffix) > 0:
                name = name[0:-len(suffix)]
        newName = replace(name, [source, destination], case)
        if not withsuffix:
            newName += suffix
        if file != newName:
            print(file, '->', newName)
            change_flag = True
        os.rename(os.path.join(path, file), os.path.join(path, newName))

    if change_flag is False:
        print('未发生变化')


def insert_handle(args, parser):
    """插入命令处理流程

    Parameters
    ----------
    args : Namespace
        参数的Namespace
    parser : parser对象
        解析器的parser对象
    """
    # 解析参数列表
    source = args.source
    regular = args.regular
    if source and not regular:
        for c in special_character:
            source = source.replace(c, "\\"+c)
    back = args.back
    front = args.front
    destination = args.destination

    path = args.directory
    if not os.path.isabs(path):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        path = os.path.join(dirname, path)

    suffix_set = args.S
    withsuffix = args.withsuffix
    case = args.case

    # 批处理文件名
    change_flag = False
    for file in os.listdir(path):
        # 安全校验
        if len(suffix_set) > 0:
            if get_suffix(file)[1:] not in suffix_set:
                continue
        name = file
        # 后缀名校验
        suffix = get_suffix(file)
        if not withsuffix:
            if len(suffix) > 0:
                name = name[0:-len(suffix)]

        # 插入处理
        if back:
            newName = insert_tail(name, destination)
        elif front:
            newName = insert_head(name, destination)
        else:
            newName = insert_after(name, [source, destination], case)

        # 后缀名合成
        if not withsuffix:
            newName += suffix
        if file != newName:
            print(file, '->', newName)
            change_flag = True

        # 保存为新文件名
        os.rename(os.path.join(path, file), os.path.join(path, newName))

    if change_flag is False:
        print('未发生变化')


def delate_handle(args, parser):
    """删除命令处理流程

    Parameters
    ----------
    args : Namespace
        参数的Namespace
    parser : parser对象
        解析器的parser对象
    """
    source = args.source
    regular = args.regular
    if source and not regular:
        for c in special_character:
            source = source.replace(c, "\\"+c)

    path = args.directory
    if not os.path.isabs(path):
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        path = os.path.join(dirname, path)

    suffix_set = args.S
    withsuffix = args.withsuffix
    case = args.case

    change_flag = False
    for file in os.listdir(path):
        if len(suffix_set) > 0:
            if get_suffix(file)[1:] not in suffix_set:
                continue
        name = file
        suffix = get_suffix(file)
        if not withsuffix:
            if len(suffix) > 0:
                name = name[0:-len(suffix)]

        newName = delate(name, source, case)

        if not withsuffix:
            newName += suffix
        if file != newName:
            print(file, '->', newName)
            change_flag = True
        try:
            os.rename(os.path.join(path, file), os.path.join(path, newName))
        except FileExistsError:
            print(f'[{source}]删除后[{newName}]发生重名，请处理冲突')

    if change_flag is False:
        print('未发生变化')


def default_handle(args, parser):
    """默认流程

    Parameters
    ----------
    args : Namespace
        参数的Namespace
    parser : parser对象
        解析器的parser对象
    """
    parser.print_help()


def main():
    parser = argparse.ArgumentParser(description="一个简单的Windows重命名批处理工具")

    parser.set_defaults(func=default_handle)

    subparsers = parser.add_subparsers()

    replace_parser = subparsers.add_parser('replace', help="替换模式")
    replace_parser.add_argument(
        '-s', '--source', type=str, help="替换源", required=True)
    replace_parser.add_argument(
        '-d', '--destination', type=str, help="替换字段", required=True)
    replace_parser.set_defaults(func=replace_handle)
    replace_parser.add_argument('-S', default=[], type=str,
                                nargs='*', help="指定后缀集", metavar='suffix')
    replace_parser.add_argument('--case', default=False,
                                action='store_true', help="忽略大小写")
    replace_parser.add_argument('--withsuffix', default=False,
                                action='store_true', help="处理后缀名")
    replace_parser.add_argument('--regular', default=False,
                                action='store_true', help='正则匹配')
    replace_parser.add_argument('directory', help="文件目录")

    insert_parser = subparsers.add_parser('insert', help="插入模式")
    insert_option_group = insert_parser.add_mutually_exclusive_group(
        required=True)
    insert_option_group.add_argument('-s', '--source', type=str, help="插入处")
    insert_option_group.add_argument('-b', '--back', default=False,
                                     action='store_true', help="在最前方插入")
    insert_option_group.add_argument('-f', '--front', default=False,
                                     action='store_true', help="在最后方插入")
    insert_parser.add_argument('-S', default=[], type=str,
                               nargs='*', help="指定后缀集", metavar='suffix')
    insert_parser.add_argument('--case', default=False,
                               action='store_true', help="忽略大小写")
    insert_parser.add_argument('--withsuffix', default=False,
                               action='store_true', help="处理后缀名")
    insert_parser.add_argument('--regular', default=False,
                               action='store_true', help='正则匹配')
    insert_parser.add_argument('directory', help="文件目录")
    insert_parser.add_argument(
        '-d', '--destination', type=str, help="插入字段", required=True)
    insert_parser.set_defaults(func=insert_handle)

    delate_parser = subparsers.add_parser('delate', help="删除模式")
    delate_parser.add_argument(
        '-s', '--source', type=str, help="删除字段", required=True)
    delate_parser.set_defaults(func=delate_handle)
    delate_parser.add_argument('-S', default=[], type=str,
                               nargs='*', help="指定后缀集", metavar='suffix')
    delate_parser.add_argument('--case', default=False,
                               action='store_true', help="忽略大小写")
    delate_parser.add_argument('--withsuffix', default=False,
                               action='store_true', help="处理后缀名")
    delate_parser.add_argument('--regular', default=False,
                               action='store_true', help='正则匹配')
    delate_parser.add_argument('directory', help="文件目录")

    version_doc = """
    EasyRename version 1.0 \n
    Copyright © 2022 刘立博 All Rights Reserved
    """
    parser.add_argument('-v', '--version', action='version',
                        version=version_doc, help='关于我')

    args = parser.parse_args()
    args.func(args, parser)


if __name__ == '__main__':
    main()
