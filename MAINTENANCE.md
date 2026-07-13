# MTA Tiles 项目维护手册

**最后更新**: 2026-07-12
**目标读者**: 项目所有者 / 任何接手维护的人

## 1. 文件位置一览

| 内容 | 路径 | 大小 | 用途 |
| --- | --- | --- | --- |
| 原始备份 | `original/MTA Tiles Adhesive Export 2026-02-24.wpress` | 579MB | 只读原始证据，不要动 |
| 工作副本 | `working/backup.wpress` | 579MB | 已删除（节省空间） |
| 解包内容 | `extracted/` | 546MB | 数据库 + 主题/插件/上传 |
| 本地 WordPress | `recovered/` | 684MB | 完整可跑 WP，可重新导出 |
| **生产静态站** | `static/` | 58MB | 部署到 Shinjiru 的版本 |
| **部署包** | `mta-tile-static.zip` | 56MB | 一次上传整个站 |
| 报告 | `reports/` | 17MB | 每个 Phase 的执行记录 + 截图 |
| 工具脚本 | `static-crawler.py`, `static-cleanup.py` | 14KB | 重新生成静态站用 |

**所有原始数据安全吗**: ✅ 是
- 原始 .wpress 在 `original/` 是只读
- `recovered/` 是个完整的可恢复 WordPress
- 静态站 `static/` 是部署目标
- 三份都互相独立

## 2. 日常维护流程

### 场景 A: 改文字 / 改小图

1. 在 `static-redesign.py` 中找到对应页面或 `PRODUCTS` 产品资料。
2. 修改文字或图片路径后，运行 `python3 static-enhance.py` 重新生成全部静态页面。
3. 测试: `cd static && python3 -m http.server 8000` 然后浏览器看 `http://localhost:8000/<page>/`
4. 重新打包: `cd .. && zip -r mta-tile-static.zip static/ -x "*/.DS_Store"`
5. 上传新 zip 到 Shinjiru, 解压覆盖。

不要直接长期维护生成后的 `static/<page>/index.html`；下次运行 `static-enhance.py` 会按模板重新生成。

### 场景 B: 换产品图 / 加新图

1. 把新图复制到 `static/wp-content/uploads/2025/04/` (或对应月份)
2. 在 `static-redesign.py` 中更新对应产品或页面的图片路径
3. 注意保持文件大小合理 (单图 < 500KB 为佳)
4. 测试 + 打包 + 上传

### 场景 C: 加新页面

1. 在 `static-redesign.py` 的 `PRODUCTS` 中增加产品资料和页面 slug。
2. 如有 PDF，把文件放在 `static/wp-content/uploads/` 并写入 `pdf` 字段。
3. 更新 `sitemap.xml`。
4. 运行 `python3 static-enhance.py`，再测试、打包和上传。

### 场景 D: 修改品牌 / 全站样式

1. 不要在每个 HTML 页面重复写样式。
2. 设计变量和响应式规则统一在 `static/mta-site.css`。
3. 导航与轻量交互在 `static/mta-site.js`。
4. 页面结构与内容在 `static-redesign.py`，改完运行 `python3 static-enhance.py`。
5. 测试所有页面后重新打包。

## 3. 紧急回滚

### 如果新版本出问题，需要立即回退

**情况 A: 还有上一版本** (例如昨天还是好的)

1. 登录 Shinjiru cPanel File Manager
2. 把 `public_html/` 改名为 `public_html-broken-2026-07-XX/`
3. 用 cPanel Backup 恢复 (如果你启用了 cPanel 自动备份, 最少 1 天前的版本)
4. 或者从你本地的 `mta-tile-static.zip` 备份里恢复

**情况 B: 完全没备份, 站挂了**

1. 解压 `mta-tile-static.zip` (在 `original/` 那级目录)
2. 重新上传到 `public_html/`
3. 这个 zip 是**已验证可工作**的版本

**情况 C: 整个 static/ 也没了**

1. 从 `recovered/` 重新生成:
   ```bash
   cd /Users/kongjy/Documents/Work/mta-tile
   python3 static-crawler.py
   python3 static-cleanup.py
   zip -r mta-tile-static.zip static/ -x "*/.DS_Store"
   ```
2. 这个过程需要本地 WordPress 在跑 (`recovered/` 里), 如果 `recovered/` 也没了，重新解包 `original/*.wpress`

**情况 D: 原始 .wpress 也没了**

那就要花钱买 AI1WM Unlimited Extension 直接从托管商恢复 (因为我们没保留托管登录信息)。或者重新设计。

## 4. 完整重建流程 (从零)

如果 `static/` 和 `recovered/` 都没了，但 `original/` 还在：

