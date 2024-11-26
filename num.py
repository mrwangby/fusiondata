import os
import json

# 替换为你的JSON文件所在的目录路径
directory_path = "/home/wangboyu/code/fusiondata/pdfs"

# 初始化总和
all_files_total = 0

# 遍历目录下的所有JSON文件
for file_name in os.listdir(directory_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(directory_path, file_name)

        # 读取JSON文件
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)

                # 计算单个文件的总和
                file_total = sum(int(item["num"]) for item in data if item["num"] is not None)

                print(f"文件: {file_name}, 数量: {file_total}")

                # 更新所有文件的总和
                all_files_total += file_total

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error processing file {file_name}: {e}")

# 打印所有JSON文件的总和
print(f"总文献数量: {all_files_total}")