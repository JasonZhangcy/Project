# Anthropic / Claude Code 能力洞察与演进方向分析

> 用途：华为云 CodeArts 代码智能体 OBP 汇报素材（洞察页）
> 信息截止：2026 年 9 月 10 日
> 说明：模型与产品能力部分来自 Anthropic 官方文档、官方博客与 CHANGELOG，可作为事实引用；商业数据多为二手报道与第三方估算，PPT 引用时建议标注口径与来源；最后一节"未证实信号"仅供研判，不建议作为结论呈现。

---

## 一、结论先行（一句话版本）

**Anthropic 已经不是在做"更好的编码助手"，而是在做"能长期无人值守运行的软件工程劳动力"。** 过去 12 个月它的所有动作，都可以归到同一条主线：把 agent 从"人提示、单会话、前台执行"推向"agent 提示 agent、多体协作、后台常驻、跨端跟随、可被企业治理"。

三个最值得抄的判断：

1. **竞争重心正在从"模型分数"和"harness 技巧"转移到"自治闭环 + 验证器 + 单位成本 + 治理"**。Anthropic 自己在工程博客里明说：harness 会随模型变强而变薄，所以他们把长期资产押在稳定接口上（Managed Agents 的 "meta-harness"）。
2. **自治的边界不是由模型能力决定，而是由"验证成本"决定**。能被机器廉价验证的任务（CI 修复、依赖升级、重构、反馈聚类）已经进入 7×24 无人值守循环；需要人读 diff 的特性开发仍在人机协同区。
3. **产品形态正在从"一个工具"扩为"一套 agent 资产 + 多个人机接口"**：Claude Code（工程师终端）/ Cowork（知识工作者桌面）/ Claude Tag（团队 Slack）/ Claude Security（安全域）/ Managed Agents（API 层），共用同一引擎与同一套 CLAUDE.md、Skills、MCP、Plugins 资产。

---

## 二、模型层：最新发布与能力基线

### 2.1 2026 年模型发布节奏（约 6–8 周一档）

| 日期 | 模型 | 关键点 |
|---|---|---|
| 2026-02-05 | Claude Opus 4.6 | 同日 Agent Teams 进入研究预览 |
| 2026-05-28 | Claude Opus 4.8 | 面向编码与长时 agent 任务 |
| 2026-06-09 | Claude Fable 5 / Mythos 5 | 首次采用"同权重、双安全配置"发布范式 |
| 2026-06-30 | Claude Sonnet 5 | 原生 1M 上下文，成为 Claude Code 默认模型 |
| 2026-07-24 | **Claude Opus 5** | 成为默认 Opus，1M 上下文，$5/$25 per Mtok |
| 2026-09-01 | **Claude Fable 5.1 / Mythos 5.1** | 最新旗舰，缓存读取降价 75% |

### 2.2 当前旗舰能力矩阵

| 模型 | 上下文 | 最大输出 | 价格($/Mtok) | 思考 | 知识截止 |
|---|---|---|---|---|---|
| Claude Fable 5.1 | 1M | 128K | 10 / 50（缓存读 0.25） | Adaptive 常开，默认 effort=high | 2026-06 |
| Claude Opus 5 | 1M | 128K | 5 / 25 | Adaptive 常开 | 2026-05 |
| Claude Sonnet 5 | 1M | 128K | 2 / 10 | Adaptive | 2026-01 |
| Claude Haiku 4.5 | 200K | 64K | 1 / 5 | Extended | 2025-02 |

**Fable 5.1（2026-09-01）值得单独说的三点：**

- **缓存读取从 $1.00 降到 $0.25（-75%）**，是全系唯一 0.025×输入价的档位（其他模型都是 0.1×）。Anthropic 官方口径：典型负载约省 25%，**重上下文的 agentic 负载最高约省 45%**。这是明确针对"长时间 agent 循环"的定价设计。
- **Terminal-Bench-Science 0.1 得分 52.6%**，对比 Fable 5 的 24.7%、Opus 5 的 29.0%，接近翻倍。
- **Adaptive thinking 不可关闭**，深度只能用 `effort` 参数（low→max）调节；Fable 5.1 支持**会话中途改 effort 而不失效 prompt cache**（per-message effort 仍在 beta）。

### 2.3 "同权重双配置"——高危能力发布范式

Fable 5.1 与 Mythos 5.1 **是同一套权重**，区别只在安全护栏层：

- **Fable 5.1**：通用可用，在生物、网络安全等双用途高危域加额外护栏。
- **Mythos 5.1**：放松部分域限制，仅对通过资质审查的组织开放（Project Glasswing、Cyber Verification Program、Life Sciences Verification Program）。
- **关键设计**：Claude Security 产品用 Mythos 5.1 驱动扫描，但**只返回结论（CWE 分类、置信度、补丁建议），不暴露模型本身**——让防御方拿到能力，同时不把能力交给可能滥用的人。

> **洞察**：这是"能力分级发放"的工程化范式。对国内平台的启示是，高危能力（安全攻防、漏洞挖掘）可以通过"资质审查 + 只出结论不出模型"的产品形态释放，而不是简单封禁。

### 2.4 基准体系正在崩塌与重建

- **SWE-bench Verified 已被 OpenAI 公开"退役"**（2026 年 2 月声明：审计发现 ≥59.4% 的失败题目测试本身有缺陷，建议其他厂商也停止上报）。
- Anthropic 的头条基准已转向 **Frontier-Bench v0.1**（Terminal-Bench 团队构建，74 项跨编码/金融/音乐/生物/硬件设计任务）和 Terminal-Bench 系列。
- **顶部模型已高度收敛**：Terminal-Bench 2.1 上 GPT-5.6 Sol 89.5% vs Claude Opus 5 89.1%，差 0.4 分。

参考分数（口径不同，勿直接横比）：

