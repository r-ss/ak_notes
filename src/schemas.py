
# https://www.youtube.com/watch?v=WkqM_SIXEuQ&t=3566s

# from typing import List

from pydantic import BaseModel

class PostBase(BaseModel):
    ''' Basic model '''
    title: str
    slug: str
    category_id: int

    class Config:
        orm_mode = True


class PostList(PostBase):
    pass

class PostCreate(PostBase):
    description: str