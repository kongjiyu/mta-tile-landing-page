# SEO 状态 + Google Search Console 指引

**时间**: 2026-07-12 22:20
**当前版本**: redesign (从 `static-redesign.py` 重新生成)

## ✅ SEO 设置都到位

| 项 | 状态 | 详情 |
| --- | --- | --- |
| **sitemap.xml** | ✅ | 7 个 URL, valid XML, `lastmod` 标了 2026-07-12 |
| **robots.txt** | ✅ | `User-agent: * / Allow: /` + sitemap 引用 |
| **meta description** | ✅ 7/7 页 | 长度 95–165 字符 (理想 120-160)，3 页短了一点点但 OK |
| **canonical URL** | ✅ 7/7 页 | 都指向 `https://mtatileadhesive.com/...` |
| **meta robots** | ✅ 6/7 页 | 6 个是默认 (index, follow)，`mta-grout/` 是 `noindex, nofollow` (Coming Soon，故意) |
| **JSON-LD (rich results)** | ✅ 4 页 | Homepage 是 LocalBusiness, 3 个 product 页是 Product + Brand + Organization |
| **OG meta** | ✅ 7/7 页 | og:title / og:description / og:url / og:image / og:type |
| **Twitter Cards** | ✅ 7/7 页 | summary_large_image |
| **Favicon** | ✅ | 32x32 站点 logo |
| **.htaccess** | ✅ | HTTPS redirect, 404.html, gzip, cache headers |

**结论**: Google **可以**直接抓和索引这个站. **不需要等什么**.

## ⚠️ mta-grout/ 是 noindex

`mta-grout/index.html` 有 `<meta name="robots" content="noindex, nofollow">`. 这是 `static-redesign.py` 给 "Coming Soon" 产品故意加的 — 你不想让一个不完整的产品页出现在 Google 搜索里。

这不会影响其他页面的索引。OK.

## 关于 "要不要重新 request indexing"

**简短答案**: 是的, 强烈建议在 GSC 里重新提交。

**为什么**:
- 你的站以前是 WordPress (Pressable / WordPress.com 托管)
- 现在变成了静态站, **HTML 完全不同** (redesign 重写了所有 markup)
- Google 已经索引过旧站, 缓存里可能还是旧的
- 如果不重新 request, Google 不会**主动**来抓新内容 — 它会等下个 crawl cycle (可能几周)

**该做什么 (按顺序, 1-2 小时搞定)**:

### 1. 验证 GSC Property (如果之前没做过)

1. 打开 https://search.google.com/search-console/
2. 加 property → URL prefix → 输入 `https://mtatileadhesive.com`
3. 验证方法选 **HTML file upload**:
   - 下载 GSC 给的 `googleXXXXX.html`
   - 传到 Shinjiru `public_html/` (你已经有部署流程，几分钟)
   - 点 "Verify"
4. 如果**之前已经验证过**了 (用其他方法比如 DNS TXT), 跳过这步

### 2. 提交 Sitemap

1. GSC → 你的 property → **Sitemaps** (左栏)
2. "Add a new sitemap" → 输入 `sitemap.xml` (GSC 会自动加 `https://mtatileadhesive.com/` 前缀)
3. 点 **Submit**
4. 等几分钟, GSC 会显示 "Success" + 7 个 discovered URLs

### 3. Request Indexing (关键步骤)

最快让 Google 看到新内容的方法:

1. GSC → 顶部搜索框输入 `https://mtatileadhesive.com/` (首页 URL)
2. 等待 "URL Inspection" 加载 (会显示当前 Google 看到的版本)
3. 如果显示**旧版缓存**, 点 **"Request Indexing"** → 等待 1-2 分钟处理
4. 对每个**重要页面**重复:
   - `https://mtatileadhesive.com/`
   - `https://mtatileadhesive.com/about-us/`
   - `https://mtatileadhesive.com/contact-us/`
   - `https://mtatileadhesive.com/mta991/`
   - `https://mtatileadhesive.com/mta993/`
   - `https://mtatileadhesive.com/mta_admix_123/`
5. **不要 request** mta-grout (noindex)
6. 每个 URL 间隔 1-2 分钟, GSC 限速

**预期**:
- Request 后几小时到几天, Google 会爬
- 1-2 周内, 搜索结果会显示新 title / description / rich results

### 4. (可选) 用 Indexing API 加速批量

如果想一次 request 全部 6 个 URL (不用手动一个个来):

1. 用 Google Cloud Console 创建 service account
2. 启用 Indexing API
3. 下载 service account JSON key
4. 用下面任一工具 POST 6 个 URL:
   - [indexing-api-tool](https://github.com/googledevelopers/indexing-api-tools) (官方)
   - 或者 `curl` + JWT 手动 POST

**复杂度**: 中. 如果你不想搞这步, 手动一个个 Request 也行, 反正只有 6 个 URL.

## 验证

提交后 1-2 周观察 GSC 这些面板:

- **Pages** → 应该显示 6-7 个 "Indexed" (mta-grout 是 Excluded, 因为 noindex)
- **Enhancements** → 应该有 LocalBusiness / Product rich results
- **Performance** → 看哪个关键词带来流量 (前 2 周会很少, 正常)
- **Coverage** → 如果有错误 (404, redirect chain), GSC 会高亮

## 时间线

| 行动 | 预期见效 |
| --- | --- |
| 提交 sitemap | 立即 (GSC 内可见) |
| Request indexing 首页 | 1-3 天 (Google 重新爬) |
| Request indexing 其他页 | 1-3 天 |
| 搜索结果更新 (title/desc/rich) | 1-2 周 |
| 自然搜索流量回来 | 1-2 个月 |

## 注意事项

- **不要 noindex mta-grout** by mistake (设计故意 noindex, 不是 bug)
- **不要在 robots.txt 里 Disallow** 任何东西 (当前是 Allow: /, 正确)
- **SSL 必须** (你的 .htaccess 强制 HTTPS, 正确)
- **不要改 canonical URL** 指向别的域名 (都是 mtatileadhesive.com, 正确)

## 我的建议

**今天就做**:
1. 登录 GSC, 加 property
2. 提交 sitemap
3. 手动 request indexing 6 个 URL

**不用今天做** (但建议了解):
- Indexing API 自动化
- PageSpeed Insights 检查 (https://pagespeed.web.dev/)
- 移动友好测试
- 关键词监控
