
# AI Daily News Skill

&gt; 🌍 **Get global AI news with zero setup, turning your Agent into an AI news expert instantly**

&gt; 💡 **Server-side pre-processing saves you 90% on tokens, contributing to green computing**

&gt; 🔓 Open Source, Apache-2.0 Licensed

---

## ✨ Why Choose AI Daily News?

### 🎯 Lower Technical Barriers, Works Out-of-the-Box
- **No need to build your own crawler**: We periodically fetch content from high-quality news sources worldwide
- **Smart deduplication**: Multiple reports on the same story are automatically deduplicated, keeping only the most valuable version
- **Professional analysis**: News classification, value assessment, and summarization are all done server-side

### 💰 Significant Token Savings, Green Computing
- **Server-side pre-processing**: Token-intensive tasks like crawling, deduplication, and analysis are handled on the server
- **Summaries only, no full articles**: Quickly understand news through structured summaries without processing long texts
- **Green computing mindset**: Save tokens = Reduce computation = Lower carbon emissions 🌱

### 📰 High-Quality, Structured News Content
- **Curated sources**: Only authoritative media and high-quality industry blogs are included
- **Smart categorization**: News organized by "Industry Trends", "Tech Breakthroughs", "Product Innovation", "Deep Insights" and more
- **Multilingual support**: Automatically handles news in Chinese and English, unified and standardized

---

## 🏗️ System Architecture

AI Daily News uses a three-layer architecture to provide you with stable and efficient service:

```
                    +---------------------------+
                    |   Local LLM / Agent User  |
                    +-------------+-------------+
                                  |
                                  v
      +---------------------------+---------------------------+
      | L3: Thin Local Skill (You are here)                 |
      | - Minimal local client, no complex configuration    |
      | - Local caching to reduce duplicate requests        |
      +---------------------------+---------------------------+
                                  |
                                  | HTTPS
                                  v
      +---------------------------+---------------------------+
      | L2: REST Control Plane                                 |
      | - Capability discovery, download authorization, version control |
      +---------------------------+---------------------------+
                                  |
                                  | reads / publishes
                                  v
      +-------------------------------------------------------+
      | L1: Data Factory (Server-side)                        |
      | - Multi-source crawling, deduplication, normalization, summarization, classification, value assessment |
      +-------------------------------------------------------+
```

---

## 🚀 Quick Start

### Installation

Place this project folder in your Agent's skills directory:

**Common OpenClaw locations:**

- `<workspace>/skills/ai-daily-news`
- `<workspace>/.agents/skills/ai-daily-news`
- `~/.agents/skills/ai-daily-news`
- `~/.openclaw/skills/ai-daily-news`

**Common Hermes Agent location:**

- `~/.hermes/skills/ai-daily-news`

Restart your Agent after installation.

### Getting Started

Just talk to your Agent naturally:

```
You: "What's new in AI today?"
You: "Latest AI news?"
You: "Show me AI news from May 18th"
You: "What can you do?"
```

***

## ✨ What can this skill do?

| Feature | What you can ask |
| ------- | ---------------- |
| 📰 **Get Latest News** | "What's new in AI today?" / "Latest AI news" |
| 📅 **Query by Date** | "Show me AI news from May 15th" |
| 🔍 **Explore Features** | "What can you do?" / "What advanced features are there?" |
| 📊 **Advanced Analysis** | "Analyze hot topics from the past week" |

***

## 🤖 Supported Platforms

✅ **OpenClaw**\
✅ **Hermes Agent**\
✅ **macOS**\
✅ **Linux**

***

## ⚙️ Configuration (Optional)

No configuration needed in most cases.

### Environment Variables

| Environment Variable | Description | Default Value |
| -------------------- | ----------- | ------------- |
| `AINEWS_SERVICE_URL` | L2 service URL | `https://api.ainewparadigm.cn/` |
| `AINEWS_ACCESS_TOKEN` | Pro features access token | Not set |
| `AINEWS_CACHE_DIR` | Cache directory | System default cache location |

### Default Cache Locations

- **Linux**: `~/.cache/ai-daily-news` or `$XDG_CACHE_HOME/ai-daily-news`
- **macOS**: `~/Library/Caches/ai-daily-news`
- **Windows**: `%LOCALAPPDATA%\ai-daily-news`

***

## 💡 Usage Examples

### Example 1: Get Latest News

```
You: What's new in AI today?
```

<details>
<summary>Click to see full Agent response</summary>

