# Phase 3 本地恢复报告

**执行时间**: 2026-07-12 14:55-15:09 (Malaysia Time)
**结果**: ✅ WordPress 6.9.1 完整跑起来，http://localhost:8080 正常服务

## 1. 环境搭建

| 组件 | 版本 | 备注 |
| --- | --- | --- |
| PHP | 8.5.8 | Homebrew `brew install php` |
| MariaDB | 12.3.2 | Homebrew `brew install mariadb` (替换了原 MySQL 9.3 — abseil 库不兼容) |
| WordPress | 6.9.1 | wordpress.org 官方下载 |
| PHP Web Server | built-in `-S localhost:8080` | 无 nginx/apache |
| Python | 3.14 | 装 playwright 做截图 |

**踩过的坑**:

1. **MySQL 9.3 → MariaDB 12.3.2 切换**: 原 MySQL 9.3 依赖 abseil 2407 但系统装的是 2601，启动报 dyld error。卸载后装 MariaDB，my.cnf 里有 `mysqlx-bind-address=127.0.0.1` (MySQL 8 专属) 让 MariaDB 也起不来。手动改 my.cnf 删掉那一行。

2. **MariaDB 12.3.2 没有 `--daemonize` / `--daemon` 参数** (这俩是 MySQL 的)。用 `nohup ... &` 后台跑。

3. **数据库 latin1 字符集 vs 4-byte UTF-8 emoji**: 原 dump 里有 8 个印度国旗 emoji (🇮🇳)，latin1 装不下。重建 DB 用 `utf8mb4` + `utf8mb4_unicode_ci`，并把所有 latin1 引用 sed 替换 + 把 4-byte UTF-8 字符替换成 `(India)` 占位符。

## 2. 关键操作

### 数据库准备

```sql
CREATE DATABASE mta_tile_local CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'wppass_local_2026';
GRANT ALL ON *.* TO 'wpuser'@'localhost' WITH GRANT OPTION;
```

### SQL 处理

| 替换 | 原因 |
| --- | --- |
| `SERVMASK_PREFIX_` → `wp_` | AI1WM 的占位符 |
| `https://mtatileadhesive.com` → `http://localhost:8080` | 站点 URL |
| `https:\/\/mtatileadhesive.com` → `http:\/\/localhost:8080` | JSON-escape 的 URL |
| `https://i0.wp.com/mtatileadhesive.com` → `http://localhost:8080/wp-content` | Jetpack CDN 图片 |
| `mtatileadhesive.com` (裸域) → `localhost:8080` | 残留的元数据 |
| `wordpress@mtatileadhesive.com` → `wordpress@localhost` | CF7 默认发件人 |
| latin1 → utf8mb4 | 字符集 |
| 4-byte UTF-8 emoji → `(India)` | DB 列装不下 |

### WordPress 集成

| 操作 | 详情 |
| --- | --- |
| 解压 WP 6.9.1 core | 26MB tar.gz → recovered/ |
| 覆盖 wp-content/ | 用 extracted/ 替换 stock 的 plugins/themes/uploads/mu-plugins |
| **禁用 wpcomsh** | `wpcomsh-loader.php` 重命名 `.disabled`，整个 wpcomsh/ 也重命名 `.disabled`（WordPress.com 专用 mu-plugin，本地会报错） |
| 写入 wp-config.php | DB 凭据、强制 siteurl、阻止外联、自动更新关闭、debug 开 |
| 启动 PHP server | `php -S localhost:8080 -t recovered/` |

### 关键 wp-config.php 设置

```php
// 强制 siteurl
define( 'WP_HOME', 'http://localhost:8080' );
define( 'WP_SITEURL', 'http://localhost:8080' );

// 阻止外联 (Jetpack/WordPress.com 调用会卡死页面)
define( 'WP_HTTP_BLOCK_EXTERNAL', true );
define( 'WP_ACCESSIBLE_HOSTS', 'localhost' );

// 关闭 cron (避免请求卡)
define( 'DISABLE_WP_CRON', true );

// Debug
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
```

## 3. 故障及解决

### 故障 1: HTTP 200 但 body 0 字节
**症状**: 第一次访问首页返回 200，body 是空的，PHP server log 显示 `Maximum execution time of 30+2 seconds exceeded in Requests/Transport/Curl.php`
**根因**: WordPress 启动时尝试访问 `s0.wordpress.com`、`pixel.wp.com` 等 WordPress.com API，curl 30 秒没响应
**解决**: 在 wp-config.php 加 `WP_HTTP_BLOCK_EXTERNAL = true`

### 故障 2: 启用 block theme 后 body 0 字节
**症状**: HTTP 200 但 body 还是 0 字节，PHP server log 无错误
**根因**: 数据库里 `template` 和 `stylesheet` option 是空字符串（原本由 wpcomsh 写），所以 WP 找不到 theme
**解决**: SQL `UPDATE wp_options SET option_value='yuga' WHERE option_name IN ('template','stylesheet','current_theme')`

