def generate_engagement_suggestions(title, summary, category):
    clean_summary = summary[:200] if summary else title
    
    linkedin = f"💡 Insights on {category}:\n\n\"{title}\"\n\nKey takeaway: {clean_summary}...\n\nHow is your team adapting to this shift in the industry? Let's discuss in the comments below! #TechTrends #{category.replace(' ', '').replace('&', '')} #Innovation"
    
    twitter_post = f"🚀 Quick Take on: {title}\n\nKey point: {clean_summary[:120]}...\n\nWhat are your thoughts on this movement? 👇 #Tech #{category.replace(' ', '').replace('&', '')}"
    
    comment_take = f"Great perspective on this. The shift toward {category} continues to reshape how we approach scalable systems. Particularly interested in how this impacts overall developer workflow over the next 12 months."

    return {
        "linkedin": linkedin,
        "x": twitter_post,
        "comment": comment_take
    }
