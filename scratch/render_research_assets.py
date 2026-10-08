import os
from PIL import Image, ImageDraw, ImageFont

scratch_dir = r"E:\Video Gen Skill\scratch\assets"
os.makedirs(scratch_dir, exist_ok=True)

font_regular = "C:\\Windows\\Fonts\\segoeui.ttf"
font_bold = "C:\\Windows\\Fonts\\segoeuib.ttf"
font_mono = "C:\\Windows\\Fonts\\consola.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

f_title = get_font(font_bold, 44)
f_sub = get_font(font_bold, 30)
f_text = get_font(font_regular, 24)
f_text_bold = get_font(font_bold, 24)
f_small = get_font(font_regular, 18)
f_small_bold = get_font(font_bold, 18)
f_mono_large = get_font(font_mono, 32)
f_mono_med = get_font(font_mono, 26)
f_mono_small = get_font(font_mono, 21)

def draw_canvas(bg_color="#F4F4F6"):
    img = Image.new("RGB", (1080, 1080), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Dot grid
    for x in range(20, 1080, 36):
        for y in range(20, 1080, 36):
            draw.ellipse([x, y, x+3, y+3], fill="#D8DAE2")
    return img, draw

def draw_shadow_card(draw, box, radius=36, fill="#FFFFFF", border="#E2E8F0"):
    # Shadow
    for off, col in [(24, "#E2E8F0"), (16, "#CBD5E1"), (8, "#94A3B8")]:
        draw.rounded_rectangle([box[0]+off, box[1]+off, box[2]+off, box[3]+off], radius=radius, fill=col)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=border, width=2)

# ==========================================
# SCENE 5: Browser Address Bar with Token
# ==========================================
def make_scene_5():
    img, draw = draw_canvas()
    box = [70, 160, 1010, 920]
    draw_shadow_card(draw, box, radius=36, fill="#FFFFFF")
    
    # Window header bar
    draw.rounded_rectangle([box[0], box[1], box[2], box[1]+90], radius=36, fill="#F8FAFC")
    draw.rectangle([box[0], box[1]+50, box[2], box[1]+90], fill="#F8FAFC") # square bottom
    draw.line([box[0], box[1]+90, box[2], box[1]+90], fill="#E2E8F0", width=2)
    
    # macOS window dots
    draw.ellipse([110, 200, 128, 218], fill="#EF4444")
    draw.ellipse([142, 200, 160, 218], fill="#F59E0B")
    draw.ellipse([174, 200, 192, 218], fill="#10B981")
    
    draw.text((220, 195), "Burstrex Web Experience", font=f_text_bold, fill="#475569")
    
    # URL bar box
    url_box = [110, 290, 970, 380]
    draw.rounded_rectangle(url_box, radius=20, fill="#F1F5F9", outline="#CBD5E1", width=2)
    # Lock icon
    draw.rounded_rectangle([135, 320, 155, 350], radius=4, fill="#10B981")
    draw.text((170, 316), "https://swiggy.com/burstrex/play?token=", font=f_mono_med, fill="#334155")
    
    # Highlight token container
    tok_box = [110, 420, 970, 620]
    draw.rounded_rectangle(tok_box, radius=24, fill="#FAF5FF", outline="#C084FC", width=3)
    
    draw.rounded_rectangle([135, 440, 280, 475], radius=10, fill="#7C3AED")
    draw.text((150, 445), "TOKEN PARAM", font=f_small_bold, fill="#FFFFFF")
    
    draw.text((135, 500), "eyJ1c2VySWQiOiI3ODQ5MiIs", font=f_mono_large, fill="#6B21A8")
    draw.text((135, 550), "Im5hbWUiOiJTdXNodSJ9...", font=f_mono_large, fill="#6B21A8")
    
    # Metadata badges below
    draw.rounded_rectangle([110, 660, 520, 860], radius=24, fill="#F8FAFC", outline="#E2E8F0", width=2)
    draw.text((140, 690), "PARAMETER PATTERN", font=f_small_bold, fill="#64748B")
    draw.text((140, 725), "Appended to every URL link", font=f_text_bold, fill="#0F172A")
    draw.text((140, 765), "Static query parameter string", font=f_text, fill="#475569")
    draw.text((140, 805), "Length: 52 Characters", font=f_mono_small, fill="#7C3AED")

    draw.rounded_rectangle([560, 660, 970, 860], radius=24, fill="#F8FAFC", outline="#E2E8F0", width=2)
    draw.text((590, 690), "INSPECTION FINDING", font=f_small_bold, fill="#64748B")
    draw.text((590, 725), "Looks like random token", font=f_text_bold, fill="#0F172A")
    draw.text((590, 765), "No server-side signature (HMAC)", font=f_text, fill="#DC2626")
    draw.text((590, 805), "Suspect: Client-only token", font=f_mono_small, fill="#DC2626")

    p = os.path.join(scratch_dir, "scene_05.png")
    img.save(p)
    return p

