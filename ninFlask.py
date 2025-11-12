from flask import Flask, request, redirect
import requests
from supabase import create_client
import os
import path

app = Flask(__name__)

supabase = create_client(path.SUPABASE_URL, path.SUPABASE_KEY)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no code"

    token_data = {
        "client_id": path.CLIENT_ID,
        "client_secret": path.CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": path.REDIRECT_URI
    }

    res = requests.post("https://discord.com/api/oauth2/token", data=token_data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    if res.status_code != 200:
        return f"Discord token exchange failed: {res.text}"

    token_json = res.json()
    access_token = token_json["access_token"]

    user_res = requests.get("https://discord.com/api/users/@me", headers={"Authorization": f"Bearer {access_token}"})
    user_json = user_res.json()
    user_id = user_json["id"]

    # Supabaseに保存 or 更新
    data = {"user_id": user_id, "access_token": access_token}
    supabase.table("user_tokens").upsert(data).execute()

    return "ログイン完了！このウィンドウを閉じてOKです。"

@app.route("/")
def index():
    oauth_url = (
        f"https://discord.com/api/oauth2/authorize?client_id={path.CLIENT_ID}"
        f"&redirect_uri={path.REDIRECT_URI}"
        "&response_type=code&scope=identify"
    )
    return f'<a href="{oauth_url}">Discordでログイン</a>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
