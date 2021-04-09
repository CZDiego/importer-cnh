import pandas
import json
from variables import AUTH_TEMPLATE, CONTENT_TYPE, RESOURCE, EXCEL_MAPPING_VARIABLES
import utils
from models import Resource


PIECES_OF_CONTENT_MAPPING = []
HUBS = []
TOPICS = []

# Add category list
for i in range(1, 11):
    HUBS.append(EXCEL_MAPPING_VARIABLES.get("hub" + str(i)))

# Add topic list
for i in range(1, 10):
    TOPICS.append(EXCEL_MAPPING_VARIABLES.get("topic" + str(i)))


class DataMapping:
    def __init__(self, properties, auth_template, content_type):
        self.properties = properties
        self.auth_template = auth_template
        self.content_type = content_type


# Add posts
for i in range(1, 6):

    # Add post files for each post
    for j in range(1, 6):

        post_file = Resource(masterId="Post " + str(i) + " File " + str(j) + " title",
                             authoringTemplateName="id_pays",
                             name="Post " + str(i) + " File " + str(j) + " title",
                             title="Post " + str(i) + " File " + str(j) + " title",
                             geographyVisibility="id_pays",
                             brandContractVisibility="theme",
                             dealershipTypeVisibility="Post " + str(i) + " File " + str(j) + " Targets",
                             contentLibraryName="langue",
                             linkURL="Post " + str(i) + " File " + str(j) + " LINK",
                             overrideLink="Post " + str(i) + " File " + str(j) + " URL",
                             path="Post " + str(i) + " Banner")

        PIECES_OF_CONTENT_MAPPING.append(DataMapping(post_file, RESOURCE, "post_file"))

    post = Resource(masterId="Post " + str(i) + " master id",
                    authoringTemplateName="id_pays",
                    name="Post " + str(i) + " Title",
                    title="Post " + str(i) + " Title",
                    description="Post " + str(i) + " Description",
                    geographyVisibility="id_pays",
                    brandContractVisibility="theme",
                    dealershipTypeVisibility="Post " + str(i) + " Targets",
                    contentLibraryName="langue",
                    creationDate="Post " + str(i) + " created",
                    path="Post " + str(i) + " Banner",
                    thumbnail="Post " + str(i) + " Thumbnail",
                    image="Post " + str(i) + " Banner",
                    siteLocation="Special pages (\"Last Minute\" or \"Promotions\")")

    PIECES_OF_CONTENT_MAPPING.append(DataMapping(post, RESOURCE, "post"))


# Add kits
for i in range(1, 6):

    # Add kit file for each kit
    for j in range(1, 21):

        kit_file = Resource(masterId="Communication kit section " + str(i) + " - file " + str(j) + " title",
                            authoringTemplateName="id_pays",
                            name="Communication kit section " + str(i) + " - file " + str(j) + " title",
                            title="Communication kit section " + str(i) + " - file " + str(j) + " title",
                            geographyVisibility="id_pays",
                            brandContractVisibility="theme",
                            dealershipTypeVisibility="targets",
                            contentLibraryName="langue",
                            linkURL="Communication kit section " + str(i) + " - file " + str(j) + " LINK",
                            path="Communication kit section " + str(i) + " - file " + str(j) + " title")

        PIECES_OF_CONTENT_MAPPING.append(DataMapping(kit_file, RESOURCE, "kit_file"))

    kit = Resource(masterId="Communication kit files section " + str(i),
                   authoringTemplateName="id_pays",
                   name="Communication kit files section " + str(i),
                   title="Communication kit files section " + str(i),
                   geographyVisibility="id_pays",
                   brandContractVisibility="theme",
                   dealershipTypeVisibility="targets",
                   contentLibraryName="langue",
                   creationDate="created",
                   path="Communication kit files section " + str(i),
                   siteLocation="Special pages (\"Last Minute\" or \"Promotions\")")

    PIECES_OF_CONTENT_MAPPING.append(DataMapping(kit, RESOURCE, "kit"))


# Add page
page = Resource(masterId="master_id",
                authoringTemplateName="id_pays",
                name="Page title",
                title="Page title",
                geographyVisibility="id_pays",
                brandContractVisibility="theme",
                dealershipTypeVisibility="targets",
                contentLibraryName="langue",
                path="Page title",
                creationDate="created",
                image="Introvisuel - main banner on page",
                thumbnail="Thumbnail (for catalog page)",
                description="Page Short Description",
                wysiwyg="Wysiwyg",
                siteLocation="Special pages (\"Last Minute\" or \"Promotions\")")
