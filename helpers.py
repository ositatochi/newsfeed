def generate_engagement_suggestions(title, summary, body_text, category, origin):
    # Use full scraped body if available, otherwise fall back to summary
    intel_content = body_text if body_text and len(body_text) > 100 else summary
    words = intel_content.split()
    key_excerpt = " ".join(words[:40]) if len(words) >= 40 else intel_content

    # Option A: Deep Intel & Executive Analysis
    post_option_1 = (
        f"💡 Industry Analysis: {title}\n\n"
        f"Deep Dive Intel: {key_excerpt}...\n\n"
        f"Key Takeaway: Moving beyond surface headlines, this shift in {category} impacts operational scalability, data policy, and engineering strategy. "
        f"How is your team positioning for this?\n\n"
        f"#{category.replace(' ', '').replace('&', '')} #TechLeadership #{origin.replace(' ', '').replace('/', '')} #Innovation"
    )

    # Option B: Conversational / Viral Engagement
    post_option_2 = (
        f"🔥 Quick Take on: {title}\n\n"
        f"Here is what's happening behind the scenes: {key_excerpt[:180]}...\n\n"
        f"The big question: Is this the right move for the industry, or are we moving too fast? Let's discuss in the replies 👇\n\n"
        f"#TechTrends #{category.replace(' ', '').replace('&', '')} #{origin.replace(' ', '').replace('/', '')}"
    )

    # Comments for quick engagement under other people's posts
    auto_comment_1 = (
        f"Solid writeup. The core point regarding '{words[0] if words else category}' is critical. "
        f"Ensuring robust execution while managing overhead will determine the true long-term impact."
    )
    
    auto_comment_2 = (
        f"Spot on! This aligns directly with how {category} systems are evolving. "
        f"Particularly interested to see how local providers adapt over the next quarter."
    )

    return {
        "posts": [
            {"id": "post1", "label": "Option A: Deep Intel & Executive Analysis", "text": post_option_1},
            {"id": "post2", "label": "Option B: Conversational / Viral Engagement", "text": post_option_2}
        ],
        "comments": [
            {"id": "comment1", "label": "Comment Option 1 (Executive)", "text": auto_comment_1},
            {"id": "comment2", "label": "Comment Option 2 (Direct/Supportive)", "text": auto_comment_2}
        ]
    }