# ==========================================
# SCENE 6: Secured Token Assumption Card
# ==========================================
def make_scene_6():
    img, draw = draw_canvas()
    box = [110, 150, 970, 930]
    draw_shadow_card(draw, box, radius=36, fill="#FFFFFF")

    # Big lock circle
    draw.ellipse([450, 210, 630, 390], fill="#F1F5F9", outline="#E2E8F0", width=3)
    # Draw padlock shape
    draw.rounded_rectangle([505, 290, 575, 360], radius=12, fill="#0F172A")
    draw.ellipse([515, 250, 565, 305], outline="#0F172A", width=10) # shackle
    draw.ellipse([533, 315, 547, 335], fill="#FFFFFF") # keyhole

    draw.text((540, 420), "COMMON ASSUMPTION", font=f_small_bold, fill="#64748B", anchor="ms")
    draw.text((540, 475), "\"Secured Token\"", font=f_title, fill="#0F172A", anchor="ms")
    
    # False sense of security pill
    draw.rounded_rectangle([320, 510, 760, 560], radius=999, fill="#FEF3C7", outline="#F59E0B", width=2)
    draw.text((540, 535), "FALSE SENSE OF SECURITY", font=f_small_bold, fill="#B45309", anchor="mm")

    # Spec table box
    t_box = [170, 600, 910, 870]
    draw.rounded_rectangle(t_box, radius=24, fill="#0F172A")
    
    draw.text((210, 640), "SURFACE APPEARANCE", font=f_small_bold, fill="#94A3B8")
    draw.text((210, 675), "eyJ1c2VySWQiOiI3ODQ5MiIsIm5hbWUi...", font=f_mono_med, fill="#38BDF8")
    
    draw.line([210, 730, 870, 730], fill="#334155", width=2)
    
    draw.text((210, 760), "PERCEIVED CIPHER:", font=f_small_bold, fill="#94A3B8")
    draw.text((450, 760), "Cryptographic Hash / JWT", font=f_text_bold, fill="#F8FAFC")
    
    draw.text((210, 810), "REALITY CHECK:", font=f_small_bold, fill="#EF4444")
    draw.text((450, 810), "ZERO ENCRYPTION AT ALL", font=f_text_bold, fill="#EF4444")

    p = os.path.join(scratch_dir, "scene_06.png")
    img.save(p)
    return p

# ==========================================
# SCENE 7: Base64 Decode Terminal Function
# ==========================================
def make_scene_7():
    img, draw = draw_canvas()
    box = [70, 160, 1010, 920]
    draw_shadow_card(draw, box, radius=36, fill="#0F172A", border="#1E293B")
    
    # Terminal header bar
    draw.rounded_rectangle([box[0], box[1], box[2], box[1]+80], radius=36, fill="#1E293B")
    draw.rectangle([box[0], box[1]+40, box[2], box[1]+80], fill="#1E293B")
    
    draw.ellipse([110, 195, 126, 211], fill="#EF4444")
    draw.ellipse([140, 195, 156, 211], fill="#F59E0B")
    draw.ellipse([170, 195, 186, 211], fill="#10B981")
    draw.text((540, 203), "bash — base64 analysis — 80x24", font=f_small_bold, fill="#94A3B8", anchor="mm")
    
    # Terminal body
    draw.text((120, 280), "$ echo \"$TOKEN\" | base64 --decode", font=f_mono_large, fill="#A6E3A1")
    draw.text((120, 340), "--------------------------------------------------", font=f_mono_med, fill="#475569")
    
    draw.text((120, 390), "DECODED OUTPUT (ASCII):", font=f_mono_small, fill="#94A3B8")
    draw.text((120, 430), "{\"userId\": \"78492\", \"name\": \"Sushu\"}", font=f_mono_large, fill="#F9E2AF")
    
    draw.text((120, 510), "--------------------------------------------------", font=f_mono_med, fill="#475569")
    draw.text((120, 560), "$ file_format: RFC 4648 Base64 (Standard)", font=f_mono_med, fill="#89B4FA")
    draw.text((120, 605), "$ cipher_detected: NONE (Plain encoding only)", font=f_mono_med, fill="#F38BA8")
    draw.text((120, 650), "$ status: atob() decodes cleanly with 0 errors", font=f_mono_med, fill="#A6E3A1")
    
    # Bottom verdict pill
    v_box = [120, 730, 960, 860]
    draw.rounded_rectangle(v_box, radius=20, fill="#181825", outline="#F38BA8", width=2)
    draw.text((160, 765), "ANALYTICAL CONCLUSION", font=f_small_bold, fill="#F38BA8")
    draw.text((160, 805), "BASE64 ENCODING — NOT ENCRYPTION", font=f_title, fill="#FFFFFF")

    p = os.path.join(scratch_dir, "scene_07.png")
    img.save(p)
    return p