| 基准 | Opus 5 | Fable 5 | Sonnet 5 | Opus 4.8 |
|---|---|---|---|---|
| SWE-bench Verified | 96.0 | 95.0 | 85.2 | 88.6 |
| SWE-bench Pro | 79.2 | 80.0 | 63.2 | 69.2 |
| Terminal-Bench 2.1 | 89.1 | 84.3 | 80.5 | 82.7 |
| Frontier-Bench v0.1 | 43.3 | 33.7 | — | 18.7 |

> **洞察**：**模型分数已经不再是选型决策依据**。这对我们是好消息——竞争战场从"模型军备"移到了"agent loop 质量、集成深度、单位成本、企业治理"，这些是平台厂商能打的。

---

## 三、Claude Code 最新能力全景（按能力域）

当前版本 v2.1.267（2026-09-09），更新节奏约每 1–2 天一个版本、每周数十项变更。

### 3.1 多智能体编排（最核心的演进方向）

四种并行方式，官方明确区分了适用场景：

| 机制 | 上下文 | 通信 | 协调方式 | 适用 |
|---|---|---|---|---|
| **Subagents** | 独立上下文，结果回主会话 | 只能向主 agent 汇报 | 主 agent 统一调度 | 只关心结果的聚焦任务 |
| **Agent View** | 各自独立会话 | — | 人工分发、状态一屏可见 | 独立任务分发后回头查 |
| **Agent Teams** | 完全独立 | **teammate 之间直接互发消息** | 共享任务列表、自协调 | 需要讨论、互相质疑的复杂协作 |
| **Dynamic Workflows** | 结果存脚本变量 | 脚本编排 | Claude 现写 JS 编排脚本 | 大规模审计、迁移、交叉验证研究 |

**近半年的关键变化：**

- **子代理分叉（fork）默认开启**（v2.1.232, 8/13）：`subagent_type: "fork"` 的子代理**继承完整对话与 prompt cache**，不再需要手动搬运上下文。
- **取消每会话 200 子代理硬上限**（v2.1.224, 8/7），长时任务编排器不再被拒绝 spawn。
- **Dynamic Workflows（6/2 预览 → GA）**：Claude 为任务现场写一个 JS 编排脚本（`agent()` / `parallel()` / `pipeline()` / `phase()`），**最多 16 并发、单次运行上限 1000 个 agent**。关键设计：**结果存在脚本变量里而不是模型上下文里，编排规模因此与上下文窗口彻底解耦**。内置 `/deep-research`；用 `ultracode`（effort=xhigh）触发；`/config` 可设规模指引（默认 medium，<15 agents）；管理员可通过 managed settings 禁用。官方说法是"原本按季度规划的工作，现在几天完成"。
- **跨会话协作**：`SendMessage` / `ListAgents`（v2.1.224），在提示框输入 `@` 即可点名**另一台机器上**正在运行的会话并发消息；配套 `crossSessionInbound`（入站消息接受/暂存/拒绝）与 `dialogExpiry` 策略。
- **Agent Teams 的质量门禁**：`TeammateIdle` / `TaskCompleted` hooks、`Task(agent_type)` spawn 限制、agent 的持久 `memory` 字段（user/project/local 三级作用域）、delegate mode（把 lead 限制为只读工具，专注协调不下场实现）。

> **洞察**：agent 组织形态正在从**树形调用**（主 agent → 子 agent → 返回）走向**网状协作**（agent 之间直接通信、共享任务板、互相挑战结论）。这是 CodeArts 代码智能体架构上最需要提前布局的一点。

### 3.2 自治闭环（Loop / 无人值守）

这是 Anthropic 内部叙事里"下一个和 agent 同等量级的跃迁"。

| 原语 | 触发下一轮的条件 | 停止条件 |
|---|---|---|
| `/goal`（v2.1.139, 5/11） | 上一轮结束即触发 | **由独立的、更快的模型**判定完成条件是否满足 |
| `/loop` | 时间间隔到 | 人工停止 / Claude 判断做完 / 7 天上限 |
| `Stop` hook | 上一轮结束 | 自定义脚本判断 |
| **Routines**（4/14） | 定时（时/日/工作日/周）、API POST 触发、GitHub 事件触发 | 云端常驻，关电脑照跑 |

配套的自治基础设施：

- **Auto Mode**（3/24 预览 → **7/10 GA**）：用分类器审查每次工具调用，常规动作直接放行、风险动作拦截或回问人。9/1 起进一步收紧：不再自动批准读取云元数据凭据、规避网络管控、跨租户访问；首次读取工作目录外文件会问一次，并可用 `permissions.blockReadsOutsideWorkingDirectories` 彻底封死。
- **后台会话 + Agent View**：`claude agents` 一屏管理所有后台会话；后台化时**在途工作（后台 shell、子代理、动态工作流、`/loop` 定时任务）会整体迁移到新进程继续跑**。
- 定时任务工具化：`CronCreate` / `CronList` / `CronDelete`。

**Anthropic 官方与 Boris Cherny 的原话（可直接引用到 PPT）：**

> "两年前我们手写源码。后来转变成 agent 写代码。**现在正在转变成 agent 提示 agent、再由 agent 写代码。从源码到 agent 那一步有多大，loop 这一步就有多大。**" —— Boris Cherny, Meta @Scale 大会, 2026-06

> "我不再给 Claude 写提示词了。我有一堆 loop 在跑，由它们来提示 Claude、决定该做什么。**我的工作是写 loop。**"

他自己常驻的 loop：一个持续寻找架构改进点，一个持续寻找可以统一的重复抽象——它们像普通开发者一样提 PR，且因为代码一直在变，**它们永不停止**。

**关键约束（这条最重要，建议单独放一页）：**

> **Loop 只在"验证成本低"的地方赢。** CI 修复能最先自动化，是因为测试套件本身就是现成的验证器；反馈聚类能自动化，是因为报错是免费的真值。特性开发抗拒自动化，是因为验证仍然要一个人读 diff。
>
> 所以**真正的护城河不是提示词工程，而是"决定什么可以无人值守"的判断，以及为它造出的验证器**。`/goal` 的设计细节印证了这点：**判定完成的模型和写代码的模型是分开的**——建造者不能当自己的裁判。

