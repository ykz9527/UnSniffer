import os
import cv2
import sys
import copy
import torch
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from detectron2.engine import default_argument_parser
from detectron2.utils.visualizer import Visualizer, VisImage
import xml.etree.ElementTree as ET
from PIL import Image

def get_inference_output_dir(output_dir_name,
                             test_dataset_name,
                             inference_config_name,
                             image_corruption_level):
    return os.path.join(
        output_dir_name,
        'inference',
        test_dataset_name,
        os.path.split(inference_config_name)[-1][:-5],
        "corruption_level_" + str(image_corruption_level))

def set_up_parse():
    args = default_argument_parser()
    args.add_argument('--manual_device', default='')
    args.add_argument("--dataset-dir", type=str,
                      default="temp",
                      help="path to dataset directory")
    args.add_argument("--img-dir", type=str,
                      default="img",
                      help="path to img directory")
    args.add_argument("--test-dataset", type=str,
                      default="",
                      help="test dataset")
    
    args.add_argument(
        '--outputdir',
        type=str,
        default='../output'
    )

    args.add_argument(
        "--random-seed",
        type=int,
        default=0,
        help="random seed to be used for all scientific computing libraries")

    # Inference arguments, will not be used during training.
    args.add_argument(
        "--inference-config",
        type=str,
        default="",
        help="Inference parameter: Path to the inference config, which is different from training config. Check readme for more information.")
    args.add_argument(
        "--image-corruption-level",
        type=int,
        default=0,
        help="Inference parameter: Image corruption level between 0-5. Default is no corruption, level 0.")

    return args.parse_args()


