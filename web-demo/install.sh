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
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29
cd ..
