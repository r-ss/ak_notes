from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserTokenBM
from models.tag import TagBM

from services.tags import TagsService
from services.users.auth import token_required

from pydantic import UUID4

router = InferringRouter(tags=["Tags"])


@cbv(router)
class TagsCBV:

    """CREATE"""

    @router.post("/notes/{note_uuid}/tags", status_code=status.HTTP_201_CREATED)
    def tag_create(self, note_uuid: UUID4, tag: TagBM, token: UserTokenBM = Depends(token_required)):
        return TagsService.create(note_uuid, tag, token)

    """ READ """

    @router.get("/tags", summary="Read all tags")
    def tag_read_all(self, token: UserTokenBM = Depends(token_required)):
        return TagsService.read_all(token)

    @router.get("/users/{user_uuid}/tags", summary="Read all tags by current user")
    def tag_read_by_user(self, user_uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return TagsService.read_all_for_user(user_uuid, token)

    @router.get("/notes/{note_uuid}/tags", summary="Read all tags attached to note")
    def tag_read_in_note(self, note_uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return TagsService.read_all_in_note(note_uuid, token)

    @router.get("/tags/{uuid}", summary="Read specific tag")
    def tag_read(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return TagsService.read_specific(uuid, token)

    """ UPDATE """

    @router.patch("/tags/{uuid}")
    def tag_update(self, tag: TagBM, token: UserTokenBM = Depends(token_required)):
        return TagsService.update(tag, token)

    """ DELETE """

    @router.delete("/tags/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
    def tag_delete(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        TagsService.delete(uuid, token)
        return {"tag deleted"}
