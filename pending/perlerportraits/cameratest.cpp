#include <opencv2/opencv.hpp>
#include <opencv2/objdetect/objdetect.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <algorithm> // for copy
#include <iterator> // for ostream_iterator
#include <vector>
#include <fstream>
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;


void webcamfunc(){

    Mat frame, frameCopy;
    int halfbox = 170;
    Rect r;
    
    CvCapture* capture = 0;    
    capture = cvCaptureFromCAM( 0 ); //0=default, -1=any camera, 1..99=your camera
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH,  1280);
    cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, 800);

    if(!capture) cout << "No camera detected" << endl;
    
    namedWindow( "result", CV_WINDOW_NORMAL );
    
    if( capture ){

        cout << "In capture ..." << endl;
        for(;;)
            {
                IplImage* iplImg = cvQueryFrame( capture );
                frame = iplImg;
                if( frame.empty() )
                    break;

                cout << frame.rows << ", ";
                cout << frame.cols << "\n";
                
                imshow("result", frame);;

                
                if( waitKey( 10 ) >= 0 ){
                    cvReleaseCapture( &capture );
                    break;
                }
            }
        
        //waitKey(0);
        
        cvDestroyWindow("result");
    }

}    

int main( int argc, const char** argv )
{

    webcamfunc();
    
}