# ==========================================
# SCENE 8: Security Deny List
# ==========================================
def make_scene_8():
    img, draw = draw_canvas()
    box = [90, 150, 990, 930]
    draw_shadow_card(draw, box, radius=36, fill="#FFFFFF")
    
    draw.rounded_rectangle([330, 190, 750, 240], radius=999, fill="#0F172A")
    draw.text((540, 215), "SECURITY AUDIT FINDING", font=f_small_bold, fill="#5EFC8D", anchor="mm")
    
    # Item 1 card
    card1 = [130, 280, 950, 550]
    draw.rounded_rectangle(card1, radius=28, fill="#FEF2F2", outline="#FECACA", width=2)
    # Red X badge
    draw.ellipse([170, 330, 260, 420], fill="#EF4444")
    draw.text((215, 375), "X", font=f_title, fill="#FFFFFF", anchor="mm")
    
    draw.text((290, 335), "NOT ENCRYPTION", font=f_title, fill="#991B1B")
    draw.text((290, 400), "Base64 is a data serialization format, not a cipher.", font=f_text_bold, fill="#1F2937")
    draw.text((290, 445), "Requires no secret key or password to decode.", font=f_text, fill="#4B5563")
    draw.text((290, 490), "Vulnerability Score: CWE-312 (Cleartext Storage)", font=f_mono_small, fill="#DC2626")

    # Item 2 card
    card2 = [130, 600, 950, 870]
    draw.rounded_rectangle(card2, radius=28, fill="#FEF2F2", outline="#FECACA", width=2)
    # Red X badge
    draw.ellipse([170, 650, 260, 740], fill="#EF4444")
    draw.text((215, 695), "X", font=f_title, fill="#FFFFFF", anchor="mm")
    
    draw.text((290, 655), "EASILY DECODED", font=f_title, fill="#991B1B")
    draw.text((290, 720), "Any browser can decode this with atob() instantly.", font=f_text_bold, fill="#1F2937")
    draw.text((290, 765), "Anyone with the link sees the underlying values.", font=f_text, fill="#4B5563")
    draw.text((290, 810), "Attack Effort: Trivial (< 1 second execution)", font=f_mono_small, fill="#DC2626")

    p = os.path.join(scratch_dir, "scene_08.png")
    img.save(p)
    return p

