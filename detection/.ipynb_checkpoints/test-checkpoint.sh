python pre_img.py --img-dir img 
python apply_net.py --dataset-dir img --test-dataset coco_mixed_val --config-file UnSniffer.yaml --inference-config standard_nms.yaml --random-seed 0 --image-corruption-level 0 --visualize 0

cd evaluator/

python visualization.py --img-dir ../img --dataset-dir ../configs --test-dataset coco_mixed_val --outputdir ../output/  --config-file UnSniffer.yaml --inference-config standard_nms.yaml --random-seed 0 --image-corruption-level 0
