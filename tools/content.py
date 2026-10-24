"""Page content. Edit here, then run: python3 tools/build.py

Amazon work is described in generic terms only: no internal project, system, partner,
business or marketplace names, and no metrics.
"""

GITHUB = "https://github.com/homeo26"
LINKEDIN = "https://linkedin.com/in/homeo"
CODEFORCES = "https://codeforces.com/profile/homeo"
LEETCODE = "https://leetcode.com/u/homeo/"
EMAIL = "homam.manasra26@gmail.com"

# The first stat is highlighted.
HERO_STATS = [
    ("10M+", 10, "M+", "Customers whose traffic my projects handle"),
    ("100+", 100, "+", "Features & projects serving users"),
    ("3+", 3, "+", "Years shipping software"),
    ("2nd", 2, "nd", "Of 5,000+ in Amazon's internal coding contest"),
]
ROLE_TITLE = "Software Development Engineer"
TAGLINE = "I deliver software solutions, from backend services to Android, iOS and web apps. At Amazon, I build payment systems."
LOCATION = "Amman, Jordan"

# Logos that circle the portrait.
ORBIT = ["openjdk", "kotlin", "typescript", "react", "python", "springboot", "aws", "android", "cplusplus", "firebase"]

EXPERIENCE = [
    {
        "art": "pay",
        "dates": ("2024-05", "May 2024", None, "Present"),
        "role": "Software Development Engineer",
        "org": "Amazon",
        "where": "Amman, Jordan · Full-time",
        "summary": "Payments engineering across the checkout stack: backend payment services, payment data, "
                   "and the payment UI customers see on web and in the app.",
        "years": {
            "2026": [
                "Built a centralized payment-data system: the SDK, event processors that stay correct under concurrent "
                "writes and duplicate or out-of-order delivery, backfill tooling, dashboards and alarms. Its data feeds "
                "payment-method recommendations at checkout.",
                "Built an internal console for exploring payment data, with an LLM-powered analyzer that summarizes any "
                "record on demand.",
                "Shipped new payment-method patterns on a cross-platform payments UI: an auto-applied method that customers "
                "can't toggle, and bank accounts with SWIFT/BIC capture, each through design review with the platform team.",
                "Built an MCP server that turns change-management authoring into a natural-language workflow for the team.",
            ],
            "2025": [
                "Moved add-a-card and payment-selection experiences onto a new cross-platform payments UI across desktop, "
                "mobile web and the native app.",
                "Added right-to-left (Arabic) support to the platform's web and native widgets.",
                "Designed marketplace-aware card-brand detection for co-branded and local card networks; the platform "
                "adopted the design.",
                "Rolled out contactless NFC card features and wrote the rollout runbooks other marketplaces reuse.",
                "Added local card-network support for central-bank requirements, inline CVV collection, and a logging "
                "migration to CloudWatch.",
            ],
            "2024": [
                "Led an end-to-end security review of a payments application handling critical data, including "
                "cryptography upgrades with an external partner.",
                "Launched card-on-file checkout and risk-based 3DS authentication for new businesses.",
                "Rebuilt customer payment emails on a new notification platform and templating system.",
                "Added new banks to bank-transfer payments, and wrote the team's first consolidated documentation for a "
                "payments area it took over.",
            ],
        },
        "also": "Throughout: on-call for live payment systems, code reviews, and mentoring teammates and interns.",
        "tags": ["openjdk", "kotlin", "typescript", "reactnative", "aws", "dynamodb"],
    },
    {
        "art": "ci",
        "dates": ("2023-07", "Jul 2023", "2024-01", "Jan 2024"),
        "role": "Software Development Engineer Intern",
        "org": "Amazon",
        "where": "Amman, Jordan",
        "summary": "Joined the payments team while finishing my degree, and returned full-time after graduating. "
                   "Worked on CI/CD pipelines, integration testing and operational monitoring on AWS.",
        "tags": ["openjdk", "aws", ("stream", "CI/CD")],
    },
    {
        "art": "phone",
        "dates": ("2020-10", "Oct 2020", "2023-06", "Jun 2023"),
        "role": "Support Engineer",
        "org": "Hi Phone Cooperation",
        "where": "Irbid, Jordan",
        "summary": "Built the accessories inventory database (Python, SQLite) and the company's repair-services website. "
                   "Ran Google and Facebook ad campaigns that raised qualified leads by 20%.",
        "tags": ["python", "sqlite", "html5", "css"],
    },
    {
        "art": "cap",
        "dates": ("2020-10", "Oct 2020", "2024-09", "Sep 2024"),
        "role": "B.Sc. Software Engineering",
        "org": "Jordan University of Science and Technology",
        "where": "Irbid, Jordan",
        "summary": "Member of the JUST Programming Chapter. Delivered competitive programming training to 100+ students.",
        "tags": ["cplusplus", "openjdk", "python", ("tree", "Algorithms")],
    },
]

