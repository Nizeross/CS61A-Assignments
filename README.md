# CS61A Assignments Repository

*English | [中文](#中文说明)*

---

## English

### Overview
This repository contains **all homework (hw)**, **labs**, and **projects** for the UC Berkeley CS61A course. It is designed to facilitate practice and improve your understanding of the material.

You can fork this repository to create your own working environment, track your progress, and store your solutions. For reference and study, you can also access the [**CS61A website archive**](https://insideempire.github.io/CS61A-Website-Archive/) mirrored here.

### Features
- **Homework (hw):** Reinforce lecture topics with conceptual and coding exercises.
- **Labs:** Guided practice to understand core concepts.
- **Projects:** Comprehensive assignments to apply knowledge in larger-scale coding challenges.

### How to Use

#### 1. Fork the Repository
1. Go to the repository: [CS61A-Assignments](https://github.com/InsideEmpire/CS61A-Assignments).
2. Click the "Fork" button in the top-right corner of the page to create your own copy of the repository.

#### 2. Clone Your Forked Repository
1. Open your terminal or command prompt.
2. Clone your forked repository to your local machine:
   ```bash
   git clone https://github.com/<your-username>/CS61A-Assignments.git
   ```

#### 3. Work on Assignments
1. Navigate into the repository folder:
   ```bash
   cd CS61A-Assignments
   ```
2. Choose the directory for the assignment you want to work on (e.g., `hw01` for Homework 1):
   ```bash
   cd hw/hw01
   ```
3. Open the `.py` files in your favorite code editor and start solving!

#### 4. Test Your Work
After completing or making progress on an assignment, use the following command to test your solution locally:
```bash
python3 ok -q <function_name> --local
```
Replace `<function_name>` with the name of the specific function you want to test.

If you want to test the whole file，use the following command：
```bash
python3 ok --local
```

---

### Notes
- Ensure you have Python installed on your system to run the assignments. CS61A primarily uses Python 3.
- Use a code editor like VS Code or PyCharm for an enhanced coding experience.

### Disclaimer
- This repository is **unofficial** and is not affiliated with or endorsed by UC Berkeley or the CS61A teaching team.
- All course materials and content are property of UC Berkeley CS61A staff and are provided here for **personal learning and practice** only. Please respect academic integrity policies.

---

## 中文说明


### 中文注释说明

本仓库已将 `HW/`、`Lab/`、`Project/` 中课程源码的英文说明性注释和 Python 文档字符串翻译为简体中文，包括四个项目 Hog、Cats、Ants、Scheme，以及课程辅助工具、Scheme 编辑器、海龟绘图和测试用例中的代码注释。原本没有说明性注释的文件保持原样。

- 保留函数名、变量名、文件名和命令，便于与 [CS61A 2024 秋季课程镜像](https://insideempire.github.io/CS61A-Website-Archive/) 对照学习。
- 保留已有解答与待填写代码；本次翻译不补写习题答案。
- 保留测试输入、预期输出、选择题内容、锁定答案、运行时提示和错误字符串。
- `BEGIN/END PROBLEM`、`YOUR CODE HERE`、`locked`、`expect`、`doctest:` 等程序或评分工具使用的标记保留原文；注释中的代码、公式和示意布局也保留。
- 随附的第三方依赖、压缩或打包的网页资源、许可证及署名信息保留原文；README 原有的中英文说明保留。

术语约定：environment frame 译为“环境帧”，procedure 译为“过程”，pair 译为“点对”，abstraction barrier 译为“抽象屏障”，mutation 根据语境译为“原地修改”，mobile 译为“活动雕塑”，hailstone sequence 译为“冰雹序列”。英文标识符仍按源码书写。

翻译校验已对照修改前的本地文件，确认 Python 可执行代码结构与文档测试输入、预期输出一致；测试文件除注释外的内容，以及 Scheme、SQL、JavaScript、CSS 和 HTML 的非注释内容保持一致。这些校验只验证翻译未改变代码与测试，不代表尚未完成的题目已经通过课程测试。

### 项目简介
本仓库包含了 UC Berkeley CS61A 课程的所有 **家庭作业 (hw)**、**实验 (labs)** 和 **项目 (projects)**。通过 Fork 本仓库，您可以创建自己的工作环境，跟踪学习进度并保存作业的解答。同时，您还可以访问我们提供的 [**CS61A 网站镜像**](https://insideempire.github.io/CS61A-Website-Archive/)，用于参考和学习。


### 功能特色
- **家庭作业 (hw)：** 巩固课程讲解内容，包含概念和代码练习。
- **实验 (labs)：** 指导练习，帮助理解核心概念。
- **项目 (projects)：** 通过大型项目综合应用所学知识。

### 使用方法

#### 1. Fork 本仓库
1. 打开仓库：[CS61A-Assignments](https://github.com/InsideEmpire/CS61A-Assignments)。
2. 点击页面右上角的 "Fork" 按钮，将仓库复制到您的 GitHub 账号下。

#### 2. 克隆您 Fork 的仓库
1. 打开终端或命令提示符。
2. 将 Fork 后的仓库克隆到本地：
   ```bash
   git clone https://github.com/<your-username>/CS61A-Assignments.git
   ```

#### 3. 开始完成作业
1. 进入仓库目录：
   ```bash
   cd CS61A-Assignments
   ```
2. 选择您想完成的作业目录，例如 `hw01` 表示家庭作业 1：
   ```bash
   cd hw/hw01
   ```
3. 打开 `.py` 文件，开始编写代码！

#### 4. 测试您的代码
完成作业或取得进展后，使用以下命令在本地测试代码：
```bash
python3 ok -q <function_name> --local
```
将 `<function_name>` 替换为您希望测试的具体函数名称。

如果想测试整个文件，使用以下命令：
```bash
python3 ok --local
```

---

### 注意事项
- 确保您的系统已安装 Python，CS61A 主要使用 Python 3。
- 推荐使用 VS Code 或 PyCharm 等代码编辑器，提升编程体验。

### 免责声明
- 本仓库为 **非官方** 项目，与 UC Berkeley 及 CS61A 教学团队无关。
- 所有课程内容版权归 UC Berkeley CS61A 团队所有，仅供 **个人学习和练习** 使用，请遵守学术诚信规定。
  