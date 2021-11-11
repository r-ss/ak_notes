import os
import shutil
# import zipfile


class FileSystemUtils:

    def is_file_exist(self, path):
        if os.path.isfile(path) or os.path.isdir(path):
            return True
        else:
            return False

    def check_dir(self, dir):
        if not os.path.isdir(dir):
            # os.mkdir(dir)
            os.makedirs(dir)

    # def listdir(self, dir):
    #     files = []
    #     if os.path.isdir(dir):
    #         for file in os.listdir(dir):
    #             f = {}
    #             f['name'] = file
    #             files.append(f)
    #     return files

    # # for further JSON dumping
    # def dir_to_list(self, dirname, path=os.path.pathsep):
    #     data = []
    #     for name in os.listdir(dirname):
    #         dct = {}
    #         dct['name'] = name
    #         dct['path'] = path + name

    #         full_path = os.path.join(dirname, name)
    #         if os.path.isfile(full_path):
    #             dct['type'] = 'file'
    #         elif os.path.isdir(full_path):
    #             dct['type'] = 'folder'
    #             dct['children'] = self.dir_to_list(full_path, path=path + name + os.path.pathsep)

    #         if not name.startswith('.'):
    #             data.append(dct)
    #     return data
    
    def delete_file(self, path):
        if os.path.isfile(path):
            os.remove(path)

    def remove_directory(self, dir):
        if os.path.isdir(dir):
            shutil.rmtree(dir)

    # def make_zip(self, src, dest):
    #     if os.path.isfile(dest):
    #         os.remove(dest)
    #     shutil.make_archive(dest[:-4], 'zip', src)

    # def unzip(self, src, dest):
    #     if zipfile.is_zipfile(src): # if it is a zipfile, extract it
    #         with zipfile.ZipFile(src) as item: # treat the file as a zip
    #             item.extractall(dest)  # extract it in the specific directory

    def move_file(self, src, dst):
        shutil.move(src, dst)

    def copy(self, src, dest, rewrite = False, ignore = False):
        if os.path.isdir(dest):
            if rewrite:
                shutil.rmtree(dest)

        try:
            if ignore:
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns('.*'))
            else:
                shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == 20:
                shutil.copy(src, dest)
            else:
                raise Exception('Directory not copied. Error: %s' % e)