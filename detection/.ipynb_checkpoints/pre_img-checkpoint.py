import os
from PIL import Image
import re

image_folder = "img"
images = []

def set_up_parse():
     args.add_argument("--img-dir", type=str, default="img", help="path to img directory")

self.args = set_up_parse()
image_folder = self.args.img_dir + "/"
for filename in os.listdir(image_folder):
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".png"):
        file_path = os.path.join(image_folder, filename)
        image = Image.open(file_path)
        width, height = image.size
        image_id = len(images) + 1
        print(f"filename={filename}")
        if not re.match(r"\d{12}\.jpg", filename):
            new_file_name = "{:012d}.jpg".format(image_id)
            os.rename(file_path, os.path.join(image_folder, new_file_name))
            filename = new_file_name
        else:
            fileid, _ = os.path.splitext(filename)  # 去掉扩展名  
            image_id = int(fileid)
        image_info = {
            "license": 1,
            "file_name": filename,
            "height": height,
            "width": width,
            "id": image_id
        }
        images.append(image_info)

import json

type_know = [
        {
            "id": 1,
            "name": "person",
            "supercategory": "person"
        },
        {
            "id": 2,
            "name": "bird",
            "supercategory": "animal"
        },
        {
            "id": 3,
            "name": "cat",
            "supercategory": "animal"
        },
        {
            "id": 4,
            "name": "cow",
            "supercategory": "animal"
        },
        {
            "id": 5,
            "name": "dog",
            "supercategory": "animal"
        },
        {
            "id": 6,
            "name": "horse",
            "supercategory": "animal"
        },
        {
            "id": 7,
            "name": "sheep",
            "supercategory": "animal"
        },
        {
            "id": 8,
            "name": "airplane",
            "supercategory": "vehicle"
        },
        {
            "id": 9,
            "name": "bicycle",
            "supercategory": "vehicle"
        },
        {
            "id": 10,
            "name": "boat",
            "supercategory": "vehicle"
        },
        {
            "id": 11,
            "name": "bus",
            "supercategory": "vehicle"
        },
        {
            "id": 12,
            "name": "car",
            "supercategory": "vehicle"
        },
        {
            "id": 13,
            "name": "motorcycle",
            "supercategory": "vehicle"
        },
        {
            "id": 14,
            "name": "train",
            "supercategory": "vehicle"
        },
        {
            "id": 15,
            "name": "bottle",
            "supercategory": "indoor"
        },
        {
            "id": 16,
            "name": "chair",
            "supercategory": "indoor"
        },
        {
            "id": 17,
            "name": "dining table",
            "supercategory": "indoor"
        },
        {
            "id": 18,
            "name": "potted plant",
            "supercategory": "indoor"
        },
        {
            "id": 19,
            "name": "couch",
            "supercategory": "indoor"
        },
        {
            "id": 20,
            "name": "tv",
            "supercategory": "indoor"
        }
    ]

type_unknow = [        {
            "id": 81,
            "name": "unknow object",
            "supercategory": "unknow object"
        }
    ]

licenses = [
        {
            "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
            "id": 1,
            "name": "Attribution-NonCommercial-ShareAlike License"
        },
        {
            "url": "http://creativecommons.org/licenses/by-nc/2.0/",
            "id": 2,
            "name": "Attribution-NonCommercial License"
        },
        {
            "url": "http://creativecommons.org/licenses/by-nc-nd/2.0/",
            "id": 3,
            "name": "Attribution-NonCommercial-NoDerivs License"
        },
        {
            "url": "http://creativecommons.org/licenses/by/2.0/",
            "id": 4,
            "name": "Attribution License"
        },
        {
            "url": "http://creativecommons.org/licenses/by-sa/2.0/",
            "id": 5,
            "name": "Attribution-ShareAlike License"
        },
        {
            "url": "http://creativecommons.org/licenses/by-nd/2.0/",
            "id": 6,
            "name": "Attribution-NoDerivs License"
        },
        {
            "url": "http://flickr.com/commons/usage/",
            "id": 7,
            "name": "No known copyright restrictions"
        },
        {
            "url": "http://www.usa.gov/copyright.shtml",
            "id": 8,
            "name": "United States Government Work"
        }
    ]

info = {
        "description": "COCO 2017 Dataset",
        "url": "http://cocodataset.org",
        "version": "1.0",
        "year": 2017,
        "contributor": "COCO Consortium",
        "date_created": "2017/09/01"
    }

data = {
    "info": info,
    "licenses": licenses,
    "images": images,
    "annotations": [],
    "categories": type_know
}

data_unknow = {
    "info": info,
    "licenses": licenses,
    "images": images,
    "annotations": [],
    "categories": type_unknow
}

json_data = json.dumps(data, indent=4)
with open("configs/instances_val2017_mixed_ID.json", "w") as file:
    file.write(json_data)
    
json_data_unknow = json.dumps(data_unknow, indent=4)
with open("configs/instances_val2017_mixed_OOD.json", "w") as file:
    file.write(json_data_unknow)