### 3.3 上下文与成本工程（被产品化的 Token 经济学）

方向不是"更大的窗口"，而是**"更少的东西进窗口"**：

- **Tool Search**：工具定义不预载入上下文，按需检索加载。默认开启，工具定义超过上下文 10% 时自动激活（可用 `ENABLE_TOOL_SEARCH=auto:5` 等自定义阈值）。官方数据：**上下文从约 72,000 token 降到约 8,700 token（-85%），且工具选择准确率从 49% 提升到 74%**——省钱的同时还更准。
- **Prompt cache 深度产品化**：Fable 5.1 缓存读取降价 75%；fork 子代理继承父会话缓存；`/cost` 新增每会话缓存明细（命中率、未命中、重新缓存 token 数）；`SessionStart` resume hook 能拿到会话陈旧度与预估重缓存成本；状态栏可读 `prompt_cache` 对象。
- **Effort 分级与上限管控**：`low → high → max`，加上 Claude Code 专属的 `ultracode`（=xhigh 且允许自动触发动态工作流）；**v2.1.267 新增 `maxEffortLevel`**，可在顶层或按模型设置 effort 上限，覆盖 Bedrock / Vertex / Foundry 全部渠道——用户只能往低选，不能往高选。这是**给企业的成本刹车**。
- **溢写与截断**：工具结果落盘上限 1GB 并在预览中标注截断；Managed Agents 侧超过 10 万字符（约 2.5 万 token）的工具输出自动溢写到沙箱文件，模型只拿到截断预览 + 文件路径，需要时自己去读。
- Auto-compact、1M 上下文模型的压缩策略优化、会话 transcript 体积优化（编辑密集会话最高降 79 倍）。

> **洞察**：**"上下文管理"已经从技巧变成了产品能力和商业模式**。CodeArts 如果按 token 计费或有算力预算约束，这一整套（按需工具加载 + 缓存分层 + effort 分级 + 管理员成本上限）是可以直接对标落地的，且 ROI 明确。

### 3.4 多端与执行位置：三态统一

**接入端**：CLI / VS Code / JetBrains / Desktop 应用（4/14 重构为多会话工作区 + 内置终端 + 文件编辑器）/ Web（claude.ai/code）/ 移动端 / Slack。

**执行位置三态**：

1. **本地**：终端、IDE 会话一直在本机。
2. **Anthropic 云**：Claude Code on the web、Routines、移动端会话。
3. **客户自托管**（2026-08-06 公测，Team/Enterprise）：`claude self-hosted-runner` 把自有机器/容器变成执行底座。
   - 两种模式：**fixed**（固定数量常驻）与 **on-demand**（编排器按队列拉起、做完销毁，容量随需求走）。
   - 每个会话独立 checkout，互相隔离；支持企业出口代理、mTLS、`--proxy-authorization-command` 动态 Proxy 头、Anthropic git proxy（不把凭据烤进镜像）；`--defer-shutdown-max-min` 优雅停机。
   - **限制**：默认关闭，需管理员开启；**ZDR（零数据保留）组织不可用**；Claude Tag、Claude Security、Code Review 三类会话暂不路由到自托管环境。Anthropic 自己也明确劝退："绝大多数企业建议用托管版，自托管请配备平台团队长期运维。"

**会话可迁移性**：Remote Control 把本地会话桥接到网页/手机（执行和文件访问仍在本机）；`claude --teleport`；跨端会话跟随 Claude 账号；Cowork 云端会话在关笔记本后继续跑。

> **洞察**：**这是"agent 作为常驻数字员工"的基础设施层**。注意 Anthropic 的自托管刚公测、限制不少（ZDR 不可用、部分产品不支持），而**私有化/信创部署恰恰是国内云厂商的天然主场**——这是明确的差异化窗口。

### 3.5 扩展与生态：agent 资产的标准化与分发

Anthropic 已经把"agent 资产"做成了完整的**打包—分发—治理**体系，这是最容易被低估、但对平台方最关键的一层。

| 资产 | 作用 | 分发方式 |
|---|---|---|
| `CLAUDE.md` | 项目上下文与规范（可分层：根目录 + 子目录 + 系统级组织规范） | 随仓库 |
| **Skills**（`SKILL.md`） | 可复用的工作流指令包，可被模型按描述自动加载或人工 `/xxx` 调用 | `.claude/skills/`、插件 |
| **Hooks** | 生命周期事件驱动的强制逻辑（不依赖模型"记得遵守"） | settings |
| **Subagents** | 角色化专家定义，**可同时用作子代理和 agent team 队友** | 项目/用户/插件/CLI |
| **MCP servers** | 外部系统连接（本地 stdio、远程 HTTP/SSE + OAuth） | `.mcp.json`、组织级下发 |
| **LSP servers** | 语言服务能力 | 插件 |
| **Plugins** | 以上全部的打包单元 | **Marketplace** |

**插件市场机制（值得直接抄）：**

- 官方市场 `claude-plugins-official`（Anthropic 策展，首次交互启动时自动注册）+ 社区市场 `claude-plugins-community`（通过自动化校验与安全筛查后入库，**每个插件固定到具体 commit SHA**，CI 自动 bump）。
- 分发源支持 git / GitHub / GitLab / 本地路径 / **HTTPS ZIP 归档（可固定 SHA-256）**；**认证源**（`headersHelper` 命令动态生成短时令牌，用于私有目录与同源归档拉取，安装前展示该命令并要求确认）。
- 治理侧：`strictKnownMarketplaces`、`extraKnownMarketplaces`、`pluginSuggestionMarketplaces`（管理员白名单哪些市场的插件可被智能推荐）、版本按 SHA 固定而非 latest。
- 体验侧：`/plugin` 浏览页在安装前展示插件提供的 commands/agents/skills/hooks/MCP/LSP，**以及预估的上下文开销（每轮和每次调用的 token 估算）**。