FOCUS = [
    ("card", "f-pay", "Payments", "Card, bank-transfer, refund and wallet flows. Third-party gateway integrations, 3DS "
     "authentication, local card networks."),
    ("stream", "f-stream", "Event-driven data", "Idempotent, concurrency-safe processing of high-volume event streams, "
     "with ordering and duplicate delivery handled explicitly."),
    ("shield", "f-shield", "Security", "Security reviews, threat modeling and cryptography for money-movement flows."),
    ("devices", "f-devices", "Full-stack & mobile", "Java and TypeScript services, React and React Native frontends, "
     "native Android, infrastructure as code."),
]

FEATURED = {
    "title": "Robou3 Al-Naserah",
    "kicker": "Business platform · Web + iOS + Android",
    "desc": "Online catalog for a packaging-supply business in Amman. An Arabic right-to-left website, a customer app "
            "and an admin app share one Firestore database, with no backend server; Firestore security rules do the "
            "authorization.",
    "points": [
        ("globe", "Website", "Vanilla TypeScript, server-rendered product pages, hosted on Netlify."),
        ("phone", "Customer app", "React Native with Expo: catalog, cart, push notifications, dark mode."),
        ("lock", "Admin app", "Product and category management with drag-to-reorder, plus a notification composer."),
    ],
    "tags": ["typescript", "reactnative", "expo", "firebase", "netlify", "html5"],
    "site": "https://nasrapack.com",
    "fallback": "https://lawazempack.netlify.app",  # used if the custom domain doesn't answer
    "logo": "assets/logo-robou3.webp",
    "desktop": ("assets/shots/nasrapack-desktop.webp", 1200, 750, "Robou3 Al-Naserah website on desktop"),
    "phones": [
        ("assets/shots/nasrapack-phone.webp", 360, 779, "Website on a phone"),
        ("assets/shots/lzapp-home.webp", 360, 802, "Customer app home"),
        ("assets/shots/lzapp-products.webp", 360, 802, "Customer app product list"),
        ("assets/shots/lzadmin-products.webp", 360, 802, "Admin app product management"),
    ],
}

