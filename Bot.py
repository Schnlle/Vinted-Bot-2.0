import requests from flask import Flask, request, render_template_string

app = Flask(name)

HTML_PAGE = '''

<!DOCTYPE html><html><head>
    <title>Nintendo 3DS Bot - Vinted Search</title>
</head>
<body>
    <h1>Enter Your Vinted Access Token</h1>
    <form method="POST">
        <input type="text" name="access_token" placeholder="Access Token" style="width:300px" required>
        <button type="submit">Start Bot</button>
    </form>
    {% if error %}
        <p style="color: red;">Error: {{ error }}</p>
    {% endif %}
    {% if userinfo %}
        <h2>Status:</h2>
        <pre>{{ userinfo }}</pre>
    {% endif %}
</body>
</html>
'''Liste aller Suchbegriffe

NORMAL_CONSOLES = [ "New Nintendo 3DS", "New Nintendo 3DS XL", "Nintendo 3DS", "Nintendo 3DS XL", "New Nintendo 2DS XL" ]

SPECIAL_CONSOLES = [ "Monster Hunter", "Pokémon", "Pikachu", "Minecraft", "Animal Crossing", "Super Smash Bros", "Zelda", "Luigi", "Mario Kart", "Fire Emblem", "Metroid" ]

NORMAL_2DS = [ "Nintendo 2DS", "2DS Mario Kart 7", "2DS New Super Mario Bros 2", "2DS Transparent Blau", "2DS Transparent Rot" ]

SPECIAL_2DS = [ "2DS Pink", "2DS Pokémon Omega Rubin", "2DS Pokémon Alpha Saphir", "2DS Pokémon Sun", "2DS Pokémon Moon" ]

DEFECT_KEYWORDS = [ "defekt", "kaputt", "geht nicht", "Display gebrochen", "stark zerkratzt", "Schaden" ]

@app.route('/', methods=['GET', 'POST']) def home(): userinfo = None error = None if request.method == 'POST': token = request.form['access_token'] headers = { 'Authorization': f'Bearer {token}', 'Accept': 'application/json', } try: response = requests.get('https://www.vinted.de/api/v2/items', headers=headers) if response.status_code == 200: items = response.json() matched_items = [] for item in items.get('items', []): title = item.get('title', '').lower() price = float(item.get('price', {}).get('amount', 0)) / 100

if any(word.lower() in title for word in DEFECT_KEYWORDS):
                    matched_items.append({"manual_review": item})
                    continue

                if any(console.lower() in title for console in NORMAL_CONSOLES) and price <= 60:
                    matched_items.append({"normal_console": item})
                elif any(console.lower() in title for console in SPECIAL_CONSOLES) and price <= 90:
                    matched_items.append({"special_console": item})
                elif any(console.lower() in title for console in NORMAL_2DS) and price <= 30:
                    matched_items.append({"normal_2ds": item})
                elif any(console.lower() in title for console in SPECIAL_2DS) and price <= 45:
                    matched_items.append({"special_2ds": item})
            userinfo = matched_items
        else:
            error = f'API Error: {response.status_code} - {response.reason}'
    except Exception as e:
        error = str(e)

return render_template_string(HTML_PAGE, userinfo=userinfo, error=error)

if name == 'main': app.run(host='0.0.0.0', port=3000)

