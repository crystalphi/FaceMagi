BACKEND="torch"
#BACKEND="caffe+scipy"

#INPUT_IMAGE=images/facemodel/lfwgoogle/Aaron_Eckhart/00000004.jpg
#INPUT_IMAGE=images/input.png
INPUT_IMAGE=images/input-400x300.png

#INPUT_IMAGE=images/jpg-816x1000/jdas-07.jpg
#INPUT_IMAGE=images/jpg-816x1000/three-ladies.jpg
INPUT_IMAGE=images/jpg-816x1000/vvdd-11.jpg

#EFFECT=facehair
EFFECT=younger
#EFFECT=older
#EFFECT=senior

K="--K 50" # default 100
SPEED="--iter 100" # default 500

# For most transformations, an ideal delta value will be between 0.0 and 1.0 with --scaling beta (between 0.0 and 5.0 with --scaling none).

#python2 demo2.py $EFFECT $K $INPUT_IMAGE $SPEED --delta 2.5,3.5,4.5 --backend $BACKEND
#python2 demo2.py $EFFECT $K $INPUT_IMAGE $SPEED --delta 3.5 --extradata --backend $BACKEND
python3 demo2.py $EFFECT $K $INPUT_IMAGE $SPEED --delta 2.5 --backend $BACKEND

#python2 demo2.py $EFFECT $K $INPUT_IMAGE $SPEED --delta 0.6 --scaling beta # scaling beta not good

