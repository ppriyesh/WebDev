from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Serve styles.css from main directory
@app.route('/styles.css')
def serve_css():
    return send_from_directory('.', 'styles.css')

# Serve logo from main directory
@app.route('/logo-removebg-preview.png')
def serve_logo():
    return send_from_directory('.', 'logo-removebg-preview.png')

@app.route('/profile')
def serve_prof():
    return send_from_directory('.', 'profile.html')


@app.route('/brands')
def serve_brands():
    return send_from_directory('.', 'brands.html')

@app.route('/about')
def serve_about():
    return send_from_directory('.', 'about.html')

# ----- ADVANCED SCORE CALCULATION FUNCTION -----
def calculate_social_score(followers, engagement_rate, posts_per_month, conversion_rate, blac_fit_score):
    # Audience score
    if followers < 1000:
        audience_score = 50
    elif followers < 5000:
        audience_score = 150
    elif followers < 10000:
        audience_score = 250
    else:
        audience_score = 350

    # Engagement score
    if engagement_rate >= 18:
        engagement_score = 300
    elif engagement_rate >= 10:
        engagement_score = 200
    elif engagement_rate >= 5:
        engagement_score = 100
    else:
        engagement_score = 50

    # Consistency score
    if posts_per_month >= 12:
        consistency_score = 150
    elif posts_per_month >= 6:
        consistency_score = 100
    elif posts_per_month >= 1:
        consistency_score = 50
    else:
        consistency_score = 0

    # Conversion score
    if conversion_rate >= 5:
        conversion_score = 100
    elif conversion_rate >= 2:
        conversion_score = 75
    elif conversion_rate >= 1:
        conversion_score = 50
    else:
        conversion_score = 25

    # BLAC score
    blac_score = min(max(blac_fit_score, 0), 100)

    total_score = (
        audience_score +
        engagement_score +
        consistency_score +
        conversion_score +
        blac_score
    )

    return {
        "Audience Score": audience_score,
        "Engagement Score": engagement_score,
        "Content Consistency Score": consistency_score,
        "Conversion Score": conversion_score,
        "BLAC Fit Score": blac_score,
        "Total Social Score": total_score
    }

# ----- ROUTE for both / and /calculate -----
@app.route("/", methods=["GET", "POST"])
@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    result = None
    form_data = {
        "followers": "",
        "engagement": "",
        "posts": "",
        "conversion": "",
        "blac": ""
    }

    if request.method == "POST":
        followers = int(request.form["followers"])
        engagement = float(request.form["engagement"])
        posts = int(request.form["posts"])
        conversion = float(request.form["conversion"])
        blac = int(request.form["blac"])

        result = calculate_social_score(followers, engagement, posts, conversion, blac)

        form_data = {
            "followers": followers,
            "engagement": engagement,
            "posts": posts,
            "conversion": conversion,
            "blac": blac
        }

    return render_template("calculate.html", result=result, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)