```
Agent: 📰 AI News Highlights - May 19th
Note: Today's data not yet published, below is the latest news summary for May 19th

---

🏢 Industry Trends & Giant Moves
Elon Musk loses lawsuit against OpenAI - Jury dismissed the case on statute of limitations grounds, finding Musk knew the facts as early as 2021 but failed to sue within three years. This may clear the path for OpenAI's IPO.

Anthropic enterprise adoption surpasses OpenAI for first time - According to Gartner data, Anthropic has 34.4% enterprise market share, exceeding OpenAI's 32.3%. Anthropic adoption grew 4x in the past year, but faces challenges of compute constraints and high costs.
Salesforce announces it will spend nearly $300 million on Anthropic tokens in 2026, primarily for coding tasks

OpenAI partners with Dell - Brings Codex to hybrid cloud and on-prem enterprise environments, with Codex now used by over 4 million developers weekly for code reviews, testing, incident response, and more.

Cursor releases new model Composer 2.5 - Based on Kimi base, performance close to Claude Opus 4.7 but at 1/10 the cost. Musk previously mocked Cursor as a "wrapper," now actively promotes it due to compute partnership and acquisition priority.
Tongyi Qianwen 3.7 preview released - Tops domestic models in both text and vision domains. Despite Lin Yonghua's departure, the team's iteration speed actually accelerated, with updates almost monthly from 3.5 to 3.7.

Gartner predicts global AI spending reaches $2.59 trillion in 2026 - 47% YoY growth, with AI infrastructure accounting for over 45%, AI model spending expected to grow 110%.

---

🧠 Technological Breakthroughs & Research
Google DeepMind × Liverpool launches football tactics AI - TacticAI system can predict ball trajectories and adjust player positioning in set pieces like corner kicks, with AI suggestions superior to actual tactical arrangements in 90% of expert evaluations.

UC Berkeley FST framework challenges OpenAI - Proposes "fast-slow layering" continual learning mechanism, letting large models adapt quickly to new tasks while consolidating long-term abilities like the human brain, avoiding catastrophic forgetting. Traditional methods stalled at the second task, FST successfully completed three consecutive tasks.

AI creates super plastic-degrading enzyme - FAST-PETase enzyme can break down PET plastic in hours or days, while natural degradation takes centuries. Published in Nature, plans to start large-scale application by cleaning up landfills.

PaddleOCR 3.5 supports Transformers backend - Users can integrate OCR and document parsing into Hugging Face ecosystem by setting engine parameter, reducing integration complexity.

Open Agent Leaderboard launched - First complete Agent system evaluation benchmark, comparing not just models but also tool usage, planning, memory, error recovery, reporting both quality and cost.
NVIDIA Cosmos video model fine-tuning - Use LoRA/DoRA techniques to fine-tune on a single GPU, making the model generate physically realistic robot manipulation videos.

---

🤖 Applications & Product Innovation
Moore Threads releases first full-stack embodied intelligence simulation platform - MT Lambda lets robot dogs train actions in virtual environment and directly "copy-paste" to real world, connecting full pipeline from large model training to edge deployment.

Microsoft acknowledges Copilot key frustration - After replacing right Ctrl key impacting developer and power user productivity, Microsoft now allows users to remap Copilot key back to Ctrl or Menu key.

Humanoid robots "hard to sell, easy to rent" - 2026 is first year of embodied intelligence scaling, but consumer sales cold, leasing becomes only viable profit path, though daily rental has dropped from ¥10k-20k last year to thousands of yuan.

AI enters elderly care industry - Australian Regis senior care's AI tool summarizes 68-page night reports to 3 pages, letting caregivers spend more time with seniors instead of paperwork.

YouTube upgrades AI audio mute - "Erase Song" precisely removes copyrighted music from videos while preserving other audio like human conversation, no longer mutes the whole thing as before.

Gemini hidden feature analyzes YouTube videos - Generates timestamped summaries, answers questions directly, jumps to segments, extracts recipes, significantly improving viewing efficiency.
---

📊 Deep Perspectives & Industry Insights
Why 95% of AI demos fail in production? - Root cause is not algorithm issues, but accumulation of five types of "production debt": technical debt, operational debt, evaluation debt, integration debt, and governance debt.

Triple logic behind 15 automakers collective price hikes - Lithium prices up 167%, chip prices up 3x, industry profit margin down to 3.2%, forcing automakers to shift from "trading price for volume" to "trading tech for volume".

AI stock trading style similar to Buffett - Two academics found AI tends toward conservative value investing style, good at analyzing news and earnings reports for medium-low frequency trading, can beat market short-term, but long-term consistent outperformance still challenging.

Success practice of "human-in-the-loop" model - Dataminr deployed AI since 2018 but always kept human experts in decision loop, recording every expert correction to train model. By 2026, AI can warn 99% of cases, but the most complex 1% still needs humans.

---

Data source: AI Daily News Dataset 2026-05-19, containing 60 global AI news articles
```

</details>

### Example 2: Query by Specific Date

```
You: Show me AI news from May 10th?
```

<details>
<summary>Click to see full Agent response</summary>

