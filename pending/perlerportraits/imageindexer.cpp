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


Mat index_image(Mat img, vector<Vec3b> indexcolors){
    Mat labimg = img.clone();
    cvtColor(img, labimg, CV_BGR2Lab);

    Vec3b p;
    for(int r = 0; r < img.rows; r++){
        for(int c = 0; c < img.cols; c++){
            p = labimg.at<Vec3b>(r,c);
            //printf("(%u,%u,%u) ", p[0], p[1], p[2]);
            // get the value from indexcolors that is closest to p
            // set labimg to that value
            Vec3b closest;
            double dist;
            double mindist = 100000; 

            for(int i = 0; i < indexcolors.size(); i++){
                dist = norm(p, indexcolors[i]);
                if (dist < mindist){
                    closest = indexcolors[i];
                    mindist = dist;
                }
            }
            
            labimg.at<Vec3b>(r,c) = closest;
        }
    }
    
    cvtColor(labimg, img, CV_Lab2BGR);
    return img;
}

// load palette colors from an image (this
// image is assumed to contain only colors from this palette
vector<Vec3b> read_palette_img(string paletteimg){

    vector<Vec3b> elems;
        
    // each pixel is a unique color.
    Mat palette = imread(paletteimg, 1);
    cvtColor(palette, palette, CV_BGR2Lab);
    
    Vec3b p;
    for(int r = 0; r < palette.rows; r++){
        for(int c = 0; c < palette.cols; c++){
            p = palette.at<Vec3b>(r,c);
            //printf("(%u,%u,%u) ", p[0], p[1], p[2]);
            elems.push_back(p);
        }
    }
    
    // namedWindow( "key", CV_WINDOW_NORMAL );
    // imshow("key", palette);
    // waitKey(0);
        
    return elems;
}

void webcamfunc(){
    CvCapture* capture = 0;
    Mat frame, frameCopy, subimg;
    int halfbox = 170;
    Rect r;
    
    vector<Vec3b> indexcolors = read_palette_img("palette.png");
    
    // can also be 49 x 69
    subimg = cvCreateImage(Size(29,29), IPL_DEPTH_8U, 3);
    
    capture = cvCaptureFromCAM( 0 ); //0=default, -1=any camera, 1..99=your camera
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
                
                r = Rect(frame.cols/2 - halfbox, frame.rows/2 - halfbox, 2*halfbox, 2*halfbox);
                resize(frame(r), subimg, subimg.size(), 0, 0, INTER_NEAREST);
                
                subimg = index_image(subimg, indexcolors);
                
                //printf("m.type() = %d\n", subimg.type());
                
                imshow("result", subimg);
                
                if( waitKey( 10 ) >= 0 ){
                    cvReleaseCapture( &capture );
                    break;
                }
            }
        
        //waitKey(0);
        
        cvDestroyWindow("result");
    }

}    

// Index an image using the given palette
void cvtImage(string fname, string palettename){
    printf("Reading file: %s\n", fname.c_str());
    vector<Vec3b> indexcolors = read_palette_img(palettename);
    Mat m = imread(fname, 1);
    m = index_image(m, indexcolors);
    imwrite("palout-" + fname, m);
    printf("Writing to file: palout-%s\n", fname.c_str());
}


int main( int argc, const char** argv )
{
    //webcamfunc();
    if (argc < 2){
        printf("Usage: w for webcam, nothing to show the palette.\n");
        return 0;
    }

    if (argv[1][0] == 'w'){
        printf("Ah yes, the webcam!\n");
        webcamfunc();
    }else{
        cvtImage(argv[1], "palette.png");
    }
}
