# auto_surrender_hearthstone v0.2

## 项目简介
这是一个自动投降脚本，用于《炉石传说》。
该脚本通过识别图片并执行点击操作来实现自动投降。
有GUI可以自己设置投降条件。

## 使用指南
1. 使用 PyCharm 打开项目，并安装标红的依赖包。
2. 运行，依次选择需要点击的图片文件夹和投降图片。
3. 请注意，如果识别不了需要自己重新截图。
4. GUI界面有参考信息，最好看视频。

## 参考视频
如果对使用过程有疑问，可以观看这个视频：[跳转到BiliBili](https://www.bilibili.com/video/BV1feCdYuEgv/)
v0.2 更新介绍视频[跳转到BiliBili](https://www.bilibili.com/video/BV1iPSJY1Eev/)

## 备注
这是一个有趣的小项目，供爱好者玩耍。

## 可能的更新
更好看的GUI界面
更完整的教程
优化随机轨迹
增加超时处理

## 介绍

### `main.py`
- `run_gui()`: 启动 GUI 应用程序。

### `app.py`
- `ClickAutomationApp`: 点击自动化应用程序的主类。
  - `__init__(self, master)`: 初始化应用程序。
  - `setup_ui(self)`: 设置用户界面。
  - `select_images_directory(self)`: 选择要加载的图片目录。
  - `fetch_instructions(self)`: 从指定 URL 获取说明并显示。
  - `select_can_throw_image(self)`: 选择用于投降的条件图片。
  - `toggle_clicking(self)`: 切换点击状态，开始或停止点击。
  - `start_clicking_thread(self)`: 启动一个线程以执行点击操作。
  - `start_clicking(self)`: 执行点击操作的主逻辑。
  - `update_image_display(self)`: 更新当前显示的图片。

### `utils.py`
- `update_surrender_count(count)`: 更新投降次数的逻辑。
- `find_and_click(image_path)`: 查找并点击指定的图片。
