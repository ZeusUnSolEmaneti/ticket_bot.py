import discord 
from discord.ext import commands
import random
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all()) #botun izinleri ve prefixi belirtilir
random_ticket=random.randint(1,10000)

@bot.event #bot herhangi bir eylem yaptıgı zaman kullanılır
async def on_ready(): #bot açıldıgı zaman vereceği mesaj 
    await bot.tree.sync()
    print("I'm Ready!")

@bot.command() #bota bir komut verileceği zaman oluşturulur
async def hey(ctx):
    username = ctx.message.author.mention
    await ctx.send("Hi " + username)

@bot.command()
@commands.has_role("admin") #komudu kullanabilcek rolleri gösterir
async def ban(ctx, member:discord.Member, *, reason):
    if reason == None:
        reason = "This user banned" #Sebep yok ise otomatik olarak banladıgını söyler
        await member.ban(reason=reason)
    await member.ban(reason=reason) #kişiyi banlar ve verilen sebebi sebep olarak atar

@bot.command()
@commands.has_role("admin") #komudu kullanabilcek rolleri gösterir
async def kick(ctx, member:discord.Member, *, reason):
    if reason == None:
        reason = "This user kicked" #Sebep yok ise otomatik olarak banladıgını söyler
        await member.kick(reason=reason)
    await member.kick(reason=reason) #kişiyi banlar ve verilen sebebi sebep olarak atar

@bot.command()
async def yardım(ctx):
    embed=discord.Embed(title="Help", description="Botun kullanımı açıklar", color=0x7431bc)
    embed.add_field(name="!kick", value="Belirtilen kullanıcıyı sunucudan atar.", inline=False)
    embed.add_field(name="!ban", value="Belirtilen kullanıcıyı sunucudan banlar.", inline=False)
    embed.add_field(name="!hey", value="merhaba", inline=False)
    embed.add_field(name="/ticket", value="Ticket oluşturma penceresi için kullanılır (Just Admin)", inline=False)
    embed.set_footer(text="Created By ! balboa#0666")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_role("admin")
async def ticket(ctx):
    embed=discord.Embed(title="Ticket", description="Nasıl Ticket Açılır", color=0x7431bc)
    embed.add_field(name="/ticket", value="Bu komut ile kendinize ait bir ticket açabilirsiniz. (ticket-aç kanalında kullanınız.)", inline=False)
    embed.set_footer(text="Created By ! balboa#0666")
    await ctx.send(embed=embed)

class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Ticket 🎫", style=discord.ButtonStyle.green)
    async def test(self, interaction: discord.Interaction, Button: discord.ui.Button):
        guild=interaction.guild
        category = discord.utils.get(guild.categories, name="tickets")
        role = discord.utils.get(guild.roles, name="admin")
        overwrites={
        interaction.user : discord.PermissionOverwrite(view_channel=True),
        guild.default_role : discord.PermissionOverwrite(view_channel=False),
        role : discord.PermissionOverwrite(view_channel=True)
        }
        channel = await guild.create_text_channel(f"ticket {random_ticket}",overwrites=overwrites, category=category)
        await channel.send("Nasıl Yardımcı Olabilirim?")

@bot.tree.command(name="ticket")
async def ticket(interaction: discord.Interaction):
    await interaction.response.send_message(content="Ticket oluşturmak için tıklayınız", view=TicketButtons())

bot.run("MTA3NTA4MTE5NjMxMDExODQ0MQ.GhL8uU.mGH6WptmLVNXpzZHufrQ3X5nbMONbJ3E84PVOE")