**Hooks 事件已非常密集**（可作为治理插桩点）：`PreToolUse`、`PostToolUse`、`SessionStart`、`Stop`、`StopFailure`、`Notification`、`DirectoryAdded`、`PreModelSwitch` / `PostModelSwitch`（可阻止/确认/标注模型切换）、`TeammateIdle`、`TaskCompleted`。

**MCP 侧的组织化演进**：`managedMcpServers`（组织统一下发 HTTP/SSE MCP 服务）、`allowedMcpServers` / `deniedMcpServers` 策略、**MCP tunnels**（研究预览，连通企业私网内的 MCP 服务器）。

> **洞察**：**Anthropic 真正的护城河正在从"模型"转向"agent 资产的标准与市场"**。CLAUDE.md / SKILL.md / MCP 已经在事实上成为行业标准格式。CodeArts 的选择题是：兼容这套标准（快速借力生态），还是自建（可控但要独自养生态）。**我的建议是兼容 MCP + Skills 格式，在其上叠加华为云特有的资产（信创工具链、企业规范、CI/CD 门禁）**。

### 3.6 安全与治理：自治度的对价

**核心逻辑**：自治度提高后，交互式权限提示消失了，**沙箱、deny 规则、hook 就成了唯一护栏**。官方文档写得很直白——"auto mode 不是把权限系统关掉，它是在你画的边界内自动批准，**所以画边界本身才是工作**"。

- **Bash 沙箱**（macOS Seatbelt / Linux bubblewrap）：默认 deny，写权限限于工作目录，网络仅限 localhost，出网走本地代理白名单。`sandbox.network.strictAllowlist` 直接拒绝非白名单主机不再询问；`allowUnsandboxedCommands: false` 关闭"逃生舱"（否则命令在沙箱内失败时 Claude 会带提示重试于沙箱外）；`sandbox.credentials` 阻止沙箱命令读取凭据文件与密钥环境变量。
- **凭据掩码**（Linux/WSL）：`mode: "mask"` 让沙箱内命令读到哨兵值，代理在出网时替换回真实密钥；支持 `extract` 只掩码结构化变量中的敏感片段、`decode: "jwt"` + `maskClaims` 按 JWT 声明粒度遮蔽、`awsPairs` + `sigv4` 对 AWS 请求掩码后自动重签（掩码后仍能通过 AWS 校验）。
- **`@anthropic-ai/sandbox-runtime`**：把整个进程（含 hooks、MCP server、文件工具）都包进同一隔离边界，而不只是 Bash。
- **`--restricted` 受限模式**（8/27）：为共享机器上的评测harness设计，移除内置命令与代码执行工具及 WebFetch（除非用 `--tools` 显式指定），文件工具限于工作目录，忽略用户/项目/本地配置，拒绝 `bypassPermissions`——但 managed settings 仍生效。
- **`--safe-mode`**：一键禁用所有定制（CLAUDE.md、插件、Skills、Hooks、MCP）用于排障。
- **组织策略强制**：server-managed settings（claude.ai 网页端下发，无需 MDM）与 endpoint-managed settings（MDM）**并列最高优先级，连命令行参数都无法覆盖**；且是"整体替换"而非合并。官方也诚实标注了局限——服务端下发本质是客户端控制，在非受管设备上有 sudo 权限的用户可绕过，强约束仍需 MDM。
- **可观测与合规**：OpenTelemetry 导出会话/工具/token/成本（`OTEL_LOG_TOOL_DETAILS=1` 可记录完整 shell 命令与 MCP/skill 名）、Analytics 仪表盘 + Analytics API、支出与速率限制、**Compliance API**（Enterprise 专属，实时程序化获取使用数据与内容，可接 SIEM，支持选择性删除以满足 GDPR）、SSO / SCIM / RBAC / IP 白名单 / SOC 2 Type II。
- **多云部署**：Amazon Bedrock、Google Cloud Agent Platform（Vertex）、Microsoft Foundry、Claude Platform on AWS，对接企业既有 IAM / CloudTrail / VPC。

### 3.7 研发流程闭环（从写代码到管交付）

- **Code Review**：PR 进入人工评审前自动按组织规范预审、标记问题、给改进建议。
- **Cloud auto-fix**：网页/移动会话可自动跟踪 PR、修复 CI 失败、回应评审意见——**你回来时看到的是一个 ready-to-go 的 PR**。
- **GitLab 深度支持**（8 月起密集补齐）：MR URL 可用于 `--worktree` 和 `claude agents`、9 类 GitLab 令牌自动脱敏、插件市场原生支持 gitlab.com 与自建 GitLab、修复自建 GitLab OAuth scope 问题。GitHub Enterprise Server 同样支持。
- **`/diff` 面板**（v2.1.260）：全屏模式下在对话旁开一栏，实时展示 Claude 正在改的未提交变更。
- Checkpoint 与回滚、`/verify` 与 `/code-review` 技能（注意：9 月起 Claude **不再自作主张调用**这两个技能，改为人工显式触发——这是"该由人守的门就让人守"的产品判断）。

---

## 四、产品矩阵：从一个 CLI 到一套 agent 平台

这是 OBP 上最有说服力的一张图——**同一个 agent 引擎，长出五个面向不同人群的接口**。

| 产品 | 发布 | 面向 | 在哪用 | 用谁的权限 | 谁能看到 |
|---|---|---|---|---|---|
| **Claude Code** | 2025-02 预览 / 05 GA | 工程师 | 终端 / IDE / 桌面 / 网页 / 手机 | 你的本地凭据与文件系统 | 只有你 |
| **Cowork** | 2026-01-12 | 知识工作者 | Claude 桌面端 / 网页 / 移动 | 你的个人 OAuth 连接器 | 只有你 |
| **Claude Tag** | 2026-08-23 | 团队 | Slack 频道 | **管理员按频道配置的服务账号** | **频道里所有人** |
| **Claude Security** | 2026-02 预览 / 公测 | 安全团队 | claude.ai/security | 组织 GitHub 授权 | 安全团队 |
| **Managed Agents** | 2026 beta | 开发者/平台 | Claude API | API Key + vault | 调用方 |