# ==========================================
# SCENE 9: Decoded JSON Payload Card
# ==========================================
def make_scene_9():
    img, draw = draw_canvas()
    box = [80, 160, 1000, 920]
    draw_shadow_card(draw, box, radius=36, fill="#FFFFFF")
    
    draw.text((130, 210), "DECODED TOKEN PAYLOAD", font=f_small_bold, fill="#64748B")
    
    draw.rounded_rectangle([720, 195, 950, 245], radius=999, fill="#DC2626")
    draw.text((835, 220), "CRITICAL LEAK", font=f_small_bold, fill="#FFFFFF", anchor="mm")
    
    # Dark code container
    c_box = [130, 275, 950, 720]
    draw.rounded_rectangle(c_box, radius=24, fill="#0F172A", outline="#1E293B", width=2)
    
    draw.text((170, 310), "{", font=f_mono_large, fill="#94A3B8")
    
    # Highlight row 1: userId
    draw.rounded_rectangle([170, 370, 910, 440], radius=12, fill="#261824", outline="#EF4444", width=2)
    draw.text((200, 390), "\"userId\":", font=f_mono_large, fill="#38BDF8")
    draw.text((370, 390), "\"78492\",", font=f_mono_large, fill="#F87171")
    draw.text((580, 395), "// Raw Account ID", font=f_mono_small, fill="#EF4444")
    
    # Highlight row 2: name
    draw.rounded_rectangle([170, 460, 910, 530], radius=12, fill="#261824", outline="#EF4444", width=2)
    draw.text((200, 480), "\"name\":", font=f_mono_large, fill="#38BDF8")
    draw.text((370, 480), "\"Rahul Sharma\",", font=f_mono_large, fill="#F87171")
    draw.text((680, 485), "// Full Name", font=f_mono_small, fill="#EF4444")
    
    draw.text((200, 560), "\"role\":", font=f_mono_large, fill="#38BDF8")
    draw.text((370, 560), "\"customer\",", font=f_mono_large, fill="#FBBF24")

    draw.text((200, 620), "\"issuedAt\":", font=f_mono_large, fill="#38BDF8")
    draw.text((370, 620), "1728362400", font=f_mono_large, fill="#A6E3A1")
    
    draw.text((170, 670), "}", font=f_mono_large, fill="#94A3B8")
    
    # Bottom summary callout
    draw.rounded_rectangle([130, 755, 950, 875], radius=20, fill="#FEF2F2", outline="#FCA5A5", width=2)
    draw.text((160, 785), "EXPOSURE RISK: Direct Identifiers Plaintext", font=f_text_bold, fill="#991B1B")
    draw.text((160, 825), "User ID and customer full name exposed to anyone viewing the URL.", font=f_text, fill="#7F1D1D")

    p = os.path.join(scratch_dir, "scene_09.png")
    img.save(p)
    return p

# ==========================================
# SCENE 10: 3-Step Exploit Flow Diagram
# ==========================================
def make_scene_10():
    img, draw = draw_canvas()
    box = [80, 150, 1000, 930]
    draw_shadow_card(draw, box, radius=36, fill="#FFFFFF")
    
    draw.rounded_rectangle([350, 190, 730, 240], radius=999, fill="#0F172A")
    draw.text((540, 215), "THE EXPLOIT CHAIN", font=f_small_bold, fill="#FFFFFF", anchor="mm")
    
    # Step 1
    s1 = [130, 270, 950, 420]
    draw.rounded_rectangle(s1, radius=24, fill="#F8FAFC", outline="#E2E8F0", width=2)
    draw.ellipse([160, 310, 220, 370], fill="#0F172A")
    draw.text((190, 340), "1", font=f_title, fill="#FFFFFF", anchor="mm")
    draw.text((250, 310), "DECODE THE TOKEN", font=f_title, fill="#0F172A")
    draw.text((250, 365), "Extract readable JSON plaintext using standard atob()", font=f_text, fill="#64748B")
    
    # Down Arrow 1
    draw.polygon([(540, 455), (525, 435), (555, 435)], fill="#64748B")
    
    # Step 2
    s2 = [130, 470, 950, 620]
    draw.rounded_rectangle(s2, radius=24, fill="#FEF3C7", outline="#FCD34D", width=2)
    draw.ellipse([160, 510, 220, 570], fill="#D97706")
    draw.text((190, 540), "2", font=f_title, fill="#FFFFFF", anchor="mm")
    draw.text((250, 510), "MODIFY TARGET VALUES", font=f_title, fill="#92400E")
    draw.text((250, 565), "Change userId \"78492\" -> \"10001\" (Target Account)", font=f_text_bold, fill="#B45309")

    # Down Arrow 2
    draw.polygon([(540, 655), (525, 635), (555, 635)], fill="#64748B")

    # Step 3
    s3 = [130, 670, 950, 820]
    draw.rounded_rectangle(s3, radius=24, fill="#F8FAFC", outline="#E2E8F0", width=2)
    draw.ellipse([160, 710, 220, 770], fill="#0F172A")
    draw.text((190, 740), "3", font=f_title, fill="#FFFFFF", anchor="mm")
    draw.text((250, 710), "RE-ENCODE AND SEND", font=f_title, fill="#0F172A")
    draw.text((250, 765), "Encode modified JSON back into base64 via btoa()", font=f_text, fill="#64748B")

    draw.text((540, 870), "NO CRYPTOGRAPHIC SIGNATURE TO PREVENT FORGERY", font=f_small_bold, fill="#DC2626", anchor="mm")

    p = os.path.join(scratch_dir, "scene_10.png")
    img.save(p)
    return p

