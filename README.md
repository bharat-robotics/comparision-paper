# Utils for Comparision-paper 2018

# Usage
Since perceptin does not provide automatic exposure corrections, slight change in lighting condition affected the image quality. Thus, some sort of image enhancement technique was required to balance the lighting effects. Adaptive histogram equalization [1] is used to enhance images.

Some packages can work by streaming bag files while others might require to read a collection of image or read directly from bag files. Thus, two methods are implemented separately.

However, it should be better to produce the enhanced bag file first and then, run it.

### Record CPU and Memory Usage
We are sampling the cpu and memory usage per second. The script *record_usage.py* will record the cpu and memory usage to different files so that we can use that later.

Script will record the memory usage of any number of process id's. We must pass the process id of all nodes that the package is running and total usage is recorded in files.

- **python record_usage.py --p *process_ids* --mem_file *memory file* --cpu_file *cpu file***

  *python record_usage.py --p 11234 12434 1242 --mem_file mem.txt --cpu_file cpu.txt*

### Storing enhanced images in another bag file
Used if the package directly parses the bag file or read images from folder.

- **rosrun vo_comparision bag_exposure_enhance.py --inbag *input_bag_file* --outbag *output_bag_file***

If sequence of image are required to be read from folder, we can dump images to folder using

- **rosrun image_view image_saver image:=*image_topic* _filename_format:=image%06d.jpg**

The files should be saved in the current working directory.

### Using ros node

If the package subscribes to topics directly, enhanced images can be published directly using ros node.
- **rosrun vo_comparision enhance_images.py**

This node subscribes to /pirvs/left/image_raw/compressed and publishes on /pirvs/left/image/compressed topic. Similar for right stereo image as well.

Package requiring raw image must use image transport to convert compressed to raw images.
- **rosrun image_transport republish compressed in:=in_topic raw out:=out_topic**

### Changing enhancement parameters

Two paremeters can be tuned for best performance for correonding package clipLimit and tileGridSize in both the files mentioned above.

I got good results with:
- **Indoor husky data: clipLimit=1.0, tileGridSize=(2, 2)**
- **Outdoor husky data: clipLimit=2.0, tileGridSize=(5, 5)**

But it may vary with package and this could be staring point.


## References
[1] https://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
