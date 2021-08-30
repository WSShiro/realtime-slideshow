# -*- coding: utf-8 -*-

import os
import json
import sys
from traceback import print_exc
from PIL import Image
from PIL.ExifTags import TAGS


def _exif(file_path):
    try:
        # simply format from bytes to str for json serialization
        def _format_bytes(obj_):
            res = {}
            for key_, value_ in obj_.items():
                if isinstance(value_, bytes):
                    res[key_] = "{}".format(value_)
                elif isinstance(value_, dict):
                    res[key_] = _format_bytes(value_)
                else:
                    res[key_] = value_
            return res

        # read exif
        with Image.open(file_path) as f:
            exif_ = f._getexif()
        # convert to readable dict
        info_ = {}
        for key_ in exif_.keys():
            tag_ = TAGS.get(key_, key_)
            # skip longer value
            if tag_ in ["MakerNote", "UserComment"]:
                continue
            info_[tag_] = exif_[key_]

        return _format_bytes(info_)

    except AttributeError:
        # it might not have exif attached ('exif_' is None)
        return {}
    except BaseException:
        raise


def list_exif(dir_path):
    # generator for picking up jpeg files
    def _scan():
        for root, _, files in os.walk(dir_path):
            for file_ in files:
                flags_ = [file_.lower().endswith(x)
                          for x in [".jpeg", ".jpg", ".jpe"]]
                if sum(flags_) > 0:
                    yield os.path.join(root, file_)
                else:
                    continue
    # check path
    if not os.path.isdir(dir_path):
        raise Exception("invalid directory path")

    # build info for each jpeg file
    res = []
    for item in _scan():
        path_ = os.path.normpath(item)
        buf_ = {"path": path_,
                "file": os.path.basename(path_),
                "dir": os.path.dirname(os.path.relpath(path_, dir_path))}
        # add metadata
        buf_["exif"] = _exif(path_)
        res.append(buf_)

    return res


def remove_exif(dir_path):
    # transpose and remove exif for each image files
    for item in [x for x in list_exif(dir_path) if x["exif"] != {}]:
        orientation_ = item["exif"]["Orientation"]
        # skip files if not need to be transposed
        if orientation_ < 2:
            continue
        # new file name with 'r' appended
        #path_ = "{}-r{}".format(*os.path.splitext(item["path"]))
        # new file name without 'r' appended
        path_ = "{}{}".format(*os.path.splitext(item["path"]))
        print("save file: {} (orientation:{})...".format(path_, orientation_))
        trans_ = [0, 3, 1, 5, 4, 6, 2][orientation_ - 2]
        # save modified image as new file
        with Image.open(item["path"]) as image_:
            # transpose to upright angle
            image_ = image_.transpose(trans_)
            image_.save(path_)


if __name__ == "__main__":
    try:
        # specify directory path where JPEG image files are stored
        path_ = "D:\Dropbox\ForSuzuki\mySlideshow\DropboxPhoto"
        if len(sys.argv) == 2:
            if sys.argv[1] == 'rm':				
                remove_exif(path_)

            else:
                res = list_exif(path_)
                # save as json file
                with open(os.path.join(path_, "exif.json"), 'w') as f:
                    json.dump(res, f, indent=2, ensure_ascii=False)
					
    except BaseException:
        print_exc()
