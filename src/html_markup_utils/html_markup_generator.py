import logging
from enum import Enum
import MarkupPy.markup as markup_py


class TemplateNames(Enum):
    CAMPAIGN = "CAMPAIGN"


def create_rich_text(items):
    markup = markup_py.page()
    for item in items:
        try:
            if item.text is not None:
                markup.p()
                markup.__getattr__(item.tag_name)(item.text, **item.attrs)
                markup.p.close()
            else:
                markup.p()
                markup.__getattr__(item.tag_name)()
                markup.p.close()
        except Exception as e:
            logging.exception(e)
    return str(markup)


def generate_campaign_template(html_body_template):
    description = html_body_template.description
    wysiwyg = html_body_template.wysiwyg
    collapsible_elements = html_body_template.collapsible_elements
    markup = markup_py.page()
    if description is not None:
        markup.p(description)
        markup.p(wysiwyg)
        for collapsible_element in collapsible_elements:
            markup.h3(collapsible_element.title)
            for body_element in collapsible_element.body_elements:
                markup.p()
                markup.__getattr__(body_element.tag_name)(body_element.text, **body_element.attrs)
                markup.p.close()
    return str(markup)


TEMPLATES = {
    "CAMPAIGN": generate_campaign_template
}


def generate(html_body_template, template_name=TemplateNames.CAMPAIGN.value):
    generate_func = TEMPLATES.get(template_name)
    if generate_func is not None:
        return generate_func(html_body_template)
