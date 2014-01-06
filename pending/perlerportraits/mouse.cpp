#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <opencv2/contrib/contrib.hpp>

using namespace cv;

void my_mouse_callback( int event, int x, int y, int flags, void* param );

Rect box;
bool drawing_box = false;
Mat image;
Mat orig;

void draw_box( Mat img, Rect box2 ){
    rectangle( img, Point(box2.x, box2.y), Point(box2.x+box2.width,box2.y+box2.height),
               Scalar(255,255,255), 1, 8);
}

// Implement mouse callback
void my_mouse_callback( int event, int x, int y, int flags, void* param ){

    switch( event ){
    case CV_EVENT_MOUSEMOVE:
        if( drawing_box ){
            box.width = x-box.x;
            //box.height = y-box.y;
            box.height = box.width;
        }
        break;

    case CV_EVENT_LBUTTONDOWN:
        drawing_box = true;
        box = Rect( x, y, 0, 0 );
        break;

    case CV_EVENT_LBUTTONUP:
        drawing_box = false;
        if( box.width < 0 ){
            box.x += box.width;
            box.width *= -1;
        }
        if( box.height < 0 ){
            box.y += box.height;
            box.height *= -1;
        }
        draw_box( image, box );
        break;
    }
}

void crop(){
    Mat croppedImage;
    Mat(orig, box).copyTo(croppedImage);
    image = croppedImage;
}


int main(int argc, char** argv)
{
    const char* name = "Box Example";
    box = Rect(-1,-1,0,0);

    //IplImage* image = cvLoadImage( "alan.jpg" );
    
    image = imread("alan.jpg", 1);

    orig = image.clone();
    //image = Mat::zeros(500, 700, CV_32F);
    Mat temp = image.clone();
    //IplImage* temp = cvCloneImage( image );

    namedWindow( name, CV_WINDOW_NORMAL );

    // Set up the callback
    setMouseCallback( name, my_mouse_callback, 0);

    int k;
    // Main loop
    while( 1 ){
        //temp = cvCloneImage( image );
        temp = image.clone();
        if( drawing_box )
            draw_box( temp, box );
        imshow( name, temp );

        k = waitKey(15); // wait 15ms
        if( k  == 27 ) // this is escape
            break;
        else if( k == 10 ){ // this is enter
            if (box.x != -1){
                crop();
            }
        }else if(k == 117){ // this is u
            // undo!
            image = orig.clone();
            box = Rect(-1, -1, 0,0);
        }else if (k == 103) { // this is g
            if (image.rows != image.cols){
                printf("The image needs to be a square first! Select an area\n");
            }else{
                // resize
                Mat n = cvCreateImage(Size(29,29), IPL_DEPTH_8U, 3);
                resize(image, n, n.size(), 0, 0, INTER_NEAREST);
                image = n;
            }
        }
        //printf("key: %d\n", k);
    }

    return 0;
}
