import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()


def gather_md(summary_dir):
    docs_dir = PROJECT_ROOT / "docs"
    # 汇总所有md文件内容
    summary_md = summary_dir / "summary.md"
    exclude_files = ["_sidebar.md", "README.md"]

    # 定义三份输出文件路径（对应三个章节范围）
    part1_file = summary_dir / "summary_part1.md"  # 第01-11章
    part2_file = summary_dir / "summary_part2.md"  # 第14-21章
    part3_file = summary_dir / "summary_part3.md"  # 第23-28章

    # 打开三份文件并初始化（添加目录和分隔符）
    with open(part1_file, "w", encoding="utf-8") as part1_out, \
            open(part2_file, "w", encoding="utf-8") as part2_out, \
            open(part3_file, "w", encoding="utf-8") as part3_out:

        # 为每份文件添加独立目录和分隔符
        part1_out.write("[toc]\n\n---\n\n")
        part2_out.write("[toc]\n\n---\n\n")
        part3_out.write("[toc]\n\n---\n\n")

        # 遍历所有md文件
        for root, _, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(".md") and file not in exclude_files:
                    md_path = Path(root) / file

                    try:
                        rel_path = md_path.relative_to(docs_dir)
                        chapter_dir = rel_path.parts[0]
                        if not chapter_dir.startswith("chapter"):
                            continue
                        chapter_num = int(chapter_dir[len("chapter"):])
                    except (ValueError, IndexError):
                        continue

                    # 根据章节号判断归属文件
                    target_out = None
                    if 1 <= chapter_num <= 11:
                        target_out = part1_out  # 第01-11章 → part1
                    elif 14 <= chapter_num <= 21:
                        target_out = part2_out  # 第14-21章 → part2
                    elif 23 <= chapter_num <= 28:
                        target_out = part3_out  # 第23-28章 → part3
                    else:
                        continue  # 不在目标范围内的章节跳过

                    # 读取内容并写入对应文件
                    with open(md_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        content = content.replace("../images", "./images")
                        target_out.write(content)
                        target_out.write("\n\n")


def gather_output_images(summary_dir):
    # 收集所有图片文件并复制到汇总目录
    image_files = []
    docs_dir = PROJECT_ROOT / "docs"
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if (file.startswith("output_") and
                    (file.endswith(".png") or file.endswith(".svg"))):
                src_path = Path(root) / file
                # 处理可能的文件名冲突
                dest_filename = file
                counter = 1
                while (summary_dir / dest_filename).exists():
                    name, ext = os.path.splitext(file)
                    dest_filename = f"{name}_{counter}{ext}"
                    counter += 1

                dest_path = summary_dir / dest_filename
                shutil.copy2(src_path, dest_path)
                image_files.append((src_path, dest_path))
    return image_files


def copy_images(summary_dir):
    docs_images = PROJECT_ROOT / "docs" / "images"
    if docs_images.exists() and docs_images.is_dir():
        target_images = summary_dir / "images"
        if target_images.exists():
            shutil.rmtree(target_images)
        shutil.copytree(docs_images, target_images)


def main():
    # 创建汇总目录
    summary_dir = Path("summary_docs")
    summary_dir.mkdir(exist_ok=True)

    # 拷贝docs/images目录到summary_docs
    # copy_images(summary_dir)

    # gather_output_images(summary_dir)

    gather_md(summary_dir)

    print(f"汇总完成！结果保存在 {summary_dir} 目录中")


if __name__ == "__main__":
    main()