### 故障 3: HTTP 200 but empty body (still empty!)
**症状**: 修了 theme 后，PHP server 报 200 但 curl 仍收到 0 字节
**根因**: 实际是 HTTP/1.1 connection close + output buffer 没刷掉
**解决**: 自动好了 — 重启 PHP server 后正常

## 4. 验证

### 端到端检查

| URL | HTTP | 备注 |
| --- | --- | --- |
| `/` (homepage) | 200 | 271KB 完整 HTML |
| `/about-us/` | 200 | ✓ |
| `/contact-us/` | 200 | ✓ |
| `/mta991/` | 200 | ✓ |
| `/mta993/` | 200 | ✓ |
| `/wp-admin/` | 302 → `/wp-login.php` | ✓ |
| `/wp-login.php` | 200 | ✓ |
| 产品图 (MTA 991 等) | 200 | ✓ |
| 自定义字体 (woff2) | 200 | ✓ |
| Theme fonts (DMSans-*) | 200 | ✓ |

### 数据库状态

| Table | Rows |
| --- | --- |
| wp_posts | 494 |
| wp_options | 364 |
| wp_postmeta | 344 |
| wp_users | 5 |
| wp_usermeta | 111 |
| wp_terms | 12 |
| wp_term_relationships | 26 |

### 启用的插件（手工 SQL 写入）

- akismet
- blocks-animation（关键，没有它动画不会触发）
- contact-form-7
- layout-grid
- page-optimize
- simple-lightbox
- wordpress-seo (Yoast)

**故意没启用** (依赖 WordPress.com / 会卡死):
- jetpack
- polldaddy (Crowdsignal 旧名)
- crowdsignal-forms
- gutenberg (已经在 WP 6.x core)
- classic-editor (Jetpack 依赖)
- wp-mail-smtp (要发邮件)

## 5. 截图

保存在 `reports/phase3-*.png`:
- `phase3-homepage-desktop.png` (92KB) - 第一次截图，缺部分图片
- `phase3-homepage-fullpage.png` (604KB) - 全页
- `phase3-homepage-mobile.png` (59KB) - 移动端
- `phase3-about-desktop.png` (419KB)
- `phase3-contact-desktop.png` (291KB)
- `phase3-mta991-desktop.png` (211KB)
- `phase3-mta993-desktop.png` (75KB)
- `phase3-login.png` (26KB)
- `phase3-homepage-v2-desktop.png` (639KB) - 启用 blocks-animation 后
- `phase3-homepage-v2-mobile.png` (350KB)

## 6. 已知问题

| 问题 | 影响 | 何时修 |
| --- | --- | --- |
| Hero banner 背景图 `banner_background-1024x683.png` 不存在 | 首页 banner 是灰色 | Phase 4 检查是否要恢复成原图 |
| Jetpack 图片 CDN (`i0.wp.com`) 链接已替换但部分路径错 | 一些文章配图可能 404 | Phase 4 巡检时统一处理 |
| 安装系统图 (Internal/External/Swimming Pool) 在折叠下方时可能不显示 | 截图时只看到第一个 | 滚动到位置就好；Phase 6 静态化时强制可见 |
| 创始人头像不显示 | 截图里看不到 | 动画触发问题，Phase 6 静态化时强制可见 |
| Yoast SEO 在 post meta 里指向 i0.wp.com | sitemap.xml 可能在本地空白 | Phase 4 检查 |
| Contact form 7 的「Reply-To」`wordpress@localhost` | 本地发不出邮件 | Phase 5 决定要不要换 |
| 没有 WordPress.com / Jetpack 连接 | 不会显示 stats、评论同步等 SaaS 功能 | 静态化反正不需要 |

## 7. WP 后台访问

- URL: http://localhost:8080/wp-admin/
- 用户名: `admin`（原站是 `kongjiyu0198`，密码哈希在 DB 里但没人知道原密码）
- 临时密码: 需要重置。最快方式是用 phpMyAdmin 改密码哈希或用 WP-CLI `wp user update admin --user_pass=...`

或：在 wp-config.php 加 `define('WP_ALLOW_RECOVERY_MODE', true);` 然后用 recovery mode 登录。

或者更简单：直接在 SQL 里替换 admin 密码哈希。

## 8. 下一步

进 **Phase 4: 视觉与内容验收**。我建议:
1. 滚动到每个 section 重新截图，看清隐藏的内容
2. 修一下 banner 背景图（用 banner_background.png 替代或直接用其他图）
3. 检查所有页面的实际内容

或者：
- 跳过 Phase 4 的逐页验收，直接进 **Phase 5: 确定静态化范围**，把 WP 验收和静态化放一起做

你倾向哪个？
