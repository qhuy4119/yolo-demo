# build the darknet framework
echo Building darknet and yolov4-tiny
cd web-demo
if [ ! -d "darknet" ]
then
	git clone https://github.com/AlexeyAB/darknet
else
	echo Found existing darknet
fi
cd darknet
sed -i 's/OPENCV=0/OPENCV=1/' Makefile
sed -i 's/AVX=0/AVX=1/' Makefile
sed -i 's/OPENMP=0/OPENMP=1/' Makefile
make
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights data/dog.jpg -dont_show
echo Finish building darknet and yolov4-tiny

# set up trained custom model
echo Setting up trained custom model
cd ../../custom-data
sed -i '/train/c\train = data/custom-data/train.txt' obj.data
sed -i '/valid/c\valid = data/custom-data/val.txt' obj.data
sed -i '/names/c\names = data/custom-data/obj.names' obj.data
sed -i 's@^.*darknet/@@' train.txt val.txt test.txt
sed -i '/backup/c\backup = ' obj.data
cd ..
echo Copying trained custom model into web-demo/darknet/data/custom-data
yes | cp -rf custom-data web-demo/darknet/data
echo Finish setting up trained custom model
