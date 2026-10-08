---
format: 1080x1920
message: "Swiggy Burstrex security vulnerability exposé — base64 token flaw found and reported"
arc: Hook → Develop → Payoff
audience: short-form viewers
mode: autonomous
language: tel
---

## Frame 1 — Swiggy Burstrex new feature launched

- scene: Hook — Swiggy sticker with new feature reveal (Pattern A)
- duration: 2.76s
- transition_in: cut
- sfx: pop
- status: built
- voiceover: "Recently Swiggy Burstrex అనే కొత్త feature launch చేసింది."
- src: compositions/frames/01-swiggy-burstrex-new-feature-launched.html
- start_s: 0.14
- end_s: 2.9
- visual_type: generated_graphic
- motion: pop_scale_in

Hook — Swiggy sticker with new feature reveal (Pattern A)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/ea92f525735690d7_cec8d10cfe98941d.jpg`

Search: Swiggy app icon sticker cutout white border

## Frame 2 — discontinued within days

- scene: Tension — discontinued quickly (Pattern J kinetic type)
- duration: 2.36s
- transition_in: zoom-through
- sfx: whoosh, hit
- status: built
- voiceover: "But within few days లోనే వాళ్ళు discontinue చేశారు."
- src: compositions/frames/02-discontinued-within-days.html
- start_s: 3.46
- end_s: 5.82
- visual_type: text_only
- motion: punch_in

Tension — discontinued quickly (Pattern J kinetic type)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

## Frame 3 — no official reason but we found something

- scene: Mystery / no official reason — doc card with question mark (Pattern D)
- duration: 5.26s
- transition_in: cut
- sfx: whoosh
- status: built
- voiceover: "Swiggy దీన్ని ఎందుకు discontinue చేశారో officiallyగా ఏమి చెప్పలేదు. And I am not saying this is the reason అని."
- src: compositions/frames/03-no-official-reason-but-we-found-somethin.html
- start_s: 6.14
- end_s: 11.4
- visual_type: generated_graphic
- motion: float_settle

Mystery / no official reason — doc card with question mark (Pattern D)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/5076bcec564057b1_a5afb5def58bfb29.jpg`

Search: official document card with question mark mystery

## Frame 4 — security issue found while live

- scene: Security issue reveal — sticker + alert (Pattern A)
- duration: 2.78s
- transition_in: push-slide LEFT
- sfx: whoosh
- status: built
- voiceover: "But ఈ feature liveలో ఉన్నప్పుడు we found a security issue."
- src: compositions/frames/04-security-issue-found-while-live.html
- start_s: 11.7
- end_s: 14.48
- visual_type: generated_graphic
- motion: pop_scale_in

Security issue reveal — sticker + alert (Pattern A)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/895ad66088f1cb71_e833f7c3c35907fe.jpg`

Search: security shield warning icon red alert sticker

## Frame 5 — every link has a random token

- scene: URL pattern with suspicious token — floating browser card (Pattern C)
- duration: 6.44s
- transition_in: cut
- sfx: whoosh
- status: built
- voiceover: "ఏంటి అంటే ప్రతి Burstrexలో link చివర్లో మనకొక similar pattern కనిపిస్తుంది. Like ఒక random token లాగా."
- src: compositions/frames/05-every-link-has-a-random-token.html
- start_s: 14.76
- end_s: 21.2
- visual_type: generated_graphic
- motion: float_settle

URL pattern with suspicious token — floating browser card (Pattern C)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/52a0fd7bfefc6dc4_6b52ca0ae5422c24.png`

Search: browser URL bar with highlighted token parameter

## Frame 6 — looks like a secured token

- scene: False sense of security — looks like secured token (Pattern J)
- duration: 4.52s
- transition_in: crossfade
- sfx: rise
- status: built
- voiceover: "normalగా చూసినప్పుడు మనకి ఇది just ఒక probably ఒక secured token అనిపించొచ్చు."
- src: compositions/frames/06-looks-like-a-secured-token.html
- start_s: 21.44
- end_s: 25.96
- visual_type: generated_graphic
- motion: zoom_in

False sense of security — looks like secured token (Pattern J)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/9fba2d8defbb67d3_dd22220a653e3ec1.png`

Search: secured token lock credential card

## Frame 7 — base64 encoding

- scene: Reveal — it's just base64 encoding (Pattern B big number/code reveal)
- duration: 4.22s
- transition_in: cut
- sfx: pop
- status: built
- voiceover: "But మనం దీన్ని properగా analyze చేస్తే ఇది base64 encoding అని మనకు తెలుస్తుంది."
- src: compositions/frames/07-base64-encoding.html
- start_s: 26.36
- end_s: 30.58
- visual_type: generated_graphic
- motion: punch_in

Reveal — it's just base64 encoding (Pattern B big number/code reveal)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/24a91d6dca98ba4a_823eabe988d4e622.png`

