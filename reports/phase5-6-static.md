# Phase 5+6 静态化报告

**执行时间**: 2026-07-12 15:21-15:27 (Malaysia Time)
**结果**: ✅ 7 个页面 + 404 + sitemap + robots 全部生成，零失败请求

## 1. 方法：Playwright 全页爬取

写了一个 `static-crawler.py`:
- 用 Playwright 跳转到每个 URL
- 滚动到底再回顶，触发所有 `animate.css` 动画
- 等 `networkidle` 让所有 asset 加载
- 提取 HTML 中所有 `img src`/`srcset`/`link href`/`script src`/`source srcset`
- 解析 CSS 里的 `url(...)` 引用
- 下载每个 asset 到 `static/` 下的对应路径
- 最后保存 HTML

**清理脚本 `static-cleanup.py`**:
- 把所有 `http(s)://localhost:8080/...` 路径替换成相对路径
- 内部页面链接加上 `/index.html` 后缀
- 移除 feed/comments/wp-json/EditURI/wlwmanifest 等无用引用
- 加入 canonical URL `https://mtatileadhesive.com/...`
- 写 sitemap.xml, robots.txt, 404.html, README.md

## 2. 静态站结构

```
static/                                  58MB total, 118 files
├── index.html                          268KB  (Homepage)
├── about-us/index.html                 263KB
├── contact-us/index.html               244KB
├── mta991/index.html                   253KB
├── mta993/index.html                   253KB
├── mta_admix_123/index.html            247KB
├── mta-grout/index.html                252KB
├── 404.html                            2KB
├── sitemap.xml                         1.3KB
├── robots.txt                          73B
├── README.md                           1.3KB
├── wp-content/                         56MB   (uploads, themes, plugins assets)
└── wp-includes/                        128KB  (WP core CSS/JS)
```

## 3. 测试结果

### 端到端测试（Playwright）

| URL | HTTP | 失败请求数 |
| --- | --- | --- |
| `/` | 200 | 0 |
| `/about-us/` | 200 | 0 |
| `/contact-us/` | 200 | 0 |
| `/mta991/` | 200 | 0 |
| `/mta993/` | 200 | 0 |
| `/mta_admix_123/` | 200 | 0 |
| `/mta-grout/` | 200 | 0 |
| `/404.html` | 200 | 0 |
| `/sitemap.xml` | 200 | 0 |

**内部导航测试**: 点击首页 "About Us" 链接 → 跳转到 `/about-us/index.html` ✓

### 内部链接（首页）

```
href="https://mtatileadhesive.com/"        ← canonical
href="mta991/index.html"
href="mta993/index.html"
href="mta_admix_123/index.html"
href="about-us/index.html"
href="contact-us/index.html"
```

✓ 所有页面链接包含 `/index.html` 后缀
✓ 0 个 localhost 残留
✓ 0 个 wp-json 残留
✓ 0 个 feed/ 残留

### 字体路径修复

原始 WP 输出里 `@font-face` 引用 `https://localhost:8080/wp-content/uploads/fonts/jiz...woff2`。
已替换为相对路径 `wp-content/uploads/fonts/jiz...woff2`（首页）或 `../wp-content/uploads/fonts/...`（子页面）。

## 4. 部署清单

**Shinjiru 部署时上传的内容**:
- `static/` 整个目录 → 服务器 `public_html/`

**部署后**:
- `https://mtatileadhesive.com/` → 显示首页
- `https://mtatileadhesive.com/about-us/` → 显示关于页
- `https://mtatileadhesive.com/mta991/` → 显示 MTA 991
- `https://mtatileadhesive.com/sitemap.xml` → SEO sitemap
- `https://mtatileadhesive.com/robots.txt` → 爬虫规则
- 任何不存在路径 → 服务器默认 404，**或者**配置 `.htaccess` 指向 404.html

## 5. 注意事项

| 项 | 状态 | 备注 |
| --- | --- | --- |
| HTTPS 资源（fonts.googleapis.com 之类） | 已用 `route` 拦截 | 部署时如果 Shinjiru 没有问题就不需要 |
| wp-includes 的 JS 文件 | 已下载 | 但有些是 WordPress 编辑器用的，访问者不需要 |
| Jetpack 像素追踪 | 已拦截 | 静态站不需要 |
| 服务端代码（PHP） | 没有 | 纯静态 |
| 动态功能 | 不支持 | 评论、搜索、登录、CF7 提交都不可用 |
| Contact Form 7 表单 | 静态化时变成静态按钮 | Phase 7 决定怎么处理 |
| SSL 证书 | Shinjiru 提供 | 部署时自动配 Let's Encrypt |

## 6. 已知遗留问题

1. **404 处理**: 默认 Shinjiru 404 页面。可以配 `.htaccess` 重定向到 404.html
2. **Contact Form**: CF7 表单在静态站上提交不了。需要换方案 (Formspree, mailto, 简单 PHP form 等)
3. **Search**: 搜索功能没了，但首页导航没有搜索入口所以无影响
4. **WP-admin**: 不可用（预期 — 这是公开网站）

## 7. 截图

保存在 `reports/phase5-static-*.png`:
- `phase5-static-homepage.png` (initial)
- `phase5-static-homepage-final.png` (after cleanup, 桌面)
- `phase5-static-homepage-mobile.png` (移动)
- `phase5-static-navigation-test.png` (点击 About Us 后的 about 页)

## 8. 下一步

进 **Phase 7: 部署到 Shinjiru**。需要：

1. 登录 Shinjiru cPanel 或 FTP
2. 备份现有 `public_html/`
3. 删除空白 WordPress 安装（如果还有）
4. 上传 `static/` 内容到 `public_html/`
5. 配置 `.htaccess` 重定向到 404.html（可选）
6. 测试线上 URL

**关于 contact form 替换**: 这是 Phase 7 部署时必须决定的。三个选项：
- A. 简单 mailto: 链接（最简单，无后端）
- B. Formspree 或类似第三方表单服务（免费版够用）
- C. Shinjiru 自带 PHP form（如果 host 支持）

你倾向哪个？我可以进 Phase 7 之前先帮你快速 wire up form 替换，或者部署完再说。
