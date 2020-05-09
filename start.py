# -*- coding: utf-8 -*-

import os
import json
import codecs
from datetime import date, datetime
import time
import exifmodify

# Convert datetime to charactor
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

def list_difference(list1, list2):
    result = list1.copy()
    for value in list2:
        if value in result:
            result.remove(value)
    result.sort(key=lambda x: -x['time-from-epoch'])
    return result

# Make image list in the path as json
def json_tree_image(path):
    target_json = []
    for item in os.listdir(path):
        full_path = os.path.join(path,item)
        new_hash = {}
        new_hash['title'] = item.split(' -',1)[0]
        new_hash['href'] = full_path.replace(os.getcwd()+'/','')
        new_hash['time'] = time.ctime(os.path.getmtime(full_path))
        #new_hash['time'] = time.localtime(os.path.getmtime(full_path))
        new_hash['time-from-epoch'] = os.path.getmtime(full_path)
        target_json.append(new_hash)
    target_json.sort(key=lambda x: -x['time-from-epoch'])
    return target_json

if __name__ == '__main__':

    # Make the initial json
    path = os.getcwd()+'\DropboxPhoto'
    list_new = json_tree_image(path)
    print('{}'.format(json.dumps(list_new,indent=4, ensure_ascii=False, sort_keys=True, default=json_serial)))
    
    # Json update loop
    count = 0;
    while True:
##        # Read the previous json
##        with codecs.open('image.json','r','utf-8') as f:
##            list_old = json.load(f)
            
        # Make the new json
        list_new = json_tree_image(path)
        with codecs.open('image.json','w','utf-8') as f:
            dump = json.dumps(list_new,indent=4, ensure_ascii=False, sort_keys=True, default=json_serial)
            f.write(dump)
        
##        # Check difference
##        item_new = list_difference(list_new, list_old)
##        print('{}'.format(json.dumps(item_new,indent=4, ensure_ascii=False, sort_keys=True, default=json_serial)))
##        with codecs.open('image_new.json','w','utf-8') as f:
##            dump = json.dumps(item_new,indent=4, ensure_ascii=False, sort_keys=True, default=json_serial)
##            f.write(dump)

        # Remove exif info of image for standardize orientation
        try :
            exifmodify.remove_exif(path)
        except Exception as e :
            pass
        
        time.sleep(2)
        count = count +1
        print('Item Num: ',len(list_new))


        
