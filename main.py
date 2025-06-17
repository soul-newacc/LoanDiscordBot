import os
import json
import discord
from discord.ext import commands
from discord import app_commands
from config import token # this was easier for me than a .env or a lil lines of code for a .json

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(synced)
    except Exception as e:
        print(e)

@bot.tree.command(name="crearprestamo", description="crea prestamos pues!!")
async def ping(interaction: discord.Interaction, nombre: str, id: str, monto: str):
    data = {"Nombre": nombre, "ID": id, "Monto": monto}
    nom = nombre+".json"
    os.chdir("loans")
    with open(nom, "w") as file:
        json.dump(data, file, indent=4)
    embed = discord.Embed(title="Operacion exitosa! ✅:", description=f"Guardado en {nom}", color=14536588)
    await interaction.response.send_message(embed=embed)
    os.chdir("..")

@bot.tree.command(name="verprestamos", description="ver prestamos pues!!")
async def verprestamos(interaction: discord.Interaction):
    os.chdir("loans")
    prestamos = os.listdir()
    embed = discord.Embed(title="Los prestamos disponibles son:", description=f"{prestamos}", color=14536588)
    await interaction.response.send_message(embed=embed)
    os.chdir("..")

@bot.tree.command(name="infoprestamo", description="ver info de un prestamo en especifico")
@app_commands.describe(prestamoo="Especificar prestamo con nombre del archivo completo, ej: Moserati.json")
async def infoprestamo(interaction: discord.Interaction, prestamoo: str):
    os.chdir("loans")
    prestamo = json.load(open(prestamoo))
    embed = discord.Embed(title=f"{prestamoo}", description=f"{json.dumps(prestamo, indent=4)}", color=14536588)
    await interaction.response.send_message(embed=embed)
    os.chdir("..")

@bot.tree.command(name="borrarprestamo", description="borrar un prestamo pues!")
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

bot.run(token)
