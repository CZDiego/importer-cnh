import logging
import json
from variables import *
import html_markup_utils.html_markup_generator as html_markup_generator
import service.importer_service as importer_service
from models import CollapsibleElement, Resource, HTMLElement, CampaignHTMLBodyTemplate, TransformHeaders, \
    DealershipTypes
import utils
import service.preprocess as preprocessing

TemplateNames = html_markup_generator.TemplateNames

# TODO: Read excel file from local volume instead of having it in docker container
EXCEL_PATH = r'/export-content-20210302121846.xlsx'

# Main
pieces_of_content = preprocessing.get_pieces_of_content(EXCEL_PATH)

json_array = []

for i in range(0, len(pieces_of_content)):
    # json_array.append(pieces_of_content[i].__dict__)
    json_array.append(utils.remove_nones_from_dict(pieces_of_content[i].__dict__))


def get_downloads_rich_text(downloads):
    html_downloads = []
    for download in downloads:
        text = download.get("title")
        file_name = download.get("fileName", "#")
        file_name = "#" if file_name is None else file_name
        link = WEBSPHERE_VARIABLES.get("StorageAPIBaseURL") + file_name
        attrs = dict(href=link, target="_blank")
        html_downloads.append(HTMLElement("a", text=text, attrs=attrs))
    return html_downloads


def get_related_content_rich_text(related_content):
    html_related_content = []
    for content in related_content:
        text = content.get("title")
        # TODO add real link
        link = "#"
        attrs = dict(href=link)
        html_related_content.append(HTMLElement("a", text=text, attrs=attrs))
    return html_related_content


def map_item(item):
    content_type = item.get("contentType")
    if content_type is not None or content_type is not "page":
        downloads = item.get("downloads")
        item["originalDownloads"] = downloads
        related_content = item.get("relatedContent")
        html_downloads = []
        html_related_content = []
        if downloads is not None:
            html_downloads = get_downloads_rich_text(downloads)
        if related_content is not None:
            html_related_content = get_related_content_rich_text([dict(title=item.get("pageTitle"))])
        item["downloads"] = html_markup_generator.create_rich_text(html_downloads)
        item["relatedContent"] = html_markup_generator.create_rich_text(html_related_content)
    item["originalName"] = item["name"]
    master_id = "-" + str(item["masterId"]) if item["masterId"] is not None else ""
    item["name"] = item["name"] + str(master_id)
    return item


json_array = list(map(map_item, json_array))
json_data = json.dumps(json_array, indent=2)


def init_migration(items):
    print(json.dumps(items, indent=2))
    posts = []
    kits = []
    pages = []
    for item in items:
        try:
            content_type = item.get("contentType")
            if content_type is "post" or content_type is "kit":
                print("Saving " + content_type)
                del item["contentType"]
                response = importer_service.save_item(item)
                print(json.dumps(response, indent=2))
                saved_item = dict(response=response, item=item)
                posts.append(saved_item) if content_type is "post" else kits.append(saved_item)
            elif content_type is "page":
                page_type = item.get("pageType", "campaign").lower()
                html_posts = []
                for post in posts:
                    post_item = post.get("item")
                    post_response = post.get("response")
                    text = post_item.get("title")
                    uuid = post_response.get("newId")
                    path = post_response.get("path")
                    link = utils.create_websphere_link(uuid, path)
                    attrs = dict(href=link)
                    html_posts.append(HTMLElement("a", text=text, attrs=attrs))
                item["relatedContent"] = html_markup_generator.create_rich_text(html_posts)
                print(page_type)
                if page_type == "product" or page_type == "generic":
                    print("Inside product or generic")
                    html_kits = ""
                    print(kits)
                    for kit in kits:
                        kit_item = kit.get("item")
                        downloads = kit_item.get("downloads")
                        html_kits += downloads
                    print(html_kits)
                    item["downloads"] = html_kits
                    body = CampaignHTMLBodyTemplate(item.get("description", ""), item.get("wysiwyg", ""))
                    print("body")
                    item["body"] = html_markup_generator.generate(body, template_name=TemplateNames.CAMPAIGN.value)
                elif page_type == "campaign":
                    print("Inside campaign")
                    html_kits = []
                    for kit in kits:
                        kit_item = kit.get("item")
                        title = kit_item.get("title")
                        original_downloads = kit_item.get("originalDownloads")
                        body_elements = get_downloads_rich_text(original_downloads)
                        html_kits.append(CollapsibleElement(title, body_elements=body_elements))
                    body = CampaignHTMLBodyTemplate(item.get("description", ""), item.get("wysiwyg", ""), html_kits)
                    item["body"] = html_markup_generator.generate(body, template_name=TemplateNames.CAMPAIGN.value)
                print("Saving page")
                del item["contentType"]
                item["transformHeadersH3"] = TransformHeaders.COLLAPSIBLE_SECTIONS.value
                saved_page = importer_service.save_item(item)
                print(json.dumps(saved_page, indent=2))
                saved_page["posts"] = posts
                saved_page["kits"] = kits
                pages.append(saved_page)
                kits = []
                posts = []

        except Exception as e:
            logging.exception(e)


