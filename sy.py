import json
import os
from pathlib import Path

def process_directory(directory):
    data = {
        "sources": [],
        "collections": []
    }

    for file_path in Path(directory).rglob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            relative_path = file_path.relative_to(directory).as_posix()
            
            if isinstance(content, list):
                # 如果数组只有一个元素，也视为普通书源
                if len(content) == 1:
                    item = content[0]
                    data["sources"].append({
                        "title": item.get("bookSourceName", "未命名书源"),
                        "subtitle": item.get("bookSourceUrl", ""),
                        "comment": item.get("bookSourceComment", ""),
                        "path": relative_path
                    })
                else:
                    # 合集只记录基本信息
                    data["collections"].append({
                        "title": file_path.stem,
                        "path": relative_path
                    })
            else:
                # 普通书源
                data["sources"].append({
                    "title": content.get("bookSourceName", "未命名书源"),
                    "subtitle": content.get("bookSourceUrl", ""),
                    "comment": content.get("bookSourceComment", ""),
                    "path": relative_path
                })
                
        except Exception as e:
            print(f"处理失败 {file_path}: {str(e)}")
    
    return data

if __name__ == "__main__":
    sy_dir = "sy"
    output = process_directory(sy_dir)
    
    with open("data.json", "w", encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
