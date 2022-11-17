import discord
from discord.ext import commands
from discord.utils import get as util_get
import os
import time
import json
import logging

logger = logging.getLogger(__name__)

helpdesk_id = os.getenv('HELPDESK_ID')

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.helpdesk_id = os.getenv('HELPDESK_ID')
        self.message_id = os.getenv('ROLES_MESSAGE_ID')
        self.roles = {}
        f = open("/mnt/roles.json", "r")
        with f:
            self.roles = json.load(f)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        helpdesk = self.bot.get_channel(int(self.helpdesk_id))

        if payload.message_id == self.message_id and payload.member != self.bot.user:
            emote = payload.emoji.name

            guild = await self.bot.fetch_guild(payload.guild_id)
            roles = await guild.fetch_roles()
            user = payload.member
            for role in roles:
                if role.name == self.roles.get(emote):
                    # print("Attempted to add role " + role.name + " to " + user.name)
                    try:
                        await user.add_roles(role)
                        logger.info("Gave " + str(role.name) + " role to " + str(user.name))
                        confirmation = await helpdesk.send("Gave " + role.name + " role to " + user.name)
                        time.sleep(3)
                        await confirmation.delete()
                    except Exception as e:
                        error_message = await helpdesk.send(e)
                        # logger.error(error_message)
                        time.sleep(3)
                        await error_message.delete()

    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):

    #     helpdesk = self.bot.get_channel(int(self.helpdesk_id))
    #     role, user = await self.parse_payload(payload)
    #     await helpdesk.send("role: " + str(role) + " user: " + str(user))
    
    #     try:
    #         await user.remove_roles(role)
    #         logger.info("Removed " + role.name + " role from " + user.name)
    #         confirmation = await helpdesk.send("Removed " + role.name + " role from " + user.name)
    #         time.sleep(3)
    #         await confirmation.delete()
    #     except Exception as e:
    #         error_message = await helpdesk.send("Error removing " + str(e))
    #         logger.error("Problem removing role: " + str(error_message))
    #         time.sleep(3)
    #         await error_message.delete()

    @commands.command(name='add-role', help='adds a role in helpdesk')
    async def add_role(self, ctx, *args):
        if(ctx.message.author.guild_permissions.administrator):
            helpdesk = self.bot.get_channel(int(self.helpdesk_id))

            self.roles[args[1]] = args[0]
            with open("/mnt/roles.json", "w") as f:
                f.write(json.dumps(self.roles))
            self.generate()
        else:
            await ctx.send("You do not have permission, server admins will be notified of this incident 😠") 

    @commands.command(name='generate-roles', help='generates message for roles')
    async def generate(self, ctx):
            helpdesk = self.bot.get_channel(int(self.helpdesk_id))
            message = "**React here to get these roles** \n"
            for key, val in self.roles.items():
                message += "`" + val + "` - " + key + "\n"
            message += "\n"
            roles_message = await helpdesk.send(message)
            self.message_id = roles_message.id
            for emote in self.roles:
                await roles_message.add_reaction(emote)

    @commands.command(name='refresh-roles', help='refresh role list')
    async def refresh_roles(self, ctx):
        with open("/mnt/roles.json", "w") as f:
            f.write(json.dumps(self.roles))
        await ctx.send(self.roles)
    
    @commands.command(name='purge-roles', help='purge all roles in helpdesk')
    async def purge(self, ctx):
        if(ctx.message.author.guild_permissions.administrator):
            self.roles = {}
            await ctx.send(self.roles)
        else:
            await ctx.send("Permission denied")

    @commands.command(name='remove-role', help='deletes role from list')
    async def purge(self, ctx, *, role_name):
        if(ctx.message.author.guild_permissions.administrator):
            self.roles.pop(role_name)
            await ctx.send(self.roles)
        else:
            await ctx.send("Permission denied")

    @commands.command(name='roles', help='get list of roles')
    async def roles(self, ctx):
        await ctx.send("```" + str(self.roles) + "```")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = await self.bot.fetch_guild(payload.guild_id)
        # user = await self.bot.fetch_user(payload.user_id)
        member = await guild.fetch_member(payload.user_id)
        emote = payload.emoji.name
        roles = await guild.fetch_roles()
        
        if payload.message_id == self.message_id and payload.member != self.bot.user:
            for role in roles:
                if role.name == self.roles.get(emote):
                    await member.remove_roles(role)


    # async def parse_payload(self, payload: discord.RawReactionActionEvent):
    #     if payload.message_id == self.message_id and payload.member != self.bot.user:
    #         emote = payload.emoji.name

    #         guild = await
    #         roles = await guild.fetch_roles()
    #         user = guild.get_member(payload.user_id)
    #         logger.info("parse_payload user id: " + str(payload.user_id))

    #         for role in roles:
    #             if role.name == self.roles.get(emote):
    #                 return role, user

    #     return None, None 