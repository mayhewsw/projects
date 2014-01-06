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


void index_image(Mat img, vector<Vec3b> indexcolors){
    //cvtColor(subimg, subimg, CV_BGR2Lab);
    
    vector<Vec3b> v;
    v.push_back(Vec3b(3, 4, 5));

    
}

vector<string> &split(const string &s, char delim, vector<string> &elems) {
    stringstream ss(s);
    string item;
    while (getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}


vector<string> split(const string &s, char delim) {
    vector<string> elems;
    split(s, delim, elems);
    return elems;
}

vector<Vec3b> read_file(){
    string fname = "PixelArt.gpl";

    vector<Vec3b> elems;
    
    string line;
    ifstream myfile;
    myfile.open("PixelArt.gpl");

    int i = 0;
    if (myfile.is_open()){
        
        while ( getline (myfile, line) ){
            // there are 4 lines of rubbish at the top of the file
            if (i >= 4){ 
                //cout << line << '\n';
                vector<string> ss = split(line, ' ');
                elems.push_back(Vec3b(atoi(ss[0].c_str()), atoi(ss[1].c_str()), atoi(ss[2].c_str())));
            }
            i++;
        }
    }
    myfile.close();
    
    return elems;
}
    


//void draw_box( Mat img, Rect box2 ){
//    rectangle( img, Point(box2.x, box2.y), Point(box2.x+box2.width,box2.y+box2.height),
//               Scalar(255,255,255), 1, 8);
//}


int main( int argc, const char** argv )
{
    CvCapture* capture = 0;
    Mat frame, frameCopy, subimg;
    int halfbox = 170;
    Rect r;

    vector<Vec3b> indexcolors = read_file();
    
    // 49 x 69
    subimg = cvCreateImage(Size(29,29), IPL_DEPTH_8U, 3);
    
    capture = cvCaptureFromCAM( 0 ); //0=default, -1=any camera, 1..99=your camera
    if(!capture) cout << "No camera detected" << endl;
    
    namedWindow( "result", CV_WINDOW_NORMAL );
    
    if( capture )
        {
            cout << "In capture ..." << endl;
            for(;;)
                {
                    IplImage* iplImg = cvQueryFrame( capture );
                    frame = iplImg;
                    if( frame.empty() )
                        break;
                    
                    r = Rect(frame.cols/2 - halfbox, frame.rows/2 - halfbox, 2*halfbox, 2*halfbox);
                    resize(frame(r), subimg, subimg.size(), 0, 0, INTER_NEAREST);
                    
                    index_image(frame, indexcolors);
                    
                    // double sum=0;
                    // for(int i = 0; i < subimg.rows; i++){
                    //     const double* Mi = subimg.ptr<double>(i);
                    //     for(int j = 0; j < subimg.cols; j++)
                    //         sum += max(Mi[j], 0.);
                    //     printf(
                    // }
                    //printf("sum %f\n", sum);
                    Vec3b s = subimg.at<Vec3b>(0,0);
                    printf("B: %u G: %u R: %u\n", s[0], s[1], s[2]);
                    
                    //printf("m.type() = %d\n", subimg.type());
                    
                    imshow("result", subimg);
                    
                    if( waitKey( 10 ) >= 0 ){
                        cvReleaseCapture( &capture );
                        break;
                    }
                }

            //waitKey(0);

            cvDestroyWindow("result");

            return 0;
        }
}
