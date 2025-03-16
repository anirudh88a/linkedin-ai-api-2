from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)  # This allows your Bubble.io app to call this API

# Get API key from Replit secrets
claude_api_key = os.environ.get("CLAUDE_API_KEY")


# Add a root route for testing
@app.route('/', methods=['GET'])
def index():
    return """
<h1>LinkedIn AI Assistant API</h1>
<p>API is running with the following endpoints:</p>
<ul>
    <li><a href="#headline">Headline Optimizer</a> - <code>/optimize-headline</code></li>
    <li><a href="#summary">Summary Optimizer</a> - <code>/optimize-summary</code></li>
    <li><a href="#post">Content Post Generator</a> - <code>/generate-post</code></li>
</ul>

<h2 id="headline">Test Headline Optimizer</h2>
<form id="headlineForm" style="margin: 20px 0; padding: 20px; border: 1px solid #ccc;">
    <div style="margin-bottom: 10px;">
        <label>Current Headline:</label><br>
        <input type="text" id="headline" value="Marketing Manager" style="width: 300px;">
    </div>
    <div style="margin-bottom: 10px;">
        <label>Industry:</label><br>
        <input type="text" id="industry" value="Technology" style="width: 300px;">
    </div>
    <div style="margin-bottom: 10px;">
        <label>Target Job:</label><br>
        <input type="text" id="target" value="Marketing Director" style="width: 300px;">
    </div>
    <button type="button" onclick="testHeadlineAPI()">Test Headline API</button>
</form>

<div id="headlineResults" style="white-space: pre-wrap; padding: 20px; background: #f5f5f5; display: none;"></div>

<h2 id="summary">Test Summary Optimizer</h2>
<form id="summaryForm" style="margin: 20px 0; padding: 20px; border: 1px solid #ccc;">
    <div style="margin-bottom: 10px;">
        <label>Current Summary:</label><br>
        <textarea id="current_summary" rows="4" style="width: 100%;">Experienced marketing professional with a focus on digital campaigns and brand strategy.</textarea>
    </div>
    <div style="margin-bottom: 10px;">
        <label>Experience:</label><br>
        <textarea id="experience" rows="4" style="width: 100%;">5 years as Marketing Manager, 2 years as Marketing Specialist. Led teams of up to 5 people.</textarea>
    </div>
    <div style="margin-bottom: 10px;">
        <label>Key Achievements:</label><br>
        <textarea id="achievements" rows="4" style="width: 100%;">Increased website traffic by 45%, Generated $2M in pipeline, Reduced CAC by 30%.</textarea>
    </div>
    <div style="margin-bottom: 10px;">
        <label>Target Job:</label><br>
        <input type="text" id="summary_target" value="Marketing Director" style="width: 300px;">
    </div>
    <button type="button" onclick="testSummaryAPI()">Test Summary API</button>
</form>

<div id="summaryResults" style="white-space: pre-wrap; padding: 20px; background: #f5f5f5; display: none;"></div>

<h2 id="post">Test Content Post Generator</h2>
<form id="postForm" style="margin: 20px 0; padding: 20px; border: 1px solid #ccc;">
    <div style="margin-bottom: 10px;">
        <label>Industry:</label><br>
        <input type="text" id="post_industry" value="Technology" style="width: 300px;">
    </div>
    <div style="margin-bottom: 10px;">
        <label>Topic:</label><br>
        <input type="text" id="topic" value="Digital Marketing Trends 2025" style="width: 300px;">
    </div>
    <div style="margin-bottom: 10px;">
        <label>Content Type:</label><br>
        <select id="content_type" style="width: 300px;">
            <option value="thought leadership">Thought Leadership</option>
            <option value="industry news">Industry News</option>
            <option value="personal story">Personal Story</option>
            <option value="tips and advice">Tips & Advice</option>
            <option value="career insights">Career Insights</option>
        </select>
    </div>
    <div style="margin-bottom: 10px;">
        <label>Tone:</label><br>
        <select id="tone" style="width: 300px;">
            <option value="professional">Professional</option>
            <option value="conversational">Conversational</option>
            <option value="inspirational">Inspirational</option>
            <option value="educational">Educational</option>
        </select>
    </div>
    <div style="margin-bottom: 10px;">
        <label>Include Hashtags:</label>
        <input type="checkbox" id="include_hashtags" checked>
    </div>
    <button type="button" onclick="testPostAPI()">Generate LinkedIn Post</button>
</form>

<div id="postResults" style="white-space: pre-wrap; padding: 20px; background: #f5f5f5; display: none;"></div>

<script>
function testHeadlineAPI() {
    document.getElementById('headlineResults').innerHTML = "Loading... This may take 15-20 seconds...";
    document.getElementById('headlineResults').style.display = "block";

    fetch('/optimize-headline', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            current_headline: document.getElementById('headline').value,
            industry: document.getElementById('industry').value,
            target_job: document.getElementById('target').value
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('headlineResults').innerHTML = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('headlineResults').innerHTML = "Error: " + error;
    });
}

function testSummaryAPI() {
    document.getElementById('summaryResults').innerHTML = "Loading... This may take 15-20 seconds...";
    document.getElementById('summaryResults').style.display = "block";

    fetch('/optimize-summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            current_summary: document.getElementById('current_summary').value,
            experience: document.getElementById('experience').value,
            achievements: document.getElementById('achievements').value,
            target_job: document.getElementById('summary_target').value
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('summaryResults').innerHTML = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('summaryResults').innerHTML = "Error: " + error;
    });
}

function testPostAPI() {
    document.getElementById('postResults').innerHTML = "Loading... This may take 15-20 seconds...";
    document.getElementById('postResults').style.display = "block";

    fetch('/generate-post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            industry: document.getElementById('post_industry').value,
            topic: document.getElementById('topic').value,
            content_type: document.getElementById('content_type').value,
            tone: document.getElementById('tone').value,
            include_hashtags: document.getElementById('include_hashtags').checked
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('postResults').innerHTML = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        document.getElementById('postResults').innerHTML = "Error: " + error;
    });
}
</script>
"""


