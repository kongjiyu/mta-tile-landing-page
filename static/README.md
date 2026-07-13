# MTA Tiles - Static Site Deployment Guide

**Generated**: 2026-07-12
**Source**: `original/MTA Tiles Adhesive Export 2026-02-24.wpress` (579MB)
**Target**: Shinjiru Eco Premium hosting at `https://mtatileadhesive.com`

## 1. 部署前检查

新版网站以 WhatsApp 为主要询价渠道，不依赖 Formspree 或其他后端服务。部署前确认以下资料仍然有效：

- WhatsApp / 电话：`+60 12-414 8562`
- Email：`mtaspecialist99@gmail.com`
- 地址与营业时间
- 三份产品 PDF 可以正常打开

## 2. 上传到 Shinjiru

### 方法 A：cPanel File Manager (最简单)

1. 登录 Shinjiru cPanel: https://mtatileadhesive.com:2083 (或给你的 cPanel URL)
2. 点 **File Manager**
3. 导航到 `public_html/` 目录
4. **先备份**: 选中所有现有文件 → Compress → 下载 zip
5. **删除旧 WP**: 选中所有现有文件 → Delete
6. **上传新静态站**:
   - 先在 cPanel File Manager 里创建 `public_html/` 下的所有子目录
   - 或者：用 cPanel 的 "Upload" 按钮 → 拖入整个 `static/` 文件夹（**不包括上一级 `static` 这个目录本身**）
   - **重要**: 上传后文件应在 `public_html/` 根下，结构如：
     ```
     public_html/
     ├── index.html
     ├── about-us/index.html
     ├── ...
     ├── 404.html
     ├── sitemap.xml
     ├── robots.txt
     ├── .htaccess
     └── wp-content/, wp-includes/
     ```
7. **验证 .htaccess 是否上传**: cPanel 默认隐藏 dotfiles。在 File Manager 右上角 Settings → 勾 "Show Hidden Files (dotfiles)"

### 方法 B：FTP (FileZilla / Cyberduck)

1. 用 FileZilla 连 `ftp://mtatileadhesive.com` (cPanel 给的 FTP host)
2. 用户名 / 密码 = cPanel 凭据
3. 本地 = `static/` 文件夹内容
4. 远端 = `/public_html/`
5. 拖拽上传所有文件 (包括 .htaccess)

### 方法 C：打包上传 (如果你想一次传完)

我已经准备好了 zip 包: `mta-tile-static.zip` (在 `static-crawler.py` 同级目录)
- 大小以当前重新生成的 zip 为准
- 在 cPanel File Manager 里: Upload → 选 zip → 解压到 `public_html/`

## 3. 部署后验证

按顺序测试：

```bash
# 这些 URL 都应该 200
https://mtatileadhesive.com/
https://mtatileadhesive.com/about-us/
https://mtatileadhesive.com/contact-us/
https://mtatileadhesive.com/mta991/
https://mtatileadhesive.com/mta993/
https://mtatileadhesive.com/mta_admix_123/
https://mtatileadhesive.com/mta-grout/
https://mtatileadhesive.com/sitemap.xml
https://mtatileadhesive.com/robots.txt
https://mtatileadhesive.com/404.html
https://mtatileadhesive.com/some-nonexistent-page  ← 应该跳到 404.html
```

页面内要测:
- [ ] 首页 4 个产品入口都加载
- [ ] Hero 背景图加载
- [ ] 安装系统 3 张图加载
- [ ] 所有页面 Footer 一致
- [ ] 移动菜单、技术资料折叠项和移动端底部 WhatsApp 按钮正常
- [ ] 每个产品页 WhatsApp 预填文字包含正确型号
- [ ] MTA 991、MTA 993、Admix 123 的 PDF 正常下载
- [ ] SSL 锁显示 (https)

## 4. 常见问题

**Q: 上传后访问 mtatileadhesive.com 还是显示旧 WordPress**
A: 旧文件没清干净。cPanel File Manager 里**先全选再 Delete** (不是 Move to Trash, 是永久删除)。

**Q: 看到 "Index of /" 列表**
A: 没有 `index.html` 在根目录。检查上传是否成功，根目录有 `index.html`。

**Q: 图片 404**
A: 检查 `wp-content/uploads/` 整个目录是否上传了。可以用 cPanel "Show Hidden Files" 看 `.htaccess` 也上传了。

**Q: WhatsApp 没有打开或预填文字不正确**
A: 检查设备是否安装 WhatsApp，并在 `static-redesign.py` 确认 `PHONE` 和对应页面的 enquiry message，之后重新运行 `python3 static-enhance.py`。

**Q: 静态站没 .htaccess**
A: cPanel 默认隐藏 dotfiles。File Manager → Settings → 勾 "Show Hidden Files"。

**Q: 旧 WordPress 的 URL 怎么办 (像 /wp-admin/)**
A: 静态站完全没有 `/wp-admin/`，访问会跳到 404.html (因为 .htaccess ErrorDocument 404 配了)。这是好事。

**Q: Google Search Console 怎么更新**
A: 上线后:
1. 去 https://search.google.com/search-console/
2. 验证域名 (DNS TXT 记录)
3. 提交新的 sitemap: `https://mtatileadhesive.com/sitemap.xml`

## 5. 备份与回滚

**上线后立刻做的事**:
- 在本地 `static/` 目录打个 zip: `static-crawler.py` 同级
- 这个 zip 就是**生产镜像**。内容修改应先更新 `static-redesign.py` 或 `static/mta-site.css`，运行 `python3 static-enhance.py` 后再重新打包。

**如果新版本出问题**:
- 在 cPanel File Manager 里把 `public_html/` 改名 `public_html.broken/`
- 把 `public_html-backup-xxx/` 改回 `public_html/`
- 立即恢复

**或者用 git 跟踪**:
- `static/` 整个目录初始化成 git repo
- 每次改完 commit
- 部署: zip 整个 repo，cPanel 上传解压

## 6. 静态站结构

```
static/
├── .htaccess                  # 部署必带 (HTTPS redirect, 404, caching, security)
├── index.html                 # 首页
├── about-us/index.html
├── contact-us/index.html      # WhatsApp、电话、Email 与地址
├── mta991/index.html
├── mta993/index.html
├── mta_admix_123/index.html
├── mta-grout/index.html
├── 404.html
├── sitemap.xml
├── robots.txt
├── README.md                  # 本文件
├── mta-site.css               # 新版共用设计系统与响应式样式
├── mta-site.js                # 导航与轻量滚动呈现
└── wp-content/                # 产品图、施工图与产品 PDF
```

## 7. 紧急联系

如果上线后有任何问题:
- 看本目录的 `reports/` 里有完整的恢复报告
- 原始 `.wpress` 在 `original/` 还可以重新解包
- `recovered/` 是完整可跑的 WordPress 本地副本 (PHP 8.5 + MariaDB 12.3)
- 需要回到 WordPress 动态站: 把 `recovered/` 内容上传 + 导入 `recovered/wp-content/database-utf8mb4.sql` 到 Shinjiru MySQL
