#EXP_NAME=128_shortcut1_inject1_none
EXP_NAME=384_shortcut1_inject0_none_hq
#EXP_NAME=384_shortcut1_inject1_none_hq

DEVICE=--gpu


# To test with single attribute editing

#CUDA_VISIBLE_DEVICES=0 \
#python3 -m test \
#--experiment_name $EXP_NAME \
#--test_int 1.0 \
#--custom_img \
#$DEVICE

# To test with multiple attributes editing

CUDA_VISIBLE_DEVICES=0 \
python3 -m test_multi \
--experiment_name $EXP_NAME \
--test_atts Bangs Young \
--test_ints 0.5 0.5 \
--custom_img \
$DEVICE

# To test with attribute intensity control

#CUDA_VISIBLE_DEVICES=0 \
#python3 -m test_slide \
#--experiment_name $EXP_NAME \
#--test_att Male \
#--test_int_min -1.0 \
#--test_int_max 1.0 \
#--n_slide 10 \
#$DEVICE

# To test with your custom images (supports test.py, test_multi.py, test_slide.py)

#CUDA_VISIBLE_DEVICES=0 \
#python3 -m test \
#--experiment_name $EXP_NAME \
#--test_int 1.0 \
#--custom_img \
#$DEVICE

# Your custom images are supposed to be in ./data/custom and you also need an attribute list of the images ./data/list_attr_custom.txt. Please crop and resize them into square images in advance.<Paste>
