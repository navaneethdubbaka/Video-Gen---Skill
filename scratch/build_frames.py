import json
from pathlib import Path

PROJECT = Path(r"e:\Video Gen Skill\videos\smoke-director-short")
FRAMES_DIR = PROJECT / "composition" / "hyperframes" / "compositions" / "frames"
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

FRAMES = [
    {
        "id": "01-swiggy-burstrex-new-feature-launched",
        "dur": 2.76,
        "is_text_only": False,
        "asset": "assets/images/ea92f525735690d7_cec8d10cfe98941d.jpg",
        "badge": "NEW RELEASE",
        "badge_color": "#FC8019",
        "title": "Swiggy Burstrex",
        "subtitle": "new feature launched",
        "emphasis": "Swiggy Burstrex",
        "motion": "pop_scale"
    },
    {
        "id": "02-discontinued-within-days",
        "dur": 2.36,
        "is_text_only": True,
        "badge": "ALERT",
        "badge_color": "#EF4444",
        "title": "discontinued",
        "subtitle": "within a few days",
        "emphasis": "discontinued",
        "motion": "punch_shake"
    },
    {
        "id": "03-no-official-reason-but-we-found-somethin",
        "dur": 5.26,
        "is_text_only": False,
        "asset": "assets/images/5076bcec564057b1_a5afb5def58bfb29.jpg",
        "badge": "INVESTIGATION",
        "badge_color": "#111111",
        "title": "no official reason",
        "subtitle": "but we found something",
        "emphasis": "found something",
        "motion": "float_settle"
    },
    {
        "id": "04-security-issue-found-while-live",
        "dur": 2.78,
        "is_text_only": False,
        "asset": "assets/images/895ad66088f1cb71_e833f7c3c35907fe.jpg",
        "badge": "CRITICAL",
        "badge_color": "#DC2626",
        "title": "security issue",
        "subtitle": "found while live",
        "emphasis": "security issue",
        "motion": "slide_pop"
    },
    {
        "id": "05-every-link-has-a-random-token",
        "dur": 6.44,
        "is_text_only": False,
        "asset": "assets/images/52a0fd7bfefc6dc4_6b52ca0ae5422c24.png",
        "badge": "URL INSPECTION",
        "badge_color": "#3B82F6",
        "title": "every link has a",
        "subtitle": "random token parameter",
        "emphasis": "random token",
        "motion": "float_settle"
    },
    {
        "id": "06-looks-like-a-secured-token",
        "dur": 4.52,
        "is_text_only": False,
        "asset": "assets/images/9fba2d8defbb67d3_dd22220a653e3ec1.png",
        "badge": "FIRST GLANCE",
        "badge_color": "#6B7280",
        "title": "looks like a",
        "subtitle": "secured token at first",
        "emphasis": "secured token",
        "motion": "zoom_float"
    },
    {
        "id": "07-base64-encoding",
        "dur": 4.22,
        "is_text_only": False,
        "asset": "assets/images/24a91d6dca98ba4a_823eabe988d4e622.png",
        "badge": "ANALYSIS REVEAL",
        "badge_color": "#10B981",
        "title": "base64",
        "subtitle": "encoding discovered",
        "emphasis": "base64",
        "motion": "punch_reveal"
    },
    {
        "id": "08-not-encryption-easily-decoded",
        "dur": 5.20,
        "is_text_only": False,
        "asset": "assets/images/f83bfc07bebba4f1_968a8610253d26b4.png",
        "badge": "SECURITY AUDIT",
        "badge_color": "#EF4444",
        "title": "✕ not encryption",
        "subtitle": "✕ easily decoded",
        "emphasis": "not encryption",
        "motion": "line_reveal"
    },
    {
        "id": "09-user-id-name-exposed-in-plaintext",
        "dur": 6.02,
        "is_text_only": False,
        "asset": "assets/images/47f8b8bbfd547fbe_305f9199daba4e10.png",
        "badge": "DATA EXPOSURE",
        "badge_color": "#DC2626",
        "title": "user ID + name",
        "subtitle": "exposed in plaintext",
        "emphasis": "exposed in plaintext",
        "motion": "float_settle"
    },
    {
        "id": "10-1-decode-2-modify-values-3-re-encode",
        "dur": 5.98,
        "is_text_only": False,
        "asset": "assets/images/e34b1f42a10ff616_94b72fbb8c046b0b.png",
        "badge": "EXPLOIT CYCLE",
        "badge_color": "#8B5CF6",
        "title": "the exploit steps",
        "subtitle": "1. decode → 2. modify → 3. re-encode",
        "emphasis": "exploit steps",
        "motion": "slide_pop"
    },
    {
        "id": "11-that-s-exactly-what-we-did",
        "dur": 5.60,
        "is_text_only": False,
        "asset": "assets/images/6b8150f02725c8ba_aeb25bcd81e18e77.png",
        "badge": "TESTING LIVE",
        "badge_color": "#2563EB",
        "title": "that's exactly",
        "subtitle": "what we verified",
        "emphasis": "what we verified",
        "motion": "float_settle"
    },
    {
        "id": "12-link-accepted-still-working",
        "dur": 1.92,
        "is_text_only": False,
        "asset": "assets/images/84ec0f1a3c0882c7_4b9fb9095a98f86a.png",
        "badge": "VERIFIED 200 OK",
        "badge_color": "#10B981",
        "title": "link accepted",
        "subtitle": "still working on server",
        "emphasis": "link accepted",
        "motion": "punch_reveal"
    },
    {
        "id": "13-reported-to-swiggy-details-in-next-part",
        "dur": 6.78,
        "is_text_only": False,
        "asset": "assets/images/e129f134d37d7e80_87e98fc8ceca7536.png",
        "badge": "DISCLOSURE",
        "badge_color": "#111111",
        "title": "reported to Swiggy",
        "subtitle": "details in next part",
        "emphasis": "reported to Swiggy",
        "motion": "float_settle"
    },
    {
        "id": "14-follow-for-more",
        "dur": 2.12,
        "is_text_only": True,
        "badge": "PART 2 SOON",
        "badge_color": "#111111",
        "title": "follow",
        "subtitle": "for more breakdowns",
        "emphasis": "follow",
        "motion": "punch_reveal"
    }
]

