import logging
import json
from variables import *
import html_markup_utils.html_markup_generator as html_markup_generator
import service.importer_service as importer_service
from models import CollapsibleElement, HTMLElement, CampaignHTMLBodyTemplate, TransformHeaders
import utils
import service.preprocess as preprocessing
from datetime import datetime
import os

TemplateNames = html_markup_generator.TemplateNames

now = datetime.now()
current_time = now.strftime("%-d_%b_%Y")

base_dir = "/data/" + current_time + "/"
if not os.path.exists(base_dir):
    os.mkdir(base_dir)

logging.basicConfig(filename=base_dir + "app.log", format='%(asctime)s %(levelname)-4s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)

# TODO: Read excel file from local volume instead of having it in docker container
# EXCEL_PATH = r'/export-content-20210302121846.xlsx'
EXCEL_PATH = r'/BC export map - UK nhag-CE - IE Ag-CE - 2021 04 13 v1.xlsx'

# Main
pieces_of_content = preprocessing.get_pieces_of_content(EXCEL_PATH)

json_array = []

for i in range(0, len(pieces_of_content)):
    json_array.append(utils.remove_nones_from_dict(pieces_of_content[i].__dict__))


def write_file(f_path, cont):
    f = open(f_path, "a")
    f.write(cont)
    f.close()


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


def get_save_like_items(items):
    items = list(items.values())
    result = []
    for item in items:
        response = dict(name=item["name"], path=item["path"], warning="Kits aren't being created as pieces of content")
        result.append(dict(response=response, item=item))
    return result


def init_migration(items):
    posts = {}
    kits = {}
    report = []
    logger.info("--------STARTING IMPORTATION-------")
    logger.info(current_time)
    for item in items:
        try:
            logger.info(item.get("name"))
            content_type = item.get("contentType")
            if content_type is "post" or content_type is "kit":
                logger.info(item.get("authoringTemplateName"))
                del item["contentType"]
                if content_type == "post":
                    posts[item.get("name")] = item
                elif content_type == "kit":
                    kits[item.get("name")] = item
            elif content_type is "page":
                logger.info("Saving posts ...")
                logger.info(json.dumps(posts, indent=2))
                posts = save_items(posts)
                logger.info(json.dumps(posts, indent=2))
                # todo don't save kits
                logger.info("Saving kits ...")
                logger.info(json.dumps(kits, indent=2))
                kits = get_save_like_items(kits)
                logger.info(json.dumps(kits, indent=2))
                page_type = item.get("pageType", "campaign").lower()
                html_posts = []
                for post in posts:
                    post_item = post.get("item")
                    post_response = post.get("response")
                    post_response["type"] = "post"
                    report.append(post_response)
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
                        kit_response = kit.get("response")
                        kit_response["type"] = "kit"
                        report.append(kit_response)
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
                        kit_response = kit.get("response")
                        kit_response["type"] = "kit"
                        report.append(kit_response)
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
                saved_page["type"] = "page"
                report.append(saved_page)
                kits = {}
                posts = {}

        except Exception as e:
            logger.info(e)
    report_file_path = base_dir + "generated_report_" + timestamp + ".json"
    logger.info("Creating json file in " + file_path)
    write_file(report_file_path, json.dumps(report, indent=2))
    logger.info("--------ENDING IMPORTATION-------")


logger.info("Importer tool CNH")
content = json.dumps(json_array, indent=2)
timestamp = str(now.timestamp())
file_path = base_dir + "generated_json_" + timestamp + ".json"
logger.info("Creating json file in " + file_path)
write_file(file_path, content)
init_migration(json_array)
