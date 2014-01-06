#include <stdio.h>
#include <opencv2/opencv.hpp>

using namespace cv;

int main( int argc, char** argv )
{
    Mat image;
    image = imread( argv[1], 1 );

    if( argc != 2 || !image.data )
        {
            printf( "No image data \n" );
            return -1;
        }


    Mat dst;
    dst = image.clone();

    Mat ff = cvCreateImage(Size(29, 29), IPL_DEPTH_8U, 3);
    resize(image, ff, ff.size(), 0, 0, INTER_NEAREST);
    std::cout << "blahblah" << "\n";
    
    namedWindow( "Display Image", CV_WINDOW_NORMAL );
    imshow( "Display Image", image );

    waitKey(0);

    return 0;
}