class Draw:
    def __init__(self):
        self.args = set_up_parse()
        modelname = (self.args.config_file).split(".")[0]
        cfg_OUTPUT_DIR = "../data/{}".format(modelname)

        self.outpathfigdir_ = self.args.outputdir
        if not os.path.exists(self.outpathfigdir_):
            os.makedirs(self.outpathfigdir_)
        self.vis_path = self.outpathfigdir_
        if not os.path.exists(self.vis_path):
            os.makedirs(self.vis_path)
        print("output path: {}".format(self.vis_path))
        # load groundtruth
        self.img_path = self.args.img_dir + "/"
        self.test_OODdataset = self.args.test_dataset  
        if self.test_OODdataset == "coco_extended_ood_val":
            self.gt_OODcoco_api = COCO(self.args.dataset_dir + "/instances_val2017_extended_ood.json")
        elif self.test_OODdataset == "coco_mixed_val":
            self.gt_OODcoco_api = COCO(self.args.dataset_dir + "/instances_val2017_mixed_OOD.json")
            self.gt_IDcoco_api = COCO(self.args.dataset_dir + "/instances_val2017_mixed_ID.json")
        # load prediction
        inference_output_dir = get_inference_output_dir(
            cfg_OUTPUT_DIR,
            self.test_OODdataset,
            self.args.inference_config,
            self.args.image_corruption_level)
        #prediction_file_name = os.path.join('../configs','instances_val2017_mixed_OOD.json')
        prediction_file_name = os.path.join('../data','coco_instances_results_idood.json')
        self.res_coco_api = self.gt_OODcoco_api.loadRes(prediction_file_name)

        imgidlist = list(self.gt_OODcoco_api.imgs.keys())
        print(f"imgidlist={imgidlist}")
        self.imgidlist = []
        for imgID in imgidlist:
            #gt_list_this_img = self.gt_OODcoco_api.loadAnns(self.gt_OODcoco_api.getAnnIds(imgIds=imgID))
            #if len(gt_list_this_img) == 0:
            #    continue
            
            self.imgidlist.append(imgID)
        self.voc_class = ['person', 'bird', 'cat', 'cow', 'dog', 'horse', 'sheep', 'airplane', 'bicycle', 'boat', 'bus', 'car', 'motorcycle', 'train', 'bottle', 'chair', 'dining table', 'potted plant','couch', 'tv']

    def func(self, img, boxes, color, text):
        newimg = VisImage(img[:,:,::-1])
        for i in range(len(boxes)):
            newimg.ax.add_patch(
                mpl.patches.Rectangle(
                    (int(boxes[i][0]), int(boxes[i][1])),
                    int(boxes[i][2]),
                    int(boxes[i][3]),
                    fill=False,
                    edgecolor=color,
                    linewidth=2,
                    alpha=0.5,
                    linestyle="-",
                )
            )

            newimg.ax.text(int(boxes[i][0]) + 5,
                            int(boxes[i][1]) + 4,
                            text[i],
                            size=8,
                            family="sans-serif",
                            bbox={"facecolor": "black", "alpha": 0.8, "pad": 0.7, "edgecolor": "none"},
                            verticalalignment="top",
                            horizontalalignment="left",
                            color="white",
                            zorder=10,
                            rotation=0,
                            )
        return newimg.get_image()[:,:,::-1]


    def generate_xml(self,img_name, boxes, classes):
        img_path = self.img_path
        root = ET.Element("annotation")

        folder = ET.SubElement(root, "folder")
        folder.text = img_name

        filename = ET.SubElement(root, "filename")
        filename.text = img_name

        size = ET.SubElement(root, "size")
        width = ET.SubElement(size, "width")
        height = ET.SubElement(size, "height")
        depth = ET.SubElement(size, "depth")
        
        file_path = os.path.join(img_path, img_name)
        image = Image.open(file_path)
        img_width, img_height = image.size
        
        # 设置图像的宽度、高度和通道数
        width.text = str(img_width)
        height.text = str(img_height)
        depth.text = str("3")
        
        for i in range(len(boxes)):
            
            box = boxes[i]
            class_name = classes[i]
            print(f"box={box}")
            object_elem = ET.SubElement(root, "object")
            name = ET.SubElement(object_elem, "name")
            name.text = class_name

            bndbox = ET.SubElement(object_elem, "bndbox")
            xmin = ET.SubElement(bndbox, "xmin")
            ymin = ET.SubElement(bndbox, "ymin")
            xmax = ET.SubElement(bndbox, "xmax")
            ymax = ET.SubElement(bndbox, "ymax")
            # 设置边界框的坐标
            xmin.text = str(box[0].item())
            ymin.text = str(box[1].item())
            xmax.text = str(box[2].item())
            ymax.text = str(box[3].item())

        tree = ET.ElementTree(root)
        xml_path = os.path.join(img_path, img_name.replace(".jpg", ".xml"))
        tree.write(xml_path)

    def readdata(self):
        self.img_dict = {}
        for imgID in self.imgidlist:
            self.img_dict[imgID] = {}
            # load ood gt
            OOD_gt_this_img = self.gt_OODcoco_api.loadAnns(self.gt_OODcoco_api.getAnnIds(imgIds=[imgID]))
            self.img_dict[imgID].update({"OOD_gt": torch.Tensor([gti['bbox'] for gti in OOD_gt_this_img]).reshape(-1, 4)})
            # load id gt
            if self.test_OODdataset == "coco_mixed_val":
                ID_gt_this_img = self.gt_IDcoco_api.loadAnns(self.gt_IDcoco_api.getAnnIds(imgIds=imgID))
                self.img_dict[imgID].update({"ID_gt": torch.Tensor([gti['bbox'] for gti in ID_gt_this_img]).reshape(-1, 4)})
            # load id prediction
            res_list_this_img = self.res_coco_api.loadAnns(self.res_coco_api.getAnnIds(imgIds=[imgID]))
            ID_res_list_this_img = [res for res in res_list_this_img if res["category_id"]!=81]
            self.img_dict[imgID].update({"ID_res": torch.Tensor([res['bbox'] for res in ID_res_list_this_img]).reshape(-1, 4)})
            self.img_dict[imgID].update({"ID_res_score": torch.Tensor([res['score'] for res in ID_res_list_this_img])})
            self.img_dict[imgID].update({"ID_res_class": [res['category_id'] for res in ID_res_list_this_img]})
            # load ood prediction
            OOD_res_list_this_img = [res for res in res_list_this_img if res["category_id"]==81]
            self.img_dict[imgID].update({"OOD_res": torch.Tensor([res['bbox'] for res in OOD_res_list_this_img]).reshape(-1, 4)})
            
            self.img_dict[imgID].update({"img_path": self.img_path + self.gt_OODcoco_api.loadImgs(imgID)[0]['file_name']})

    
    def vis_all(self, vis_gtID, vis_gtOOD, vis_resID, vis_resOOD):
        print(f"self.imgidlist={self.imgidlist}")
        for imgID in self.imgidlist:
            img_with_gt = cv2.imread(self.img_dict[imgID]["img_path"])
            # OOD gt
            if vis_gtOOD:
                OODgt_boxes = self.img_dict[imgID]["OOD_gt"]
                self.func(img_with_gt, OODgt_boxes, color=(0, 255, 0), thickness=4)

            # ID gt
            if vis_gtID and self.test_OODdataset == "coco_mixed_val":
                IDgt_boxes = self.img_dict[imgID]["ID_gt"]   
                self.func(img_with_gt, IDgt_boxes, color=(255, 0, 0), thickness=4)

            boxs = []
            classes = []
            # OOD res
            if vis_resOOD:
                res_boxes = self.img_dict[imgID]["OOD_res"]
                img_with_gt = self.func(img_with_gt, res_boxes, color="blue", text=["unknown"] * len(res_boxes)) #green
                for idx in range(len(res_boxes)):
                    boxs.append(res_boxes[idx])
                    classes.append("unknown")
            # ID res
            if vis_resID:
                res_boxes_ID = self.img_dict[imgID]["ID_res"]
                res_score_ID = self.img_dict[imgID]["ID_res_score"]
                res_class_ID = self.img_dict[imgID]["ID_res_class"]
                id_text = []
                for idx, class_ID in enumerate(res_class_ID):
                    id_text.append("{} {}%".format(self.voc_class[class_ID - 1], int(res_score_ID[idx].item()*100)))
                    boxs.append(res_boxes_ID[idx])
                    classes.append(self.voc_class[class_ID - 1])
                img_with_gt = self.func(img_with_gt, res_boxes_ID, color="yellow", text=id_text)
                
            
            image_name = self.img_dict[imgID]["img_path"].split("/")[-1]
            print(f"boxs={boxs}")
            print(f"classes={classes}")
            self.generate_xml(image_name, boxs, classes)
            cv2.imwrite(self.vis_path + '/{}'.format(self.img_dict[imgID]["img_path"].split("/")[-1]), img_with_gt)


    def run(self):
        self.readdata()
        self.vis_all(vis_gtID=False, vis_gtOOD=False, vis_resID=True, vis_resOOD=True)

        


eva = Draw()
eva.run()
