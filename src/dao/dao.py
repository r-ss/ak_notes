from fastapi import status, HTTPException
# from mongoengine.queryset.visitor import Q as mongo_Q


class BasicDAOLayer:
    """ Some general methods to basic operations with database

        Operates with abstract "Object" implying mongoengine models
        This class must be inherited by more specific objects like Note, which provide context
    """

    def __init__(self):
        self.target = None
        self.readable = '--EMPTY--'

    def get(self, response_model=None, **kwargs):
        """ Get one object from DB
            Parse it to response_model if provided and return

            Query example:
            SomeDAO.get(uuid=id)
        """

        if not len(kwargs):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='kwargs not present for DB query')

        field = str(list(kwargs.keys())[0])
        value = list(kwargs.values())[0]

        if type(value) != int:
            value = str(value)

        try:
            db_obj = self.target.objects.get(__raw__={field: value})
        except self.target.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='%s object not found in DB' % self.readable)

        if response_model:
            return response_model.from_orm(db_obj)
        return db_obj

    def get_all(self, response_model=None):
        """ Get all objects """

        db_objs = list(self.target.objects.all())

        if response_model:
            return response_model.from_orm(db_objs)
        return db_objs

    def create(self, data, response_model=None):
        """ Create object of type self.target. Save all fields passed in "data" into new object """

        db_obj = self.target()

        if type(data) == dict:
            collection = data
        else:
            collection = data.dict()

        for k, v in collection.items():
            if v:
                if type(v) != int:
                    v = str(v)
                db_obj[k] = v
        db_obj.save()

        if response_model:
            return response_model.from_orm(db_obj)
        return db_obj

    def update_fields(self, fields={}, response_model=None, **kwargs):
        # db_obj = self.get(key=key, field='uuid', response_model=None)

        if not len(kwargs):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='kwargs not present for DB query')

        field = str(list(kwargs.keys())[0])
        value = list(kwargs.values())[0]

        if type(value) != int:
            value = str(value)

        try:
            db_obj = self.target.objects.get(__raw__={field: value})
        except self.target.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='%s object not found in DB' % self.readable)

        for k, v in fields.items():
            db_obj[k] = v
        db_obj.save()

        if response_model:
            return response_model.from_orm(db_obj)
        return db_obj

    def get_all_where(self, response_model=None, **kwargs):
        """ Get all objects filtered by some rule """

        # print('*args', *args)
        for key, value in kwargs.items():
            field = key.split('__')[0]
            rule = key.split('__')[1]

            # print(field, rule)

            if type(value) != list:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Only lists supported for now')

            # print("{0} = {1}".format(field, value))

            agg = []
            for item in value:
                agg.append(str(item))

            db_objs = self.target.objects(__raw__={field: {'$%s' % rule: agg}})

        if response_model:
            return response_model.from_orm(list(db_objs))
        return db_objs

    def delete(self, **kwargs):
        """ Delete one object where """

        if not len(kwargs):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='kwargs not present for DB query')

        field = str(list(kwargs.keys())[0])
        value = list(kwargs.values())[0]

        if type(value) != int:
            value = str(value)

        try:
            db_obj = self.target.objects.get(__raw__={field: value})
        except self.target.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='%s object not found in DB' % self.readable)

        db_obj.delete()
        return None
