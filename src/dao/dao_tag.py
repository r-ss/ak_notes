from dao.dao import BasicDAOLayer
from models.tag import Tag, TagBM, TagsBM


class TagDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = Tag
        self.readable = 'Tag'

    def get(self, response_model=TagBM, **kwargs):
        return super().get(response_model=response_model, **kwargs)

    def get_all(self):
        return super().get_all(response_model=TagsBM)

    def create(self, tag: TagBM):
        return super().create(tag, response_model=TagBM)

    def update_fields(self, fields: dict = {}, response_model=TagBM, **kwargs):
        return super().update_fields(fields=fields, response_model=response_model, **kwargs)

    def get_all_where(self, **kwargs):
        return super().get_all_where(response_model=TagsBM, **kwargs)
