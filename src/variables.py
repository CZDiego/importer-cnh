class DataMapping:
    def __init__(self, columns, auth_template):
        self.columns = columns
        self.auth_template = auth_template

PIECES_OF_CONTENT = []
AUTH_TEMPLATE = "auth-template"

post1_columns = dict(master_id="Post 1 master id", name="Post 1 Title", description="Post 1 Description")
post1_mapping = DataMapping(post1_columns, "post")
PIECES_OF_CONTENT.append(post1_mapping)

post2_columns = dict(master_id="Post 2 master id", name="Post 2 Title", description="Post 2 Description")
post2_mapping = DataMapping(post2_columns, "post")
PIECES_OF_CONTENT.append(post2_mapping)

post3_columns = dict(master_id="Post 3 master id", name="Post 3 Title", description="Post 3 Description")
post3_mapping = DataMapping(post3_columns, "post")
PIECES_OF_CONTENT.append(post3_mapping)

post4_columns = dict(master_id="Post 4 master id", name="Post 4 Title", description="Post 4 Description")
post4_mapping = DataMapping(post4_columns, "post")
PIECES_OF_CONTENT.append(post4_mapping)

post5_columns = dict(master_id="Post 5 master id", name="Post 5 Title", description="Post 5 Description")
post5_mapping = DataMapping(post5_columns, "post")
PIECES_OF_CONTENT.append(post5_mapping)
