INPUT_DIR=test_img

#STYLE=Hayao
#STYLE=Hosoda
#STYLE=Paprika
STYLE=Shinkai

GPU=0
#GPU=-1

python3 test.py --input_dir $INPUT_DIR --style $STYLE --gpu $GPU

