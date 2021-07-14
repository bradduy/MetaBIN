# encoding: utf-8
"""
@author:  bradduy
@contact: bradduy95@gmail.com
"""

import glob
import os.path as osp
import re

from .bases import ImageDataset
from ..datasets import DATASET_REGISTRY

@DATASET_REGISTRY.register()
class Celeb(ImageDataset):

    dataset_dir = 'Celeb-reID'
    dataset_name = "Celeb_test"

    def __init__(self, root='datasets', **kwargs):
        # self.root = osp.abspath(osp.expanduser(root))
        self.root = root
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'gallery')

        required_files = [
            self.dataset_dir,
            self.train_dir,
            self.query_dir,
            self.gallery_dir,
        ]
        self.check_before_run(required_files)

        train = self.process_dir(self.train_dir)
        query = self.process_dir(self.query_dir, is_train=False)
        gallery = self.process_dir(self.gallery_dir, is_train=False)
         
        super(Celeb, self).__init__(train, query, gallery, **kwargs)

    def process_dir(self, dir_path, is_train=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        pattern = re.compile(r'([-\d]+)_(\d)')

        data = []
        for img_path in img_paths:
            pid, camid = map(int, pattern.search(img_path).groups())

            assert 1 <= camid <= 9
            camid -= 1 
            if is_train:
                pid = self.dataset_name + "_" + str(pid)
            data.append((img_path, pid, camid))

        return data

    # def process_train(self, train_path):
    #     data = []

    #     file_path_list = ['cam_a', 'cam_b']

    #     for file_path in file_path_list:
    #         camid = self.dataset_name + "_" + file_path
    #         img_list = glob(os.path.join(train_path, file_path, "*.bmp"))
    #         for img_path in img_list:
    #             img_name = img_path.split('/')[-1]
    #             pid = self.dataset_name + "_" + img_name.split('_')[0]
    #             data.append([img_path, pid, camid])

    #     return data