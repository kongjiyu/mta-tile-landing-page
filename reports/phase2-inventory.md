# Phase 2 解包与盘点报告

**执行时间**: 2026-07-12 14:48 (Malaysia Time)
**工具**: `npx wpress-extract` (Node.js v22.23.1)
**结果**: ✅ 24秒解出 19116 个文件，无错误

## 1. 解包结果概览

| 项目 | 值 |
| --- | --- |
| 解包后大小 | 546MB (原始 579MB，差 33MB 是 AI1WM 压缩开销) |
| 文件总数 | 19,116 |
| 解包耗时 | 24 秒 |
| 工具版本 | wpress-extract (latest) |
| 文件状态 | ✅ 全部可读，无损坏 |

## 2. 顶层结构

```
extracted/
├── advanced-cache.php       28K   (WP Rocket / cache plugin drop-in)
├── database.sql             8.2M  ⭐ 完整数据库导出
├── index.php                4K    (WordPress 入口 stub)
├── object-cache.php         28K   (Redis/Memcached drop-in)
├── package.json             1.4K  (manifest，已存档到 reports/)
├── mu-plugins/              35M   ⚠️ WordPress.com 专用 (需禁用)
├── plugins/                 398M
├── themes/                  24M
└── uploads/                 81M
```

## 3. 主题 (4 个)

| 主题 | 大小 | 状态 | 备注 |
| --- | --- | --- | --- |
| **yuga** | 3.4M | ✅ Active | Automattic 官方免费主题 |
| koinonia | - | Inactive | Automattic 区块主题 |
| twentytwentyfive | - | Inactive | WP 2025 默认 |
| twentytwentytwo | - | Inactive | WP 2022 默认 |

**重要发现**: Yuga 是 Automattic 官方提供的**免费 block 主题**（来自 wordpress.com/themes），不需要购买 license。这对静态化非常有利——主题本身就是开源的，可以直接使用。

Yuga 是 **Full Site Editing (FSE)** 主题：
- 10 个 templates: `home.html`, `page.html`, `single.html`, `archive.html`, `search.html`, `404.html`, `index.html`, `blank.html`, `footer-only.html`, `header-footer-only.html`
- 4 个 template parts: `header.html`, `header-with-button.html`, `footer.html`, `post-meta.html`
- 22 个 block patterns
- `theme.json` v2 配置（颜色、间距、字体等）

## 4. 插件 (13 个)

| 插件 | 大小 | manifest 列 | 实际 | 用途 |
| --- | --- | --- | --- | --- |
| akismet | 6.7M | ✅ | ✅ | 反垃圾 |
| blocks-animation | 1.4M | ✅ | ✅ | 区块动画 (animate.css) |
| classic-editor | 1.3M | ❌ | ✅ | 经典编辑器（Jetpack 依赖） |
| contact-form-7 | 1.1M | ❌ | ✅ | 联系表单 |
| crowdsignal-forms | 2.1M | ✅ | ✅ | 调查/反馈 |
| gutenberg | 137M | ✅ | ✅ | 古腾堡编辑器 |
| jetpack | 167M | ✅ | ✅ | 多功能套件 |
| layout-grid | 468K | ✅ | ✅ | 布局网格 |
| page-optimize | 452K | ✅ | ✅ | 性能优化 |
| polldaddy | 7.6M | ✅ | ✅ | Polldaddy 投票（已弃用） |
| simple-lightbox | 972K | ✅ | ✅ | 灯箱效果 |
| wordpress-seo (Yoast) | 63M | ✅ | ✅ | SEO |
| wp-mail-smtp | 8.1M | ❌ | ✅ | SMTP 发信 |

**观察**:
- manifest 漏报了 3 个插件：classic-editor, contact-form-7, wp-mail-smtp（可能是后期加入的或 mu-plugins 自动激活）
- `active_plugins` option 是空 `a:0:{}`，说明激活是由 WordPress.com 的 wpcomsh mu-plugin 管理的
- Jetpack + Gutenberg 占了 304MB（多数是 vendor/、languages/）

## 5. mu-plugins — WordPress.com 标记

`mu-plugins/wpcomsh/` 35MB — 这是 **WordPress.com Business** 或 **Pressable** 托管的 wpcomsh 插件。

**含义**:
- 站点原本托管在 WordPress.com / Pressable
- 这个 mu-plugin 自动化管理插件激活、Jetpack 连接、站点健康等
- 本地恢复时**必须禁用** `wpcomsh-loader.php`，否则会因找不到 WordPress.com API 而报错
- 简单做法：不在 `mu-plugins/` 目录放 `wpcomsh-loader.php`，或者重命名

## 6. 上传文件 (uploads/)

| 类型 | 数量 | 大小 |
| --- | --- | --- |
| PNG 图片 | 46 | 约 50MB |
| JPG 图片 | 7 | 较小 |
| PDF 文档 | 3 | 较小 |
| woff2 字体 | 18 | 较小（fonts/）|
| 其他 (htaccess, DS_Store) | 2 | - |
| **总计** | **76 文件** | **约 81MB** |

按月份分布：

| 月份 | 文件数 | 大小 |
| --- | --- | --- |
| 2025/02 | 6 | 1.6M |
| 2025/03 | 1 | 52K |
| 2025/04 | 39 | 62M |
| 2025/05 | 7 | 2.1M |
| 2025/06 | 3 | 15M |

**注意**: 没有 2025-07 之后的图片。备份生成于 2026-02-24，但最后上传是 2025-06。**说明站点从 2025 年 6 月之后就再没更新过**。

