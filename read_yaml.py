import yaml

# 自定义解析器：处理 !!opencv-matrix 标签
def opencv_matrix_constructor(loader, node):
    try:
        # 将 YAML 节点解析为字典
        fields = loader.construct_mapping(node, deep=True)
        return {
            "rows": fields["rows"],
            "cols": fields["cols"],
            "dt": fields["dt"],
            "data": fields["data"]
        }
    except Exception as e:
        print(f"解析 !!opencv-matrix 标签失败: {e}")
        raise

# 显式注册 !!opencv-matrix 的标签解析器
from yaml.loader import SafeLoader
yaml.add_constructor('tag:yaml.org,2002:opencv-matrix', opencv_matrix_constructor, Loader=SafeLoader)

# 指定 YAML 文件路径
yaml_file = "/home/yourname/桌面/trainer/trainer.yml"

try:
    # 读取并解析 YAML 文件
    with open(yaml_file, "r") as file:
        data = yaml.load(file, Loader=SafeLoader)
        print("成功读取 YAML 文件！")
        # 示例：打印解析后的部分数据
        print("Threshold:", data["opencv_lbphfaces"]["threshold"])
        print("第一组直方图数据:", data["opencv_lbphfaces"]["histograms"][0])
except yaml.YAMLError as e:
    print(f"读取 YAML 文件失败: {e}")
except FileNotFoundError:
    print(f"文件未找到: {yaml_file}")
except Exception as e:
    print(f"其他错误: {e}")
