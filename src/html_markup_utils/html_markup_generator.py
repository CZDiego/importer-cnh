from enum import Enum
import MarkupPy.markup as markup_py


class TemplateNames(Enum):
    CAMPAIGN = "CAMPAIGN"


def generate_campaign_template(**kwargs):
    description = kwargs.get("description")
    collapsible_elements = kwargs.get("collapsible_elements")
    markup = markup_py.page()
    if description is not None:
        markup.p(description)
        for collapsible_element in collapsible_elements:
            markup.h3(collapsible_element.title)
            markup.p(collapsible_element.body_elements)
    return markup


TEMPLATES = {
    "CAMPAIGN": generate_campaign_template
}


def generate(template_name=TemplateNames.CAMPAIGN.value, **kwargs):
    generate_func = TEMPLATES.get(template_name)
    print(generate_func)
    if generate_func is not None:
        return generate_func(**kwargs)
