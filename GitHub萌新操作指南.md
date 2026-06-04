# GitHub 萌新操作指南

> 不需要懂编程，跟着步骤走就能完成。

---

## 第一步：注册 GitHub 账号

1. 打开 https://github.com
2. 输入邮箱，设置密码和用户名（用户名想好，后面会用在链接里）
3. 完成验证
4. 去邮箱点验证链接

---

## 第二步：下载 GitHub Desktop（最简单的方式）

不需要用命令行！

1. 打开 https://desktop.github.com
2. 下载对应你电脑系统的版本（Windows 或 Mac）
3. 安装并用刚才注册的账号登录

---

## 第三步：创建仓库

1. 打开 GitHub Desktop
2. 点击左上角的 **File → New Repository**
3. 填写：
   - **Name**：`zhonglun-modern`（必须和你想要的项目名一致）
   - **Description**：`中论现代性解读——龙树中观的后人类主义跨学科哲学重构`
   - **Local path**：选择一个你电脑上的文件夹来存放项目
   - 勾选 **Initialize this repository with a README**
4. 点击 **Create Repository**

---

## 第四步：把准备好的文件放进去

现在你的电脑上应该有一个文件夹，路径大概是：

```
你的用户名/Documents/GitHub/zhonglun-modern/
```

1. 打开这个文件夹
2. 把我给你准备好的 `zhonglun-modern` 文件夹里的**所有内容**复制进去
   - README.md
   - LICENSE-CC-BY-NC-SA-4.0
   - CONTRIBUTING.md
   - TRANSLATION.md
   - content/zh/ch01.md 到 ch27.md
   - .github/ISSUE_TEMPLATE/
3. 复制进去后，回到 GitHub Desktop

---

## 第五步：提交并推送

在 GitHub Desktop 中：

1. 你会看到左边列出了你添加的所有文件
2. 在下方 Summary 框里写：`Initial commit: 添加全书27章内容`
3. Description 框可以写更详细的说明（也可以留空）
4. 点击 **Commit to main**
5. 然后点击右上角的 **Publish repository**
6. 确认仓库名是 `zhonglun-modern`，保持 Public（公开），点击 **Publish Repository**

🎉 完成！现在你的书已经在 GitHub 上了。

---

## 第六步：查看你的仓库

1. 打开浏览器，访问：
   ```
   https://github.com/你的用户名/zhonglun-modern
   ```
2. 你应该能看到 README 的内容和目录结构
3. 点击不同的文件可以查看内容

---

## 第七步：开启 GitHub Pages（让书可以在线阅读）

1. 在你的仓库页面，点击上方的 **Settings**（设置）
2. 左侧菜单找到 **Pages**
3. **Source** 选择 `Deploy from a branch`
4. **Branch** 选择 `main`，文件夹选 `/ (root)`
5. 点击 **Save**
6. 等几分钟，刷新页面，会看到一个绿色框，显示你的在线地址：
   ```
   https://你的用户名.github.io/zhonglun-modern/
   ```
7. 点击就能在线阅读了！

---

## 后续更新内容（发新版本）

当你修改了某个文件，想更新到 GitHub 上：

1. 修改你电脑上的文件
2. 打开 GitHub Desktop
3. 你会看到变更的文件列表
4. 填写 Summary（比如：`修正第5章错别字`）
5. 点击 **Commit to main**
6. 点击 **Push origin** 推送上去

---

## 你可以做的事

作为仓库主人，你有以下权限：

### 1. 修改内容
- 直接在 GitHub 网页上点击文件 → 铅笔图标 → 修改 → 提交
- 或者在电脑上修改后通过 GitHub Desktop 推送

### 2. 管理 Issue（反馈）
- 别人发现错误会通过 Issue 告诉你
- 点击 **Issues** 标签可以看到所有反馈
- 你可以回复、标记完成、关闭 Issue

### 3. 接受别人的贡献
- 别人可能会提交 **Pull Request**（修改建议）
- 点击 **Pull requests** 标签查看
- 你可以审阅修改内容，选择接受或拒绝

### 4. 添加英文版翻译
- 在 `content/en/` 文件夹中创建对应的英文文件
- 比如 `content/en/ch01.md`
- 逐步填充所有27章

### 5. 生成 EPUB / PDF
- 安装 [Pandoc](https://pandoc.org/installing.html)
- 使用以下命令：
  ```bash
  pandoc content/zh/*.md -o epub/zhonglun-modern.epub --toc
  pandoc content/zh/*.md -o pdf/zhonglun-modern.pdf --toc
  ```

---

## 常见问题

**Q: 我不知道命令行，能操作吗？**
A: 完全可以！上面的所有操作都可以通过 GitHub Desktop 和网页完成，不需要命令行。

**Q: 我可以把仓库设为私有的吗？**
A: 可以，但公开能让更多人看到和参与。如果你暂时不想公开，可以在 Publish 时选 Private，以后在 Settings 里改成 Public。

**Q: 有人抄袭怎么办？**
A: 许可证已经写清楚了——署名+非商业+共享。如果有人商用不署名，你可以联系 GitHub 举报。

**Q: 我想删除仓库重新开始？**
A: Settings → 拉到最下面 → Danger Zone → Delete this repository。

---

## 需要帮助？

- 在 GitHub 仓库里点击 **Issues → New Issue**
- 描述你遇到的问题
- 社区会帮你解答