# ==========================================
# SCENE 11: API Testing PoC Console
# ==========================================
def make_scene_11():
    img, draw = draw_canvas()
    box = [70, 160, 1010, 920]
    draw_shadow_card(draw, box, radius=36, fill="#0F172A", border="#1E293B")
    
    # Header bar
    draw.rounded_rectangle([box[0], box[1], box[2], box[1]+80], radius=36, fill="#1E293B")
    draw.rectangle([box[0], box[1]+40, box[2], box[1]+80], fill="#1E293B")
    draw.text((540, 200), "SECURITY POC TEST CLIENT — BURSTREX", font=f_small_bold, fill="#94A3B8", anchor="mm")
    
    # Request Line
    draw.rounded_rectangle([110, 270, 970, 350], radius=16, fill="#111827", outline="#374151", width=2)
    draw.rounded_rectangle([125, 285, 220, 335], radius=10, fill="#2563EB")
    draw.text((172, 310), "POST", font=f_text_bold, fill="#FFFFFF", anchor="mm")
    draw.text((245, 298), "https://swiggy.com/burstrex/api/claim", font=f_mono_med, fill="#F9FAFB")
    
    # Headers & Payload
    draw.text((110, 385), "HEADERS & PAYLOAD SENT:", font=f_small_bold, fill="#94A3B8")
    p_box = [110, 420, 970, 580]
    draw.rounded_rectangle(p_box, radius=16, fill="#111827", outline="#374151", width=2)
    draw.text((135, 440), "X-Burstrex-Token: eyJ1c2VySWQiOiIxMDAwMSIsIm5hbWUiOiJ...", font=f_mono_med, fill="#FBBF24")
    draw.text((135, 490), "User-Agent: SecurityResearch/1.0", font=f_mono_small, fill="#9CA3AF")
    draw.text((135, 530), "Host: swiggy.com", font=f_mono_small, fill="#9CA3AF")
    
    # Response Panel
    draw.text((110, 615), "SERVER RESPONSE:", font=f_small_bold, fill="#94A3B8")
    res_box = [110, 650, 970, 870]
    draw.rounded_rectangle(res_box, radius=20, fill="#064E3B", outline="#059669", width=2)
    
    # 200 OK badge
    draw.rounded_rectangle([140, 680, 320, 735], radius=12, fill="#10B981")
    draw.text((230, 707), "200 OK", font=f_title, fill="#FFFFFF", anchor="mm")
    
    draw.text((350, 695), "Response Time: 118ms · Size: 412B", font=f_text, fill="#A7F3D0")
    
    draw.text((140, 770), "{\"status\": \"success\", \"user_claimed\": true, \"account\": 10001}", font=f_mono_med, fill="#D1FAE5")
    draw.text((140, 820), "TAMPERED TOKEN ACCEPTED WITHOUT REJECTION", font=f_text_bold, fill="#6EE7B7")

    p = os.path.join(scratch_dir, "scene_11.png")
    img.save(p)
    return p

