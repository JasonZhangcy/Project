# 码道多端协同 OBP 规划 —— 整体思路与竞争力分析

> 本文档是 PPT 生成前的思路与分析稿。结构:①竞品调研总览 → ②五端定位 → ③各端竞争力特性规划 → ④多端协同机制(PPT 图文核心) → ⑤典型使用场景 → ⑥右侧落地特性清单(含指标) → ⑦PPT 左右结构建议。

---

## 一、竞品调研总览(2026年8月)

| 竞品 | 端布局 | 核心洞察(与本次规划最相关的点) |
|---|---|---|
| **Cursor** | IDE(Cursor 3 Agent-first 界面)、Web(cursor.com/agents)、iOS App、CLI、Slack/GitHub/Linear 入口、**Origin(云端代码托管)** | ① Cursor 3 把交互模型从"编辑文件"转为"管理并行 Agent",所有端(本地/云端/移动/Slack)发起的 Agent 统一出现在一个侧边栏;② **本地⇋云端双向任务迁移已落地**(local↔cloud handoff);③ Origin 是"Agent 时代的 Git Forge":仓库+PR+代码浏览+GitHub 实时镜像同步,云端 Agent 和 Automation 直接对 Origin 仓库建分支/推送/开 PR/响应评审,规划中有 Agent 感知的 Merge Queue 与 Stacked PR;④ 云端 Agent 产出 Demo 截图/录屏等 Artifact 供人审查;⑤ iOS App 支持发起云端 Agent + Remote Control 远程操控本机正在跑的 Agent |
| **OpenAI Codex** | CLI(开源,Rust)、IDE 插件(VS Code/JetBrains/Cursor)、桌面 App、Web/Cloud、GitHub/Slack/Linear 集成、移动(ChatGPT App) | ① 明确的"一个 Agent 引擎、多个 Surface"架构:CLI/IDE/App/Web 共享配置与会话线程,会话可跨端 replay;② CLI 内 `codex cloud` 一条命令把任务甩到云端沙箱,`/app` 切到桌面 App,`/ide` 拉取 IDE 上下文;③ CLI 深耕企业与工程化:沙箱策略(read-only/workspace-write/full)、企业代理/自定义 CA、hooks、Python SDK、`codex exec` 非交互式脚本化、subagents;④ GitHub 集成 `@codex review / @codex fix` |
| **Claude Code** | CLI、桌面 App、VS Code/JetBrains 插件、Web(claude.ai/code)、iOS App、Agent SDK | ① "同一引擎、全端同能力",**`claude --teleport` 把本地终端会话一键搬到云端**,`/teleport` 反向把云端会话拉回本地终端,`claude --remote` 从 CLI 直接发起云端任务;② 移动端两个原语:**Dispatch**(手机发任务→云端执行)与 **Remote Control**(手机遥控本机会话);③ Web 独有原语:**Routines**(定时任务)、**Channels**(Slack/GitHub/Linear 事件推入在线会话);④ Skills/Subagents/Hooks/MCP 四大扩展原语;⑤ 桌面端 Computer Use(操控屏幕) |
| **VS Code + Copilot** | IDE、Agents Window(Agent-first 独立窗口)、CLI、Web、GitHub Mobile | ① 定位"多 Agent 开发之家":Agent Sessions 视图统一管理本地/后台/云端会话,且可运行 Copilot/Claude/Codex 三家 Agent;② 开放 **Agent Host Protocol(AHP)**:远程机器跑 agent host,多个客户端同时连接看到同步的会话视图,客户端全部断开会话仍继续跑;③ 会话可在 Agents Window/Chat/浏览器/CLI 间任意切换接管;④ Copilot CLI `/remote on` 把会话镜像到 GitHub,可从 github.com 或 GitHub Mobile 监控与操纵;⑤ Git worktree 隔离多会话并行 |
| **Qoder(阿里)** | IDE、CLI、Cloud Agents(全托管云端 Agent 平台) | ① **Quest 模式**:Agent-first 独立窗口,"定义目标、评审结果",Spec 驱动开发(先生成需求/设计/任务拆解/验收标准文档再执行);② **Experts 模式**:Lead Agent 自动拆解任务、组建前端/后端/QA/CodeReview 专家团并行执行;③ **Repo Wiki**:自动生成并实时维护代码库结构化知识(40万+仓库已生成),作为 Agent 上下文显著提升准确率;④ 长程执行 + 记忆 + 任务 Fork |
| **WorkBuddy(腾讯)** | 桌面智能体 + 云端任务托管 + IM 远程操控(企微/QQ/飞书/钉钉) | ① 定位"普通职场人的 AI 工作台"(非技术人员),自然语言下达任务→自主拆解→多 Agent 并行→交付文档/图表成果;② **SkillHub 专家市场:100+ 领域专家、7万+ Skills**,兼容 OpenClaw 技能生态,MCP 扩展;③ 混合架构:本地桌面执行 + 云端推理 + 云端任务托管;④ 可操控电脑(Computer Use),连接办公 IM/文档/邮箱/会议/知识库;⑤ 六层架构:大脑/感知/工具/记忆/规划/行动 |

