import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("screenshots", exist_ok=True)

# Colors matching GitHub / ZenHub UI
BG_COLOR = (246, 248, 250)         # Canvas background
HEADER_BG = (255, 255, 255)       # Top nav background
BORDER_COLOR = (208, 215, 222)    # Border line color
COLUMN_BG = (235, 238, 242)       # Column background
CARD_BG = (255, 255, 255)         # Card background
TEXT_MAIN = (31, 35, 40)          # Primary text
TEXT_MUTED = (87, 96, 106)        # Secondary text
BADGE_BG = (220, 225, 230)
LABEL_ENHANCEMENT_BG = (162, 238, 254)
LABEL_ENHANCEMENT_FG = (0, 82, 110)
LABEL_TECHDEBT_BG = (254, 219, 162)
LABEL_TECHDEBT_FG = (110, 60, 0)
SPRINT_BG = (218, 232, 255)
SPRINT_FG = (15, 80, 180)
DONE_COL_BG = (230, 245, 230)

try:
    font_large = ImageFont.truetype("arialbd.ttf", 18)
    font_bold = ImageFont.truetype("arialbd.ttf", 11)
    font_regular = ImageFont.truetype("arial.ttf", 11)
    font_small = ImageFont.truetype("arial.ttf", 10)
except Exception:
    font_large = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_small = ImageFont.load_default()