字体目录 `uploads/fonts/` 包含 18 个 woff2 文件，命名规则是 `jiz...U.woff2`，这是 **Adobe Jiz typeface** 的子集。可能是 Yuga 主题或客户定制的字体。

## 7. 数据库 (database.sql)

| 项目 | 值 |
| --- | --- |
| 大小 | 8.2MB |
| 表数 | 24 |
| 总记录 | 约 1,555 INSERT |
| 字符集 | latin1 / latin1_swedish_ci |
| 表前缀占位符 | `SERVMASK_PREFIX_`（需替换为 `wp_`） |
| 最后 INSERT 时间戳 | 2025-07-09 (Homepage post) |
| 发信最后调度 | 2025-04-07 (wp_mail_smtp) |

### 重要表

| 表 | 行数 | 说明 |
| --- | --- | --- |
| `wp_posts` | 494 | 含 page、wp_template、wp_template_part、wp_navigation、wp_global_styles、wp_block、attachment 等 |
| `wp_options` | 364 | 含 siteurl、home、template、stylesheet、active_plugins、blogname 等 |
| `wp_postmeta` | 344 | Yoast SEO meta、custom fields |
| `wp_usermeta` | 111 | 用户设置 |
| `wp_users` | 5 | 用户账号 |
| `wp_yoast_seo_links` | 58 | Yoast 内部链接 |
| `wp_termmeta` 等 | 12+ | 分类法 |

### 关键 options 值

| Option | Value |
| --- | --- |
| `siteurl` | `http://mtatileadhesive.com/` |
| `home` | `http://mtatileadhesive.com/` |
| `blogname` | `MTA Tiles adhesive Specialist` |
| `blogdescription` | `Malaysia's Trusted Name in Tile Adhesive Solutions.` |
| `admin_email` | `kongjiyu0198@gmail.com` |
| `template` | (空 — 由 wpcomsh 写入) |
| `stylesheet` | (空 — 由 wpcomsh 写入) |
| `active_plugins` | `a:0:{}` (空 — 由 wpcomsh 写入) |

### 内容样本 (Homepage)

```html
"Strength Below the Surface. Precision Above All."
"High-performance tile adhesives built for real-world application."

产品:
- MTA 991 — Normal Cementitious Tile Adhesive
- MTA 993 — Single Component Polymer Modified Flexible Tile Adhesive
- MTA ADMIX 123 — Multipurpose Latex Admixture for Mortar

Installation systems:
- Internal General Area
- External General Area
- Swimming Pool

Why Choose MTA:
- Quality, Versatility, Expertise

Founder: Victoria Huan

"At MTA Tiles Specialist, we're passionate about what holds great design
together—literally. With a focus on tile adhesive innovation, we empower
builders and designers with products they can trust."
```

## 8. 颜色与字体品牌

从 home.html 提取：

| 角色 | 颜色 | 用途 |
| --- | --- | --- |
| 主背景深 | `#121313` | 深色 CTA 卡片 |
| 文字浅 | `#f6f4ed` | 奶油色文字 |
| 强调金 | `#c9b991` | 重点高亮 |
| 文字深 | `#002a32` | 深青色链接 |
| 暗罩 | `#676767` | banner 50% 暗罩 |

字体：默认系统 + Adobe Jiz subset（从 uploads/fonts/ 看）。

## 9. Phase 3 准备工作清单

要本地恢复这个 WordPress，需要：

1. ✅ **下载 WordPress 6.9.1 核心**（备份里只有 wp-content 和 database.sql，没有 wp-admin/wp-includes）
2. ✅ **安装 PHP 8.2+**（备份里说原站是 8.2.30）
3. ✅ **安装 MariaDB 11.x** 或 MySQL 8（数据库兼容）
4. ✅ **创建本地数据库** `mta_tile_local`，字符集 `latin1`，排序 `latin1_swedish_ci`
5. ✅ **将 SERVMASK_PREFIX_ 全部替换为 wp_**
6. ✅ **配置 wp-config.php**（DB 凭据、密钥、table_prefix = `wp_`）
7. ✅ **将 `extracted/` 下的 plugins/、themes/、uploads/、mu-plugins/ 放到 wp-content/ 下**
8. ❌ **移除 mu-plugins/wpcomsh-loader.php**（WordPress.com 专用，本地不需要）
9. ❌ **在 wp-config.php 强制 siteurl 为 http://localhost:PORT**（避免重定向到 mtatileadhesive.com）
10. ❌ **用 WP-CLI 或 phpMyAdmin 搜索/替换域名**（mtatileadhesive.com → localhost）

## 10. Go/No-Go 决策

✅ **GO** — 强烈建议继续 Phase 3。

理由：
- 数据库完整，24 张表全在
- 主题是免费的 Yuga，没 license 障碍
- 上传文件齐全（虽然不多）
- 内容结构清晰：1 个 homepage + 几个产品页 + 安装系统 + about
- 字体已包含在 uploads 里
- 整体站点规模小（约 100MB assets），非常适合做静态化

**风险点**:
- wpcomsh mu-plugin 必须禁用
- 表前缀需要批量替换
- siteurl/home 需要在导入后改成 localhost
- 一些依赖 WordPress.com API 的功能（Jetpack stats、crowdsignal）会在本地不可用 — 但这些是 SaaS，静态化后本来就不需要

## 11. 下一步

进 **Phase 3**: 本地恢复 WordPress。
- 用 `brew install php` 或 `brew install --cask local` 起 PHP 环境
- 拿 WordPress 6.9.1 core
- 用 Python 脚本批量替换 `SERVMASK_PREFIX_` → `wp_` 和 `https://mtatileadhesive.com` → 本地 URL
- 用 mysql 命令行导入
- 跑起来后验收
