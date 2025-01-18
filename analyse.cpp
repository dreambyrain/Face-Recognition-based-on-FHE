#include <iostream>
#include <yaml-cpp/yaml.h>
#include <opencv2/core.hpp>

int main() {
    // 加载 YAML 文件
    YAML::Node config = YAML::LoadFile("/home/flutter/桌面/trainer/trainer.yml");
    
    // 解析阈值、半径、邻居数等字段
    double threshold = config["opencv_lbphfaces"]["threshold"].as<double>();
    int radius = config["opencv_lbphfaces"]["radius"].as<int>();
    int neighbors = config["opencv_lbphfaces"]["neighbors"].as<int>();
    int grid_x = config["opencv_lbphfaces"]["grid_x"].as<int>();
    int grid_y = config["opencv_lbphfaces"]["grid_y"].as<int>();

    std::cout << "Threshold: " << threshold << std::endl;
    std::cout << "Radius: " << radius << std::endl;
    std::cout << "Neighbors: " << neighbors << std::endl;
    std::cout << "Grid X: " << grid_x << std::endl;
    std::cout << "Grid Y: " << grid_y << std::endl;

    // 解析 OpenCV 矩阵
    YAML::Node histograms = config["opencv_lbphfaces"]["histograms"];
    for (const auto& hist : histograms) {
        if (hist["!!opencv-matrix"]) {
            YAML::Node matrixNode = hist["!!opencv-matrix"];
            int rows = matrixNode["rows"].as<int>();
            int cols = matrixNode["cols"].as<int>();
            std::vector<float> data = matrixNode["data"].as<std::vector<float>>();

            // 将数据转换为 OpenCV 矩阵
            cv::Mat matrix(rows, cols, CV_32F, data.data());
            std::cout << "Matrix: " << matrix << std::endl;
        }
    }

    return 0;
}

