#include "ros/ros.h"
#include "sensor_msgs/Image.h"
#include "sensor_msgs/CompressedImage.h"
#include "cv_bridge/cv_bridge.h"
#include "message_filters/subscriber.h"
#include "message_filters/synchronizer.h"
#include "message_filters/sync_policies/approximate_time.h"

#include <opencv2/highgui/highgui.hpp>

typedef message_filters::Subscriber<sensor_msgs::CompressedImage> CompressedImage_Sub_Type;
typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::CompressedImage,sensor_msgs::CompressedImage> StereoSyncPolicy;


class enhance_images
{

  protected:

    ros::Publisher left_enhance_pub; // Publisher to the enhanced left image
    ros::Publisher right_enhance_pub; // Publisher to the enhanced right image

    CompressedImage_Sub_Type *left_image_sub; // Subscriber to the left image
    CompressedImage_Sub_Type *right_image_sub; // Subscriber to the right image
    message_filters::Synchronizer<StereoSyncPolicy>* stereo_sync_policy; //Synvhronizer for stereo images

    float clim;
    cv::Size tilesize;


  public:

      enhance_images(ros::NodeHandle& nh) {

        left_enhance_pub = nh.advertise<sensor_msgs::CompressedImage>("/pirvs/left/image/compressed", 5);
        right_enhance_pub = nh.advertise<sensor_msgs::CompressedImage>("/pirvs/left/image/compressed", 5);

        left_image_sub = new CompressedImage_Sub_Type(nh,"/pirvs/left/image_raw/compressed", 5);
        right_image_sub = new CompressedImage_Sub_Type(nh,"/pirvs/right/image_raw/compressed", 5);

        stereo_sync_policy = new message_filters::Synchronizer<StereoSyncPolicy>(StereoSyncPolicy(5),*left_image_sub,*right_image_sub);
        stereo_sync_policy->registerCallback(boost::bind(&enhance_images::stereoCallback, this, _1, _2));

        clim = 1.0;
        tilesize =  cv::Size(2,2);

      }

    void stereoCallback(const sensor_msgs::CompressedImage::ConstPtr& left_image_msg, const sensor_msgs::CompressedImage::ConstPtr& right_image_msg) {

      cv::Mat cv_left =  cv::imdecode(cv::Mat(left_image_msg->data),CV_LOAD_IMAGE_GRAYSCALE);
      cv::Mat cv_right =  cv::imdecode(cv::Mat(right_image_msg->data),CV_LOAD_IMAGE_GRAYSCALE);

      cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE();
      clahe->setClipLimit(clim);
      clahe->setTilesGridSize(tilesize);

      cv::Mat enhanced_left,enhanced_right;
      clahe->apply(cv_left, enhanced_left);
      clahe->apply(cv_right, enhanced_right);

      sensor_msgs::CompressedImage left_enhanced_msg,right_enhanced_msg;
      left_enhanced_msg.header = left_image_msg->header;
      right_enhanced_msg.header = right_image_msg->header;
      left_enhanced_msg.format = "jpeg";
      right_enhanced_msg.format = "jpeg";


      cv::imencode(".jpg", cv_left, left_enhanced_msg.data);
      cv::imencode(".jpg", cv_right, right_enhanced_msg.data);

      left_enhance_pub.publish(left_enhanced_msg);
      right_enhance_pub.publish(right_enhanced_msg);
    }
};


int main(int argc, char **argv){
  ros::init(argc,argv,"enhance_images");

  ros::NodeHandle n;
  enhance_images enhancer(n);

  ros::spin();
}