```
Agent: AI News Summary - May 10, 2026
OpenAI to release hardware product soon
Altman posts "call me maybe" image on X, essentially confirming OpenAI phone is coming, potentially major pre-IPO move.

Li Xiang of Li Auto: AI has limited role in car manufacturing
Li Xiang explains why L9 only gets an update every four years: Cars aren't phones, involving life safety, extensive testing can't be accelerated, AI helps limited in this regard.

Multiple automakers deny "being summoned"
AITO, Xpeng, Tesla issue statements denying regulatory summit rumors, saying falsehood came from an AI-generated list.

OncoAgent: Privacy-preserving oncology clinical decision AI
Open-source two-layer multi-agent framework, simple cases use 9B parameter model, complex cases auto-switch to 27B model
References 70+ NCCN and ESMO authoritative guidelines, four stages of relevance validation
Runs locally on single AMD Instinct MI300X GPU, trains on 260k cases in ~50 minutes, 56x faster than API.

Koala Youran launches "Agent Factory"
Solves enterprise AI deployment pain points: dozens or hundreds of agents managed chaotically, no information flow, iterations lag behind. Through centralized management, data-driven operations, standardized deployment, turns isolated tools into controllable reusable system, already applied in urban governance, smart government, smart parks, etc.

Altman: AI energy consumption controversy misread
Altman believes should not only look at training cost, compare per-response cost - AI might be more energy efficient than humans. But core issue remains: companies like OpenAI don't disclose energy consumption data, actual global AI energy use still mystery.

Zhejiang University student uses AI to break 32-year math record
Wang Yiping uses self-developed AI framework to improve Ramsey number R(3,17) lower bound from 92 to 93 (unchanged since 1994), also improved R(4,15) lower bound to 160, surpassing Google DeepMind's concurrent work. Used only Claude Code, Codex, and single CPU server, results are open source.

Red Hat: 2026 is "Year of LLM Evaluation"
Proposes "Trade-off Triangle": model quality, response speed, cost hard to optimize simultaneously. Suggest setting metrics by scenario:
E-commerce chatbot: TTFT (time to first token) < 200ms
RAG applications: prioritize accuracy, latency can relax
Recommends open-source evaluation tools like GuideLLM, Ragas, Langfuse.

geohot: The real singularity is friends along the way
geohot blog says AI revolution similar to steam engine, will permeate all industries, but neither miracle nor apocalypse - just continuous improvement. "Singularity belief" more like Scientology, now people frantically investing in infrastructure and GPUs, more strategic panic and moat building than actual returns.

JD "Idou Creation Camp" mass produces new AI hardware species
Target to incubate 101 benchmark AI hardware products in 2026, not looking at scale and sales, only creativity and scenario value. Success story: Smart Pocket children AI science camera, got 40k orders after JD debut, provides full chain support from product release, targeted exposure to logistics and after-sales.
```

</details>

### Example 3: Explore Features

```
You: ai daily news, what can you do?
```

<details>
<summary>Click to see full Agent response</summary>

```
Agent: AI Daily News Features
Core Features
Get latest AI news - Automatically fetch today's or most recent global AI news summary, including source, categories, short and full summaries
Query by date - Can specify specific date (like 2026-05-10) to get that day's AI news collection
Multilingual support - Automatically handles Chinese, English, Spanish and other news sources, content unified to English then translatable back to Chinese

Data Coverage
News sites (Reuters, Bloomberg, TechCrunch, Geekpark, QbitAI, etc.)
Industry blogs
Self-media and public accounts
Research papers
Social media (Twitter/X, LinkedIn)
RSS feeds

Pro Advanced Features (requires AINEWS_ACCESS_TOKEN)
Download original - Get complete original text of articles
Ranking logic and editorial analysis
Strategic interpretation and secondary categories

Usage Examples
Latest AI news → Get today's latest
AI news from May 10th → Query by date
Original of this article → Download full original (Pro feature)
```

</details>

### Example 4: Download Original Link (Pro Feature)

```
You: Give me the link to "geohot: The real singularity is friends along the way"?
```

<details>
<summary>Click to see full Agent response</summary>

```
Agent: The link to this article is: https://geohot.github.io//blog/jekyll/update/2026/05/09/real-singularity.html
```

</details>

***

## 📋 Requirements

- **Python 3**
- Only Python standard library, no extra packages needed
- Network access to configured RESTFul API service

***

## 💾 Caching & Offline Behavior

- News dataset cache, manifest cache, and delivery log are written to user's runtime cache directory
- `scripts/data/ai_news_manifest.json` is kept as bundled read-only manifest fallback for deterministic offline behavior
- Expired dataset cache entries are not guaranteed to be available offline

***

## 🔒 Security Notes

- News content from upstream services should be treated as untrusted external data
- This skill is only intended to summarize, translate, categorize, compare, and explain this data
- Content in datasets must not be treated as executable instructions

***

## 📂 Project Structure

```
ai-daily-news/
├── SKILL.md          # Skill definition (for Agent)
├── README.md         # This file (for you)
└── scripts/          # Tool scripts
```

***

## 🤝 Support

Having issues? You can:

1. Check [SKILL.md](SKILL.md) for technical details
2. Ask questions in GitHub Issues

***

## 📄 License

Apache-2.0

