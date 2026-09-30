const CONFIG = {
  qa:        { url: "/qa",                     label: "Your question",              hint: "Which is the largest ocean?" },
  explain:   { url: "/explain",                label: "Concept to explain",         hint: "Pythagoras Theorem" },
  quiz:      { url: "/quiz",                   label: "Topic or passage for quiz",  hint: "Pythagoras Theorem" },
  summarize: { url: "/summarize",              label: "Paste a long passage",       hint: "Paste the text you want summarized…" },
  recommend: { url: "/learn/recommendations",  label: "What do you want to learn?", hint: "SQL" },
};

const $ = (id) => document.getElementById(id);
const task = $("task"), input = $("input"), btn = $("submit");
const loader = $("loader"), errorBox = $("error"), resultBox = $("result");

task.addEventListener("change", () => {
  $("input-label").textContent = CONFIG[task.value].label;
  input.placeholder = CONFIG[task.value].hint;
});

// Escape HTML first (safe), then apply tiny markdown formatting.
function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function renderMarkdown(text) {
  const lines = escapeHtml(text).split("\n");
  let html = "", inList = false;
  for (let line of lines) {
    line = line.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/`(.+?)`/g, "<code>$1</code>");
    const bullet = line.match(/^\s*[*-]\s+(.*)/);
    const heading = line.match(/^#{1,4}\s+(.*)/);
    if (bullet) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${bullet[1]}</li>`;
    } else {
      if (inList) { html += "</ul>"; inList = false; }
      if (heading) html += `<h3>${heading[1]}</h3>`;
      else if (line.trim()) html += `<p>${line}</p>`;
    }
  }
  return html + (inList ? "</ul>" : "");
}

function renderQuiz(questions) {
  resultBox.innerHTML = "";
  let score = 0, answered = 0;
  const scoreEl = document.createElement("div");
  scoreEl.className = "score";

  questions.forEach((q, i) => {
    const wrap = document.createElement("div");
    wrap.className = "q";
    const title = document.createElement("p");
    title.textContent = `${i + 1}. ${q.question}`;
    wrap.appendChild(title);
    const fb = document.createElement("div");
    fb.className = "feedback";

    q.options.forEach((opt) => {
      const b = document.createElement("button");
      b.className = "opt";
      b.textContent = opt;
      b.onclick = () => {
        wrap.querySelectorAll(".opt").forEach((x) => {
          x.disabled = true;
          if (x.textContent === q.answer) x.classList.add("correct");
        });
        answered++;
        if (opt === q.answer) { score++; fb.textContent = "✅ Correct!"; }
        else { b.classList.add("wrong"); fb.textContent = `❌ Wrong. Correct answer: ${q.answer}`; }
        if (answered === questions.length) scoreEl.textContent = `Your score: ${score} / ${questions.length} 🎉`;
      };
      wrap.appendChild(b);
    });
    wrap.appendChild(fb);
    resultBox.appendChild(wrap);
  });
  resultBox.appendChild(scoreEl);
}

btn.addEventListener("click", async () => {
  const text = input.value.trim();
  errorBox.classList.add("hidden");
  resultBox.classList.add("hidden");
  if (text.length < 2) { errorBox.textContent = "Please enter some text first."; errorBox.classList.remove("hidden"); return; }

  btn.disabled = true;
  loader.classList.remove("hidden");
  try {
    const res = await fetch(CONFIG[task.value].url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Something went wrong.");
    if (task.value === "quiz") renderQuiz(data.result);
    else resultBox.innerHTML = renderMarkdown(data.result);
    resultBox.classList.remove("hidden");
  } catch (err) {
    errorBox.textContent = err.message;
    errorBox.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    loader.classList.add("hidden");
  }
});
