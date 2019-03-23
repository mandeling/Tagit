# TAGIT

我们通常使用文件夹结构来分类管理文档/个人知识，但单一的目录结构难以有效组织具有交叉关系的内容。例如，以电影类型例如科幻片、战争片、剧情片来命名分类文件夹是个不错的选择，但同时我们很可能希望将同一导演/演员的作品组织在一起，于是不得不按照这个标准重新建立分类文件夹，并且需要重复复制文档。针对此类问题，考虑以虚拟的目录结构和标签来管理硬盘上实际存储的文档（文本/多媒体），这便是`Tagit`。

区别于笔记类应用，`Tagit`并不进行实际文档的创建和编辑，而是侧重以逻辑分类和标签来管理已经存在的文档；它更倾向于文献管理类软件，但不涉及文献格式方面的功能，而是着重于分类组织的能力。

## 开发工具

Python3, PyQt5

## 任务列表

项目的初衷是解决对本地存储的学习资源的管理，顺便成为学习和实践PyQt5的一次机会。

- [x] 分类管理 - 无限级分类
- [x] 标签管理
- [x] 对象管理 - 建立与源文档的映射，添加/修改分类/标签
	- [x] 按分类/标签筛选对象
	- [x] 关键字搜索
	- [x] 拖拽分类
	- [x] 数据存储 - 直接`pickle`存储数据
- [x] 用户界面
	- [x] 自定义UI样式

## 预览

![UI example](docs/user_interface.jpg)



