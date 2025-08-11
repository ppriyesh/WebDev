// calculator.js — calculates score and animates the God → Poor indicator

function calculateScore() {
  const followers = parseInt(document.getElementById("followers").value) || 0;
  const engagement = parseFloat(document.getElementById("engagement").value) || 0;
  const posts = parseInt(document.getElementById("posts").value) || 0;
  const niche = document.getElementById("niche").value;
  const quality = parseInt(document.getElementById("quality").value) || 3;
  const verified = document.getElementById("verified").checked;

  // weights
  const followersScore = Math.min(Math.log10(followers + 1) * 40, 300);
  const engagementScore = Math.min((engagement / 10) * 400, 400);
  const postsScore = Math.min(posts * 10, 200);
  const nicheScore = (niche === 'High') ? 100 : (niche === 'Medium') ? 50 : 20;
  const qualityScore = Math.min(quality * 10, 50);
  const verifiedScore = verified ? 50 : 0;

  let total = followersScore + engagementScore + postsScore + nicheScore + qualityScore + verifiedScore;
  total = Math.round(Math.min(total, 1000));

  let tier = 'Nano';
  if (total >= 750) tier = 'Elite';
  else if (total >= 450) tier = 'Pro';
  else if (total >= 200) tier = 'Micro';

  // show result
  const resultBox = document.getElementById('resultBox');
  resultBox.style.display = 'flex';
  resultBox.innerHTML = `
    <div style="text-align:left">
      <div style="color:var(--muted);font-size:0.9rem">Your CREDIFY Score</div>
      <div class="score">${total} <span style="font-size:0.85rem;color:var(--muted)">/ 1000</span></div>
      <div class="tier">${tier}</div>
    </div>
    <div style="text-align:right">
      <button class="btn" id="downloadReport">Download Report</button>
    </div>
  `;

  // animate indicator
  animateIndicator(total);
  // attach download
  document.getElementById('downloadReport').onclick = () => downloadReport(total, tier, {
    followersScore, engagementScore, postsScore, nicheScore, qualityScore, verifiedScore
  });
}

function animateIndicator(score) {
  // score range 0-1000 -> 0-100%
  const pct = (score / 1000) * 100;
  const bar = document.getElementById('indicatorBar');
  const pointer = document.getElementById('pointerDot');

  // pointer left position relative to bar width
  const barWidth = bar.getBoundingClientRect().width;
  const leftPx = (pct / 100) * barWidth;
  // set pointer (with 50% transform to center)
  pointer.style.left = `${leftPx}px`;

  // highlight segment by adding a class
  const segs = Array.from(document.querySelectorAll('.indicator-seg'));
  segs.forEach(s => s.style.opacity = 0.95); // reset
  // Decide segment index:
  // 0: God (>=900), 1: Excellent (700-899), 2: Average (400-699), 3: Low (200-399), 4: Poor (<200)
  let idx = 4;
  if (score >= 900) idx = 0;
  else if (score >= 700) idx = 1;
  else if (score >= 400) idx = 2;
  else if (score >= 200) idx = 3;
  else idx = 4;

  segs.forEach((s,i)=>{
    s.style.opacity = (i === idx) ? 1 : 0.55;
    s.style.transition = 'opacity .4s ease';
  });
}

function downloadReport(total, tier, breakdown) {
  const win = window.open('', '_blank');
  win.document.write(`<pre style="font-family:Arial;padding:20px">
CREDIFY Report

Score: ${total} / 1000
Tier: ${tier}

Breakdown:
Followers: ${Math.round(breakdown.followersScore)}/300
Engagement: ${Math.round(breakdown.engagementScore)}/400
Posts: ${Math.round(breakdown.postsScore)}/200
Niche: ${breakdown.nicheScore}/100
Quality: ${breakdown.qualityScore}/50
Verified: ${breakdown.verifiedScore}/50

Generated: ${new Date().toLocaleString()}
</pre>`);
  win.document.close();
}