def render_frame_html(f, idx):
    fid = f["id"]
    dur = f["dur"]
    is_text = f["is_text_only"]
    prefix = f"f{idx:02d}"
    
    if is_text:
        content_html = f"""
      <div class="{prefix}-badge" id="{prefix}-badge">{f['badge']}</div>
      <div class="{prefix}-text-card" id="{prefix}-card">
        <div id="{prefix}-text">
          <h1 class="{prefix}-title">{f['title']}</h1>
          <p class="{prefix}-subtitle">{f['subtitle']}</p>
        </div>
      </div>
"""
    else:
        # Non-text card with real img
        content_html = f"""
      <div class="{prefix}-sticker-wrap" id="{prefix}-card">
        <div class="{prefix}-badge" id="{prefix}-badge">{f['badge']}</div>
        <div class="{prefix}-img-card">
          <img class="{prefix}-hero-img" src="{f['asset']}" alt="{f['title']}" />
        </div>
      </div>
      <div class="{prefix}-text-card" id="{prefix}-text">
        <h1 class="{prefix}-title">{f['title']}</h1>
        <p class="{prefix}-subtitle">{f['subtitle']}</p>
      </div>
"""

    # Motion script generator
    motion = f["motion"]
    if motion == "pop_scale":
        anim_js = f"""
      tl.from("#{prefix}-card", {{
        scale: 0.6,
        opacity: 0,
        y: 60,
        rotation: -4,
        duration: 0.65,
        ease: "back.out(1.8)"
      }}, 0);
      tl.from("#{prefix}-badge", {{
        scale: 0,
        opacity: 0,
        duration: 0.4,
        ease: "back.out(2)"
      }}, 0.2);
      tl.from("#{prefix}-text", {{
        opacity: 0,
        y: 35,
        duration: 0.5,
        ease: "power3.out"
      }}, 0.3);
      tl.to("#{prefix}-card", {{
        y: -12,
        duration: 1.2,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1
      }}, 0.65);
"""
    elif motion == "punch_shake":
        anim_js = f"""
      tl.from("#{prefix}-card", {{
        scale: 2.2,
        opacity: 0,
        duration: 0.45,
        ease: "power4.out"
      }}, 0);
      tl.from("#{prefix}-badge", {{
        scale: 0,
        opacity: 0,
        duration: 0.35,
        ease: "back.out(2)"
      }}, 0.15);
      tl.to("#{prefix}-card", {{
        x: "+=8",
        yoyo: true,
        repeat: 5,
        duration: 0.05,
        ease: "sine.inOut"
      }}, 0.45);
"""
    elif motion == "float_settle":
        anim_js = f"""
      tl.from("#{prefix}-card", {{
        y: 100,
        opacity: 0,
        scale: 0.9,
        duration: 0.7,
        ease: "power3.out"
      }}, 0);
      tl.from("#{prefix}-badge", {{
        scale: 0,
        opacity: 0,
        duration: 0.4,
        ease: "back.out(2)"
      }}, 0.25);
      tl.from("#{prefix}-text", {{
        opacity: 0,
        y: 40,
        duration: 0.5,
        ease: "power2.out"
      }}, 0.35);
      tl.to("#{prefix}-card", {{
        y: -14,
        duration: 1.6,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1
      }}, 0.7);
"""
    elif motion == "slide_pop":
        anim_js = f"""
      tl.from("#{prefix}-card", {{
        x: -120,
        opacity: 0,
        rotation: -5,
        duration: 0.65,
        ease: "power3.out"
      }}, 0);
      tl.from("#{prefix}-badge", {{
        scale: 0,
        opacity: 0,
        duration: 0.4,
        ease: "back.out(2)"
      }}, 0.2);
      tl.from("#{prefix}-text", {{
        opacity: 0,
        y: 35,
        duration: 0.5,
        ease: "power3.out"
      }}, 0.3);
      tl.to("#{prefix}-card", {{
        y: -10,
        duration: 1.3,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1
      }}, 0.65);
"""
    elif motion == "punch_reveal":
        anim_js = f"""
      tl.from("#{prefix}-card", {{
        scale: 0.7,
        opacity: 0,
        duration: 0.5,
        ease: "back.out(1.8)"
      }}, 0);
      tl.from("#{prefix}-badge", {{
        scale: 0,
        opacity: 0,
        duration: 0.35,
        ease: "back.out(2)"
      }}, 0.15);
      tl.from("#{prefix}-text", {{
        opacity: 0,
        y: 30,
        duration: 0.45,
        ease: "power2.out"
      }}, 0.25);
      tl.to("#{prefix}-card", {{
        scale: 1.02,
        duration: 0.9,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1
      }}, 0.5);
"""
    elif motion == "line_reveal":
        anim_js = f"""
      tl.from("#{prefix}-card", {{
        opacity: 0,
        scale: 0.88,
        y: 70,
        duration: 0.65,
        ease: "power3.out"
      }}, 0);
      tl.from("#{prefix}-badge", {{
        scale: 0,
        opacity: 0,
        duration: 0.4,
        ease: "back.out(2)"
      }}, 0.2);
      tl.from("#{prefix}-text", {{
        opacity: 0,
        y: 40,
        duration: 0.55,
        ease: "power3.out"
      }}, 0.35);
      tl.to("#{prefix}-card", {{
        y: -10,
        duration: 1.4,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1
      }}, 0.65);
"""
    else: # zoom_float
        anim_js = f"""
      tl.from("#{prefix}-card", {{
        scale: 0.8,
        opacity: 0,
        y: 50,
        duration: 0.6,
        ease: "power3.out"
      }}, 0);
      tl.from("#{prefix}-badge", {{
        scale: 0,
        opacity: 0,
        duration: 0.35,
        ease: "back.out(2)"
      }}, 0.2);
      tl.from("#{prefix}-text", {{
        opacity: 0,
        y: 35,
        duration: 0.5,
        ease: "power2.out"
      }}, 0.3);
      tl.to("#{prefix}-card", {{
        y: -12,
        duration: 1.3,
        ease: "sine.inOut",
        yoyo: true,
        repeat: -1
      }}, 0.6);
"""

    return f"""<template id="{fid}-template">
  <div
    data-composition-id="{fid}"
    data-width="1080"
    data-height="1920"
    data-duration="{dur:.2f}"
    id="{prefix}-root"
  >
    <div class="{prefix}-bg"></div>
    <div class="{prefix}-container">
{content_html}
    </div>
  </div>

  <style>
    #{prefix}-root {{
      position: absolute;
      inset: 0;
      width: 1080px;
      height: 1920px;
      background: #F4F4F6;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      overflow: hidden;
    }}
    .{prefix}-bg {{
      position: absolute;
      inset: 0;
      background-image: radial-gradient(#d1d5db 1.5px, transparent 1.5px);
      background-size: 32px 32px;
      opacity: 0.6;
    }}
    .{prefix}-container {{
      position: absolute;
      top: 340px;
      left: 70px;
      right: 70px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 40px;
    }}
    .{prefix}-sticker-wrap {{
      position: relative;
      filter: drop-shadow(0 26px 44px rgba(0,0,0,0.12));
      transform-origin: center center;
      max-width: 940px;
      width: 100%;
    }}
    .{prefix}-badge {{
      position: absolute;
      top: -18px;
      right: 28px;
      background: {f['badge_color']};
      color: #FFFFFF;
      font-size: 22px;
      font-weight: 800;
      letter-spacing: 0.08em;
      padding: 8px 24px;
      border-radius: 999px;
      border: 3px solid #FFFFFF;
      box-shadow: 0 8px 18px rgba(0,0,0,0.14);
      z-index: 10;
    }}
    .{prefix}-img-card {{
      background: #FFFFFF;
      border-radius: 36px;
      padding: 16px;
      border: 6px solid #FFFFFF;
      overflow: hidden;
      display: flex;
      justify-content: center;
      align-items: center;
    }}
    .{prefix}-hero-img {{
      width: 100%;
      height: auto;
      max-height: 820px;
      object-fit: contain;
      border-radius: 24px;
      display: block;
    }}
    .{prefix}-text-card {{
      text-align: center;
      max-width: 900px;
      width: 100%;
    }}
    .{prefix}-title {{
      margin: 0;
      font-size: 72px;
      font-weight: 900;
      line-height: 1.15;
      letter-spacing: -0.03em;
      color: #111111;
      text-transform: uppercase;
    }}
    .{prefix}-subtitle {{
      margin: 14px 0 0 0;
      font-size: 48px;
      font-weight: 600;
      line-height: 1.25;
      color: #52525B;
    }}
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    (function() {{
      var tl = gsap.timeline({{ paused: true }});
{anim_js}
      tl.to({{}}, {{ duration: {dur:.2f} }}, 0);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["{fid}"] = tl;
    }})();
  </script>
</template>
"""

# Generate all 14 frames
for idx, f in enumerate(FRAMES, start=1):
    html_content = render_frame_html(f, idx)
    filename = f"{f['id']}.html"
    filepath = FRAMES_DIR / filename
    filepath.write_text(html_content, encoding="utf-8")
    print(f"Generated frame {idx:02d}: {filename}")

print("\nAll 14 frames built successfully!")
