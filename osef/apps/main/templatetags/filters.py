from django import template

register = template.Library()

@register.filter(name = 'money_format')
def money_format(value):
  return "{:,.2f}".format(value)