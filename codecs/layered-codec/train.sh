if (( $# != 2 )); then
    echo "Usage: ./train.sh [0-2], e.g. ./train.sh 2 levels"
    exit
fi
hier=$1
level=$2

modeldir=model

train="/home/mallesh/deepvideo/data/kinetics/train"
eval="/home/mallesh/deepvideo/data/vtl/test"
train_mv="/home/mallesh/deepvideo/data/kinetics/train_mv"
eval_mv="/home/mallesh/deepvideo/data/vtl/test_mv"

if [[ ${hier} == "0" ]]; then
  distance1=6
  distance2=6
  bits=16
  encoder_fuse_level=1
  decoder_fuse_level=1
elif [[ ${hier} == "1" ]]; then
  distance1=3
  distance2=3
  bits=16
  encoder_fuse_level=2
  decoder_fuse_level=3
elif [[ ${hier} == "2" ]]; then
  distance1=1
  distance2=2
  bits=8
  encoder_fuse_level=1
  decoder_fuse_level=1
else
  echo "Usage: ./train.sh [0-2], e.g. ./train.sh 2"
  exit
fi

# Warning: with --save-out-img, output images are stored
# each time we run evaluation. This can take a lot of space
# when using a big evaluation dataset.
# (for the demo data it's okay.)

#  --load-model-name "demo" \
#  --load-iter 10000 \

python3 -u train.py \
  --train ${train} \
  --eval ${eval} \
  --train-mv ${train_mv} \
  --eval-mv ${eval_mv} \
  --encoder-fuse-level ${encoder_fuse_level} \
  --decoder-fuse-level ${decoder_fuse_level} \
  --v-compress --warp --stack --fuse-encoder \
  --bits ${bits} \
  --distance1 ${distance1} --distance2 ${distance2} \
  --max-train-iters 100000 \
  --prev-levels ${level} \
  --save-out-img \
  --save-codes \
  --load-model-name "demo" \
  --load-iter 100000 \