### 三条关键行业趋势(规划立足点)

1. **"一个 Agent 引擎、N 个 Surface"成为标准架构。** 四家头部(Cursor/Codex/Claude Code/VS Code)全部收敛到:任务与会话是云端一等公民,端只是发起、观察、接管、审批的界面。竞争焦点从"哪个端强"转向"**跨端会话连续性**"。
2. **"本地任务一键转云端"已被友商实现**(回答规划要点3-2):Cursor 3 的 local→cloud handoff、Claude Code 的 `claude --teleport`、Codex 的 `codex cloud`,且都支持**反向拉回本地**。这已不是差异化项而是及格线,差异化在于迁移的完整度(上下文/环境/未提交变更/终端状态是否无损)。
3. **Repo 正在成为云端 Agent 的"主场"而非"外部资源"。** Cursor Origin 把代码托管、PR、评审、CI、Agent 编排收拢到一个 Agent 原生平台;下一步竞争是 Agent 感知的 Merge Queue、Stacked PR、事件驱动 Automation。

---

## 二、五端定位

| 端 | 一句话定位 | 目标人群 |
|---|---|---|
| **码道 IDE** | 专业开发者的**深度创作主场**:人机结对、精准可控、Agent 编排指挥中心 | 专业开发者(交互式、强掌控) |
| **码道 Space** | 码道 Agent Space 全新升级,面向**泛研发和泛办公**场景的一站式 AI 工作台:融合 AI 专家、专家团队与丰富技能,覆盖软件开发、产品设计、数据分析、办公协同、深度研究等核心场景,以 AI 驱动研发全链路提效,开启全民开发、全民创造时代 | 泛研发/泛办公人员(产品、测试、运营、数据、行政) |
| **码道 Web** | **以 Repo 为中心的云端 Agent 工场**:云端任务执行与委派、长程并行、任意设备可达的任务总控台 | 全体用户(浏览器即入口) |
| **码道 Mobile** | **随身的 Agent 指挥端**:随时发起、随地掌控、即时审批——把等待时间变成生产时间 | 全体用户(碎片时间场景) |
| **码道 CLI** | **终端原生的 Agent 引擎**:可脚本化、可编排、可嵌入,是自动化流水线与二次集成的运行时底座 | 专业开发者 + 平台工程/DevOps + 被三方产品集成 |

### 码道 Mobile 定位详解(用户待定项)

参考业界(Cursor iOS、Claude iOS、GitHub Mobile),Mobile 的价值不是"在手机上写代码",而是三个动词:**发起、掌控、审批**。

- **发起(Dispatch)**:通勤/会议间隙,一句话(支持语音)把任务派发到云端 Agent 执行,手机只是遥控器;
- **掌控(Remote Control)**:远程接管正在本机 IDE/CLI 上跑的 Agent 会话——离开工位后继续指挥、纠偏、补充指令;
- **审批(Approve)**:Agent 请求敏感权限(执行命令/访问密钥/合并 PR)时手机推送审批;PR Diff 审查、一键合并;任务完成通知与 Demo 截图/录屏审看。

三种载体的差异化分工:**微信小程序**主打零安装的任务查看/审批/通知(触达最广);**鸿蒙元服务**主打卡片化任务状态 + 系统级流转(碰一碰接续到 PC,发挥鸿蒙分布式能力,这是友商没有的差异化);**码道 App** 承载完整能力(远程控制、语音发起、Diff 审查)。

