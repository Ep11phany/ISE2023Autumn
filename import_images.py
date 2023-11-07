#!/usr/bin/env python3

import os
import shutil
from glob import glob
from datetime import datetime

from pymongo.collection import Collection
from tqdm import tqdm

import clip_model
import utils


def import_single_image(filename: str, model: clip_model.CLIPModel,
                        config: dict, mongo_collection: Collection, copy=True):

    index = filename.find(".", 2)
    filetype = filename[index+1:]
    if filetype is None:
        print("skip file:", filename)
        return
    image_feature, image_size = model.get_image_feature(filename)
    if image_feature is None:
        print("skip file:", filename)
        return
    image_feature = image_feature.astype(config['storage-type'])
    if copy:
        md5hash = utils.calc_md5(filename)
        new_basename = md5hash + '.' + filetype
        new_full_path = utils.get_full_path(
            config['import-image-base'], new_basename)
        if os.path.isfile(new_full_path):
            # print("duplicate file:", filename)
            return
        shutil.copy2(filename, new_full_path)
        stat = os.stat(new_full_path)
    else:
        stat = os.stat(filename)
        new_full_path = filename

    image_mtime = datetime.fromtimestamp(stat.st_mtime)
    image_datestr = image_mtime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # save images to mongodb
    document = {
        'filename': new_full_path,
        'extension': filetype,
        'height': image_size[1],
        'width': image_size[0],
        'filesize': stat.st_size,
        'date': image_datestr,
        'feature': image_feature.tobytes(),
    }

    x = mongo_collection.insert_one(document)
    return x


def import_dir(base_dir: str, model: clip_model.CLIPModel,
               config: dict, mongo_collection: Collection, copy=False):
    list_file = os.listdir(base_dir)

    filelist = [base_dir+'/'+f for f in list_file]
    filelist = [f for f in filelist if os.path.isfile(f)]

    for filename in tqdm(filelist):
        import_single_image(filename, model, config,
                            mongo_collection, copy=copy)


def main():
    config = utils.get_config()
    mongo_collection = utils.get_mongo_collection()
    model = clip_model.get_model()
    import_dir("./imgs", model, config, mongo_collection, True)


if __name__ == '__main__':
    main()
