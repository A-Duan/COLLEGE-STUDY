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
//OSTU�㷨���ͼ���ֵ����ֵ
int OTSU(Mat srcImage){
	int nCols = srcImage.cols;
	int nRows = srcImage.rows;
	int threshold = 0;
	//��ʼ������
	int nSumPix[256];
	float nProDis[256];
	for (int i = 0; i < 256; i++) {
		nSumPix[i] = 0;
		nProDis[i] = 0;
	}
	//ͳ�ƻҶȼ���ÿ���������������еĸ���
	for (int i = 0; i < nRows; i++) {
		for (int j = 0; j < nCols; j++) {
			nSumPix[(int)srcImage.at<uchar>(i, j)]++;
		}
	}
	//����ÿ���Ҷȼ�ռͼ���еĸ��ʷֲ�
	for (int i = 0; i < 256; i++) {
		nProDis[i] = (float)nSumPix[i] / (nCols * nRows);
	}
	//�����Ҷȼ�[0,255],����������䷽���µ���ֵ
	float w0, w1, u0_temp, u1_temp, u0, u1, delta_temp;
	double delta_max = 0.0;
	for (int i = 0; i < 256; i++) {
		//��ʼ�����ϵ��
        //����ǰ�������ص���ռ����ͼ��ı�����Ϊw0����ƽ���Ҷ�u0
        //�������ص���ռ����ͼ��ı���Ϊw1����ƽ���Ҷ�Ϊu1
        //ͼ�����ƽ���Ҷȼ�Ϊu��u = w0*u0 + w1*u1
        //delta=w0(u0-u)^2+w1(u1-u)^2
		w0 = w1 = u0 = u1 = u0_temp = u1_temp = delta_temp = 0;

		for (int j = 0; j < 256; j++) {
            //��������
            if (j <= i)
            {
                w0 += nProDis[j];
                u0_temp += j * nProDis[j];
            }
            //ǰ������
            else
            {
                w1 += nProDis[j];
                u1_temp += j * nProDis[j];
            }
        }
        //�������������ƽ���Ҷ�
        u0 = u0_temp / w0;
        u1 = u1_temp / w1;
        //�����ҵ������䷽���µ���ֵ
        delta_temp = (float)(w0 * w1 * pow((u0 - u1), 2)); //ǰ���뱳��֮��ķ���(��䷽��)
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
    //ͼ���ȡ���ж�
    Mat srcImage;
    srcImage = imread("C:\\Users\\Administrator\\Desktop\\env\\datas\\1.bmp");
    if (!srcImage.data)
    {
        return -1;
    }
    Mat srcGray;
    cvtColor(srcImage, srcGray, COLOR_RGB2GRAY);
    imshow("srcGray", srcGray);

    //����otsu�㷨�õ�ͼ��
    int otsuThreshold = OTSU(srcGray);
    cout << otsuThreshold << endl;
    //����������ͼ��
    Mat otsuResultImage = Mat::zeros(srcGray.rows, srcGray.cols, CV_8UC1);

    //���õõ�����ֵ���ж�ֵ������
    for (int i = 0; i < srcGray.rows; i++)
    {
        for (int j = 0; j < srcGray.cols; j++)
        {
            //cout << (int)srcImage.at<uchar>(i, j) << endl;
            //��������ֵ�ж�
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