### 4.1 Cowork —— 把 agent 能力交给非程序员

- 2026-01-12 发布（macOS 研究预览，仅 Max），现已覆盖 macOS + Windows 桌面端，Pro / Max / Team / Enterprise 均可用。
- **"与 Claude Code 相同的 agentic 架构，但不需要打开终端"**。授予指定文件夹读写权限，自主规划多步任务，产出**真实文件**（.docx / .xlsx / .pptx），而不是聊天文本。
- 云端远程会话（beta）：会话与文件存在 Claude 账号里、跨桌面/网页/移动跟随；**关上笔记本工作在 Anthropic 服务器的隔离环境里继续跑**。
- Chat 与 Cowork 共用同一个 home 与输入框；支持 Projects（持久工作区，各自的文件、连接、说明与记忆）和 scheduled tasks。
- 官方定位对比：**Chat 是顾问，Cowork 是执行助理，Claude Code 是给工程师造自动化机器的**。

### 4.2 Claude Tag —— 最值得关注的新形态（团队级 agent）

2026-08-23 发布，从 Slack 起步，Team/Enterprise 公测，取代原有的 Claude in Slack。

- 在频道里 `@Claude` 像叫同事一样派活，它拆解任务、逐阶段执行、在 thread 里回结果。
- **能主动参与**：会跟踪对话、结合记忆和常驻指令，自己判断何时该插话。
- **身份与权限模型是关键差异**：用**管理员按频道配置的服务账号凭据**，不是任何个人的权限；工作对频道全员可见（对比 Cowork/Claude Code 是个人私有）。
- 每个会话跑在 Anthropic 托管的临时沙箱里，**跑的是与 Claude Code on the web 相同的引擎**；克隆仓库、改代码、推分支，**以 Claude GitHub App 的独立身份**开草稿 PR（所以它出现在你的评审队列里，和普通 PR 一样）。
- 自动加载仓库里的 `CLAUDE.md`、`.claude/rules/*.md`、`.claude/skills/`——**同一套 agent 资产在不同接口间复用**。
- **Anthropic 自曝数据：其产品团队 65% 的代码由内部版 Claude Tag 产生。**"@Claude 现在是我们在 Anthropic 干活的主要方式之一"；用法已扩散到工程之外——追产品指标、处理支持工单、定位疑难 bug 根因。

> **洞察**：这是"**agent 从个人工具变成团队成员**"的关键一跃。技术不难（同一个引擎换个接口），难的是**身份模型**：服务账号 + 频道级权限 + 独立 Git 身份 + 全员可见。CodeArts 完全可以在企业微信/钉钉/WeLink + CodeArts 项目管理上复刻，且国内 IM 与研发平台的绑定比 Slack + GitHub 更紧。

### 4.3 Claude Security —— agent 能力反向变成安全产品

- 前身 Claude Code Security（2026-02-20 限量预览）→ 公测（Claude Enterprise），**扫描由 Mythos 5 驱动**，按标准 token 计费、无独立附加费。
- **不是模式匹配**：读 Git 历史、追跨文件数据流、理解业务逻辑，像安全研究员一样推理，专找内存破坏、注入、认证绕过、复杂逻辑缺陷这类模式匹配工具抓不到的问题。
- **多阶段验证管线**：每条发现在到达分析师前被独立复核，压低误报，并给出置信度评级。
- 工程化配套：定时扫描、定向扫描（指定目录/分支）、带理由驳回（后续评审可信任前次三查结论）、CSV/Markdown 导出、Slack/Jira webhook。
- 修复动线：在 **Claude Code on the web** 里打开做交互式补丁，**每个补丁必须人工审批**。
- 配套 3500 万美元开源软件安全基金。

### 4.4 Claude Managed Agents —— 长期最重要的一步棋

Anthropic 的 API 侧托管 agent 平台（beta，`managed-agents-2026-04-01`）。三类资源：

- **Agent**：模型 + 系统提示 + 工具 + MCP servers + skills，**版本化资源**（会话可 pin 版本，也可单次 override）。
- **Environment**：会话在哪跑——Anthropic 托管沙箱，**或客户自托管沙箱**。
- **Session**：环境里的一个运行实例，**append-only 的事件日志**，支持流式、预算约束、`vault_ids` 管理 MCP 认证。

**其工程博客《Scaling Managed Agents: Decoupling the brain from the hands》里的观点，是理解 Anthropic 战略最关键的一段：**

> "Harness 编码了会随模型变强而过时的假设。所以我们把 Managed Agents 建立在**能比任何具体实现活得更久的接口**之上——包括我们今天自己在跑的实现。"
>
> "我们把 agent 拆成 session（发生过的一切的 append-only 日志）、harness（把 Claude 的工具调用路由到具体基础设施的循环）、tool（各自的实现），**任何一层都能被替换而不惊动其他层**。"
>
> "Managed Agents 是一个 **meta-harness**……Claude Code 是一个很棒的 harness，我们广泛使用它；我们也证明了任务专用 harness 在窄域里更强。Managed Agents 能容纳任何一种。"

配套演进：session 事件日志作为**活在上下文窗口之外的上下文对象**，`getEvents()` 支持按位置切片（从上次停下的地方接着读、回退几个事件看前因、重读某个动作前的上下文）；大工具输出自动溢写文件；可在活跃会话中途更新 MCP 与工具配置；`agent_toolset_20260401` 内置工具集可按域限制 `web_search` / `web_fetch`。

