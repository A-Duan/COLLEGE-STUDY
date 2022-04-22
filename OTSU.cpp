#include"opencv2/opencv.hpp"
#include"opencv2/highgui/highgui.hpp"
#include<iostream>
#include<string>

using namespace cv;
using namespace std;
void ImageThreshold(String str) {
	Mat image = imread(str);
	Mat binary;
	cvtColor(image, binary, COLOR_BGR2GRAY);
	imshow("test_opencv_srtup", binary);
	waitKey(0);
}
//OSTU算法求出图像二值化阈值
int OTSU(Mat srcImage){
	int nCols = srcImage.cols;
	int nRows = srcImage.rows;
	int threshold = 0;
	//初始化参数
	int nSumPix[256];
	float nProDis[256];
	for (int i = 0; i < 256; i++) {
		nSumPix[i] = 0;
		nProDis[i] = 0;
	}
	//统计灰度集中每个像素在整幅画中的个数
	for (int i = 0; i < nRows; i++) {
		for (int j = 0; j < nCols; j++) {
			nSumPix[(int)srcImage.at<uchar>(i, j)]++;
		}
	}
	//计算每个灰度级占图像中的概率分布
	for (int i = 0; i < 256; i++) {
		nProDis[i] = (float)nSumPix[i] / (nCols * nRows);
	}
	//遍历灰度级[0,255],计算出最大类间方差下的阈值
	float w0, w1, u0_temp, u1_temp, u0, u1, delta_temp;
	double delta_max = 0.0;
	for (int i = 0; i < 256; i++) {
		//初始化相关系数
        //属于前景的像素点数占整幅图像的比例记为w0，其平均灰度u0
        //背景像素点数占整幅图像的比例为w1，其平均灰度为u1
        //图像的总平均灰度记为u：u = w0*u0 + w1*u1
        //delta=w0(u0-u)^2+w1(u1-u)^2
		w0 = w1 = u0 = u1 = u0_temp = u1_temp = delta_temp = 0;

		for (int j = 0; j < 256; j++) {
            //背景部分
            if (j <= i)
            {
                w0 += nProDis[j];
                u0_temp += j * nProDis[j];
            }
            //前景部分
            else
            {
                w1 += nProDis[j];
                u1_temp += j * nProDis[j];
            }
        }
        //计算两个分类的平均灰度
        u0 = u0_temp / w0;
        u1 = u1_temp / w1;
        //依次找到最大类间方差下的阈值
        delta_temp = (float)(w0 * w1 * pow((u0 - u1), 2)); //前景与背景之间的方差(类间方差)
        if (delta_temp > delta_max)
        {
            delta_max = delta_temp;
            threshold = i;
        }
    }
    return threshold;
}
int main()
{
    namedWindow("srcGray", 0);
    resizeWindow("srcGray", 640, 480);
    namedWindow("otsuResultImage", 0);
    resizeWindow("otsuResultImage", 640, 480);
    namedWindow("dst", 0);
    resizeWindow("dst", 640, 480);
    //图像读取及判断
    Mat srcImage;
    srcImage = imread("C:\\Users\\Administrator\\Desktop\\env\\datas\\1.bmp");
    if (!srcImage.data)
    {
        return -1;
    }
    Mat srcGray;
    cvtColor(srcImage, srcGray, COLOR_RGB2GRAY);
    imshow("srcGray", srcGray);

    //调用otsu算法得到图像
    int otsuThreshold = OTSU(srcGray);
    cout << otsuThreshold << endl;
    //定义输出结果图像
    Mat otsuResultImage = Mat::zeros(srcGray.rows, srcGray.cols, CV_8UC1);

    //利用得到的阈值进行二值化操作
    for (int i = 0; i < srcGray.rows; i++)
    {
        for (int j = 0; j < srcGray.cols; j++)
        {
            //cout << (int)srcImage.at<uchar>(i, j) << endl;
            //高像素阈值判断
            if (srcGray.at<uchar>(i, j) > otsuThreshold)
            {
                otsuResultImage.at<uchar>(i, j) = 255;
            }
            else
            {
                otsuResultImage.at<uchar>(i, j) = 0;
            }
            //cout <<(int)otsuResultImage.at<uchar>(i, j) << endl;
        }
    }
    imshow("otsuResultImage", otsuResultImage);
    waitKey(0);
    return 0;
}