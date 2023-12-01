# 基于Unknown Sniffer for Object Detection的labelImg辅助生成项目

关于Unknown Sniffer for Object Detection学习:
### [`Paper`](https://arxiv.org/abs/2303.13769) [`Bilibili`](https://www.bilibili.com/video/BV1xM4y1z7Hv/?buvid=XYC2EDBCCC2B3C4802E4AAD1035EFACB2AC57&is_story_h5=false&mid=vL1Nha2VQkhwiq6%2FLPmtbA%3D%3D&plat_id=147&share_from=ugc&share_medium=android&share_plat=android&share_session_id=a280f047-3ced-4b9d-acb2-40244f9a55fb&share_source=WEIXIN&share_tag=s_i&timestamp=1679647440&unique_k=2n8pmaV&up_id=253369834&vd_source=668f39404189897ee2f8d0c7596f9f4e) [`Youtube`](https://www.youtube.com/watch?v=AI2mfO2CycM) [`Slides`](https://docs.google.com/presentation/d/1YUxG_NnjeIiSZjHpIgS9wtETqZQ1MD0s/edit?usp=sharing&ouid=104225774732865902245&rtpof=true&sd=true) [`Project`](https://github.com/Went-Liang/UnSniffer)

# Introduction

  一个简单的labelImg生成项目,将图片放入指定目录,如(img下),会自动生成可以被labelImg识别的xml文件,因为模型的特性,除了可以识别到的类别,也可以识别到一些Unknown的类别. 由于是通用模型,所以一开始的识别可能不尽人意,但是也能减轻部分工作量了,一些图片还是比较好识别的.
  
基于目前的版本只是基于源预训练模型进行推理,稍微调整了一些参数.

# Requirements
```bash
pip install -r requirements.txt
pip install ujson
apt update
apt install libmagickwand-dev

```

In addition, install detectron2 following [here](https://detectron2.readthedocs.io/en/latest/tutorials/install.html).
```bash
# 根据自己的版本来
python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html
```

预训练文件: 需要放入data目录下
[model_final.pth](https://drive.google.com/file/d/1kp60e6nh0iIOPd41f4JI6Yo9r_r7MqRo/view?usp=sharing).

# Dataset Preparation

**COCO**

可以将图片放入img目录下(或者在test.sh里配置自定义目录)

项目需要coco格式的文件,稍微做了点优化,会自己生成其他配置文件,所以只用放入图片到文件夹就可以了

!!!! 为了方便,如果图片文件名不符合规范会直接修改,所以如果文件名有用,最好将图片copy到img目录下

# Start
```bash
sh test.sh
```

# License

This repository is released under the Apache 2.0 license as found in the [LICENSE](LICENSE) file.


# Citation

    @inproceedings{liang2023unknown,
    title={Unknown Sniffer for Object Detection: Don't Turn a Blind Eye to Unknown Objects},
    author={Liang, Wenteng and Xue, Feng and Liu, Yihao and Zhong, Guofeng and Ming, Anlong},
    booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
    year={2023}
    }

**Acknowledgments:**

UnSniffer builds on previous works code base such as [VOS](https://github.com/deeplearning-wisc/vos) and [OWOD](https://github.com/JosephKJ/OWOD). If you found UnSniffer useful please consider citing these works as well.