PIECES_OF_CONTENT_MAPPING.append(DataMapping(page, RESOURCE, "page"))


def is_json_serializable(value):
    try:
        json.dumps(value)
        return True
    except TypeError:
        return False


def are_lists_equal(list1, list2):
    list1.sort()
    list2.sort()
    return list1 == list2


def parse_pieces_of_content(excel_path):
    pieces_of_content_result = []
    excel_data = pandas.read_excel(excel_path)

    for index, row in excel_data.iterrows():
        for piece_of_content_mapping in PIECES_OF_CONTENT_MAPPING:

            if pandas.isnull(row[piece_of_content_mapping.properties.masterId]):
                continue

            ans = dict()
            for column_name, column_mapping in piece_of_content_mapping.properties.__dict__.items():
                ans[column_name] = None if column_mapping is None or pandas.isnull(row[column_mapping]) \
                    else row[column_mapping]

                if not is_json_serializable(ans[column_name]):
                    ans[column_name] = str(ans[column_name])

            categories = []
            for hub in HUBS:
                if not pandas.isnull(row[hub]):
                    categories.append(hub.lower())

            topics = []
            for topic in TOPICS:
                if not pandas.isnull(row[topic]):
                    topics.append(topic.lower())

            ans["categories"] = categories
            ans["topics"] = topics
            ans[AUTH_TEMPLATE] = piece_of_content_mapping.auth_template
            ans[CONTENT_TYPE] = piece_of_content_mapping.content_type
            pieces_of_content_result.append(ans)

    return pieces_of_content_result


def clean_piece_of_content(item):

    item["brandContractVisibility"] = utils.get_mapped_value(item["brandContractVisibility"])
    item["geographyVisibility"] = utils.get_mapped_value(item["geographyVisibility"])
    item["name"] = utils.to_kebab_case(item["name"])
    item["contentLibraryName"] = utils.get_mapped_value(item["contentLibraryName"])

    item["thumbnail"] = utils.get_file_name_from_url(item["thumbnail"])
    item["image"] = utils.get_file_name_from_url(item["image"])

    item["categories"] = [utils.get_mapped_value(x) for x in item["categories"]]
    item["topics"] = [utils.get_mapped_value(x) for x in item["topics"]]

    dealership_type_visibility = item["dealershipTypeVisibility"].split(",")
    mapped_dealership_type_visibility = []
    for dealership_type in dealership_type_visibility:
        mapping = utils.get_mapped_value(dealership_type)
        if mapping is not None:
            mapped_dealership_type_visibility.append(mapping)

    separator = ","
    item["dealershipTypeVisibility"] = separator.join(mapped_dealership_type_visibility)



    return item


def clean_pieces_of_content(items):
    post_files = []
    kit_files = []
    clean_items = []

    for item in items:
        content_type = item["contentType"]
        if content_type == "kit_file":
            attachment = dict(title=item["title"], link=item["linkURL"],
                              fileName=utils.get_file_name_from_url(item["linkURL"]))
            kit_files.append(attachment)
        elif content_type == "kit":
            item["attachment"] = kit_files
            kit_files = []
            clean_items.append(clean_piece_of_content(item))
        elif content_type == "post_file":
            attachment = dict(title=item["title"], link=item["linkURL"], url=item["overrideLink"],
                              fileName=utils.get_file_name_from_url(item["linkURL"]),
                              dealershipTypeVisibility=item["dealershipTypeVisibility"])
            post_files.append(attachment)
        elif content_type == "post":
            item["attachment"] = []

            # Only add post files with the same dealershipTypeVisibility as the post parent
            for file in post_files:
                if are_lists_equal(item["dealershipTypeVisibility"].split(","), file["dealershipTypeVisibility"].split(",")):
                    del file["dealershipTypeVisibility"]
                    item["attachment"].append(file)

            post_files = []
            clean_items.append(clean_piece_of_content(item))
        else:
            clean_items.append(clean_piece_of_content(item))
    return clean_items


def get_pieces_of_content(excel_path):

    pieces_of_content = parse_pieces_of_content(excel_path)
    pieces_of_content = clean_pieces_of_content(pieces_of_content)

    return pieces_of_content
