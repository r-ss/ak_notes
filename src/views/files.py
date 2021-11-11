from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi_utils.inferring_router import InferringRouter

from fastapi import UploadFile
from fastapi import File as FastAPIFile

from models.file import File, FileBM, FilesBM

from typing import List

from config import Config


from filesystem import FileSystemUtils
fs = FileSystemUtils()

router = InferringRouter()


@cbv(router)
class FilesCBV:

    ''' CREATE '''
    @router.post("/files", status_code=status.HTTP_201_CREATED)
    def create(self, uploads: List[UploadFile] = FastAPIFile(...)):

        # print(uploads)

        fs.check_dir(Config.STORAGE['ROOT'])


        for upload in uploads:

            # print( upload.filename )
            file_location = '%s%s' % (Config.STORAGE['ROOT'], upload.filename )
            f = open(file_location, 'wb')
            f.write(upload.file.read())
            f.close()

        
        
        # db_file = File(filename = file.filename).save()
        # file = FileBM.parse_raw(db_file.to_json()) 
        return uploads

    ''' READ '''
    @router.get("/files/{id}")
    def read(self, id: str):

        try:
            db_file = File.objects.get(id = id)
        except File.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'File does not found'}
            )

        db_file = File.objects.get(id = id)
        file = FileBM.parse_raw(db_file.to_json())
        return file

    # TODO - implement downloads
    # @
    # def download()
    # return FileResponse(path)

    @router.get("/files")
    def read_all(self):
        db_files = File.objects.all()

        files = FilesBM.parse_raw(db_files.to_json())
        return files    

    # ''' UPDATE '''
    # @router.put("/files/{numerical_id}")
    # def update(self, numerical_id: int, file: FileBM):
    #     db_file = File.objects.get(numerical_id = numerical_id)
    #     db_file.name = file.name
    #     db_file.save()
    #     file = FileBM.parse_raw(db_file.to_json())
    #     return file

    ''' DELETE '''
    @router.delete("/files/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, id: str):

        db_file = File.objects.get(id = id)
        file = FileBM.parse_raw(db_file.to_json())

        db_file.delete()
        return {'deteted file': file}

        