"""
# Command
: /user user_id

# Param
str user_id: 유저 ID
"""
from discord import Embed
from discord import File
from discord import Interaction

import solvedac
from utils.logger import get_logger

user_log = get_logger("send.user")


async def send_user(interaction: Interaction, user_id: str, ephemeral: bool = False) -> None:
    await interaction.response.defer(ephemeral=ephemeral)

    try:
        user = solvedac.get_user(user_id=user_id)
    except solvedac.UserNotExistError:
        await interaction.followup.send(
            f"ERROR user id '{user_id}' does not exist"
        )
        user_log.warning(f"user does not exist: {user_id}")
        return

    files = []

    tier_icon = File(
        fp=f"resource/rank/{user.level}.png", filename=f"level_{user.level}.png"
    )
    files.append(tier_icon)

    embed = Embed(description=user.bio)
    if user.image_url is not None:
        profile_url = user.image_url
    else:
        profile_icon = File(
            fp="resource/default_profile.png", filename="default_profile.png"
        )
        files.append(profile_icon)
        profile_url = "attachment://default_profile.png"
    embed.set_author(name=user.name, url=user.url, icon_url=profile_url)
    embed.set_thumbnail(url=f"attachment://level_{user.level}.png")
    embed.set_image(url=user.background.image_url)

    if user.badge is not None:
        embed.set_footer(text=user.badge.name, icon_url=user.badge.image_url)
    embed.add_field(name="랭크", value=f"#{user.rank}", inline=True)

    org_text = "-"
    if user.organizations:
        org_text = ", ".join([org.name for org in user.organizations])
    embed.add_field(
        name="소속", value=org_text
    )

    embed.add_field(name="레이팅", value=user.rating, inline=True)
    embed.add_field(name="클래스", value=str(user.class_))
    embed.add_field(name="푼 문제", value=user.solved_count, inline=True)
    embed.add_field(name="최대 연속 풀이", value=user.max_streak, inline=True)
    embed.add_field(name="기여 문제 수", value=user.vote_count, inline=True)
    embed.add_field(name="라이벌 수", value=user.rival_count, inline=True)

    await interaction.followup.send(
        embed=embed, files=files
    )
    user_log.info(f"user found: {user_id}")
    return