Search: base64 encoding code terminal decode

## Frame 8 — ✕ not encryption ✕ easily decoded

- scene: Not encryption — deny list (Pattern H)
- duration: 5.20s
- transition_in: blur-crossfade
- sfx: rise
- status: built
- voiceover: "And base64 encoding అనేది any encryption technique కాదు. And దీన్ని మనం easyగా decode చేయగలం."
- src: compositions/frames/08-not-encryption-easily-decoded.html
- start_s: 30.84
- end_s: 36.04
- visual_type: generated_graphic
- motion: line_reveal

Not encryption — deny list (Pattern H)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/f83bfc07bebba4f1_968a8610253d26b4.png`

Search: security checklist deny list icon

## Frame 9 — user ID + name exposed in plaintext

- scene: Shocking decoded data — user ID + name exposed (Pattern C floating card)
- duration: 6.02s
- transition_in: cut
- sfx: whoosh
- status: built
- voiceover: "And surprisingly దీన్ని decode చేస్తే లోపల basically ఒక user ID and name ఉన్నాయి. Something like this."
- src: compositions/frames/09-user-id-name-exposed-in-plaintext.html
- start_s: 36.28
- end_s: 42.3
- visual_type: generated_graphic
- motion: float_settle

Shocking decoded data — user ID + name exposed (Pattern C floating card)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/47f8b8bbfd547fbe_305f9199daba4e10.png`

Search: JSON data card user ID name decoded plaintext

## Frame 10 — 1. decode 2. modify values 3. re-encode

- scene: The exploit — decode, change, re-encode (Pattern H allow/deny list)
- duration: 5.98s
- transition_in: push-slide LEFT
- sfx: whoosh
- status: built
- voiceover: "So theoretically మనం దీన్ని decode చేసి values మార్చవచ్చు. And మళ్ళీ అదే formatలో encode చేయొచ్చు."
- src: compositions/frames/10-1-decode-2-modify-values-3-re-encode.html
- start_s: 42.62
- end_s: 48.6
- visual_type: generated_graphic
- motion: line_reveal

The exploit — decode, change, re-encode (Pattern H allow/deny list)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/e34b1f42a10ff616_94b72fbb8c046b0b.png`

Search: decode modify encode cycle arrows

## Frame 11 — that's exactly what we did

- scene: We tested it — action confirmation (Pattern J kinetic type)
- duration: 5.60s
- transition_in: cut
- sfx: whoosh
- status: built
- voiceover: "And that's exactly what we did. So కొత్త valuesతో ఒక token generate చేసి దాన్ని మేము test చేశాం."
- src: compositions/frames/11-that-s-exactly-what-we-did.html
- start_s: 48.82
- end_s: 54.42
- visual_type: generated_graphic
- motion: punch_in

We tested it — action confirmation (Pattern J kinetic type)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/6b8150f02725c8ba_aeb25bcd81e18e77.png`

Search: API testing client console verifying crafted token

## Frame 12 — link accepted still working

- scene: Shocking result — link accepted (Pattern B big reveal)
- duration: 1.92s
- transition_in: squeeze
- sfx: hit
- status: built
- voiceover: "And that link was still being accepted."
- src: compositions/frames/12-link-accepted-still-working.html
- start_s: 54.68
- end_s: 56.6
- visual_type: generated_graphic
- motion: punch_in

Shocking result — link accepted (Pattern B big reveal)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/84ec0f1a3c0882c7_4b9fb9095a98f86a.png`

Search: green checkmark accepted verified badge

## Frame 13 — reported to Swiggy details in next part

- scene: Reported to Swiggy — doc/paper card (Pattern D)
- duration: 6.78s
- transition_in: cut
- sfx: whoosh
- status: built
- voiceover: "So immediateగా మేము ఏం చేశామంటే Swiggyకి ఈ issue కోసం report చేశాం. And దీని గురించి మనం detailedగా next partలో చూద్దాం."
- src: compositions/frames/13-reported-to-swiggy-details-in-next-part.html
- start_s: 56.8
- end_s: 63.58
- visual_type: generated_graphic
- motion: float_settle

Reported to Swiggy — doc/paper card (Pattern D)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.

Asset: `assets/images/e129f134d37d7e80_87e98fc8ceca7536.png`

Search: bug report document security vulnerability report card

## Frame 14 — follow for more

- scene: CTA — follow (Pattern K dot-grid, no watermark)
- duration: 2.12s
- transition_in: zoom-through
- sfx: hit
- status: built
- voiceover: "And follow for more."
- src: compositions/frames/14-follow-for-more.html
- start_s: 63.76
- end_s: 65.88
- visual_type: text_only
- motion: pop_scale_in

CTA — follow (Pattern K dot-grid, no watermark)

Motion required: GSAP entrance on hero + staggered captions; idle micro-float OK.
