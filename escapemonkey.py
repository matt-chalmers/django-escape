"""
This module implements a stronger html escaping than the standard Django offering, to increase
safety when placing text into html element attributes.
"""

import six

from django.utils.encoding import force_text
from django.utils.functional import keep_lazy
from django.utils.safestring import SafeText, mark_safe


unichr = six.unichr


HTML_ESCAPE_FMT = u'&#x%X;'
HTML_NOESCAPE_CHARS = u'._'
HTML_ESCAPE_MAP = {
    unichr(code): (
        unichr(code)
        if unichr(code).isalnum() or unichr(code) in HTML_NOESCAPE_CHARS
        else HTML_ESCAPE_FMT % code
    )
    for code in range(256)
}


@keep_lazy(six.text_type, SafeText)
def escape_html(text):
    text = force_text(text)
    text = u''.join([
        HTML_ESCAPE_MAP.get(ch) or (HTML_ESCAPE_FMT % ord(ch))
        for ch in text
    ])
    return mark_safe(text)


def install():
    import django.utils.html
    django.utils.html.escape = escape_html