> **洞察（本节最重要）**：**Anthropic 自己已经判定 harness 会贬值，所以把长期资产押在"稳定接口 + 会话状态 + 托管执行"上。** 这对 CodeArts 的战略含义极强——如果我们把投入全押在"更好的对话交互、更巧的提示词、更聪明的编排技巧"，这些会随模型变强而快速折旧；真正保值的是**会话/事件的持久化标准、验证器资产、企业数据与权限的接入面、以及跨研发全流程的集成深度**。

---

## 五、商业与市场数据（PPT 引用请标注口径）

### 5.1 Anthropic 整体

| 时间 | 年化收入运行率(ARR) |
|---|---|
| 2024 年底 | ~$1B |
| 2025-08 | >$5B |
| 2025 年底 | ~$9B |
| 2026-02 | $14B |
| 2026-04 | $30B+ |
| 2026-05 | $47B+（Series H 披露，融资 $65B，估值 $965B） |
| 2026-07 | >$65B（彭博/路透，投资人材料） |

- 2026 实际确认收入预计 $20–26B（run-rate 领先于确认收入）。
- Q2 2026 录得**正的调整后经营利润**（彭博看到的初步财务文件）。
- 2026 年中已**保密提交 IPO**。
- 收入结构估算：API 模型服务 70–75%，订阅与席位 10–15%，Claude Code 与 agentic 产品其余部分。

### 5.2 Claude Code 单品

| 时间 | ARR | 备注 |
|---|---|---|
| 2025-11 | $1B | **GA 后 6 个月，企业软件史上最快** |
| 2026-02 | >$2.5B | 约占公司 18%；商业订阅自 1 月起翻两番 |
| 2026-05 | ~$8B（第三方预测） | 约占公司 17% |
| 2027-05 | ~$21B（FutureSearch 预测中位数） | — |

- **企业用户贡献超过一半收入**；1000+ 客户年花费超 100 万美元（$1M+ 企业客户数在两个月内从 500+ 翻倍到 1000+）。
- **Claude Code 生成的代码占公开 GitHub 提交的 4%**，SemiAnalysis 预测 2026 年底超 20%。
- Anthropic 内部工程生产力提升 200%；Boris Cherny 自 2025 年 11 月起**代码 100% 由 AI 编写（零手动编辑），日均 10–30 个 PR**。

### 5.3 竞争格局（2026 年初 JetBrains 等调研）

| 工具 | 认知度 | 工作场景采用率 | 规模 | 趋势 |
|---|---|---|---|---|
| GitHub Copilot | 76% | 29%（付费工具份额约 42%） | 26M+ 用户 / 4.7M 付费 | **停滞**，同比持平 |
| Cursor | 69% | 18% | ~7M MAU / 1M+ 付费 / $2B ARR | **放缓** |
| **Claude Code** | 57% | 18%（美加 24%） | — | **爆发：9 个月 6 倍** |
| OpenAI Codex | 27% | 3% | 1M+ WAU（3 月）→ 3M WAU | 加速 |
| JetBrains Junie / AI Assistant | — | 5% / 9% | — | 稳定 |
| Google Antigravity | — | 6% | — | 新进入者 |

**开发者"最爱工具"（2026-04 调研）：Claude Code 46% > Cursor 19% > Copilot 9%。** Claude Code CSAT 91%、NPS 54。

其他结构性观察：

- AI 编码工具市场规模 2026 约 $9.5B（2025 约 $7.65B）；企业侧年化接近 $11B；84% 开发者已在用 AI 工具。
- **Cursor 把大部分 agent 模式流量路由到 Claude 后端**——Anthropic 是 Cursor 增长的隐形受益者，Anysphere 拿应用层经济。
- 2026 年 6 月市场领导者从固定订阅转向按量计费信用池，引发大规模流失与替代品搜索——**定价模式是这个市场当前最大的不稳定因素**。
- 差异化已从"补全质量"转移到"**agent loop 质量**"：多文件规划、跑测试、按失败迭代、长会话上下文保持。
- 行业预计 18 个月内收敛到 3–5 个应用层主产品 + IDE 内置方案。

---

## 六、未来演进方向洞察（PPT 核心页）

### 方向一：从"人提示 agent"到"agent 提示 agent"——Loop 成为一等公民

- **已发生**：`/goal`（条件达成即停）、`/loop`（按时钟轮询）、Routines（云端定时/API/GitHub 事件）、Auto Mode GA、Stop hook。
- **正在发生**：模型开始**自己主动提议开 loop**（Boris 的例子：他要一次数据查询，模型注意到数据会随时间变化，主动提议每 30 分钟出一次报告并接到 Slack）。Boris 对此的评价是"这不该是用户去学怎么用好工具，**这是产品设计问题，是我没做好**"。
- **未来 12 个月**：loop 的创建、验证、编排、成本约束会全面产品化，"写 loop"取代"写提示词"成为主要人机接口。
- **给 CodeArts 的动作**：把"定时/事件驱动的研发 agent 任务"做成一等公民（对接流水线事件、代码仓事件、缺陷单事件、告警事件），而不是只做对话式助手。

### 方向二：验证成本决定自动化边界——验证器是新的护城河

- **规律**：CI 修复最先自治（测试套件即验证器）→ 依赖升级、rebase、重复抽象消除、反馈聚类（真值免费）→ 特性开发最晚（验证需要人读 diff）。
- **产品化体现**：`/goal` **用与建造者分离的、更快的模型做完成判定**；dynamic workflow 内部让 agent 从不同角度攻击同一问题、**互相反驳、迭代到答案收敛**；Claude Security 的多阶段独立验证管线 + 置信度评级；`/verify` 与 `/code-review` 改为人工显式触发。
- **给 CodeArts 的动作（最大机会点）**：**华为云在"验证器"这件事上比 Anthropic 更有资产**——CodeArts 内部就有测试管理、代码检查、编译构建、流水线门禁、部署校验、性能压测。把这些统统包装成 agent 可调用的验证器，是我们能建立而 Anthropic 建不了的壁垒。**这一条建议在 OBP 上单独成页。**