结论:**用户的判断正确**——Mobile 本身不构建重型竞争力特性,它的竞争力=多端协同体验的"最后一公里",其中鸿蒙系统级流转是唯一可做出独有差异化的点。

### 码道 CLI 定位详解(用户待定项):与 IDE 的区分

两者都面向专业开发者,但业界(Claude Code/Codex)已给出清晰分界——**IDE 是"人的界面",CLI 是"机器的界面"**:

| 维度 | 码道 IDE | 码道 CLI |
|---|---|---|
| 交互模式 | 人主导、交互式、可视化(Diff/调试/预览) | 终端原生 + **无头模式**(非交互执行,如 `madao exec`) |
| 核心场景 | 深度开发、精细评审、结对编程 | 脚本化/批处理、CI/CD 流水线、终端工作流(tmux/ssh/远程服务器) |
| 生态角色 | 开发工具 | **Agent 运行时引擎**:SDK 可嵌入、可被三方产品/内部平台集成 |
| 扩展方式 | 插件、可视化配置 | Hooks、MCP、Unix 管道组合、配置即代码 |
| 用户心智 | "我和 AI 一起写" | "我把 AI 编排进我的自动化" |

Codex CLI 开源(67K stars)带来生态与信任;Claude Code 以 CLI 为引擎长出全部端。CLI 的战略价值不在"另一个聊天入口",而在于**它是码道所有端共享的那个 Agent 引擎的直接暴露形态**,也是渗透 DevOps/流水线/服务器场景的唯一形态。

---

## 三、各端竞争力特性规划

### 3.1 码道 IDE(专业开发者)

用户已想到:Token 消耗降低、代码准确率提升。结合 VS Code/Cursor 3/Qoder 洞察补充如下:

| 特性方向 | 内容 | 对标 |
|---|---|---|
| **① 工程效率双指标** | Token 效率:上下文智能压缩、Prompt 缓存、Subagent 上下文隔离(脏活在子上下文完成只回传摘要)、语义检索代替全文投喂;准确率:生成-验证闭环(编译/测试/Lint 自动验证再交付) | Claude Code Subagents、Codex 缓存策略 |
| **② 代码知识引擎** | 自动生成并实时维护仓库级结构化知识(架构/模块/约定),作为 Agent 长期记忆,大仓准确率的胜负手 | **Qoder Repo Wiki(40万+仓库)** |
| **③ Agent-first 工作台** | IDE 内独立 Agent 视图:统一呈现本地/后台/云端所有会话(含其它端发起的),看任务而非看文件;编辑器降级为"审查界面" | **Cursor 3、VS Code Agents Window** |
| **④ 多 Agent 并行 + Worktree 隔离** | 一人同时驱动 N 个 Agent,各自在 Git worktree 隔离分支工作,互不冲突;会话 Fork 探索多方案 | VS Code 1.127+、Cursor、Qoder Fork |
| **⑤ Spec 驱动开发** | 复杂任务先产出需求/设计/任务拆解/验收标准文档,人确认后 Agent 长程执行,确保方向正确 | Qoder Quest Spec-driven |
| **⑥ 自主验证能力** | Agent 内置浏览器工具/运行时验证:改完前端自己打开页面截图验证,产出可视化验证 Artifact | Cursor 云端 Demo 截图、VS Code browser tools |
| **⑦ 下一代 IDE 形态** | 从"文本编辑器+AI 插件"演进为"**Agent 编排台**":以任务/会话为一级对象,代码视图按需展开;开放会话协议(参考 AHP)允许三方 Agent 接入 | Cursor 3(据其数据 35% 用户已很少手改代码)、VS Code AHP |

### 3.2 码道 Space(泛研发/泛办公)

用户已列:专家/专家团、项目空间、Computer Use/Browser Use、DeepResearch、WebSearch、多模态。补充与深化:

