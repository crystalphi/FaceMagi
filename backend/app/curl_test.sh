#IMAGE_FILE=app/static/mnist/4.jpg
#IMAGE_FILE=app/static/attgan_pt/jdas-07.jpg
#IMAGE_FILE=app/static/attgan_pt/vvdd-03.jpg
#IMAGE_FILE=app/static/attgan_pt/vvdd-11-x178.jpg
#IMAGE_FILE=app/static/attgan_pt/vvdd-11-x384.jpg
#IMAGE_FILE=app/static/attgan_pt/vvdd-11.jpg
IMAGE_FILE=app/static/attgan_pt/vvdd-11-full.jpg
#IMAGE_FILE=app/static/attgan_pt/vvdd-14.jpg
# 下面这个图片的宽高比较奇怪，看起来是竖长型，file 查解析度则显示宽度比高度更大，而且输入系统检测不到人脸。
# 但使用预览打开该图片后，将其等比缩放为原来的一半保存，然后恢复原尺寸保存，再查解析度就正常了，输入系统也能正常检测到人脸。
# 应该是原图片有某种问题。
#IMAGE_FILE=app/static/attgan_pt/vvdd-14-full.jpg
#IMAGE_FILE=app/static/attgan_pt/vvdd-15.jpg
#IMAGE_FILE=app/static/attgan_pt/3-ladies-2.png
#IMAGE_FILE=app/static/attgan_pt/three-ladies.jpg

# ----------------------
# wrong request test:
# ----------------------

#curl -F file=@$IMAGE_FILE -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/process'
#curl -F attr=$ATTR -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/process'
#curl -F file='plainxxx' -F attr=$ATTR -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/process'
#curl -F file=@$IMAGE_FILE -F attr=$ATTR -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/processxxx'
#curl -F file=@$IMAGE_FILE -F attr="" -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/process'
#curl -F file=@$IMAGE_FILE -F attr="aaa" -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/process'
#curl -F file=@$IMAGE_FILE -F attr="Bangs,aaa" -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/process'

# ----------------------
# attgan_pt test:
# ----------------------

# 可用的人脸属性参数值：
# Bald Bangs Black_Hair Blond_Hair Brown_Hair Bushy_Eyebrows Eyeglasses
# Male Mouth_Slightly_Open Mustache No_Beard Pale_Skin Young

ATTS='Bangs'
#ATTS='Blond_Hair'
#ATTS='Young'
#ATTS='Pale_Skin,Young'
#ATTS='Mustache,Male'
#ATTS='Bangs,Brown_Hair'
#ATTS='Bangs,Pale_Skin,Blond_Hair'

curl -F image=@$IMAGE_FILE -F params='{"atts":"'$ATTS'"}' -X POST 'http://127.0.0.1:5000/api/v1/attgan_pt/process'

# ----------------------
# attgan_pt test:
# ----------------------

#ITEM='xxx'
#ITEM='XMY-014'
ITEM='XMY-074'
#curl -F image=@$IMAGE_FILE -F params='{"makeup_name":"'$ITEM'"}' -X POST 'http://127.0.0.1:5000/api/v1/beautygan/process'