init_migration(json_array)

# print(json_data)
print("-------------------------------------------")
"""
TemplateNames = html_markup_generator.TemplateNames

authoringTemplateName = "Resource"
contentLibraryName = "content-english"
path = "cnhi/discover/internal/resources"

try:
    kit1 = HTMLElement("a", text="Google", attrs={"href": "https://www.google.com"})
    kit2 = HTMLElement("a", text="Facebook", attrs={"href": "https://www.facebook.com"})
    kit3 = HTMLElement("a", text="Instagram", attrs={"href": "https://www.instagram.com"})
    kit4 = HTMLElement("a", text="Apple", attrs={"href": "https://www.apple.com"})
    post = Resource(name="post-1", title="Post 1", authoringTemplateName=authoringTemplateName,
                    contentLibraryName=contentLibraryName, path=path,
                    transformHeadersH3=TransformHeaders.COLLAPSIBLE_SECTIONS.value)
    post2 = Resource(name="post-2", title="Post 2", authoringTemplateName=authoringTemplateName,
                     contentLibraryName=contentLibraryName, path=path,
                     transformHeadersH3=TransformHeaders.COLLAPSIBLE_SECTIONS.value)
    result_post_1 = importer_service.save_item(post.to_dict())
    result_post_2 = importer_service.save_item(post2.to_dict())
    related_post_1 = HTMLElement("a", text=result_post_1.get("title", ""),
                                 attrs={"href": utils.create_websphere_link(result_post_1.get("newId", ""),
                                                                            result_post_1.get("path", ""))})
    related_post_2 = HTMLElement("a", text=result_post_2.get("title", ""),
                                 attrs={"href": utils.create_websphere_link(result_post_2.get("newId", ""),
                                                                            result_post_2.get("path", ""))})
    kit_file1 = HTMLElement("a", text="20201208 CanadaContent (2) (1).json",
                            attrs={"href": WEBSPHERE_VARIABLES.get(
                                "StorageAPIBaseURL") + "20201208 CanadaContent (2) (1).json",
                                   "target": "_blank"})
    kit_file2 = HTMLElement("a", text="tbio_config (1).jsp",
                            attrs={"href": WEBSPHERE_VARIABLES.get("StorageAPIBaseURL") + "tbio_config (1).jsp",
                                   "target": "_blank"})
    collapsible_elements = [CollapsibleElement("My first title", [kit1, kit2]),
                            CollapsibleElement("My second title", [kit3, kit4]),
                            CollapsibleElement("Related Content", [related_post_1, related_post_2]),
                            CollapsibleElement("LGF Space", [kit_file1, kit_file2])]
    downloads = html_markup_generator.create_rich_text([kit_file1, kit_file2])
    related_content = html_markup_generator.create_rich_text([related_post_1, related_post_2])
    print("related_content")
    print(related_content)
    campaign_body = CampaignHTMLBodyTemplate("Awesome Description", "<pre>This the WYSIWYG</pre>", collapsible_elements)
    page = html_markup_generator.generate(campaign_body, template_name=TemplateNames.CAMPAIGN.value)
    campaign = Resource(name="campaign-1", title="Campaign 1", authoringTemplateName=authoringTemplateName,
                        contentLibraryName=contentLibraryName, path=path, body=str(page),
                        transformHeadersH3=TransformHeaders.COLLAPSIBLE_SECTIONS.value, downloads=downloads,
                        relatedContent=related_content, dealershipTypeVisibility=",".join(
            [DealershipTypes.DEALER.value, DealershipTypes.SUB_DEALER.value]))
    print("-------------------------------------------")
    print(page)
    result = importer_service.save_item(campaign.to_dict())
    print(result)
except (ConnectionError, Exception) as e:
    logging.exception(e)

print(utils.get_mapped_value("cih"))
print(utils.get_mapped_value("ADVANCED FARMING SYSTEMS"))
print(utils.get_mapped_value("UK"))

# print(json_data)


div = HTMLElement("div")
bannerTitle = HTMLElement("span", "Facebook Banners")
hr = HTMLElement("hr")
banner1 = HTMLElement("a", "Facebook Banner 1", dict(href="#"))
banner2 = HTMLElement("a", "Facebook Banner 2", dict(href="#"))

downloads = html_markup_generator.create_rich_text([div, bannerTitle, hr, banner1, banner2])
print(downloads)
"""