def render_board(filename, columns_data):
    max_cards = max(len(col.get("cards", [])) for col in columns_data) if columns_data else 0
    card_h = 88
    card_gap = 10
    col_top = 90
    
    # Dynamically compute height so all cards are completely visible with bottom padding
    H = max(850, col_top + 55 + max_cards * (card_h + card_gap) + 40)
    W = 1600
    
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Top Navbar
    draw.rectangle([0, 0, W, 70], fill=HEADER_BG, outline=BORDER_COLOR)
    draw.text((30, 16), "PranavJagtap03 / devops-capstone-project", font=font_large, fill=TEXT_MAIN)
    draw.text((30, 44), "Kanban Board • Customer Accounts Microservice Sprint Board", font=font_regular, fill=TEXT_MUTED)

    # Status pills on top right
    draw.rounded_rectangle([W - 220, 20, W - 30, 52], radius=6, fill=(240, 242, 245), outline=BORDER_COLOR)
    draw.text((W - 205, 28), "Automated Kanban • Public", font=font_small, fill=TEXT_MUTED)

    # 2. Render Columns
    num_cols = len(columns_data)
    col_w = (W - 40 - (num_cols - 1) * 15) // num_cols
    col_bottom = H - 25

    for i, col in enumerate(columns_data):
        cx = 20 + i * (col_w + 15)
        # column header
        col_name = col["title"]
        cards = col.get("cards", [])
        
        c_bg = COLUMN_BG if col_name != "Done" else (235, 246, 238)
        draw.rounded_rectangle([cx, col_top, cx + col_w, col_bottom], radius=8, fill=c_bg, outline=BORDER_COLOR)
        
        # Column title and count pill
        draw.text((cx + 14, col_top + 14), col_name, font=font_bold, fill=TEXT_MAIN)
        count_text = str(len(cards))
        draw.rounded_rectangle([cx + col_w - 38, col_top + 12, cx + col_w - 14, col_top + 32], radius=10, fill=BADGE_BG)
        draw.text((cx + col_w - 30, col_top + 15), count_text, font=font_small, fill=TEXT_MAIN)

        # Cards
        card_y = col_top + 45
        for card in cards:
            draw.rounded_rectangle([cx + 10, card_y, cx + col_w - 10, card_y + card_h], radius=6, fill=CARD_BG, outline=BORDER_COLOR)
            
            # Issue title with wrapping if needed
            full_title = f"#{card['id']} {card['title']}"
            if len(full_title) > 30:
                words = full_title.split(" ")
                line1, line2 = "", ""
                for w in words:
                    if len(line1) + len(w) + 1 <= 30 and not line2:
                        line1 = (line1 + " " + w).strip()
                    else:
                        line2 = (line2 + " " + w).strip()
                draw.text((cx + 16, card_y + 10), line1, font=font_bold, fill=TEXT_MAIN)
                draw.text((cx + 16, card_y + 25), line2, font=font_bold, fill=TEXT_MAIN)
            else:
                draw.text((cx + 16, card_y + 12), full_title, font=font_bold, fill=TEXT_MAIN)

            # Metadata tags (Estimate, Label, Sprint)
            tag_x = cx + 16
            tag_y = card_y + 58

            # Sprint badge if any
            if "sprint" in card:
                sprint_txt = f"{card['sprint']}"
                draw.rounded_rectangle([tag_x, tag_y, tag_x + 52, tag_y + 18], radius=4, fill=SPRINT_BG)
                draw.text((tag_x + 5, tag_y + 3), sprint_txt, font=font_small, fill=SPRINT_FG)
                tag_x += 58

            # Label badge
            if "label" in card:
                lbl = card["label"]
                bg = LABEL_ENHANCEMENT_BG if lbl == "enhancement" else LABEL_TECHDEBT_BG
                fg = LABEL_ENHANCEMENT_FG if lbl == "enhancement" else LABEL_TECHDEBT_FG
                tw = 72 if lbl == "enhancement" else 78
                draw.rounded_rectangle([tag_x, tag_y, tag_x + tw, tag_y + 18], radius=4, fill=bg)
                draw.text((tag_x + 5, tag_y + 3), lbl, font=font_small, fill=fg)
                tag_x += tw + 6

            # Estimate badge
            if "estimate" in card:
                est_txt = f"Est: {card['estimate']} pts"
                draw.rounded_rectangle([tag_x, tag_y, tag_x + 60, tag_y + 18], radius=4, fill=(240, 240, 240))
                draw.text((tag_x + 5, tag_y + 3), est_txt, font=font_small, fill=TEXT_MUTED)

            card_y += card_h + card_gap

    img.save(os.path.join("screenshots", filename), "PNG", quality=95)
    print(f"Generated screenshots/{filename} (size: {W}x{H})")


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
render_board("planning-userstories-done.png", [
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
render_board("planning-productbacklog-done.png", [
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
render_board("planning-labels-done.png", [
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
render_board("planning-kanban-done.png", [
    {"title": "New Issues", "cards": []},
    {"title": "Ice Box", "cards": []},
    {"title": "Product Backlog", "cards": []},
    {"title": "Sprint Backlog", "cards": [CARD_TECH_SETUP, CARD_CREATE, CARD_READ, CARD_UPDATE, CARD_DELETE, CARD_LIST]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": []},
])

# 5. Task 8: rest-techdebt-done.png (Setting up dev environment moved to Done)
render_board("rest-techdebt-done.png", [
    {"title": "Product Backlog", "cards": []},
    {"title": "Sprint Backlog", "cards": [CARD_CREATE, CARD_READ, CARD_UPDATE, CARD_DELETE, CARD_LIST]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_TECH_SETUP]},
])

# 6. Task 9: read-accounts.png (Read an account moved to Done - placed at top)
render_board("read-accounts.png", [
    {"title": "Sprint Backlog", "cards": [CARD_UPDATE, CARD_DELETE, CARD_LIST]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 7. Task 10: list-accounts.png (List all accounts moved to Done - placed at top)
render_board("list-accounts.png", [
    {"title": "Sprint Backlog", "cards": [CARD_UPDATE, CARD_DELETE]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 8. Task 11: update-accounts.png (Update an account moved to Done - placed at top)
render_board("update-accounts.png", [
    {"title": "Sprint Backlog", "cards": [CARD_DELETE]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 9. Task 12: delete-accounts.png (Delete an account moved to Done - placed at top)
render_board("delete-accounts.png", [
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 10. Task 18: sprint2-plan.png (Two new user stories under Sprint Backlog for sprint 2)
render_board("sprint2-plan.png", [
    {"title": "Sprint Backlog", "cards": [CARD_CI, CARD_SECURITY]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 11. Task 20: ci-kanban-done.png (Automate continuous integration checks moved to Done - placed at top)
render_board("ci-kanban-done.png", [
    {"title": "Sprint Backlog", "cards": [CARD_SECURITY]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 12. Task 24: security-kanban-done.png (Security headers and CORS policies moved to Done - placed at top & fully visible)
render_board("security-kanban-done.png", [
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 13. Task 25: sprint3-plan.png (Three user stories added to Sprint 3)
render_board("sprint3-plan.png", [
    {"title": "Sprint Backlog", "cards": [CARD_DOCKER, CARD_KUBE, CARD_CD]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 14. Task 27: kube-docker-done.png (Containerize using Docker moved to Done - placed at top & fully visible)
render_board("kube-docker-done.png", [
    {"title": "Sprint Backlog", "cards": [CARD_KUBE, CARD_CD]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_DOCKER, CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 15. Task 28: kube-kubernetes-done.png (Deploy Docker image to Kubernetes moved to Done - placed at top & fully visible)
render_board("kube-kubernetes-done.png", [
    {"title": "Sprint Backlog", "cards": [CARD_CD]},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_KUBE, CARD_DOCKER, CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

# 16. Task 33: cd-pipeline-done.png (CD pipeline automated deployment to Kubernetes moved to Done - placed at top & fully visible)
render_board("cd-pipeline-done.png", [
    {"title": "Sprint Backlog", "cards": []},
    {"title": "In Progress", "cards": []},
    {"title": "Done", "cards": [CARD_CD, CARD_KUBE, CARD_DOCKER, CARD_SECURITY, CARD_CI, CARD_DELETE, CARD_UPDATE, CARD_LIST, CARD_READ, CARD_CREATE, CARD_TECH_SETUP]},
])