### 方向三：编排规模跃升，agent 组织从"树"变"网"

- 单会话子代理上限已取消；动态工作流单次可编排至 1000 个 agent、16 路并发；agent teams 让队友直接互发消息、共享任务板、自协调、互相挑战；跨机器跨会话消息已落地。
- **关键架构洞察**：动态工作流把**编排结果存在脚本变量而非模型上下文里**，从而让编排规模与上下文窗口彻底解耦——这是"上百 agent 协作"能成立的技术前提。
- **未来**：Coordinator 模式、agent 之间的任务市场与冲突消解、agent 组织的可观测性（谁在做什么、算力花在哪、结论冲突了找谁裁决）会成为新的产品面。
- **给 CodeArts 的动作**：架构上现在就要把"编排状态外置"设计进去，不要把编排逻辑绑死在对话上下文里。

### 方向四：Harness 会变薄，价值沉到接口、状态与集成

- Anthropic 亲口承认："模型变强，harness 变得没那么重要了"；Managed Agents 被明确设计为不对具体 harness 做假设的 **meta-harness**。
- **推论**：今天所有"agent 产品的巧思"（更好的提示模板、更妙的上下文压缩、更聪明的工具选择）都会被下一代模型内化并贬值。
- **保值的资产**：① 稳定的会话/事件持久化接口；② 企业数据与权限的接入面；③ 验证器资产；④ 跨研发全流程的集成深度；⑤ 治理与合规能力。
- **给 CodeArts 的动作**：**投入配比要向"接口 + 集成 + 治理"倾斜**，而不是向"对话体验的技巧"倾斜。

### 方向五：上下文与成本工程被产品化，成为企业采购的决策项

- 按需工具加载（-85% token，且准确率提升）、缓存读取降价 75%、fork 继承缓存、effort 分级 + **管理员侧 `maxEffortLevel` 成本刹车**、auto-compact、大结果溢写磁盘、`/cost` 缓存命中率可视化、`/usage` 按 skill/subagent/plugin/MCP 拆分消耗。
- **未来**：单位任务成本会和准确率并列成为选型指标；"每个 PR 花了多少钱"会进入企业研发效能看板。
- **给 CodeArts 的动作**：把 token 成本做成可观测、可预算、可按组织策略封顶的一等公民能力。这在国内算力受限的语境下比在美国更有说服力。

### 方向六：执行位置解耦，自托管与内网可达成为企业分水岭

- 三态（本地 / 厂商云 / 客户自托管 runner）已经统一到同一控制面，会话跨端跟随、关机继续跑。
- **Anthropic 的自托管仍有明显短板**：2026-08 才公测、默认关闭、**ZDR 组织不可用**、Claude Tag / Claude Security / Code Review 不支持路由、且官方主动劝退（需专职平台团队运维）。
- **给 CodeArts 的动作（第二大机会点）**：**私有化、信创、内网可达、数据不出域**是我们的主场而不是我们的负担。建议把"自托管即默认形态、全产品线一致支持"作为对比 Anthropic 的明确优势点。

### 方向七：产品矩阵扩张——同一引擎，多个"人机接口"

- Claude Code（工程师）→ Cowork（知识工作者）→ Claude Tag（团队）→ Claude Security（安全）→ Managed Agents（平台/API）。
- 共用同一 agent 引擎、同一套 `CLAUDE.md` / Skills / MCP 资产，**差异只在"用谁的身份、在哪个协作场域、谁能看到结果"**。
- Claude Tag 的 65% 内部代码占比说明：**团队场域（IM 频道）可能比个人场域（终端）有更大的量**。
- **给 CodeArts 的动作**：规划"一套 agent 资产 × 多接口"的产品架构（IDE / CLI / 网页 / 流水线 / IM），而不是每个入口各做一套。

### 方向八：安全治理从"合规附加项"升级为"能力项"

- 自治度上升 → 交互提示消失 → **沙箱、deny 规则、hook 成为唯一护栏**。
- 已成体系：双层沙箱隔离、凭据掩码（含 JWT claim 级、AWS SigV4 重签）、分类器权限、组织策略强制（连命令行都覆盖不了）、受限模式、OTel、Compliance API、插件市场 SHA 固定与白名单。
- **同时安全能力反向变成产品**（Claude Security），且用"只出结论不出模型"的方式释放高危能力。
- **给 CodeArts 的动作**：治理能力要作为卖点前置，而不是作为合规清单后置。国内企业对"agent 能碰什么、做了什么、能不能审计"的敏感度只会更高。

### 方向九：角色与度量体系的变化

- Boris 预测："**software engineer 这个头衔会在 2026 年底开始消失，被 builder 取代**"，同时通过 agent 写代码的人数增长百倍。
- 瓶颈从"能不能建"变成"**该建什么**"——Claude Code 已经能扫反馈渠道、缺陷报告和遥测，主动提出修复与特性。
- **给 CodeArts 的动作**：研发效能度量要从"代码产出量/采纳率"转向"**需求吞吐、验证通过率、无人值守任务成功率、单位任务成本**"。这也是 OBP 上一个很好的价值主张切入点。

---

## 七、未证实信号（低置信度，建议标注为"信号"而非事实）

来源为 2026-03 泄露的 Claude Code v2.1.88 source map（59.8MB、51.2 万行 TypeScript、32 个编译期特性开关、22+ 个 GrowthBook 运行时开关）与社区分析。**建议在 PPT 上单独标注置信度。**

- **KAIROS**：最大的未发布特性，把 Claude Code 从被动助手变成**主动自治 agent**（无人值守运行、主动行动、推送通知）。
- **Coordinator Mode**：主 agent 管理并行工作者的协调层。
- **Voice Mode**：按键说话的语音输入，代码已实现、被 `VOICE_MODE` 开关拦住。
- **BUDDY**（虚拟宠物/伴侣系统）、Dream Task。
- 未发布模型代号：Numbat、Capybara、Fennec、Tengu。
- **反蒸馏措施**：假工具注入、Undercover Mode——说明 Anthropic 对模型 IP 保护的重视程度。