# media: ("art", name) | ("phones", [(src, w, h, alt), ...]) | ("browser", (src, w, h, alt))
PROJECTS = [
    {"repo": "byd-split-launcher", "cat": "android", "kicker": "Android · Automotive",
     "desc": "Side-by-side split-screen for BYD DiLink car head units. No root, no laptop, about 16 KB.",
     "tags": ["openjdk", "android", ("devices", "Multi-window")], "media": ("art", "split")},
    {"repo": "byd-dashvoice", "cat": "android", "kicker": "Android · Automotive",
     "desc": "Offline English voice control for the BYD climate system. Vosk speech recognition drives the car's "
             "hardware API directly, with no root and no platform signature.",
     "tags": ["openjdk", "android", ("mic", "Vosk")], "media": ("art", "voice")},
    {"repo": "vid-shrink", "cat": "android", "kicker": "Android",
     "desc": "Shrinks large videos in place with the phone's hardware HEVC encoder. Verified replacement, idempotent "
             "re-runs, no Gradle, about 66 KB.",
     "tags": ["openjdk", "android", ("film", "MediaCodec")],
     "showcase": {"phones": [("assets/shots/vidshrink-main.webp", 360, 801, "vid-shrink main screen"), ("assets/shots/vidshrink-scan.webp", 360, 801, "vid-shrink scanning for large videos"),
                             ("assets/shots/vidshrink-progress.webp", 360, 801, "vid-shrink encoding progress")]},
     "media": ("phones", [("assets/shots/vidshrink-main.webp", 360, 801, "vid-shrink main screen"),
                          ("assets/shots/vidshrink-scan.webp", 360, 801, "vid-shrink scanning for large videos"),
                          ("assets/shots/vidshrink-progress.webp", 360, 801, "vid-shrink encoding progress")])},
    {"repo": "vac", "cat": "tools", "kicker": "CLI · PyPI · Homebrew",
     "desc": "Cleans, prunes, archives and repairs AI coding-agent session logs for Kiro CLI and Claude Code, fixing "
             "sessions wedged by oversized payloads.",
     "tags": ["python", "pypi", "homebrew", "githubactions"], "media": ("art", "vac")},
    {"repo": "coup-game", "cat": "mobile", "kicker": "iOS · Android",
     "desc": "The bluffing card game Coup, online for 2–6 players with 4-letter room codes, plus offline bots. Arabic "
             "and English, no server.",
     "tags": ["reactnative", "expo", "firebase", "typescript"],
     "showcase": {"phones": [("assets/shots/coup-home.webp", 360, 801, "Coup home screen"), ("assets/shots/coup-lobby.webp", 360, 801, "Coup lobby with a room code"),
                             ("assets/shots/coup-table.webp", 360, 801, "Coup game table"), ("assets/shots/coup-arabic.webp", 360, 801, "Coup in Arabic")]},
     "media": ("phones", [("assets/shots/coup-home.webp", 360, 801, "Coup home screen"),
                          ("assets/shots/coup-table.webp", 360, 801, "Coup game table"),
                          ("assets/shots/coup-arabic.webp", 360, 801, "Coup in Arabic")])},
    {"repo": "roojifeel", "cat": "mobile", "kicker": "iOS · Android",
     "desc": "A private feelings journal built on the feelings wheel. Entries stay on the device.",
     "tags": ["reactnative", "expo", "sqlite", "typescript"],
     "showcase": {"phones": [("assets/shots/rooji-wheel.webp", 360, 780, "Feelings wheel"), ("assets/shots/rooji-home.webp", 360, 780, "Journal home"),
                             ("assets/shots/rooji-stats.webp", 360, 780, "Mood statistics"), ("assets/shots/rooji-log.webp", 360, 780, "Logging a feeling")]},
     "media": ("phones", [("assets/shots/rooji-wheel.webp", 360, 780, "Feelings wheel"),
                          ("assets/shots/rooji-home.webp", 360, 780, "Journal home"),
                          ("assets/shots/rooji-stats.webp", 360, 780, "Mood statistics")])},
    {"repo": "green-branch", "cat": "web", "kicker": "Web · Arabic RTL",
     "desc": "Arabic agriculture content platform: categorized guides, a video library that pulls the latest channel "
             "videos automatically, and consultation requests.",
     "tags": ["nextdotjs", "typescript", "tailwindcss", "framer"], "live": "https://greenbranchs.com",
     "fallback": "https://greenbranchs.netlify.app",
     "showcase": {"desktop": ("assets/shots/greenbranch-desktop.webp", 1200, 750, "Green Branch website on desktop"), "url": "greenbranchs.com",
                  "phones": [("assets/shots/greenbranch-phone.webp", 360, 779, "Green Branch home on a phone"),
                             ("assets/shots/greenbranch-articles-phone.webp", 360, 779, "Green Branch articles on a phone"),
                             ("assets/shots/greenbranch-videos-phone.webp", 360, 779, "Green Branch video library on a phone")]},
     "media": ("site", (("assets/shots/greenbranch-desktop.webp", 1200, 750, "Green Branch website on desktop"),
                        ("assets/shots/greenbranch-phone.webp", 360, 779, "Green Branch website on a phone")))},
    {"repo": "mashoora", "cat": "web", "kicker": "Web · Legal tech",
     "desc": "Legal consultation platform: paid private chat with lawyers, public legal Q&A, an AI legal chatbot and "
             "provider ratings.",
     "tags": ["springboot", "flask", "postgresql", "firebase"], "media": ("art", "legal"),
     "showcase": {"desktop": ("assets/shots/mashoora-diagram.webp", 1400, 801, "Mashoora class diagram"), "url": "github.com/homeo26/mashoora"}},
    {"repo": "engagement-carpool", "cat": "web", "kicker": "Web · Local-first",
     "desc": "Plans event carpools: assign guests to cars, track confirmations, export to PDF. Auto-saves to YAML, no "
             "database.",
     "tags": ["javascript", "yaml", ("pdf", "PDF export")], "media": ("art", "carpool")},
    {"repo": "bloomberg-data-warehouse-progresssoft", "name": "fx-data-warehouse", "cat": "data", "kicker": "Backend · Data",
     "desc": "FX deals warehouse modeled on Bloomberg's. Validates each row, rejects duplicate imports and persists "
             "without rollback.",
     "tags": ["springboot", "postgresql", "docker"],
     "showcase": {"desktop": ("assets/shots/fx-console.webp", 1200, 572, "FX data warehouse console output"), "url": "github.com/homeo26/fx-data-warehouse",
                  "overlay": ("assets/shots/fx-test1.webp", 900, 548, "FX data warehouse test case")},
     "media": ("browser", ("assets/shots/fx-banner.webp", 1200, 262, "FX data warehouse banner"))},
    {"repo": "Machine-learning-on-online-education-", "name": "grade-prediction", "cat": "data", "kicker": "Machine learning",
     "desc": "Predicts student grades on an online education platform from 20+ features, with cleaning, encoding, "
             "scaling and sampling.",
     "tags": ["python", "pandas", "scikitlearn", "jupyter"], "media": ("art", "scatter")},
    {"repo": "levelic-tree-cipher", "cat": "data", "kicker": "Algorithms",
     "desc": "A cipher that encodes text into a perfect tree; the key is the number of children per node.",
     "tags": ["cplusplus", ("tree", "Trees")], "media": ("art", "tree")},
]

