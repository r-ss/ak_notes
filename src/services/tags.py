from fastapi import status, HTTPException
from pydantic import UUID4

from models.tag import TagBM, TagsBM
from models.user import UserTokenBM

from services.users.auth import check_ownership

from dao.dao_file import FileDAOLayer
from dao.dao_note import NoteDAOLayer
from dao.dao_user import UserDAOLayer
from dao.dao_category import CategoryDAOLayer
from dao.dao_tag import TagDAOLayer

FileDAO = FileDAOLayer()
NoteDAO = NoteDAOLayer()
UserDAO = UserDAOLayer()
CategoryDAO = CategoryDAOLayer()
TagDAO = TagDAOLayer()


class TagsService:

    """CREATE SERVICE"""

    def create(note_uuid: UUID4, tag: TagBM, token: UserTokenBM) -> TagBM:
        """Create tag and return it"""

        note, owner = NoteDAO.get_note_owner(uuid=note_uuid)
        check_ownership(owner.uuid, token)

        tag = TagDAO.create(TagBM.parse_obj({"name": tag.name}))
        note.tags.append(tag.uuid)
        NoteDAO.update_fields(uuid=note.uuid, fields={"tags": note.tags})
        return tag

    """ READ SERVICE """

    def read_specific(uuid: UUID4, token: UserTokenBM) -> TagBM:
        """Get specific tag item"""
        return TagDAO.get(uuid=uuid)

    def read_all(token: UserTokenBM) -> TagsBM:
        """Get all tags"""
        return TagDAO.get_all()

    def read_all_for_user(user_uuid: UUID4, token: UserTokenBM) -> TagsBM:
        """Get all tag items by current user"""

        user = UserDAO.get(uuid=user_uuid)
        categories = CategoryDAO.get_all_where(uuid__in=user.categories)

        tags_collector = []
        for category in categories:
            notes = NoteDAO.get_all_where(uuid__in=category.notes)
            for note in notes:
                tags = TagDAO.get_all_where(uuid__in=note.tags)
                for tag in tags:
                    tags_collector.append(tag)

        return TagsBM.from_orm(tags_collector)

    def read_all_in_note(note_uuid: UUID4, token: UserTokenBM) -> TagsBM:
        """Get all tag items by current user"""
        note, owner = NoteDAO.get_note_owner(uuid=note_uuid)
        check_ownership(owner.uuid, token)
        return TagDAO.get_all_where(uuid__in=note.tags)

    """ UPDATE SERVICE """

    def update(input_tag: TagBM, token: UserTokenBM) -> TagBM:
        """Method to change tag name"""

        # Get all user tags to check ownership
        # TODO - consider refactor
        usertags = TagsService.read_all_for_user(token.uuid, token)
        found = False
        for tag in usertags:
            if tag.uuid == input_tag.uuid:
                found = True
                break

        if not found:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized. Tag not found for user")

        return TagDAO.update_fields(uuid=tag.uuid, fields={"name": input_tag.name, "color": str(input_tag.color)})

    """ DELETE SERVICE """

    def delete(uuid: UUID4, token: UserTokenBM) -> None:
        """Delete Category from database"""

        # Get all user tags to check ownership
        # TODO - consider refactor
        usertags = TagsService.read_all_for_user(token.uuid, token)
        found = False
        for tag in usertags:
            if tag.uuid == uuid:
                found = True
                break

        if not found:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized. Tag not found for user")

        TagDAO.delete(uuid=uuid)