| 特性方向 | 内容 | 对标 |
|---|---|---|
| **① 专家/专家团** | Lead Agent 自动拆解任务、动态组建专家团(前端/后端/QA/评审/数据/设计)并行执行、实时对齐集成;专家可定制、可沉淀为团队资产 | Qoder Experts 模式、WorkBuddy 多 Agent 并行 |
| **② 技能与专家市场** | 技能(Skill)标准化封装 + 市场化分发,兼容开放技能生态(OpenClaw/Agent Skills 标准),企业可私有技能库 | **WorkBuddy SkillHub:100+ 专家、7万+ Skills** |
| **③ 项目空间** | 以项目为容器聚合:成员+Agent+知识库+文件+任务流,多人+多 Agent 共享上下文协作(区别于单人会话) | 业界空白点,差异化机会 |
| **④ Computer Use / Browser Use** | 操控桌面与浏览器完成跨应用任务(填报、抓取、回归测试);结合 Remote Control 可"手机下指令、桌面自动干" | WorkBuddy 桌面操控、Claude 桌面 Computer Use |
| **⑤ DeepResearch + WebSearch** | 多源深度调研产出结构化报告;实时检索增强 | Claude/OpenAI DeepResearch |
| **⑥ 多模态创作与交付** | 理解并产出文档/PPT/表格/图表/图片/视频;"成果交付"导向:交付的是可用的报告/页面/应用,不是对话 | WorkBuddy 成果交付理念 |
| **⑦ 定时任务与事件驱动(建议补充)** | Routines:定时驱动 Agent(每日晨报、周报自动生成);Channels:IM 消息/代码事件/工单推入在线 Agent 会话自动响应 | **Claude Code Web 独有原语 Routines/Channels** |
| **⑧ 办公生态连接器(建议补充)** | 打通 IM/邮箱/会议/文档/知识库(WeLink、华为云会议等华为生态),MCP 协议扩展三方系统 | WorkBuddy 腾讯生态打法,华为可复制到自有生态 |

### 3.3 码道 Web(云端 Agent 工场)

| 特性方向 | 内容 | 对标 |
|---|---|---|
| **① 云端 Agent 并行执行** | 每任务独立 VM/沙箱,克隆仓库、装依赖、跑命令、自主迭代到可合并 PR;支持 3~N 个并行 | Cursor Cloud Agents、Claude Code Web、Codex Cloud |
| **② 云端沙箱与环境即代码** | environment.json/Dockerfile/快照(Snapshot)/预构建(Builds)三级环境体系,秒级启动;密钥管理、出网域名管控、私网接入 | Cursor environment.json + Builds |
| **③ 长程任务执行** | 小时级自主执行,断点续跑,过程 Artifact(计划/日志/截图/录屏/Demo)持续可见,支持中途插话纠偏 | Qoder 长程执行、Cursor Artifacts、VS Code 中途纠偏 |
| **④ 下一代 Repo 为中心的云端 Agent 能力** | 对标 Cursor Origin:代码托管+PR+代码浏览+评审与 Agent 同平面;现有代码平台(如 CodeArts Repo/GitHub)实时镜像同步、原平台仍为 source of truth 以降低迁移阻力;**Agent 原生工作流**:事件驱动 Automation(PR 打开→自动评审、Issue 指派→自动修复、CI 红→自动修)、Agent 感知 Merge Queue(自动把 PR 推向可合并状态)、Stacked PR;App 生态(部署预览/CI 集成) | **Cursor Origin(2026.8 Beta)** |
| **⑤ 任务总控台(建议补充)** | Web 即全局任务面板:所有端发起的任务在此可见、可管、可续,是多端协同的"上帝视角" | cursor.com/agents |

### 3.4 码道 Mobile(随身指挥端)

确认用户判断:**Mobile 不做重型能力构建,聚焦轻量指挥面**。规划四件事:

1. **任务发起**:语音/文字一句话派发云端任务(Dispatch 模式),模板化快捷指令;
2. **远程控制**:接管本机 IDE/CLI 正跑的会话,继续指挥(Remote Control),对标 Cursor iOS/Claude iOS;
3. **审批与评审**:敏感操作推送审批、PR Diff 审查与一键合并、Demo 截图/录屏审看、任务完成通知;
4. **差异化:鸿蒙系统级协同**:元服务卡片实时呈现任务状态;跨设备流转(手机上看的任务碰一碰接续到 PC 的码道 IDE)——利用鸿蒙分布式能力,这是 Cursor/Anthropic 都做不了的点。微信小程序做最轻触达(查看/审批/通知)。