# Order of the auto-advancing project spotlight (Robou3 Al-Naserah is always first).
SPOTLIGHT = ["green-branch", "coup-game", "roojifeel", "vid-shrink", "byd-split-launcher", "byd-dashvoice", "vac", "mashoora",
             "engagement-carpool", "bloomberg-data-warehouse-progresssoft", "Machine-learning-on-online-education-",
             "levelic-tree-cipher"]

FILTERS = [("all", "All"), ("android", "Android"), ("mobile", "Mobile"), ("web", "Web"), ("tools", "Tools"), ("data", "Data")]

SKILLS = [
    ("Languages", ["openjdk", "kotlin", "typescript", "javascript", "python", "cplusplus", "apachegroovy", "ruby", "gnubash"]),
    ("Frontend & Mobile", ["react", "reactnative", "expo", "nextdotjs", "android", "tailwindcss", "framer", "html5", "css"]),
    ("Backend & Data", ["springboot", "nodedotjs", "flask", "postgresql", "mysql", "sqlite", "dynamodb", "firebase", "pandas"]),
    ("Cloud & Tooling", ["aws", "googlecloud", "docker", "kubernetes", "githubactions", "gradle", "git", "github", "linux",
                         "modelcontextprotocol"]),
]
PRACTICES = ["System design", "Distributed systems", "Concurrency", "Security reviews", "Algorithms", "TDD"]

CONTESTS = [
    {"num": "2nd", "count": 2, "suffix": "nd", "of": "of 5,000+", "name": "Amazon internal coding competition",
     "year": "2023", "logo": "trophy", "ahead": 99.96},
    {"num": "5th", "count": 5, "suffix": "th", "of": "overall", "name": "JUST Programming Contest", "year": "2023",
     "logo": "trophy"},
    {"num": "319th", "count": 319, "suffix": "th", "of": "of 6,000+ worldwide", "name": "IEEExtreme 16", "year": "2022",
     "logo": "ieee", "ahead": 94.7},
    {"num": "23rd", "count": 23, "suffix": "rd", "of": "ICPC qualifier", "name": "Jordanian Collegiate Programming Contest",
     "year": "2022", "logo": "trophy"},
    {"num": "Top 20%", "count": 20, "suffix": "%", "prefix": "Top", "of": "of 30,000+, round 2", "name": "Facebook Hacker Cup",
     "year": "2022", "logo": "facebook", "ahead": 80},
    {"num": "100+", "count": 100, "suffix": "+", "of": "students trained", "name": "JUST Programming Chapter",
     "year": "2021–2024", "logo": "cap"},
]

CONTACT_LINE = "I can build the software you need: a website, an iOS or Android app, a desktop app, or the backend behind them."
PLATFORMS = [("globe", "Websites"), ("apple", "iOS"), ("android", "Android"), ("desktop", "Desktop"), ("server", "Backend & cloud")]

# Skills line from the resume, verbatim and in order.
RESUME_SKILLS = ['Python', 'Java', 'Kotlin', 'Groovy', 'Ruby', 'C++', 'JavaScript', 'TypeScript', 'Bash Scripting', 'HTML', 'CSS', 'React.js', 'React Native', 'Next.js', 'Spring', 'Android', 'SQL', 'NoSQL', 'Linux', 'Git', 'GitHub', 'Version Control', 'Docker', 'Kubernetes', 'CI/CD', 'Model Context Protocol MCP', 'Object-Oriented Programming OOP', 'Data Structures', 'Algorithms', 'Design Patterns', 'Software Design', 'Code Optimization', 'System Design', 'Distributed Systems', 'Scalability', 'Concurrency', 'Multithreading', 'Operating Systems', 'Computer Networks', 'Database Internals', 'Performance Engineering', 'RESTful API', 'SOAP', 'Unit Testing', 'TDD', 'Agile', 'Data Analysis', 'AI', 'Machine Learning', 'AWS', 'GCP', 'Security', 'Secure Internet Connection', 'Problem Solving']
