# BookxNote-Tools

BookxNote可以看作是win端上的MarginNote，是一款小巧轻便PDF电子书阅读器。它不仅可以为用户提供多种阅读模式，而且还可以自动记忆上次阅读的页面位置，在最近阅读文档打开，自动跳转到上次位置，有助于学习与思考，让读者的大脑更高效的记忆，界面清爽、干净、专注阅读。

我的主要需求是读文献，在把BookxNote与知之阅读和liquidText（免费版）比较后倾向于使用BookxNote，因为感觉顺手一些，而且速度很快（我电脑上liquidText的启动速度非常硬伤）。
但BookxNote对我一个非常致命的问题就是标注没法保存回pdf上，我能理解用这类软件精读后的pdf就是药渣，但在存储不值钱的条件下保留一份原文件并没有什么压力。而且文献这种东西还是很有可能要重新再读的……有个上次阅读的记录会好一些。
BookxNote的同步也是个问题，对于不在收集篮里的文件都是使用绝对路径定位的，这没法和zotero等文献管理工具联合使用。
而且标注不能导出为markdown，（相对）很难和joplin、obsidian之类的软件联合使用。

好在作者是用json保存的标注，我能写个外置的脚本满足这些需求。

我目前的使用方式：
    1. 在zotero里直接用bookxnote打开pdf
    2. 如果需要精读就将pdf保存至笔记文件夹
    3. 阅读完运行写入pdf的脚本
    4. 脚本从笔记文件夹中找到pdf和标注 写在一起后保存在单独的output文件夹里
    5. 使用zotfile的源文件夹功能重新获取到标注过的pdf 再利用重复项合并之类的方式合在一起
    6. 标注导出成html后用pandoc之类的东西再转成markdown 然后丢进joplin或者obsidian

目前完成了写入pdf的脚本 这样来看还少个转markdown以及自动删除output文件夹里pdf的脚本 不过不太着急就看我心情了【手动狗头】

---

## 需求

- Python3
- PyMuPDF = 1.1.8 
- BookxNote Pro = V2.0.0.1026

---

别的版本的BookxNote我就不知道能不能用了 
release里有个编译了的脚本 丢在笔记数据目录里就能用

TODO很多 只写了我常用的一些标注（下划线、高亮、文本框、方形与圆形） 直线标注有些问题（作者似乎把多条直线写在一起了） 而且颜色可能有些问题 线宽也没法调 Bug可能也有不少
不过对我来说够用了 暂时不打算折腾了 欢迎大佬push