# ==========================================
# SCENE 12: Link Accepted Verified Badge
# ==========================================
def make_scene_12():
    img, draw = draw_canvas()
    box = [110, 150, 970, 930]
    draw_shadow_card(draw, box, radius=36, fill="#FFFFFF")
    
    # Large green checkmark seal
    draw.ellipse([420, 210, 660, 450], fill="#ECFDF5", outline="#A7F3D0", width=4)
    draw.ellipse([450, 240, 630, 420], fill="#10B981")
    
    # White checkmark lines
    draw.line([(500, 330), (530, 365)], fill="#FFFFFF", width=14)
    draw.line([(530, 365), (580, 295)], fill="#FFFFFF", width=14)
    
    # Status text
    draw.text((540, 490), "SERVER RESPONSE", font=f_small_bold, fill="#64748B", anchor="mm")
    draw.text((540, 545), "200 OK — ACCEPTED", font=f_title, fill="#065F46", anchor="mm")
    
    draw.rounded_rectangle([250, 600, 830, 660], radius=999, fill="#D1FAE5", outline="#34D399", width=2)
    draw.text((540, 630), "VULNERABILITY CONFIRMED LIVE", font=f_text_bold, fill="#047857", anchor="mm")

    # Metrics card
    m_box = [180, 700, 900, 870]
    draw.rounded_rectangle(m_box, radius=24, fill="#F8FAFC", outline="#E2E8F0", width=2)
    
    draw.text((220, 735), "Link Status:", font=f_text_bold, fill="#334155")
    draw.text((450, 735), "Active & Resolving", font=f_text, fill="#10B981")
    
    draw.text((220, 780), "Token Integrity Check:", font=f_text_bold, fill="#334155")
    draw.text((540, 780), "BYPASSED (No Signature)", font=f_text_bold, fill="#DC2626")

    draw.text((220, 825), "Arbitrary User ID:", font=f_text_bold, fill="#334155")
    draw.text((540, 825), "ACCEPTED AS VALID", font=f_text_bold, fill="#DC2626")

    p = os.path.join(scratch_dir, "scene_12.png")
    img.save(p)
    return p

# ==========================================
# SCENE 13: Vulnerability Report to Swiggy
# ==========================================
def make_scene_13():
    img, draw = draw_canvas()
    box = [80, 150, 1000, 930]
    draw_shadow_card(draw, box, radius=36, fill="#FFFFFF")
    
    draw.rounded_rectangle([130, 190, 480, 240], radius=999, fill="#0F172A")
    draw.text((305, 215), "RESPONSIBLE DISCLOSURE", font=f_small_bold, fill="#5EFC8D", anchor="mm")
    
    draw.rounded_rectangle([720, 190, 950, 240], radius=999, fill="#DCFCE7", outline="#86EFAC", width=2)
    draw.text((835, 215), "REPORT SUBMITTED", font=f_small_bold, fill="#15803D", anchor="mm")

    # Document header
    draw.text((130, 280), "SECURITY INCIDENT REPORT", font=f_title, fill="#0F172A")
    
    # Meta fields
    fields_box = [130, 350, 950, 520]
    draw.rounded_rectangle(fields_box, radius=20, fill="#F8FAFC", outline="#E2E8F0", width=2)
    
    draw.text((160, 380), "TO:", font=f_text_bold, fill="#64748B")
    draw.text((240, 380), "Swiggy Security & Trust Team", font=f_text_bold, fill="#0F172A")
    
    draw.text((160, 425), "DATE:", font=f_text_bold, fill="#64748B")
    draw.text((240, 425), "Reported Immediately Upon Discovery", font=f_text, fill="#334155")
    
    draw.text((160, 470), "SUBJECT:", font=f_text_bold, fill="#64748B")
    draw.text((260, 470), "Burstrex Token Insecurity & Forgery Vulnerability", font=f_text_bold, fill="#DC2626")

    # Findings summary
    f_box = [130, 550, 950, 770]
    draw.rounded_rectangle(f_box, radius=20, fill="#FEF2F2", outline="#FCA5A5", width=2)
    
    draw.text((160, 580), "REPORT HIGHLIGHTS:", font=f_small_bold, fill="#991B1B")
    draw.text((160, 620), "• Base64 encoding used instead of authenticated token.", font=f_text, fill="#7F1D1D")
    draw.text((160, 660), "• Full user ID and names exposed in plaintext in URLs.", font=f_text, fill="#7F1D1D")
    draw.text((160, 700), "• Server accepts modified client-forged tokens.", font=f_text, fill="#7F1D1D")

    # Bottom Part 2 teaser
    draw.rounded_rectangle([130, 805, 950, 885], radius=20, fill="#0F172A")
    draw.text((540, 845), "FULL DETAILS & RESPONSE IN PART 2", font=f_sub, fill="#FFFFFF", anchor="mm")

    p = os.path.join(scratch_dir, "scene_13.png")
    img.save(p)
    return p

created = []
created.append(make_scene_5())
created.append(make_scene_6())
created.append(make_scene_7())
created.append(make_scene_8())
created.append(make_scene_9())
created.append(make_scene_10())
created.append(make_scene_11())
created.append(make_scene_12())
created.append(make_scene_13())

print(f"Successfully generated {len(created)} assets:")
for c in created:
    print(c)
