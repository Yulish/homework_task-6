from django import template
import re

register = template.Library()

BAD_WORDS = [
    'Трамп',
    'негр',


]
pattern = re.compile(r'\b(' + '|'.join(BAD_WORDS) + r')\b', flags=re.IGNORECASE)


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError(f'Ошибка! Переменная должна быть "str"')
    def replace(match):
        word = match.group()
        return (word[0] + '*' * (len(word) - 1))

    return pattern.sub(replace, value)