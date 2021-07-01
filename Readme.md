web-demo: everything about the web app
yolov4: everything about the model

training procedure:
1. get darknet
2. get pretrained weights
3. test to see default model is working
4. prepare custom dataset
	1. images
		run js file to generate urls
		run python script to download from urls
	2. labels
		use LabelImg to annotate
	3. custom cfg file
	4. .data and .names file
5. training
