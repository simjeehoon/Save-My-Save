import re
import os
import shutil
import sys
from typing import Optional


class SaveHelper:

    def __init__(self, name_format, target_dir_path, backup_dir_path):
        self.__name_format = name_format
        self.target_directory_path = target_dir_path
        self.ref = re.compile(self.__name_format)
        self.backup_directory_path = backup_dir_path

    @property
    def name_format(self):
        return self.__name_format

    @name_format.setter
    def name_format(self, name_format):
        self.name_format = name_format
        self.ref = re.compile(self.__name_format)

    def backup(self, dir_name: Optional[str] = None):
        if not os.path.isdir(self.backup_directory_path):
            os.makedirs(self.backup_directory_path)
        if dir_name is None:
            dir_name = self.get_auto_version_directory_name()

        subscript = ''
        number = 1

        copied_list = []
        try:
            while os.path.isdir(os.path.join(self.backup_directory_path, dir_name + subscript)):
                number += 1
                subscript = ' ({})'.format(number)
            dir_name = dir_name + subscript
            directory_with_version = os.path.join(self.backup_directory_path, dir_name)
            os.mkdir(directory_with_version)

            for file in self.target_list():
                shutil.copy(os.path.join(self.target_directory_path, file),
                            os.path.join(directory_with_version, file))
                copied_list.append(file)
        except:
            print(sys.exc_info())
            return None
        return copied_list

    def get_auto_version_directory_name(self):
        name = "backup{}"
        number = 1
        while os.path.isdir(os.path.join(self.backup_directory_path, name.format(number))):
            number += 1
        return name.format(number)

    def rollback(self, version_name):
        directory_with_version = os.path.join(self.backup_directory_path, version_name)
        copied_list = []
        if not os.path.isdir(directory_with_version):
            print(directory_with_version)
            return None
        try:
            for file in os.listdir(directory_with_version):
                src = os.path.join(directory_with_version, file)
                dst = os.path.join(self.target_directory_path, file)
                copied_list.append(shutil.copy(src, dst))
        except:
            print(sys.exc_info())
            return None
        return copied_list

    def target_list(self):
        target = []
        for file in os.listdir(self.target_directory_path):
            if self.ref.match(file) and file != os.path.basename(self.backup_directory_path):
                target.append(file)
        return target

    def load_backup_directories(self):
        if not os.path.isdir(self.backup_directory_path):
            return []
        return [file_name for file_name in os.listdir(self.backup_directory_path)
                if os.path.isdir(os.path.join(self.backup_directory_path, file_name))]


def _test(l):
    print("현재 있는 백업 목록:")
    for i in l:
        print("\t" + i)
    print("1.백업, 2.롤백")
    return int(input())


if __name__ == '__main__':
    dir_path = r'C:\Users\Jihun Shim\PycharmProjects\saveHelper\test\save'
    file = '.+[.]txt'
    backup_path = os.path.join(dir_path, 'backup')
    helper = SaveHelper(file, dir_path, backup_path)
    while True:
        val = _test(helper.load_backup_directories())
        if val == 1:
            res = helper.backup()
            print("저장됨::", res)
        if val == 2:
            if helper.rollback(input("롤백폴더:")):
                print("성공")
