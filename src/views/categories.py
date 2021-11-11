from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.category import Category, CategoryBM, CategoriesBM

router = InferringRouter()

@cbv(router)
class CategoriesCBV:

    ''' CREATE '''
    @router.post("/categories", status_code=status.HTTP_201_CREATED)
    def create(self, category: CategoryBM):
        db_category = Category(name = category.name).save()
        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    ''' READ '''
    @router.get("/categories/{numerical_id}")
    def read(self, numerical_id: int):

        try:
            db_category = Category.objects.get(numerical_id = numerical_id)
        except Category.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'Category does not found'}
            )

        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    @router.get("/categories")
    def read_all(self):
        db_categories = Category.objects.all()

        categories = CategoriesBM.parse_raw(db_categories.to_json())
        return categories    

    ''' UPDATE '''
    @router.put("/categories/{numerical_id}")
    def update(self, numerical_id: int, category: CategoryBM):
        db_category = Category.objects.get(numerical_id = numerical_id)
        db_category.name = category.name
        db_category.save()
        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    ''' DELETE '''
    @router.delete("/categories/{numerical_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, numerical_id: int):

        db_category = Category.objects.get(numerical_id = numerical_id)
        category = CategoryBM.parse_raw(db_category.to_json())

        db_category.delete()
        return {'deteted category': category}

        