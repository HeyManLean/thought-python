#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib import parse


def test_urlparse():
    """
    解析整个 url，提取到各个组件中
    scheme://netloc/path;parameters?query#fragment
    """
    url = 'https://www.example.com/#/data?channel=1&date=2019-02-22'
    parse_ret = parse.urlparse(url)
    print(parse_ret)
    # ParseResult(scheme='https', netloc='www.example.com', path='/', params='', query='', fragment='/data?channel=1&date=2019-02-22')

    url = 'https://www.example.com/posts;python?offset=20&limit=10#文章'
    parse_ret = parse.urlparse(url)
    print(parse_ret)
    # ParseResult(scheme='https', netloc='www.example.com', path='/posts', params='python', query='offset=20&limit=10', fragment='文章')

    url = parse.urlunparse(parse_ret)
    print(url)
    # https://www.example.com/posts;python?offset=20&limit=10#文章

    parse_ret = parse.urlsplit(url)  # 似 urlparse, 但不支持params
    print(parse_ret)
    # SplitResult(scheme='https', netloc='www.example.com', path='/posts;python', query='offset=20&limit=10', fragment='文章')

    url = parse.urlunsplit(parse_ret)
    print(url)
    # https://www.example.com/posts;python?offset=20&limit=10#文章

    params_dict = parse.parse_qs(parse_ret.query)
    print(params_dict)
    # {'offset': ['20'], 'limit': ['10']}
    
    params_dict = parse.parse_qsl(parse_ret.query)
    print(params_dict)
    # [('offset', '20'), ('limit', '10')]

    query_string = parse.urlencode(params_dict)  # 将 key-value 形式生成 query 串
    print(query_string)
    # offset=20&limit=10

    # 替换文件或者整个uri
    url1 = parse.urljoin(url, 'articles')
    print(url1)
    # https://www.example.com/articles
    url1 = parse.urljoin(url, '//www.example1.com/articles')
    print(url1)
    # https://www.example1.com/articles

    url2 = parse.urldefrag(url)
    print(url2)
    # DefragResult(url='https://www.example.com/posts;python?offset=20&limit=10', fragment='文章')


def test_quote():
    """测试 url 转义编码 - for non-ASCII"""
    url = 'https://www.example.com/posts;python?offset=20&limit=10#文章'
    quote_url = parse.quote(url)
    print(quote_url)  # safe 默认为 '/', 所以没转义
    # https%3A//www.example.com/posts%3Bpython%3Foffset%3D20%26limit%3D10%23%E6%96%87%E7%AB%A0
    quote_url = parse.quote(url, safe='')
    print(quote_url)
    # https%3A%2F%2Fwww.example.com%2Fposts%3Bpython%3Foffset%3D20%26limit%3D10%23%E6%96%87%E7%AB%A0
    
    plus_url = 'https://www.example.com/posts; python?offset=20&limit=10# 文章'
    quote_plus_url = parse.quote_plus(plus_url)  # 默认 safe 为 '', 且可以编码空字符 ' '
    print(quote_plus_url)
    # https%3A%2F%2Fwww.example.com%2Fposts%3B+python%3Foffset%3D20%26limit%3D10%23+%E6%96%87%E7%AB%A0

    unquote_url = parse.unquote(quote_url)
    print(unquote_url)
    # https://www.example.com/posts;python?offset=20&limit=10#文章

    unquote_url = parse.unquote(quote_plus_url)  # 不支持空字符 ' '
    print(unquote_url)
    # https://www.example.com/posts;+python?offset=20&limit=10#+文章

    unquote_plus_url = parse.unquote_plus(quote_plus_url)
    print(unquote_plus_url)
    # https://www.example.com/posts; python?offset=20&limit=10# 文章


if __name__ == '__main__':
    test_urlparse()
    test_quote()
