# Utils for Comparision-paper 2018

# Usage
Since perceptin does not provide automatic exposure corrections, slight change in lighting condition affected the image quality. Thus, some sort of image enhancement technique was required to balance the lighting effects. Adaptive histogram equalization [1] is used to enhance images.

Some packages can work by streaming bag files while others might require to read a collection of image or read directly from bag files. Thus, two methods are implemented seaprately.

### Storing enhanced images in another bag file
Used if the package directly parses the bag file or read images from folder.

- **rosrun vo_comparision bag_exposure_enhance.py --inbag *input_bag_file* --outbag *output_bag_file* **

If sequence of image are required to be read from image, we can dump images to folder using

- **rosrun image_view image_saver image:=*image_topic* _filename_format:=image%0\6d.jpg**

## References
[1] https://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
