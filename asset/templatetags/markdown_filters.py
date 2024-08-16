"""implement markdown like syntax for text formatting"""

import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Regular expression to match markdown links
MARKDOWN_LINK_REGEX = r"\[([^\]]+)\]\(((?:http[s]?://)?[^\)]+)\)"


@register.filter(name="md_link")
def md_link(text, css_class="text-danger"):
    """Convert markdown links to HTML links"""

    def replace(match):
        # extract the link text and URL from the match
        link_text = match.group(1)
        link_url = match.group(2)

        return f"""<a href="{link_url}" target="_blank" class="{css_class}">{link_text}</a>"""

    converted_text = re.sub(MARKDOWN_LINK_REGEX, replace, text)
    return mark_safe(converted_text)
