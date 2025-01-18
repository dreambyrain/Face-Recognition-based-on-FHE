import yaml
import numpy as np

# 自定义解析器：处理 !!opencv-matrix 标签
def opencv_matrix_constructor(loader, node):
    fields = loader.construct_mapping(node, deep=True)
    return {
        "rows": fields["rows"],
        "cols": fields["cols"],
        "dt": fields["dt"],
        "data": fields["data"]
    }

# 显式注册 !!opencv-matrix 的标签解析器
from yaml.loader import SafeLoader
yaml.add_constructor('tag:yaml.org,2002:opencv-matrix', opencv_matrix_constructor, Loader=SafeLoader)

# 加载 YAML 文件路径
yaml_file = "/home/yourname/桌面/trainer/trainer.yml"

try:
    # 读取 YAML 文件
    with open(yaml_file, "r") as file:
        data = yaml.load(file, Loader=SafeLoader)
        print("成功加载 YAML 文件")

        # 提取并处理 histograms 数据
        histograms = data["opencv_lbphfaces"]["histograms"]
        processed_histograms = []
        for idx, histogram in enumerate(histograms):
            rows = histogram["rows"]
            cols = histogram["cols"]
            data_values = histogram["data"]
            np_array = np.array(data_values).reshape((rows, cols))
            processed_histograms.append(np_array)
            print(f"第 {idx + 1} 组直方图数据已处理：形状为 {np_array.shape}")

        # 保存处理后的数据到文件
        processed_file = "/home/yourname/桌面/processed_histograms.npy"
        np.save(processed_file, processed_histograms)
        print(f"处理后的数据已保存到 {processed_file}")

except Exception as e:
    print(f"保存处理后的数据时发生错误: {e}")
