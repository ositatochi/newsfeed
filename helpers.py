def generate_engagement_suggestions(title, summary, category, origin):
    clean_summary = summary[:220] if summary else title
    
    # Post Option 1: Executive & Analytical (LinkedIn/X Focus)
    post_option_1 = (
        f"Nigeria's CBN is pushing for financial data to be stored locally. "
        f"The goal: sovereignty, security, and stronger oversight of citizens' data. "
        f"The risk: higher costs and slower innovation if implementation isn't handled well. "
        f"The intent is sound. The execution is what matters.\n\n"
        f"#CBN #Fintech #{origin.replace(' ', '').replace('/', '')} #{category.replace(' ', '').replace('&', '')}"
    ) if "CBN" in title or "data" in title.lower() else (
        f"💡 Key Takeaway on {category}:\n\n"
        f"{title}\n\n"
        f"Why this matters: {clean_summary}...\n\n"
        f"As systems evolve, balancing security, infrastructure cost, and speed remains the biggest challenge. "
        f"How is your team handling this shift?\n\n"
        f"#{category.replace(' ', '').replace('&', '')} #TechLeadership #Innovation"
    )

    # Post Option 2: Conversational / Hot Take (X/Twitter Focus)
    post_option_2 = (
        f"🚀 Hot Take on: {title}\n\n"
        f"Data localization policies sound great on paper for national sovereignty, "
        f"but local tech ecosystems must have the cloud infrastructure ready to carry the load.\n\n"
        f"Are we building fast enough to keep up with regulation? What are your thoughts? 👇\n\n"
        f"#TechTrends #{origin.replace(' ', '').replace('/', '')} #Fintech"
    )

    # Smart Auto-Comment Suggestion (For engaging on other people's posts about this topic)
    auto_comment_1 = (
        f"Great breakdown. The push for data localization highlights a crucial balance between regulatory "
        f"oversight and infrastructure readiness. Highly interested to see how local cloud providers "
        f"scale to meet these compliance demands over the next 12 months."
    )
    
    auto_comment_2 = (
        f"Spot on! Compliance costs will definitely spike in the short term, but long-term data sovereignty "
        f"could stimulate local data center infrastructure if managed well."
    )

    return {
        "posts": [
            {"id": "post1", "label": "Option A: Executive & Analytical", "text": post_option_1},
            {"id": "post2", "label": "Option B: Conversational / Hot Take", "text": post_option_2}
        ],
        "comments": [
            {"id": "comment1", "label": "Comment Option 1 (Analytical)", "text": auto_comment_1},
            {"id": "comment2", "label": "Comment Option 2 (Direct/Supportive)", "text": auto_comment_2}
        ]
    }
