# YOLO Training

1. cd yolo-training

## Labeling

1. git clone https://github.com/Cartucho/OpenLabeling
2. cd OpenLabeling
3. pip3 install -r requirements.txt
4. git submodule update --init
5. cd main
6. echo licenseplate > class_list.txt
7. python3 main.py -i ../../images -o ../../labels
8. cd ../..

## Training On Prem

1. git clone https://github.com/pjreddie/darknet.git
2. mkdir backup
3. python3 processData.py
4. cd darknet
5. wget https://pjreddie.com/media/files/darknet53.conv.74
6. echo licenseplate > objects.names
7. sudo apt install -y gcc g++
8. make
9. ./darknet detector train ../trainer.data ../yolov3.cfg darknet53.conv.74

## Training On Cloud

1. Upload notebook and folders to Google Drive
2. Open notebook on Google Colab
3. Run all cells in notebook
