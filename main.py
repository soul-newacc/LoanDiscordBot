import os
import json
import discord
from discord import app_commands
from config import token #this was easier for me than doin a env or a json

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = app_commands.CommandTree(client)

@client.event
async def on_ready():
    try:
        synced = await bot.sync()
        print(synced)
    except Exception as e:
        print(e)

@bot.command(name="crearprestamo", description="crea prestamos pues!!")
async def ping(interaction: discord.Interaction, nombre: str, id: str, monto: str):
    data = {"Nombre": nombre, "ID": id, "Monto": monto}
    nom = nombre+".json"
    os.chdir("loans")
    with open(nom, "w") as file:
        json.dump(data, file, indent=4)
    embed = discord.Embed(title="Operacion exitosa! ✅:", description=f"Guardado en {nom}", color=14536588)
    await interaction.response.send_message(embed=embed)
    os.chdir("..")

@bot.command(name="verprestamos", description="ver prestamos pues!!")
async def verprestamos(interaction: discord.Interaction):
    os.chdir("loans")
    prestamos = os.listdir()
    embed = discord.Embed(title="Los prestamos disponibles son:", description=f"{prestamos}", color=14536588)
    await interaction.response.send_message(embed=embed)
    os.chdir("..")

@bot.command(name="infoprestamo", description="ver info de un prestamo en especifico")
@app_commands.describe(prestamo="Especificar prestamo con nombre del archivo completo, ej: Moserati.json")
async def infoprestamo(interaction: discord.Interaction, prestamo: str):
    try:
        os.chdir("loans")
        prestamoo = json.load(open(prestamo))
        embed = discord.Embed(title=f"{prestamo}", description=f"{json.dumps(prestamoo, indent=4)}", color=14536588)
        await interaction.response.send_message(embed=embed)
        os.chdir("..")
    except FileNotFoundError:
        embed = discord.Embed(title="Error", description="El prestamo no existe!", color=16711680)
        await interaction.response.send_message(embed=embed)
        os.chdir("..")

@bot.command(name="borrarprestamo", description="borrar un prestamo pues!")
async def borrarprestamo(interaction: discord.Interaction, prestamo: str):
    try:
        os.chdir("loans")
        embed = discord.Embed(title=f"{prestamo} ha sido borrado con exito!", color=14536588)
        os.remove(prestamo)
        await interaction.response.send_message(embed=embed)
        os.chdir("..")
    except FileNotFoundError:
        embed = discord.Embed(title="Error", description="El prestamo no existe!", color=16711680)
        await interaction.response.send_message(embed=embed)
        os.chdir("..")

@bot.command(name="help", description="Lista de comandos disponibles")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title=f"Comandos prestamistas", description="Las funciones principales del bot es el almacenamiento de prestamos, como la creacion, revision y eliminacion de los mismos. \n \n Los comandos para dichas funciones son:", color=14536588)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1383663187601395793/b0f77d11e38a4049420a2b2356705cae.png?size=512")
    embed.add_field(name="crearprestamos", value="> Almacena informacion de un prestamo (Nombre del cliente, ID del cliente y monto solicitado) en archivos json", inline=False)
    embed.add_field(name="verprestamos", value="> Lista los prestamos almacenados", inline=False)                                                                                                                
    embed.add_field(name="infoprestamo", value="> Ver informacion de un prestamo almacenado", inline=False)
    embed.add_field(name="borrarprestamo", value="> Borrar un prestamo del almacenamiento", inline=False)
    await interaction.response.send_message(embed=embed)

client.run(token)
