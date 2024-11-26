import json

# 读取JSON文件
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 统计记录总数
def count_total_records(data):
    return len(data)

# 主函数
def main():
    file_path = '/home/wangboyu/code/fusiondata/papers.json'  # 替换为你的JSON文件路径
    
    # 读取数据
    data = read_json(file_path)
    
    # 统计总记录数
    total_records = count_total_records(data)
    
    # 打印结果
    print(f"JSON 文件中总共有 {total_records} 条记录。")

if __name__ == "__main__":
    main()