**为什么值得看**：该列表中的 `BYOC_RUNNER` / `SELF_HOSTED`（→ 2026-08 自托管环境）、插件市场、多 agent 编排（→ agent teams / dynamic workflows）**都已在 2026 年陆续兑现**，说明这份线索有一定预测力。据此，**KAIROS 式的"主动自治 + 推送"和 Coordinator Mode 是未来 6–12 个月最可能落地的两项**。

---

## 八、对 CodeArts 代码智能体的对标建议（供 OBP 收敛）

### 8.1 换一个对标坐标系

不要按"IDE 插件 vs CLI 工具"对标，建议按**四层**对标，这样差距和机会都会更清楚：

| 层 | Anthropic 的做法 | 我们的位置 |
|---|---|---|
| 模型层 | 6–8 周一档，同权重双配置分级发放，1M 上下文，缓存降价打 agentic 场景 | 依赖盘古/三方模型，需明确长上下文与缓存策略 |
| Harness / 编排层 | 子代理 → agent teams → 动态工作流（1000 agent）→ loop 自治 | **主要差距区** |
| 多端与执行位置 | 本地/云/自托管三态统一，会话跨端跟随 | **自托管是我们的主场，需放大** |
| 治理与生态 | 策略强制 + OTel + Compliance API + 插件市场 + MCP 标准 | 需体系化 |

### 8.2 建议"抄"的三件事

1. **验证器优先的自治闭环**：`/goal` 式的"完成条件 + 独立裁判模型"，并把 CodeArts 已有的测试、检查、门禁、流水线全部注册为 agent 可调用的验证器。**这是我们比 Anthropic 更有资产的地方。**
2. **agent 资产的标准化与市场**：兼容 MCP + Skills（`SKILL.md`）格式借力现成生态，在其上叠加企业规范、信创工具链、行业模板；市场侧照抄"SHA 固定 + 安全筛查 + 管理员白名单 + 安装前展示上下文开销"。
3. **Token 经济学产品化**：按需工具加载、缓存分层、effort 分级 + 管理员成本上限、每任务成本可观测。

### 8.3 建议"不抄"的一件事

**不要在 harness 的交互技巧上重投入。** Anthropic 自己已经判定这层会随模型变强而贬值。把资源放到接口稳定性、企业集成深度、验证器资产和治理上。

### 8.4 差异化窗口（Anthropic 当前的短板）

1. **自托管/私有化**：他们 2026-08 才公测、默认关闭、ZDR 组织不可用、部分产品不支持路由、官方主动劝退。我们可以做到"自托管即默认、全产品线一致"。
2. **研发全流程一体化**：Anthropic 只有代码域，需求、测试、流水线、部署、运维都靠 MCP 外接；CodeArts 天然一体，做端到端闭环的验证与追溯更完整。
3. **团队协作入口本地化**：Claude Tag 绑 Slack + GitHub；国内可绑企业微信/钉钉/WeLink + CodeArts 项目管理与代码仓，绑定更紧、身份体系更统一。
4. **安全域产品化**：对标 Claude Security，结合已有代码检查、开源治理、供应链安全能力，且"只出结论不出模型"的能力释放范式可直接借鉴。

---

## 九、可直接放进 PPT 的关键数据卡片

**能力**
- Claude Fable 5.1（2026-09-01）：1M 上下文 / 128K 输出 / 缓存读取降价 75% / agentic 负载成本最高降 45%
- Claude Opus 5：SWE-bench Verified 96.0%，Terminal-Bench 2.1 89.1%
- 动态工作流：单次编排上限 **1000 个 agent**，16 路并发，"原本按季度规划的工作几天完成"
- Tool Search：上下文 72K → 8.7K token（**-85%**），工具选择准确率 49% → 74%

**商业**
- Claude Code：GA 后 **6 个月破 $1B ARR**（企业软件史上最快）→ 2026-02 $2.5B+ → 2026-05 约 $8B
- Anthropic 总 ARR：2024 年底 $1B → 2026-07 **$65B+**
- Claude Code 生成代码占**公开 GitHub 提交的 4%**，预测 2026 年底 >20%
- 开发者最爱工具：**Claude Code 46%** vs Cursor 19% vs Copilot 9%

**组织变革**
- Anthropic 内部工程生产力 **+200%**
- 其产品团队 **65% 的代码由内部版 Claude Tag 产生**
- Claude Code 负责人自 2025-11 起代码 **100% 由 AI 编写**，日均 10–30 个 PR

**战略原话**
- "从源码到 agent 那一步有多大，**loop 这一步就有多大**。"
- "我不再写提示词了。**我的工作是写 loop。**"
- "Harness 编码了会随模型变强而过时的假设——所以我们押注在**能比任何具体实现活得更久的接口**上。"

---

## 十、主要信息来源

**官方（高置信度）**
- Claude Code 官方文档与 CHANGELOG：`code.claude.com/docs`、`github.com/anthropics/claude-code`
- Claude Platform 文档与 release notes：`platform.claude.com/docs`
- Anthropic 博客：Claude Tag 发布、Claude Security 公测、自托管环境、动态工作流、Fable 5.1/Mythos 5.1 System Card
- Anthropic 工程博客：《Scaling Managed Agents: Decoupling the brain from the hands》

**访谈与一手观点（高置信度）**
- Boris Cherny（Claude Code 负责人）：Lenny's Podcast、Big Technology、Meta @Scale 大会、Sequoia 演讲、Platformer 专访

**市场与商业数据（中等置信度，多为二手估算）**
- SaaStr、Bloomberg/Reuters 转述、FutureSearch 预测、JetBrains 开发者调研、Menlo Ventures、SemiAnalysis、Artificial Analysis

**低置信度（仅供研判）**
- 泄露的 v2.1.88 source map 分析与社区整理的"未发布特性清单"
