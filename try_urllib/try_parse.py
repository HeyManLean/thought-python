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

    query_string = parse.urlencode(params_dict)
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




if __name__ == '__main__':
    test_urlparse()
