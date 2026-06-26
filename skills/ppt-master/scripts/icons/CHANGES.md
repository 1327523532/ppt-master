# 图标:本地全量库 → 远程按需拉取（变更记录）

> 一句话：图标的真实 SVG 不再随 skill 打包，安装时只带「名称索引」；生成某份 deck 时，按 `<ICON_BASE_URL>/<lib>/<name>.svg` 规则把用到的几十个图标按需拉进 `<project>/icons/`。
>
> 动机：安装 skill 时 coWork 逐文件 copy，11,631 个图标小文件在弱机上要 ~20 分钟。瓶颈是**文件数**，不是体积。
>
> 范围：**只做客户端规则**。图标托管 / 上传 / URL 映射由其他组负责，本改造不含任何服务端脚本。
> 完整设计见 `.kiro/specs/icon-cdn-on-demand/`。

## 改了什么

### 新增（运行时，随包，在本目录 `scripts/icons/`）
- `index.py` —— 读名称索引 `templates/icons/index/<lib>.txt`，`has_icon()` 判断图标名是否合法（替代过去「去全局 SVG 目录看文件在不在」）。
- `fetch.py` —— 唯一的远程取图入口。`icon_base_url()` 读 `ICON_BASE_URL`（经 `config.load_prefixed_env_file`，尾斜杠容错）；`fetch_icon()` 用标准库 `urllib` GET 单个 SVG 落进项目目录，仅 `KNOWN_LIBS` 五大库才发请求。
- `on_demand.py` —— 导出期专用薄封装：拆 `lib/name` + 调 `fetch_icon` + **吞掉 `ICON_BASE_URL` 未配的错误**（导出阶段缺图保留占位符，不中断）。

### 新增（构建 / 测试期，**不随包**，在 repo 根 `tools/`）
- `tools/build_icon_index.py` —— 扫 `icon-source/<lib>/*.svg` 重新生成五个索引文件。**图标库增删后手动跑一次**。
- `tools/icon_cdn_server.py` —— 本地图标 CDN 模拟服务，把 `icon-source/` 暴露成 `<host:port>/<lib>/<name>.svg`，本地测试按需拉取用。

### 改造（运行时）
- `icon_sync.py` —— 选图标时三步解析：①项目已有→跳过；②不在索引→missing 非零退出；③在索引→`fetch_icon` 拉取。移除原来的本地 copy；新增「拉取失败」类别（区别于 missing）；missing 提示语改为 grep 索引。
- `svg_finalize/embed_icons.py` —— `resolve_icon_path` 加 `fetch_fallback`：项目缺图时调 `fetch_missing_icon` 拉进项目再解析，仍失败保留占位符。
- `finalize_svg.py` —— 传 `fetch_fallback=True`；`icons_dir` 固定为项目目录（避免 fetch 写进 skill 包）。
- `svg_to_pptx/use_expander.py`、`svg_to_pptx/drawingml_converter.py` —— 同样接通按需拉取，`icons_dir` 改项目优先。

### 资产迁移
- `skills/ppt-master/templates/icons/<lib>/*.svg`（11,631 个）→ `git mv` 到 repo 根 `icon-source/<lib>/`（仍在 git 内、但在打包路径外）。
- 打包后的 `templates/icons/` 只剩 `index/`（5 个 txt）+ `README.md`。

### 配置
- 新增环境变量 `ICON_BASE_URL`（必填，示例 `https://cowork.lenovo.com/ppt-icon`）、可选 `ICON_AUTH_TOKEN`。见根目录与 skill 的 `.env.example`。

## 维护要点
- **图标库增删后**：把新 SVG 放进 `icon-source/<lib>/`，跑 `python3 tools/build_icon_index.py` 重建索引并提交；真实 SVG 还要同步给托管方。
- **本地验证按需拉取**：`python3 tools/icon_cdn_server.py` 起服务，按它打印的 `ICON_BASE_URL` 配好即可跑全链路。
- **两个阶段的容错不同**：选图标阶段（icon_sync）缺配置/拉不到→**硬报错非零退出**；导出阶段（on_demand）→**软容错保留占位符**。改动时别把两者搞混。
- **缓存策略**：只写项目目录，不做机器级共享缓存（保持 deck 自包含）。
