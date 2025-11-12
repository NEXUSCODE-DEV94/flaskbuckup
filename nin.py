import discord
from discord.ext import commands
from supabase import create_client
import path

supabase = create_client(path.SUPABASE_URL, path.SUPABASE_KEY)

intents = discord.Intents.default()
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    application_id=path.CLIENT_ID
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Commands synced as {bot.user}")

@bot.tree.command(name="mytoken", description="自分のトークンを確認")
async def mytoken(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    res = supabase.table("user_tokens").select("access_token").eq("user_id", user_id).execute()
    if res.data:
        await interaction.response.send_message(f"あなたのトークン: ||{res.data[0]['access_token']}||", ephemeral=True)
    else:
        await interaction.response.send_message("Supabaseにデータがありません。Flaskでログインしてください。", ephemeral=True)

bot.run(path.BOTTOKEN)
