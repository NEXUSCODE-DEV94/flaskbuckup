import discord
from discord.ext import commands
from supabase import create_client
import path

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

supabase = create_client(path.SUPABASE_URL, path.SUPABASE_KEY)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def mytoken(ctx):
    """ユーザーのアクセストークン確認（デバッグ用）"""
    user_id = str(ctx.author.id)
    res = supabase.table("user_tokens").select("access_token").eq("user_id", user_id).execute()
    if res.data:
        await ctx.send(f"あなたのトークン: ||{res.data[0]['access_token']}||")
    else:
        await ctx.send("Supabaseにデータがありません。Flaskからログインしてください。")

bot.run(path.BOTTOKEN)
