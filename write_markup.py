import os
import json
import fitz
from glob import glob

# 本脚本默认放在笔记数据目录中 保存的PDF文件在output文件夹里
note_path = './notebooks'
dst_pdf_path = './output'


def path_join(*paths):
    path = os.path.join(*paths)
    path = os.path.normcase(path)
    return path


def Hex_to_RGB(hex):
    # 作者的颜色类似于ffffed99 前两位的ff好像没用
    r = int(hex[2:4], 16) / 255
    g = int(hex[4:6], 16) / 25
    b = int(hex[6:8], 16) / 255
    return (r, g, b)


def update_pdf(markup_path, update_log):
    with open(markup_path, 'r', encoding='UTF-8') as f:
        markups = json.loads(f.read())
    pdf_file = markups['title'] + '.pdf'
    last_update = sorted([x['date'] for x in markups['markups']])[-1]

    if pdf_file not in update_log or last_update > update_log[pdf_file]:
        doc = fitz.open(
            os.path.join(os.path.dirname(markup_path), 'resources', pdf_file))
        for markup in markups['markups']:
            annot = None
            page = doc[markup['page']]
            # 高亮和下划线
            if markup['type'] == 5:
                stext = markup['textblocks'][0]['text']
                rl = page.searchFor(stext, quads=True)
                while len(rl) == 0 and len(stext) >= 0:
                    stext = stext[:-1]
                    rl = page.searchFor(stext, quads=True)
                # TODO:多行的情况每行新建一条线
                if len(rl) > 0:
                    for r in rl:
                        if 'underline' in markup:
                            annot = page.addUnderlineAnnot(r)
                            annot.setColors(
                                stroke=Hex_to_RGB(markup['linecolor']))
                            annot.set_border(width=markup['linewidth'])
                        else:
                            annot = page.addHighlightAnnot(r)
                            annot.setColors(
                                stroke=Hex_to_RGB(markup['fillcolor']))
                        annot.update()
            # 打字机和文本框
            # TODO: 文本框的箭头
            elif markup['type'] == 9 or markup['type'] == 11:
                annot = page.addFreetextAnnot(markup['rect'],
                                              markup['originaltext'],
                                              text_color=Hex_to_RGB(
                                                  markup['linecolor']))
                annot.setColors(stroke=Hex_to_RGB(markup['linecolor']))
                annot.update()
            # 方形
            elif markup['type'] == 2:
                # TODO: 线宽无法设置
                annot = page.addRectAnnot(markup['rect'])
                annot.setColors(stroke=Hex_to_RGB(markup['linecolor']))
                annot.update()
            # 圆形
            elif markup['type'] == 3:
                # TODO: 线宽无法设置
                annot = page.addCircleAnnot(markup['rect'])
                annot.setColors(stroke=Hex_to_RGB(markup['linecolor']))
                annot.update()
            # 直线
            elif markup['type'] == 1:
                # TODO: 线宽无法设置
                assert len(markup["rect"]) % 4 == 0
                for i in range(len(markup["rect"]) // 4):
                    p1 = (markup["rect"][i * 2 + 0], markup["rect"][i * 2 + 1])
                    p2 = (markup["rect"][i * 2 + 2], markup["rect"][i * 2 + 3])
                    annot = page.addLineAnnot(p1, p2)
                    annot.setColors(stroke=Hex_to_RGB(markup['linecolor']))
                    annot.set_opacity(0.7)
                    annot.update()
            # 其他都没做
            else:
                print('Unhandled annotation type:{}'.format(markup['type']))
            if 'content' in markup and annot is not None:
                # 下划线、高亮和直线的批注都在最后一个里了
                info = annot.info
                info["content"] = markup['content']
                annot.set_info(info)
                annot.update()
        doc.save(os.path.join(dst_pdf_path, pdf_file), deflate=True)

    return pdf_file, last_update


if __name__ == "__main__":
    if not os.path.exists(dst_pdf_path):
        os.makedirs(dst_pdf_path)
    # 会在notebooks的目录里生成一个log 仅处理更新过的pdf
    if os.path.exists(path_join(note_path, 'pdf_log.json')):
        with open(path_join(note_path, 'pdf_log.json'), 'r') as f:
            old_update_log = json.load(f)
    else:
        old_update_log = {}
    new_update_log = {}

    notes = glob(path_join(note_path, '*', 'markups.json'))
    if len(notes) > 0:
        for idx, markup_path in enumerate(notes):
            print('{}/{}:\t {}'.format(
                idx, len(notes),
                os.path.basename(os.path.dirname(markup_path))))
            try:
                pdf_file, last_update = update_pdf(markup_path, old_update_log)
                new_update_log[pdf_file] = last_update
            except Exception as e:
                print(e)
        # log里只记录本次处理时notepads目录里有的pdf
        with open(path_join(note_path, 'pdf_log.json'), 'w') as f:
            json.dump(new_update_log, f)
    os.system("pause")