```bash
cd /Users/kongjy/Documents/Work/mta-tile

# 1. 解包 .wpress
npx --yes wpress-extract original/*.wpress -o extracted/ -f

# 2. 下载 WordPress 6.9.1
curl -sL https://wordpress.org/wordpress-6.9.1.tar.gz -o /tmp/wp.tar.gz
mkdir -p recovered
tar -xzf /tmp/wp.tar.gz -C recovered/ --strip-components=1

# 3. 复制 extracted/ 内容到 recovered/wp-content/
for item in plugins themes uploads mu-plugins; do
  cp -R extracted/$item recovered/wp-content/
done
mv recovered/wp-content/mu-plugins/wpcomsh-loader.php{,.disabled}

# 4. 起 PHP + MariaDB
brew services start mariadb
nohup /opt/homebrew/opt/php/bin/php -S localhost:8080 -t recovered/ &

# 5. 创建数据库
mariadb -uwpuser -pwppass_local_2026 mta_tile_local < extracted/database.sql
# (需要先做 SERVMASK_PREFIX_ 和 URL 替换，参考 reports/phase3-recovery.md)

# 6. 启用 plugins (跳过 jetpack/polldaddy/crowdsignal)
mariadb -uwpuser -pwppass_local_2026 mta_tile_local -e "UPDATE wp_options SET option_value='a:7:{i:0;s:21:\"akismet/akismet.php\";i:1;s:35:\"blocks-animation/blocks-animation.php\";i:2;s:30:\"contact-form-7/wp-contact-form-7.php\";i:3;s:27:\"layout-grid/index.php\";i:4;s:27:\"page-optimize/page-optimize.php\";i:5;s:34:\"simple-lightbox/main.php\";i:6;s:24:\"wordpress-seo/wp-seo.php\";}' WHERE option_name='active_plugins';"

# 7. 重新生成缩略图
cd recovered && php wp-cli.phar media regenerate --yes --allow-root

# 8. 重新跑静态化
cd ..
python3 static-crawler.py
python3 static-cleanup.py
zip -r mta-tile-static.zip static/ -x "*/.DS_Store"
```

整个流程 ~30 分钟。

## 5. 续费 / 续期

**Shinjiru 续费时间**:
- Eco Premium 计划通常是年付
- 续费前 30 天 Shinjiru 会发邮件提醒
- 续费时考虑: **如果 static 站稳定运行了 6-12 个月**, 可以降级到 Eco Startup (RM/年, 比 Premium 便宜)
  - Eco Startup 通常支持 ~10GB 存储, 足够我们 60MB 静态站
  - 但如果需要更多 backup/email/CDN 等高级功能, Premium 也 OK

**自动续费**: 在 cPanel 里可以设信用卡自动扣款

## 6. SEO 监控

**第一个月** (2026-07 起到 2026-08):
- 在 Google Search Console 验证: https://search.google.com/search-console/
- 提交 sitemap: `https://mtatileadhesive.com/sitemap.xml`
- 监测 crawl errors

**3-6 个月后**:
- 看 Google Search Console 的 "Pages" 报告，哪些页被收录
- 看 "Performance" 报告，关键词排名
- 如果某个产品页没流量，看是不是有技术问题

**长期**:
- 域名续费 (mtatileadhesive.com)
- SSL 证书 (Shinjiru Let's Encrypt 自动续)
- 检查 uptime (可以用 uptimerobot.com 免费监控)

## 7. 联系人和参考资料

| 资源 | 链接 |
| --- | --- |
| Shinjiru cPanel | (你的登录 URL) |
| Formspree Dashboard | https://formspree.io/forms |
| Google Search Console | https://search.google.com/search-console/ |
| UptimeRobot (监控) | https://uptimerobot.com/ |
| 原始 .wpress 解析工具 | https://www.npmjs.com/package/wpress-extract |
| Yuga 主题 (Automattic 免费) | https://wordpress.com/theme/yuga |
| AI1WM Unlimited Extension (付费) | https://servmask.com/products/unlimited-extension |

## 8. 检查清单 (上线后定期过一遍)

- [ ] **每 3 个月**: 检查 Shinjiru 邮箱续费提醒
- [ ] **每 6 个月**: 检查域名续费 (mtatileadhesive.com)
- [ ] **每 6 个月**: 备份 `static/` 到外部 (Google Drive / iCloud / 外接硬盘)
- [ ] **每年**: 检查 `static/` 是否需要更新 (新主题/新功能)
- [ ] **任何时候**: 用户反馈问题 → 看 `static/<page>/index.html` 改 → 重新打包上传
- [ ] **任何时候**: 想加新内容 → 复制模板页面 → 改 → 更新 sitemap → 上传

## 9. 项目历史

| 日期 | 事件 |
| --- | --- |
| 2025-06 之前 | 原 WordPress 站活跃 (mtatileadhesive.com) |
| 2025-07-09 | 最后内容更新 (homepage) |
| 2026-02-24 14:03 | All-in-One WP Migration 备份生成 |
| 2026-07-12 | 项目恢复: 解包 + 本地恢复 + 静态化 + 部署准备 |
| (TBD) | 上线到 Shinjiru (等待你操作) |

---

**有任何问题**: 查 `reports/` 下的 Phase 1-7 报告，有完整的执行记录和命令
