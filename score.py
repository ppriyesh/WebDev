from flask import Flask, render_template, request, jsonify

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    followers = int(data['followers'])
    engagement = float(data['engagement'])
    posts = int(data['posts'])
    conversion = float(data['conversion'])
    blac = int(data['blac'])

    result = calculate_social_score(followers, engagement, posts, conversion, blac)
    return jsonify(result)


def calculate_social_score(followers, engagement_rate, posts_per_month, conversion_rate, blac_fit_score):
    if followers < 1000:
        audience_score = 50
    elif followers < 5000:
        audience_score = 150
    elif followers < 10000:
        audience_score = 250
    else:
        audience_score = 350

    if engagement_rate >= 18:
        engagement_score = 300
    elif engagement_rate >= 10:
        engagement_score = 200
    elif engagement_rate >= 5:
        engagement_score = 100
    else:
        engagement_score = 50

    if posts_per_month >= 12:
        consistency_score = 150
    elif posts_per_month >= 6:
        consistency_score = 100
    elif posts_per_month >= 1:
        consistency_score = 50
    else:
        consistency_score = 0

    if conversion_rate >= 5:
        conversion_score = 100
    elif conversion_rate >= 2:
        conversion_score = 75
    elif conversion_rate >= 1:
        conversion_score = 50
    else:
        conversion_score = 25

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        followers = int(request.form['followers'])
        engagement = float(request.form['engagement'])
        posts = int(request.form['posts'])
        conversion = float(request.form['conversion'])
        blac = int(request.form['blac'])

        result = calculate_social_score(followers, engagement, posts, conversion, blac)
        return render_template('index1.html', result=result)
    return render_template('index1.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
