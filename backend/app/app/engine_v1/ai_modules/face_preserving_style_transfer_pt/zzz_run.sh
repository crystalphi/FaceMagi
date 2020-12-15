#MODEL=models/grande-jatte.pth
#MODEL=models/manga.pth
#MODEL=models/manga-face.pth
#MODEL=models/mosaic.pth
MODEL=models/mosaic-face.pth
#MODEL=models/rains-rustle.pth
#MODEL=models/stary-night.pth
#MODEL=models/wave.pth

CONTENT_IMAGE=images/content/vvdd-11.jpg

python3 -m src.stylize --content-image $CONTENT_IMAGE --style-model $MODEL --output zzz_output.png

