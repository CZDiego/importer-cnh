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

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)

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


def get_formatted_id(item, key):
    uuid = item.get(key, "")
    try:
        uuid = int(uuid)
    except Exception:
        uuid = ""
    return str(uuid)


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
    master_id = get_formatted_id(item, "masterId")
    master_id = "-" + master_id if master_id != "" else ""
    page_master_id = get_formatted_id(item, "pageMasterId")
    page_master_id = "-" + page_master_id if page_master_id != "" else ""
    item["name"] = item["name"] + master_id + page_master_id
    return item


json_array = list(map(map_item, json_array))
json_data = json.dumps(json_array, indent=2)


def save_items(items):
    response = importer_service.save_items(list(items.values()))
    report = utils.get_report(response)
    result = []
    for response_item in report:
        item = items.get(response_item.get("name"))
        result.append(dict(response=response_item, item=item))
    return result


def init_migration(items):
    posts = {}
    kits = {}
    pages = []
    for item in items:
        try:
            content_type = item.get("contentType")
            if content_type is "post" or content_type is "kit":
                del item["contentType"]
                if content_type == "post":
                    posts[item.get("name")] = item
                elif content_type == "kit":
                    kits[item.get("name")] = item
            elif content_type is "page":
                logger.info("Saving posts ...")
                posts = save_items(posts)
                logger.info(json.dumps(posts, indent=2))
                logger.info("Saving kits ...")
                kits = save_items(kits)
                logger.info(json.dumps(kits, indent=2))
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
                logger.info(page_type)
                if page_type == "product" or page_type == "generic":
                    logger.info("Inside product or generic")
                    html_kits = ""
                    logger.info(kits)
                    for kit in kits:
                        kit_item = kit.get("item")
                        downloads = kit_item.get("downloads")
                        html_kits += downloads
                    logger.info(html_kits)
                    item["downloads"] = html_kits
                    logger.info("body")
                    body = CampaignHTMLBodyTemplate(item.get("description", ""), item.get("wysiwyg", ""))
                    item["body"] = html_markup_generator.generate(body, template_name=TemplateNames.CAMPAIGN.value)
                elif page_type == "campaign":
                    logger.info("Inside campaign")
                    html_kits = []
                    for kit in kits:
                        kit_item = kit.get("item")
                        title = kit_item.get("title")
                        original_downloads = kit_item.get("originalDownloads")
                        body_elements = get_downloads_rich_text(original_downloads)
                        html_kits.append(CollapsibleElement(title, body_elements=body_elements))
                    body = CampaignHTMLBodyTemplate(item.get("description", ""), item.get("wysiwyg", ""), html_kits)
                    item["body"] = html_markup_generator.generate(body, template_name=TemplateNames.CAMPAIGN.value)
                logger.info("Saving page")
                del item["contentType"]
                item["transformHeadersH3"] = TransformHeaders.COLLAPSIBLE_SECTIONS.value
                saved_page = importer_service.save_item(item)
                logger.info(json.dumps(saved_page, indent=2))
                saved_page["posts"] = posts
                saved_page["kits"] = kits
                pages.append(saved_page)
                kits = {}
                posts = {}

        except Exception as e:
            logger.error(e)
    logger.info("Pages:")
    logger.info(json.dumps(pages, indent=2))
    logger.info("--------END-------")


# logger.info(json.dumps(json_array, indent=2))
# init_migration(json_array)

# logger.info(json_data)
logger.info("-------------------------------------------")
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
    logger.info("related_content")
    logger.info(related_content)
    campaign_body = CampaignHTMLBodyTemplate("Awesome Description", "<pre>This the WYSIWYG</pre>", collapsible_elements)
    page = html_markup_generator.generate(campaign_body, template_name=TemplateNames.CAMPAIGN.value)
    campaign = Resource(name="campaign-1", title="Campaign 1", authoringTemplateName=authoringTemplateName,
                        contentLibraryName=contentLibraryName, path=path, body=str(page),
                        transformHeadersH3=TransformHeaders.COLLAPSIBLE_SECTIONS.value, downloads=downloads,
                        relatedContent=related_content, dealershipTypeVisibility=",".join(
            [DealershipTypes.DEALER.value, DealershipTypes.SUB_DEALER.value]))
    logger.info("-------------------------------------------")
    logger.info(page)
    result = importer_service.save_item(campaign.to_dict())
    logger.info(result)
except (ConnectionError, Exception) as e:
    logging.exception(e)

logger.info(utils.get_mapped_value("cih"))
logger.info(utils.get_mapped_value("ADVANCED FARMING SYSTEMS"))
logger.info(utils.get_mapped_value("UK"))

# logger.info(json_data)


div = HTMLElement("div")
bannerTitle = HTMLElement("span", "Facebook Banners")
hr = HTMLElement("hr")
banner1 = HTMLElement("a", "Facebook Banner 1", dict(href="#"))
banner2 = HTMLElement("a", "Facebook Banner 2", dict(href="#"))

downloads = html_markup_generator.create_rich_text([div, bannerTitle, hr, banner1, banner2])
logger.info(downloads)
"""