@app.route('/optimize-headline', methods=['POST'])
def optimize_headline():
    # Get data from request
    data = request.json
    current_headline = data.get('current_headline', '')
    industry = data.get('industry', '')
    target_job = data.get('target_job', '')

    # Create the prompt
    prompt = f"""I need help optimizing my LinkedIn headline. 
    My current headline is: {current_headline}. 
    My industry is {industry}. 
    My target job is {target_job}. 
    Please provide 3 improved headline options that will help me get more visibility with recruiters."""

    # Call Claude API directly using requests
    try:
        headers = {
            "x-api-key": claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model":
            "claude-3-7-sonnet-20250219",  # Latest Claude model as of March 2025
            "max_tokens": 500,
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }

        response = requests.post("https://api.anthropic.com/v1/messages",
                                 headers=headers,
                                 json=payload)

        # Let's log more details about the error
        if response.status_code != 200:
            error_detail = response.json()
            return jsonify({
                "success": False,
                "error":
                f"API Error: {error_detail.get('error', {}).get('message', 'Unknown error')}",
                "status_code": response.status_code,
                "details": error_detail
            }), response.status_code

        response_data = response.json()
        result = response_data.get('content', [{}])[0].get('text', '')
        return jsonify({"success": True, "result": result})

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "trace": str(e.__traceback__)
        }), 500


@app.route('/optimize-summary', methods=['POST'])
def optimize_summary():
    # Get data from request
    data = request.json
    current_summary = data.get('current_summary', '')
    experience = data.get('experience', '')
    achievements = data.get('achievements', '')
    target_job = data.get('target_job', '')

    # Create the prompt
    prompt = f"""I need help optimizing my LinkedIn summary/about section.

    Current summary: {current_summary}

    My relevant experience: {experience}

    Key achievements: {achievements}

    Target role: {target_job}

    Please write a compelling, first-person LinkedIn summary (about 200-250 words) that:
    1. Starts with an attention-grabbing opening line
    2. Highlights my expertise and experience
    3. Incorporates my key achievements with metrics when available
    4. Positions me as an ideal candidate for my target role
    5. Includes relevant keywords for LinkedIn search algorithms
    6. Ends with a clear call-to-action

    Make it conversational yet professional, and focus on the value I can bring to potential employers."""

    # Call Claude API directly using requests
    try:
        headers = {
            "x-api-key": claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-3-7-sonnet-20250219",
            "max_tokens": 800,
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }

        response = requests.post("https://api.anthropic.com/v1/messages",
                                 headers=headers,
                                 json=payload)

        response_data = response.json()

        # Extract the response from JSON structure
        if response.status_code == 200:
            result = response_data.get('content', [{}])[0].get('text', '')
            return jsonify({"success": True, "result": result})
        else:
            return jsonify({
                "success": False,
                "error":
                f"API Error: {response_data.get('error', {}).get('message', 'Unknown error')}",
                "status_code": response.status_code,
                "details": response_data
            }), response.status_code

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/generate-post', methods=['POST'])
def generate_post():
    # Get data from request
    data = request.json
    industry = data.get('industry', '')
    topic = data.get('topic', '')
    content_type = data.get('content_type', 'thought leadership')
    tone = data.get('tone', 'professional')
    include_hashtags = data.get('include_hashtags', True)

    # Create the prompt
    prompt = f"""Create an engaging LinkedIn post about {topic} for a professional in the {industry} industry.

    Content type: {content_type}
    Tone: {tone}
    Include hashtags at the end: {"Yes" if include_hashtags else "No"}

    The post should:
    1. Start with an attention-grabbing hook
    2. Include relevant insights or data points when appropriate
    3. Be personal and authentic
    4. Be between 150-250 words (ideal LinkedIn length)
    5. End with a question or call-to-action to encourage engagement
    6. Use appropriate spacing for readability (LinkedIn users prefer posts with space between paragraphs)

    For hashtags, include a mix of popular and niche tags (5-7 total) that would reach the right audience.
    """

    # Call Claude API directly using requests
    try:
        headers = {
            "x-api-key": claude_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": "claude-3-7-sonnet-20250219",
            "max_tokens": 800,
            "messages": [{
                "role": "user",
                "content": prompt
            }]
        }

        response = requests.post("https://api.anthropic.com/v1/messages",
                                 headers=headers,
                                 json=payload)

        response_data = response.json()

        # Extract the response from JSON structure
        if response.status_code == 200:
            result = response_data.get('content', [{}])[0].get('text', '')
            return jsonify({"success": True, "result": result})
        else:
            return jsonify({
                "success": False,
                "error":
                f"API Error: {response_data.get('error', {}).get('message', 'Unknown error')}",
                "status_code": response.status_code,
                "details": response_data
            }), response.status_code

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# This is important for Replit to work correctly
app.run(host='0.0.0.0', port=8080)
