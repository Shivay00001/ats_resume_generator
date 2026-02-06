
# Constants for ATS Resume Generator

# Standard Fonts
FONT_NAME = "Arial"
FONT_SIZE_BODY = 11
FONT_SIZE_HEADING = 12 # Slightly larger, but kept minimal
FONT_SIZE_NAME = 14

# Margins (Inches)
MARGIN_TOP = 1.0
MARGIN_BOTTOM = 0.5 # Slightly smaller bottom to fit more
MARGIN_LEFT = 1.0
MARGIN_RIGHT = 1.0

# Action Verbs (Categorized for potential future logic, but flattened for now)
ACTION_VERBS = [
    # Management / Leadership
    "Orchestrated", "Spearheaded", "Executed", "Directed", "Consolidated", 
    "Supervised", "Oversaw", "Delegated", "Coordinated", "Chaired", "Approved",
    "Administered", "Presided", "Enforced", "Established", "Evaluated",
    
    # Technical / Development
    "Architected", "Engineered", "Developed", "Deployed", "Implemented", 
    "Optimized", "Refactored", "Automated", "Debugged", "Integrated",
    "Migrated", "Systematized", "Formulated", "Programmed", "Fabricated",
    
    # Analysis / Research
    "Analyzed", "Quantified", "Modeled", "Forecasted", "Identified", 
    "Investigated", "Audited", "Calculated", "Derived", "Evaluated",
    "Assessed", "Diagnosed", "Measured", "Simulated", "Researched",
    
    # Communication / Sales
    "Negotiated", "Persuaded", "Influenced", "Authored", "Presented", 
    "Publicized", "Marketed", "Promoted", "Advocated", "Clarified",
    "Compose", "Corresponded", "Drafted", "Edited", "Lectured"
    
    # Achievement / Results
    "Accelerated", "Awarded", "Exceeded", "Maximized", "Generated",
    "Improved", "Increased", "Outperformed", "Saved", "Surpassed",
    "Expanded", "Boosted", "Eliminated", "Reduced", "Streamlined"
]

# Weak words to avoid (to be replaced or flagged)
WEAK_WORDS = {
    "responsible for": "Spearheaded",
    "helped": "Assisted" or "Facilitated",
    "worked on": "Executed" or "Implemented",
    "tried": "Attempted",
    "expert at": "Proficient in",
    "proficient in": "Proficient in", # Allowed
    "good at": "Skilled in",
    "familiar with": "Exposed to",
    "hard worker": "Dedicated",
    "team player": "Collaborative",
}

# Role-based Keywords (Simple dictionary for auto-suggestion/injection)
ROLE_KEYWORDS = {
    "software engineer": [
        "Python", "Java", "C++", "System Architecture", "Distributed Systems",
        "API Design", "Microservices", "CI/CD", "AWS", "Docker", "Kubernetes",
        "Algorithmic Problem Solving", "Code Review", "Agile", "Scrum", "Git"
    ],
    "data scientist": [
        "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "SQL",
        "Pandas", "NumPy", "Data Visualization", "Big Data", "Spark", "Hadoop",
        "Statistical Modeling", "A/B Testing", "NLP", "Computer Vision"
    ],
    "product manager": [
        "Product Roadmap", "Stakeholder Management", "User Stories", "JIRA",
        "Market Research", "Competitive Analysis", "KPI Tracking", "Agile",
        "Go-to-Market Strategy", "UX/UI Design Principles", "Feature Prioritization"
    ],
    "marketing manager": [
        "SEO", "SEM", "Content Strategy", "Social Media Marketing", "Google Analytics",
        "Email Marketing", "Brand Positioning", "Campaign Management", "ROI Analysis",
        "Lead Generation", "Copywriting", "Market Segmentation"
    ],
     "project manager": [
        "Risk Management", "Budgeting", "Resource Allocation", "Scheduling",
        "Waterfall", "Agile", "Scrum", "Stakeholder Communication", "Project Lifecycle",
        "Quality Assurance", "Vendor Management", "Scope Management"
     ],
     "human resources": [
        "Talent Acquisition", "Employee Relations", "Onboarding", "Performance Management",
        "Compliance", "Benefits Administration", "HRIS", "Compensation Analysis",
        "Training & Development", "Conflict Resolution", "Labor Laws"
     ]
}

# ATS formatting rules
SECTION_ORDER = [
    "Contact",
    "Professional Summary",
    "Skills",
    "Work Experience",
    "Projects",
    "Education",
    "Certifications"
]

# Measurable results indicators (regex patterns or words)
MEASURABLE_REGEX = [
    r"\d+%",          # 20%
    r"\$\d+",         # $5000
    r"\d+\s*k",       # 50k
    r"\d+\s*M",       # 5M
    r"reduced.*by",   # reduced time by
    r"increased.*by", # increased revenue by
    r"saved",         # saved
    r"improved",      # improved
    r"grew",          # grew
]
