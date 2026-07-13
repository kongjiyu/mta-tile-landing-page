# Phase 7 部署准备报告

**执行时间**: 2026-07-12 15:30-15:40 (Malaysia Time)
**结果**: ✅ 部署包准备好，等你手动上传到 Shinjiru

## 1. 部署包

**位置**: `/Users/kongjy/Documents/Work/mta-tile/mta-tile-static.zip`
- 大小: **56MB** (压缩)
- 文件数: 142
- 包含: `static/` 整个目录，解压到 `public_html/` 即可

**解包后结构** (`public_html/`):
```
.htaccess                  # 1.4KB - HTTPS 重定向、404、cache、security headers
index.html                 # 268KB - 首页
about-us/index.html
contact-us/index.html      # 含 Formspree 表单
mta991/index.html
mta993/index.html
mta_admix_123/index.html
mta-grout/index.html
404.html
sitemap.xml
robots.txt
README.md                  # 完整部署指南
wp-content/                # 56MB - 上传图、主题字体、插件资源
wp-includes/               # WP core 静态资源
```

## 2. 上传步骤（你来做）

**最简单的方法**:

1. 打开 Shinjiru cPanel (URL 你应该有)
2. 进 **File Manager** → 导航到 `public_html/`
3. **先备份** 现有内容: 选所有 → Compress → 命名为 `public_html-backup-2026-07-12.zip` 下载
4. **删除** 现有 `public_html/` 全部内容 (不是 Move to Trash, 是 Delete)
5. **Upload** `mta-tile-static.zip` 到 `public_html/`
6. 右键 zip → **Extract** → 选 `/home/USER/public_html/` → Extract
7. **关键**: 把 `static/` 目录里的所有内容**上移一层**到 `public_html/` 根（让 `index.html` 直接在 `public_html/` 下）
8. **显示隐藏文件**: File Manager 右上 Settings → 勾 "Show Hidden Files (dotfiles)" → 确认 `.htaccess` 在
9. **删除** 空的 `static/` 目录
10. **替换 Formspree ID**: 用 File Manager 编辑 `contact-us/index.html`，把 `YOUR_FORM_ID` 换成你的真实 form ID

## 3. Formspree 设置 (5 分钟)

1. 打开 https://formspree.io/register (用 GitHub 登录)
2. 创建一个新 form，名字 "MTA Tiles Contact"
3. 拿到 endpoint URL，比如 `https://formspree.io/f/xwpaqrbn`
4. 用 cPanel File Manager 编辑 `public_html/contact-us/index.html`
5. 找这一行 (用 Ctrl+F 搜 "formspree.io/f/"):
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST" id="contact-form-formspree">
   ```
6. 把 `YOUR_FORM_ID` 替换成 `xwpaqrbn` (或你拿到的)
7. 保存

**第一次提交时会触发 Formspree 确认邮件** (发给 `mtaspecialist99@gmail.com`)，需要点 confirm 才会开始转发到你的 Gmail。

## 4. 上线后测试清单

按这个顺序:

```bash
# 这些 URL 都应该 200
https://mtatileadhesive.com/
https://mtatileadhesive.com/about-us/
https://mtatileadhesive.com/contact-us/         ← 表单在底部
https://mtatileadhesive.com/mta991/
https://mtatileadhesive.com/mta993/
https://mtatileadhesive.com/mta_admix_123/
https://mtatileadhesive.com/mta-grout/
https://mtatileadhesive.com/sitemap.xml
https://mtatileadhesive.com/robots.txt
https://mtatileadhesive.com/404.html
https://mtatileadhesive.com/some-random-url      ← 应该跳到 404.html
```

**目视检查**:
- [ ] 首页 hero 背景图加载 (瓷砖安装照片)
- [ ] 3 个产品图加载 (MTA 991/993/ADMIX 123)
- [ ] 3 个安装系统图加载
- [ ] 创始人照片加载
- [ ] Footer 完整
- [ ] 移动端布局
- [ ] SSL 锁 (https://)
- [ ] 在 contact 页提交测试表单 → 收到 Formspree 邮件

## 5. Phase 7 工作完成项

- ✅ `.htaccess` 配置（HTTPS redirect, 404 页面, 浏览器 cache, 安全 headers）
- ✅ Formspree 表单注入到 contact 页
- ✅ Form 按钮 `#write-message` 锚点跳转
- ✅ 验证 form 提交逻辑（success/error states via JS）
- ✅ 打包成 zip (56MB, 142 文件, 无 .DS_Store)
- ✅ 完整 README（部署指南、故障排除、回滚步骤）

## 6. 你需要做的

1. **注册 Formspree** (5 分钟)
2. **登录 Shinjiru cPanel** (拿到登录信息)
3. **备份**现有 public_html (1 分钟)
4. **删除** 现有内容
5. **上传** mta-tile-static.zip
6. **解压**到 public_html/
7. **把文件上移一层** (让 index.html 在 public_html/ 根)
8. **替换** Formspree 的 YOUR_FORM_ID
9. **测试** 上述所有 URL
10. **提交测试表单** 确认 Formspree 工作
11. **提交 sitemap** 到 Google Search Console (可选, 1 分钟)

## 7. 注意事项

- **首加载时间**: 静态站比 WP 快很多 (没有 PHP/MySQL)，预计 < 2 秒
- **CDN 友好**: Shinjiru 的 LiteSpeed 会自动 cache 静态文件
- **搜索功能**: 没了，但原站也没用
- **评论**: 没了 (但原站也没开)
- **WP-admin**: 完全没了 (但你也用不到)

## 8. 维护模式

**以后改东西** (改文案、换图):
1. 改 `static/` 里对应文件
2. 重新打包: `cd /Users/kongjy/Documents/Work/mta-tile && zip -r mta-tile-static.zip static/ -x "*/.DS_Store"`
3. 上传并解压到 Shinjiru

**或者** 我可以每次都重新跑 `static-crawler.py` 重新生成全套。

## 9. 下一步

进 **Phase 8: 回滚与维护**。Phase 8 主要是:
- 记录所有备份位置 (本地 + 上线后)
- 写维护 SOP
- 留运营变更的 checklist

这个我可以快速做完 (~15 分钟)，主要是文档。

你 OK 让我直接进 Phase 8 吗？还是先停了等你上传到 Shinjiru 再继续？
