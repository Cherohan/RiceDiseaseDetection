'''
from django import template

register = template.library()

# 自定义过滤器，实现大写转换
@register.filter
def myupper(val):
    # print('val from template:', val)
    return val.upper()

# 自定义标签,实现减法运算
@register.simple_tag
def jian(a, b):
    res = int(a) - int(b)
    return res
'''