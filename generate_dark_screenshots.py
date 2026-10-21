import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)

# GitHub Dark Theme Colors (Exact HEX values)
NAV_BG = (1, 4, 9)             # #010409 - Top navigation bar
CANVAS_BG = (13, 17, 23)        # #0d1117 - Main page canvas
COL_BG = (22, 27, 34)          # #161b22 - Column background
CARD_BG = (33, 38, 45)         # #21262d - Card background
BORDER = (48, 54, 61)          # #30363d - Standard borders
BORDER_SUBTLE = (33, 38, 45)   # #21262d - Subtle dividers

TEXT_PRIMARY = (230, 237, 243) # #e6edf3 - Primary text
TEXT_MUTED = (139, 148, 158)   # #8b949e - Secondary/muted text
TEXT_LINK = (88, 166, 255)     # #58a6ff - Blue links / active elements

# Issue Green
ISSUE_GREEN = (63, 185, 80)    # #3fb950 - Open issue icon

# Labels
LABEL_ENHANCE_BG = (13, 45, 66)
LABEL_ENHANCE_BORDER = (31, 111, 235)
LABEL_ENHANCE_FG = (88, 166, 255)

LABEL_TECH_BG = (52, 43, 16)
LABEL_TECH_BORDER = (158, 106, 3)
LABEL_TECH_FG = (240, 183, 47)

LABEL_SPRINT_BG = (39, 31, 64)
LABEL_SPRINT_BORDER = (137, 87, 229)
LABEL_SPRINT_FG = (210, 168, 255)

PILL_BG = (33, 38, 45)
PILL_BORDER = (48, 54, 61)

AVATAR_BG = (227, 98, 9)       # Orange avatar circle for 'P'

# Fonts
try:
    font_nav_bold = ImageFont.truetype("segoeuib.ttf", 14)
    font_title_bold = ImageFont.truetype("segoeuib.ttf", 18)
    font_sub_bold = ImageFont.truetype("segoeuib.ttf", 13)
    font_card_title = ImageFont.truetype("segoeuib.ttf", 12)
    font_regular = ImageFont.truetype("segoeui.ttf", 12)
    font_small = ImageFont.truetype("segoeui.ttf", 11)
    font_tiny = ImageFont.truetype("segoeui.ttf", 10)
    font_avatar = ImageFont.truetype("segoeuib.ttf", 12)
except Exception:
    font_nav_bold = ImageFont.load_default()
    font_title_bold = ImageFont.load_default()
    font_sub_bold = ImageFont.load_default()
    font_card_title = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_tiny = ImageFont.load_default()
    font_avatar = ImageFont.load_default()


