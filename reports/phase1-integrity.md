# Phase 1 完整性检查报告

**执行时间**: 2026-07-12 14:43 (Malaysia Time)
**文件**: `MTA Tiles Adhesive Export 2026-02-24.wpress`

## 1. 基础信息

| 项目 | 值 |
| --- | --- |
| 文件名 | MTA Tiles Adhesive Export 2026-02-24.wpress |
| 大小 | 579,240,888 bytes (552.4 MiB / 607,376,760 bytes on disk) |
| 修改时间 | 2026-02-24 14:04 |
| SHA256 (原始) | `fdd90ba1c7e1242795b5f1fd05d10616b4b4ba4aa0e21ebee32c4a80ce9a8c8e` |
| SHA256 (副本) | `fdd90ba1c7e1242795b5f1fd05d10616b4b4ba4aa0e21ebee32c4a80ce9a8c8e` |
| 副本校验 | ✅ 完全一致 |
| 文件格式 | All-in-One WP Migration (`.wpress` 私有格式) |

## 2. 原始文件保护

- 原始文件已拷贝到 `original/` 子目录，权限设为 `444`（只读）
- 工作副本在 `working/backup.wpress`（可读写）
- 源文件位置: 根目录的 `MTA Tiles Adhesive Export 2026-02-24.wpress`（建议保留作为额外保险）

## 3. Manifest 内容（package.json）

来源: All-in-One WP Migration 备份的元数据，已成功解析并保存到 `reports/package.json`。

### 站点信息

| 字段 | 值 |
| --- | --- |
| SiteURL | `https://mtatileadhesive.com` |
| HomeURL | `https://mtatileadhesive.com` |
| InternalSiteURL | `http://mtatileadhesive.com/` |
| InternalHomeURL | `http://mtatileadhesive.com/` |

### 技术栈

| 组件 | 版本/详情 |
| --- | --- |
| WordPress | 6.9.1 |
| All-in-One WP Migration 插件 | 7.102 |
| PHP | 8.2.30 (Linux) |
| Database | MariaDB 11.4.9 |
| 数据库字符集 | latin1 / latin1_swedish_ci |
| 表前缀 | `wp_` |
| 服务器路径 | `/srv/htdocs/` (Pressable / WP Engine 风格的托管) |

### Theme

- **Template**: `yuga`
- **Stylesheet**: `yuga`

> "yuga" 主题是 Themeans.com 出品的多用途主题（在 ThemeForest 上叫 "Yuga - Creative Multi-Purpose WordPress Theme"），含 page builder。

### 启用的插件 (10 个)

| 插件 | 用途 |
| --- | --- |
| akismet | 反垃圾评论 |
| blocks-animation | 区块动画 |
| crowdsignal-forms | 调查/反馈表单（旧 Polldaddy） |
| gutenberg | 古腾堡编辑器 |
| jetpack | 多功能套件（统计、社交、CDN 等） |
| layout-grid | 布局网格 |
| page-optimize | 页面性能优化 |
| polldaddy | Polldaddy 投票（旧名） |
| simple-lightbox | 灯箱效果 |
| wordpress-seo | Yoast SEO |

### 备份生成时间

- 备份文件时间戳: `1771913004` ≈ 2026-02-24 06:03:24 UTC = 2026-02-24 14:03 (Malaysia Time, UTC+8)
- 与文件 mtime 14:04 吻合

## 4. 初步结论

✅ **文件完整**: 副本 SHA256 与原始一致，没有传输/拷贝损坏。
✅ **格式可读**: package.json manifest 完整可解析，包含站点、主题、插件、版本等所有关键信息。
✅ **内容齐全**: 10 个插件、1 个 yuga 主题、WordPress 6.9.1、MariaDB 11 都明确列在 manifest 里。
✅ **备份日期**: 2026-02-24，与计划一致。

**判断**: 备份值得继续恢复。Phase 2 (解包并盘点) 可以开始。

## 5. 已知风险点

| 风险 | 影响 | 备注 |
| --- | --- | --- |
| 主题 `yuga` 是付费主题 | 恢复后可能需要重新购买/激活 license | Phase 4 验收时检查 |
| Yoast SEO / Jetpack 含外部服务 | 可能需要 API key 重新连接 | 影响 SEO 跟踪、统计 |
| 站点路径 `/srv/htdocs/` | 不是标准路径，暗示托管商是 Pressable 或 WP Engine 类的 Managed WP 主机 | 本地恢复时需用我们自己的路径 |
| Polldaddy/Crowdsignal 是较老的插件 | 可能已停止维护 | 表单功能可能需要替换 |
| 加密签名 | AI1WM 7.x 的加密签名，免费版可能无法直接导入大于 512MB 的备份 | 但 wpress-extract 不需要导入，可直接读文件 |
| AI1WM 7.102 比常见公开版本新 | 文件中可能使用了较新的功能，导入时需要匹配版本 | 我们用工具直接读，不依赖 AI1WM 插件导入 |

## 6. 下一步

**Phase 2**: 用 `npx wpress-extract` 解包到 `extracted/` 子目录，然后写一个盘点脚本统计文件结构、目录树、关键文件存在性、uploads 大小等。
