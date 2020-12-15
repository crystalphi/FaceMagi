echo 'prepare celeba images according file filelist.txt.orig...'

#find img_crop_celeba -name "010*.jpg" | xargs -I{} cp {} ./img_crop_celeba_1w

# not this: IMAGE_SRC=../../../../../datasets/CelebA/Img/img_align_celeba
IMAGE_SRC=../../../../../datasets/CelebA/Img/img_crop_celeba
IMAGE_DST=../../images/celeba
rm -rf $IMAGE_DST && mkdir -p $IMAGE_DST

echo "copy images ..."
grep celeba filelist.txt.orig | xargs -I{} echo {} | cut -b 8-17 | xargs -I{} cp $IMAGE_SRC/''{} $IMAGE_DST

echo "resize to 448 ..."
find ../../images/celeba -name "*.jpg" | xargs -I{} convert -resize 448x448 {} {}

echo 'Done! total images:' `ls ../../images/celeba|wc -l`