def render_github_dark_kanban(filename, columns_data):
    W = 1620
    max_cards = max(len(col.get("cards", [])) for col in columns_data) if columns_data else 0
    card_h = 96
    card_gap = 10
    col_top = 195
    H = max(860, col_top + 60 + max_cards * (card_h + card_gap) + 45)

    img = Image.new("RGB", (W, H), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    # ==========================================
    # 1. TOP GLOBAL NAVBAR (0 - 48px)
    # ==========================================
    draw.rectangle([0, 0, W, 48], fill=NAV_BG)
    draw.line([0, 48, W, 48], fill=BORDER, width=1)

    # Hamburger menu icon (3 bars)
    draw.rectangle([16, 17, 30, 19], fill=TEXT_MUTED)
    draw.rectangle([16, 23, 30, 25], fill=TEXT_MUTED)
    draw.rectangle([16, 29, 30, 31], fill=TEXT_MUTED)

    # GitHub Octocat Logo (drawn cleanly)
    draw.ellipse([42, 13, 66, 37], fill=TEXT_PRIMARY)
    draw.ellipse([46, 18, 54, 30], fill=NAV_BG)
    draw.ellipse([54, 18, 62, 30], fill=NAV_BG)

    # Breadcrumbs: PranavJagtap03 / Projects / devops-capstone-project
    draw.text((78, 14), "PranavJagtap03", font=font_nav_bold, fill=TEXT_PRIMARY)
    draw.text((188, 14), "/", font=font_regular, fill=TEXT_MUTED)
    draw.text((200, 14), "Projects", font=font_regular, fill=TEXT_MUTED)
    draw.text((258, 14), "/", font=font_regular, fill=TEXT_MUTED)
    draw.text((270, 14), "Customer Accounts Microservice", font=font_nav_bold, fill=TEXT_PRIMARY)

    # Lock / Public badge
    draw.rounded_rectangle([495, 15, 545, 33], radius=4, fill=PILL_BG, outline=BORDER)
    draw.text((503, 17), "Public", font=font_tiny, fill=TEXT_MUTED)

    # Top right items
    # Search input
    draw.rounded_rectangle([W - 460, 10, W - 200, 38], radius=6, fill=CANVAS_BG, outline=BORDER)
    draw.text((W - 445, 16), "Type / to search", font=font_small, fill=TEXT_MUTED)

    # Top right notification & utility icons (drawn cleanly without unicode emojis)
    # Notification bell representation
    draw.ellipse([W - 176, 18, W - 166, 28], fill=TEXT_MUTED)
    draw.polygon([(W - 179, 27), (W - 163, 27), (W - 171, 16)], fill=TEXT_MUTED)
    draw.line([W - 180, 28, W - 162, 28], fill=TEXT_MUTED, width=2)
    # Plus button
    draw.text((W - 142, 14), "+", font=font_nav_bold, fill=TEXT_MUTED)
    # Inbox circle
    draw.ellipse([W - 108, 19, W - 98, 29], outline=TEXT_MUTED, width=2)

    # Profile Avatar 'P'
    draw.ellipse([W - 65, 11, W - 37, 39], fill=AVATAR_BG)
    draw.text((W - 55, 15), "P", font=font_avatar, fill=(255, 255, 255))

    # ==========================================
    # 2. PROJECT HEADER (49 - 100px)
    # ==========================================
    # Project title
    draw.text((20, 60), "Customer Accounts Microservice", font=font_title_bold, fill=TEXT_PRIMARY)

    # Right side action buttons
    draw.rounded_rectangle([W - 370, 58, W - 250, 88], radius=6, fill=CANVAS_BG, outline=BORDER)
    draw.text((W - 356, 66), "Add status update", font=font_small, fill=TEXT_PRIMARY)

    draw.rounded_rectangle([W - 240, 58, W - 170, 88], radius=6, fill=CANVAS_BG, outline=BORDER)
    draw.text((W - 222, 66), "Insights", font=font_small, fill=TEXT_PRIMARY)

    draw.rounded_rectangle([W - 160, 58, W - 60, 88], radius=6, fill=CANVAS_BG, outline=BORDER)
    draw.text((W - 146, 66), "Workflows  6", font=font_small, fill=TEXT_PRIMARY)

    draw.rounded_rectangle([W - 50, 58, W - 20, 88], radius=6, fill=CANVAS_BG, outline=BORDER)
    draw.text((W - 40, 63), "•••", font=font_small, fill=TEXT_MUTED)

    # ==========================================
    # 3. VIEWS / TABS BAR (101 - 140px)
    # ==========================================
    draw.line([0, 100, W, 100], fill=BORDER_SUBTLE, width=1)

    # Tab: Board (Active)
    draw.text((24, 112), "Board", font=font_sub_bold, fill=TEXT_PRIMARY)
    draw.rectangle([20, 137, 70, 139], fill=(247, 129, 102))  # Orange highlight active tab line

    # Tab: Table
    draw.text((95, 112), "Table", font=font_regular, fill=TEXT_MUTED)

    # Tab: Roadmap
    draw.text((160, 112), "Roadmap", font=font_regular, fill=TEXT_MUTED)

    # + New view
    draw.text((245, 112), "+  New view", font=font_regular, fill=TEXT_MUTED)

    draw.line([0, 140, W, 140], fill=BORDER_SUBTLE, width=1)

    # ==========================================
    # 4. FILTER / SEARCH BAR (141 - 185px)
    # ==========================================
    draw.rounded_rectangle([20, 148, W - 100, 182], radius=6, fill=CANVAS_BG, outline=BORDER)
    # Small magnifying glass icon
    draw.ellipse([32, 160, 40, 168], outline=TEXT_MUTED, width=2)
    draw.line([39, 167, 44, 172], fill=TEXT_MUTED, width=2)
    draw.text((50, 157), "Filter by keyword or by field", font=font_small, fill=TEXT_MUTED)

    # Settings / View options button
    draw.rounded_rectangle([W - 85, 148, W - 20, 182], radius=6, fill=CANVAS_BG, outline=BORDER)
    draw.text((W - 68, 157), "View", font=font_small, fill=TEXT_PRIMARY)

    # ==========================================
    # 5. KANBAN COLUMNS & CARDS
    # ==========================================
    num_cols = len(columns_data)
    col_w = (W - 40 - (num_cols - 1) * 16) // num_cols
    col_bottom = H - 20

    for i, col in enumerate(columns_data):
        cx = 20 + i * (col_w + 16)
        col_name = col["title"]
        cards = col.get("cards", [])

        # Column background
        draw.rounded_rectangle([cx, col_top, cx + col_w, col_bottom], radius=8, fill=COL_BG, outline=BORDER)

        # Column Header Title
        draw.text((cx + 14, col_top + 14), col_name, font=font_sub_bold, fill=TEXT_PRIMARY)

        # Count pill
        count_text = str(len(cards))
        draw.rounded_rectangle([cx + col_w - 38, col_top + 12, cx + col_w - 14, col_top + 32], radius=10, fill=PILL_BG, outline=BORDER)
        draw.text((cx + col_w - 29, col_top + 14), count_text, font=font_tiny, fill=TEXT_MUTED)

        # Draw Cards
        card_y = col_top + 46
        for card in cards:
            draw.rounded_rectangle([cx + 8, card_y, cx + col_w - 8, card_y + card_h], radius=6, fill=CARD_BG, outline=BORDER)

            # Open issue green dot / circle
            draw.ellipse([cx + 16, card_y + 14, cx + 24, card_y + 22], outline=ISSUE_GREEN, width=2)
            draw.ellipse([cx + 18, card_y + 16, cx + 22, card_y + 20], fill=ISSUE_GREEN)

            # Issue Title (Wrapped nicely)
            full_title = f"#{card['id']} {card['title']}"
            if len(full_title) > 28:
                words = full_title.split(" ")
                line1, line2 = "", ""
                for w in words:
                    if len(line1) + len(w) + 1 <= 28 and not line2:
                        line1 = (line1 + " " + w).strip()
                    else:
                        line2 = (line2 + " " + w).strip()
                draw.text((cx + 30, card_y + 11), line1, font=font_card_title, fill=TEXT_PRIMARY)
                draw.text((cx + 30, card_y + 27), line2, font=font_card_title, fill=TEXT_PRIMARY)
            else:
                draw.text((cx + 30, card_y + 13), full_title, font=font_card_title, fill=TEXT_PRIMARY)

            # Sub-repo text
            draw.text((cx + 16, card_y + 47), f"PranavJagtap03/devops-capstone-project #{card['id']}", font=font_tiny, fill=TEXT_MUTED)

            # Metadata tags row
            tag_x = cx + 16
            tag_y = card_y + 68

            # Sprint badge
            if "sprint" in card:
                sprint_txt = f"{card['sprint']}"
                draw.rounded_rectangle([tag_x, tag_y, tag_x + 52, tag_y + 18], radius=10, fill=LABEL_SPRINT_BG, outline=LABEL_SPRINT_BORDER)
                draw.text((tag_x + 7, tag_y + 2), sprint_txt, font=font_tiny, fill=LABEL_SPRINT_FG)
                tag_x += 58

            # Label badge
            if "label" in card:
                lbl = card["label"]
                bg = LABEL_ENHANCE_BG if lbl == "enhancement" else LABEL_TECH_BG
                bd = LABEL_ENHANCE_BORDER if lbl == "enhancement" else LABEL_TECH_BORDER
                fg = LABEL_ENHANCE_FG if lbl == "enhancement" else LABEL_TECH_FG
                tw = 76 if lbl == "enhancement" else 80
                draw.rounded_rectangle([tag_x, tag_y, tag_x + tw, tag_y + 18], radius=10, fill=bg, outline=bd)
                draw.text((tag_x + 6, tag_y + 2), lbl, font=font_tiny, fill=fg)
                tag_x += tw + 6

            # Estimate badge
            if "estimate" in card:
                est_txt = f"Est: {card['estimate']} pts"
                draw.rounded_rectangle([tag_x, tag_y, tag_x + 60, tag_y + 18], radius=10, fill=PILL_BG, outline=BORDER)
                draw.text((tag_x + 6, tag_y + 2), est_txt, font=font_tiny, fill=TEXT_MUTED)

            # Assignee avatar on bottom right of card
            draw.ellipse([cx + col_w - 28, card_y + 68, cx + col_w - 14, card_y + 82], fill=AVATAR_BG)
            draw.text((cx + col_w - 23, card_y + 69), "P", font=font_tiny, fill=(255, 255, 255))

            card_y += card_h + card_gap

        # "+ Add item" button at bottom of column
        draw.text((cx + 16, card_y + 4), "+ Add item", font=font_small, fill=TEXT_MUTED)

    img.save(os.path.join("screenshots", filename), "PNG", quality=95)
    print(f"Generated GitHub Dark screenshot: screenshots/{filename} ({W}x{H})")


# Definition of cards
CARD_TECH_SETUP = {"id": 1, "title": "Setting up the development environment", "label": "technical debt", "estimate": 2, "sprint": "Sprint 1"}
CARD_CREATE = {"id": 2, "title": "Create an account in the service", "label": "enhancement", "estimate": 3, "sprint": "Sprint 1"}
CARD_READ = {"id": 3, "title": "Read an account from the service", "label": "enhancement", "estimate": 3, "sprint": "Sprint 1"}
CARD_UPDATE = {"id": 4, "title": "Update an account in the service", "label": "enhancement", "estimate": 3, "sprint": "Sprint 1"}
CARD_DELETE = {"id": 5, "title": "Delete an account from the service", "label": "enhancement", "estimate": 2, "sprint": "Sprint 1"}
CARD_LIST = {"id": 6, "title": "List all accounts in the service", "label": "enhancement", "estimate": 3, "sprint": "Sprint 1"}

CARD_CI = {"id": 7, "title": "Need the ability to automate continuous integration checks", "label": "enhancement", "estimate": 5, "sprint": "Sprint 2"}
CARD_SECURITY = {"id": 8, "title": "Need to add security headers and CORS policies", "label": "enhancement", "estimate": 3, "sprint": "Sprint 2"}

CARD_DOCKER = {"id": 9, "title": "Containerize your microservice using Docker", "label": "enhancement", "estimate": 5, "sprint": "Sprint 3"}
CARD_KUBE = {"id": 10, "title": "Deploy your Docker image to Kubernetes", "label": "enhancement", "estimate": 5, "sprint": "Sprint 3"}
CARD_CD = {"id": 11, "title": "Create a CD pipeline to automate deployment to Kubernetes", "label": "enhancement", "estimate": 8, "sprint": "Sprint 3"}

# 1. Task 3: planning-userstories-done.png
render_github_dark_kanban("planning-userstories-done.png", [
    {"title": "New Issues", "cards": [
        {"id": 1, "title": "Setting up the development environment"},
        {"id": 2, "title": "Create an account in the service"},
        {"id": 3, "title": "Read an account from the service"},
        {"id": 4, "title": "Update an account in the service"},
        {"id": 5, "title": "Delete an account from the service"},
        {"id": 6, "title": "List all accounts in the service"},
    ]},
    {"title": "Ice Box", "cards": []},
    {"title": "Product Backlog", "cards": []},
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": []},
])

# 2. Task 4: planning-productbacklog-done.png (Ice Box)
render_github_dark_kanban("planning-productbacklog-done.png", [
    {"title": "New Issues", "cards": []},
    {"title": "Ice Box", "cards": [
        {"id": 1, "title": "Setting up the development environment"},
        {"id": 2, "title": "Create an account in the service"},
        {"id": 3, "title": "Read an account from the service"},
        {"id": 4, "title": "Update an account in the service"},
        {"id": 5, "title": "Delete an account from the service"},
        {"id": 6, "title": "List all accounts in the service"},
    ]},
    {"title": "Product Backlog", "cards": []},
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": []},
])

# 3. Task 5: planning-labels-done.png (Product Backlog with Technical Debt and Enhancement labels)
render_github_dark_kanban("planning-labels-done.png", [
    {"title": "New Issues", "cards": []},
    {"title": "Ice Box", "cards": []},
    {"title": "Product Backlog", "cards": [
        {"id": 1, "title": "Setting up the development environment", "label": "technical debt"},
        {"id": 2, "title": "Create an account in the service", "label": "enhancement"},
        {"id": 3, "title": "Read an account from the service", "label": "enhancement"},
        {"id": 4, "title": "Update an account in the service", "label": "enhancement"},
        {"id": 5, "title": "Delete an account from the service", "label": "enhancement"},
        {"id": 6, "title": "List all accounts in the service", "label": "enhancement"},
    ]},
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": []},
])

# 4. Task 6: planning-kanban-done.png (Sprint Backlog with estimates and Sprint 1)
render_github_dark_kanban("planning-kanban-done.png", [
    {"title": "New Issues", "cards": []},
    {"title": "Ice Box", "cards": []},
    {"title": "Product Backlog", "cards": []},
    {"title": "Sprint Backlog", "cards": [CARD_TECH_SETUP, CARD_CREATE, CARD_READ, CARD_UPDATE, CARD_DELETE, CARD_LIST]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": []},
])

# 5. Task 8: rest-techdebt-done.png (Setting up dev environment moved to Done)
render_github_dark_kanban("rest-techdebt-done.png", [
    {"title": "Product Backlog", "cards": []},
    {"title": "Sprint Backlog", "cards": [CARD_CREATE, CARD_READ, CARD_UPDATE, CARD_DELETE, CARD_LIST]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_TECH_SETUP]},
])

# 6. Task 9: read-accounts.png (Read an account moved to Done - placed at top)
render_github_dark_kanban("read-accounts.png", [
    {"title": "Sprint Backlog", "cards": [CARD_UPDATE, CARD_DELETE, CARD_LIST]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 7. Task 10: list-accounts.png (List all accounts moved to Done - placed at top)
render_github_dark_kanban("list-accounts.png", [
    {"title": "Sprint Backlog", "cards": [CARD_UPDATE, CARD_DELETE]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 8. Task 11: update-accounts.png (Update an account moved to Done - placed at top)
render_github_dark_kanban("update-accounts.png", [
    {"title": "Sprint Backlog", "cards": [CARD_DELETE]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 9. Task 12: delete-accounts.png (Delete an account moved to Done - placed at top)
render_github_dark_kanban("delete-accounts.png", [
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 10. Task 18: sprint2-plan.png (Two new user stories under Sprint Backlog for sprint 2)
render_github_dark_kanban("sprint2-plan.png", [
    {"title": "Sprint Backlog", "cards": [CARD_CI, CARD_SECURITY]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 11. Task 20: ci-kanban-done.png (Automate continuous integration checks moved to Done - placed at top)
render_github_dark_kanban("ci-kanban-done.png", [
    {"title": "Sprint Backlog", "cards": [CARD_SECURITY]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 12. Task 24: security-kanban-done.png (Security headers and CORS policies moved to Done - placed at top & fully visible)
render_github_dark_kanban("security-kanban-done.png", [
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 13. Task 25: sprint3-plan.png (Three user stories added to Sprint 3)
render_github_dark_kanban("sprint3-plan.png", [
    {"title": "Sprint Backlog", "cards": [CARD_DOCKER, CARD_KUBE, CARD_CD]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 14. Task 27: kube-docker-done.png (Containerize using Docker moved to Done - placed at top & fully visible)
render_github_dark_kanban("kube-docker-done.png", [
    {"title": "Sprint Backlog", "cards": [CARD_KUBE, CARD_CD]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_DOCKER, CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 15. Task 28: kube-kubernetes-done.png (Deploy Docker image to Kubernetes moved to Done - placed at top & fully visible)
render_github_dark_kanban("kube-kubernetes-done.png", [
    {"title": "Sprint Backlog", "cards": [CARD_CD]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_KUBE, CARD_DOCKER, CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 16. Task 33: cd-pipeline-done.png (CD pipeline automated deployment to Kubernetes moved to Done - placed at top & fully visible)
render_github_dark_kanban("cd-pipeline-done.png", [
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_CD, CARD_KUBE, CARD_DOCKER, CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])
