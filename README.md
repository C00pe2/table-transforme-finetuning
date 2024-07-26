# Why I need to fine tuning Table Transformer
__Table Transformer(TT), which is based on DETR, performed well in table detection. But in some scence table detection it's easy to miss tables.__

This limitation was occured in my task, I need a model or a method to detect the table from contract, invoice, finacial report. I use table transformer and it's pre-train checkpoint which is announced in Table-transformer's repo.

But when I use the pre-train checkpoint, detection precsion is about 70%, is good but is not good as I excepted, or as shown in original repo.

# Why TT has limitation in scence table
__Original Dateset PubTables-1M Data Distribution__
As is shown in __PubTables-1M: Towards comprehensive table extraction from unstructured documents__ , this datasets contains nearly one million tables from scientific articles.(If it contains other scence please leet me know). This implies that these tables, compared to scene-type tables, will be clearer, with less inclination and distortion, and less affected by environmental interference. I also see some example in [Dataset Ninja](https://datasetninja.com/pubtables-1m#download), for the original datasets is too huge for me to download. 

Unfortunatly, about half of images in my task(contract, invoice, reports) are collected through photography and uploaded without any artifical process. Distortion, interference, and inclination are very common in the samples. By analysing the badcase, the missing table detection case are almost scence image. I also try some pre-processing tricks, but the imporvement is very limited.I need to find a scence table dataset to fine tune TT.

# A good Finetuning Dataset - TabRecSet
Accroding to [issue#108](https://github.com/microsoft/table-transformer/issues/108). 1k could be enough for either detection or structure recognition. I finally find TabRecSet can satisfy my fine tune. [TabRecSet](https://github.com/MaxKinny222/TabRecSet?tab=readme-ov-file) contains 10855 images, and most of them are come from camera photo, you can see some extremely distorted and inclined samples for the model to learn from.

# Dataset processing
The annotation is stored in json format, not xml. Before fine tune you neet to convert info in json to xml. I upload a python file to support this process.
```
cd scripts
python process_tab_rec_set.py
```

# Training and Evaluation Data
This process is same in [Table Transformer repo](https://github.com/microsoft/table-transformer), I copy from it 

By the way you need to sort TabRecSet folder structure like below
```
- datasets_root
|_images
|_train
    |_xxxx.xml
    |_...
|_test
|_val
```
# Model Fine tune
The code trains models for 2 different sets of table extraction tasks:

1. Table Detection

For a detailed description of these tasks and the models, please refer to the paper.

To train, you need to ```cd``` to the ```src``` directory and specify: 1. the path to the dataset, 2. the task (detection or structure), and 3. the path to the config file, which contains the hyperparameters for the architecture and training.

To fine tune the detection model:
```
python main.py --data_type detection --config_file detection_config.json --data_root_dir /path/to/detection_data --model_load_path /path/to/model.pth --load_weights_only
```
