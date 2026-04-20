from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# 页面
@app.get("/", response_class=HTMLResponse)
def home():
    return """（你原来的HTML，不用改）"""

# 🔥 必须加：后端执行逻辑接口
@app.get("/run")
def run():
    # 👉 这里先用简单版本测试
    samples = [
        "BTC短线有反弹迹象，关注突破情况",
        "ETH资金回流，结构偏强",
        "山寨币分化明显，谨慎追高",
        "市场震荡，建议控制仓位",
    ]
    
    return {
        "text": random.choice(samples)
    }
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>行情生成器</title>
<style>
body {
  font-family: -apple-system;
  padding: 20px;
  background: #111;
  color: #eee;
}
button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  margin-top: 10px;
  border-radius: 8px;
  border: none;
}
#runBtn { background: #00c853; color: white; }
#copyBtn { background: #2962ff; color: white; }
#result {
  margin-top: 20px;
  white-space: pre-wrap;
  line-height: 1.5;
  background: #1e1e1e;
  padding: 15px;
  border-radius: 8px;
}
#status {
  margin-top: 10px;
  font-size: 14px;
  color: #aaa;
}
</style>
</head>

<body>

<h2>📈 行情分析</h2>

<button id="runBtn" onclick="run()">生成分析</button>
<button id="copyBtn" onclick="copyText()">一键复制</button>

<div id="status">等待操作</div>
<div id="result">点击“生成分析”</div>

<script>
let lastText = "";

// 调用后端
async function run() {
  const result = document.getElementById("result");
  const status = document.getElementById("status");

  status.innerText = "⏳ 生成中...";
  result.innerText = "";

  try {
    const res = await fetch('/run');
    const data = await res.json();

    lastText = data.text || JSON.stringify(data, null, 2);
    result.innerText = lastText;
    status.innerText = "✅ 生成完成";

  } catch (e) {
    status.innerText = "❌ 请求失败";
  }
}

// 复制功能（兼容 iOS）
function copyText() {
  const status = document.getElementById("status");

  if (!lastText) {
    status.innerText = "⚠️ 没有可复制内容";
    return;
  }

  // 优先使用现代 API
  if (navigator.clipboard) {
    navigator.clipboard.writeText(lastText).then(() => {
      status.innerText = "📋 已复制到剪贴板";
    }).catch(() => {
      fallbackCopy();
    });
  } else {
    fallbackCopy();
  }
}

// 兼容 iOS Safari 的 fallback
function fallbackCopy() {
  const textarea = document.createElement("textarea");
  textarea.value = lastText;
  document.body.appendChild(textarea);
  textarea.select();

  try {
    document.execCommand("copy");
    document.getElementById("status").innerText = "📋 已复制（兼容模式）";
  } catch (err) {
    document.getElementById("status").innerText = "❌ 复制失败，请手动长按复制";
  }

  document.body.removeChild(textarea);
}
</script>

</body>
</html>
"""
