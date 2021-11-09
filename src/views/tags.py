from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.tag import Tag, TagBM, TagsBM

router = InferringRouter()

@cbv(router)
class TagsCBV:

    ''' CREATE '''
    @router.post("/tags", status_code=status.HTTP_201_CREATED)
    def create(self, tag: TagBM):
        db_tag = Tag(name = tag.name).save()
        tag = TagBM.parse_raw(db_tag.to_json())
        return tag

    ''' READ '''
    @router.get("/tags/{numerical_id}")
    def read(self, numerical_id: int):

        try:
            db_tag = Tag.objects.get(numerical_id = numerical_id)
        except Tag.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'Tag does not found'}
            )

        tag = TagBM.parse_raw(db_tag.to_json())
        return tag

    @router.get("/tags")
    def read_all(self):
        db_tags = Tag.objects.all()

        tags = TagsBM.parse_raw(db_tags.to_json())
        return tags    

    ''' UPDATE '''
    @router.put("/tags/{numerical_id}")
    def update(self, numerical_id: int, tag: TagBM):
        db_tag = Tag.objects.get(numerical_id = numerical_id)
        db_tag.name = tag.name
        db_tag.save()
        tag = TagBM.parse_raw(db_tag.to_json())
        return tag

    ''' DELETE '''
    @router.delete("/tags/{numerical_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, numerical_id: int):

        db_tag = Tag.objects.get(numerical_id = numerical_id)
        tag = TagBM.parse_raw(db_tag.to_json())

        db_tag.delete()
        return {'deteted tag': tag}

        