### 3.5 码道 CLI(终端原生 Agent 引擎)

参考 Claude Code 和 Codex,CLI 的竞争力构建路径:

| 特性方向 | 内容 | 对标 |
|---|---|---|
| **① 无头模式与脚本化** | `madao exec` 非交互执行,stdout/JSON 输出,Unix 管道可组合——这是 CLI 区别 IDE 的根本 | `codex exec`、`claude -p` |
| **② CI/CD 原生集成** | 流水线内跑 Agent:自动修复失败构建、自动生成测试、自动代码评审;CodeArts Pipeline 深度集成(华为独有生态位) | Codex CI-friendly sandbox |
| **③ Agent SDK / 可嵌入引擎** | SDK(Python/Node)把码道 Agent 引擎嵌入三方工具与内部平台;开放(源)策略换生态与信任 | Codex CLI 开源 67K stars、Claude Agent SDK |
| **④ 企业级工程化** | 分级沙箱(read-only/workspace-write/full)、命令审批策略、企业代理/自定义 CA、审计日志、Hooks 治理钩子 | Codex 企业特性 |
| **⑤ 扩展原语** | Skills/Subagents/Hooks/MCP 四件套,与 IDE/Space 共享同一套扩展生态(一次定义,全端可用) | Claude Code 四原语 |
| **⑥ 跨端会话续接** | `madao --teleport` 本地会话上云 / `/teleport` 云端会话拉回终端 / `--remote` 从终端发起云端任务 / `/ide` 拉取 IDE 上下文 | Claude Code teleport、Codex /ide |

---

## 四、多端协同机制(PPT 图文呈现的核心)

### 4.1 协同的技术底座:「一个大脑,五个界面」

```
                    ┌─────────────────────────────────────┐
                    │        码道云端任务中枢(大脑)          │
                    │  统一会话/任务模型 · 上下文与记忆        │
                    │  云端沙箱 · Repo中心 · 知识库 · 技能库   │
                    └──────────────┬──────────────────────┘
          ┌──────────┬─────────────┼─────────────┬──────────┐
        发起/深改   发起/协作      发起/总控      发起/审批    发起/编排
          │          │             │             │          │
      码道 IDE    码道 Space     码道 Web     码道 Mobile   码道 CLI
     (专业开发)   (泛研发办公)   (云端工场)    (随身指挥)   (自动化引擎)
```

三条协同规则(图上用三种箭头/图例表达):

1. **任务全局可见(Sync)**:任务与会话存储在云端中枢,任何端发起的任务,其它端实时可见、可观察进度、可插话纠偏。例:码道 Web 触发的云端任务,码道 Space 与 Mobile 同步看到。→ 对标 Cursor 3 统一 Agent 侧边栏、VS Code Agent Sessions/AHP(多客户端连接同一会话且同步视图)。
2. **任务双向迁移(Handoff)**:本地(IDE/CLI)会话一键转云端继续执行(带上下文、未提交变更、环境);云端任务也可拉回本地深度调试。→ **友商已做到**:Cursor 3 local↔cloud handoff、Claude Code `--teleport`/`/tp`、Codex `codex cloud`。码道要做的是"无损迁移"(终端状态/环境/分支/上下文完整保留)做到业界最优。
3. **人机分工闭环(Delegate & Approve)**:重决策在人(Spec 确认、权限审批、PR 合并),重执行在云(长程/并行/沙箱),轻交互在端(发起/纠偏/审看 Artifact)。

### 4.2 协同图建议画法(左图下半部分)

- 中心:云端任务中枢(画成一个"任务卡片流",卡片上有状态:执行中/待审批/已完成);
- 五端环绕,每端到中心两根箭头:实线=发起/迁移任务,虚线=同步观察/审批;
- 特别标注两条高亮路径:①「IDE 本地会话 →(一键上云)→ 云端继续执行 → Mobile 收到完成通知」;②「Web 发起任务 → Space 同步可见 → IDE 拉回本地精修」。

---

## 五、典型使用场景(放在左侧架构图最上方,选3~4个)

