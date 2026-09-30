def generate_engagement_suggestions(title, summary, body_text, category, origin):
    intel = body_text if body_text and len(body_text) > 100 else summary or ""
    words = intel.split()
    excerpt = " ".join(words[:45]) if len(words) >= 45 else intel

    # Match the opening and insight to the article's topic.
    if category == "Cybersecurity & Hacks":
        hook = "⚠️ SECURITY & BREACH ALERT"
        hashtag = "#CyberSecurity #BreachAlert #TechHacks #DataPrivacy"
        perspective = "Data security oversight and immediate patch management must be top priority for engineering teams right now."
    elif category == "Gadgets & Hardware":
        hook = "📱 NEW DEVICE LAUNCH / REVIEW"
        hashtag = "#TechGadgets #DeviceLaunch #ProductReview #Innovation"
        perspective = "Hardware specs are impressive, but real-world battery efficiency, build quality, and pricing value will decide if this wins the market."
    elif category == "AI & ML":
        hook = "🤖 AI INNOVATION UPDATE"
        hashtag = "#ArtificialIntelligence #MachineLearning #AITrends #FutureTech"
        perspective = "The speed of AI capability iteration continues to redefine workflow benchmarks across industries."
    else:
        hook = "💡 TECH INDUSTRY BREAKING INTEL"
        hashtag = f"#{category.replace(' ', '').replace('&', '')} #TechTrends #Innovation"
        perspective = "The strategic balance between rapid execution and reliable infrastructure remains the defining factor here."

    # Option A: Executive & Professional Take
    post_option_1 = (
        f"{hook}: {title}\n\n"
        f"Key Context: {excerpt}...\n\n"
        f"Core Insight: {perspective}\n\n"
        f"What is your take on this development? Let's discuss in the comments below! 👇\n\n"
        f"{hashtag} #{origin.replace(' ', '').replace('/', '')}"
    )

    # Option B: High-Engagement Conversational / Hot Take
    post_option_2 = (
        f"🔥 Hot Take on: {title}\n\n"
        f"Here is what you need to know: {excerpt[:180]}...\n\n"
        f"Is this a game-changer for the ecosystem, or is it getting overhyped? Drop your thoughts below! 👇\n\n"
        f"{hashtag}"
    )

    # Smart Comments for platform replies
    auto_comment_1 = (
        f"Crucial update. Particularly regarding '{words[0] if words else category}'—the way teams handle implementation "
        f"and security controls over the next few months will be key."
    )
    auto_comment_2 = (
        f"Spot on! Great breakdown of {title}. The shift in {category} is moving faster than expected."
    )

    return {
        "posts": [
            {"id": "post1", "label": "Option A: Executive & Industry Analysis", "text": post_option_1},
            {"id": "post2", "label": "Option B: High-Engagement Hot Take", "text": post_option_2}
        ],
        "comments": [
            {"id": "comment1", "label": "Comment Option 1 (Executive)", "text": auto_comment_1},
            {"id": "comment2", "label": "Comment Option 2 (Direct Reply)", "text": auto_comment_2}
        ]
    }