1. **「下班不断线」**:开发者在码道 IDE 做大型重构,下班前一键把会话转到云端继续执行;通勤路上用码道 Mobile 查看进度、语音补充一条约束;到家后云端已产出 PR 和验证截图,手机审批合并。
2. **「会议室里派活」**:产品经理在码道 Space 用专家团把新需求拆解成 Spec 并派发云端实现;开发者在码道 IDE 的 Agent 视图里同步看到该任务,拉回本地精修边界用例后推回。
3. **「流水线自愈」**:CI 构建失败,流水线自动调用码道 CLI 无头模式诊断修复并开出 PR;负责人在码道 Web 总控台看到任务与修复 Diff,Mobile 一键批准合并。
4. **「全民开发」**:运营同学在码道 Space 用自然语言+技能市场做出数据周报应用,委派云端 Agent 部署;全程没打开过 IDE。

---

## 六、右侧:竞争力规划特性清单(落地项+指标建议)

> 指标为建议值,请按内部基线校准。

**多端协同(主打)**
- 统一任务模型五端全打通:任一端发起的任务,其余端 **100% 可见可续**,状态同步时延 **< 3s**
- 本地⇋云端双向无损迁移:上下文/未提交变更/环境完整保留,迁移耗时 **< 30s**
- 开放会话协议(对标 AHP),支持三方客户端接入

**码道 IDE**
- 代码生成准确率(一次通过验证)**≥ 80%**,复杂任务经 Spec+验证闭环 **≥ 90%**
- 同任务 Token 消耗降低 **≥ 50%**(上下文压缩+缓存+Subagent 隔离)
- 代码知识引擎:仓库知识自动生成覆盖率 **≥ 95%**,大仓(10万文件级)任务准确率提升 **≥ 20%**
- 单人并行驱动 **≥ 5** 个 Agent(worktree 隔离)

**码道 Space**
- 专家团多 Agent 并行,复杂任务交付周期缩短 **≥ 60%**
- 技能市场:首年 **≥ 1000** 技能、**≥ 100** 领域专家(对标 WorkBuddy 7万 Skills 生态)
- Computer Use/Browser Use 任务成功率 **≥ 85%**;DeepResearch 报告一次可用率 **≥ 80%**

**码道 Web**
- 云端沙箱预构建启动 **< 60s**;长程任务持续自主执行 **≥ 24h** 且断点续跑
- Repo 为中心:镜像同步(实时)、事件驱动 Automation、Agent 感知 Merge Queue、PR 自动评审覆盖率 100%
- 每任务自动产出验证 Artifact(截图/录屏/Demo)

**码道 Mobile**
- 任务发起→云端执行 **< 10s**;审批推送触达 **< 5s**
- 远程控制本机会话;鸿蒙元服务卡片 + 跨设备流转(独有差异化)

**码道 CLI**
- 无头模式 + SDK,CI/CD 集成开箱即用;流水线失败自动修复率 **≥ 50%**
- 企业级:分级沙箱、审批策略、审计日志 100% 覆盖
- Skills/Subagents/Hooks/MCP 与 IDE/Space 生态互通(一次定义,全端可用)

---

## 七、PPT 左右结构建议

**左侧(约55%宽)——多端协同规划架构图(自上而下三层)**
1. 顶部横条:3~4 个典型使用场景(小卡片,每个一句话+小图标);
2. 中部主体:五端布局图——每端一个色块,内含「定位一句话 + 3~4 个关键词特性」;
3. 下部:多端协同机制图(§4.2 画法:云端任务中枢居中、五端环绕、实虚两种箭头、两条高亮协同路径)。

**右侧(约45%宽)——竞争力规划特性(按端分组的落地清单)**
- 顶部放"多端协同"主打特性(含指标),下面按 IDE/Space/Web/Mobile/CLI 五组,每组 2~3 条带指标的具体特性(从 §6 精选);
- 建议每条用「特性名 + 指标」格式,右上角可加对标标签(如"对标 Cursor Origin""业界首个")。

**一句话主题(页标题备选)**
- 「一个大脑,五个界面:码道多端协同,任务随人走、算力在云端」
- 「多端协同:随时随地发起、掌控、交付」
