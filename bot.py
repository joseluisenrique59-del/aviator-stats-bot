    import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from statistics import mean

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "10000"))

logging.basicConfig(level=logging.INFO)

results = {}


def menu():
    keyboard = [
        [
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
            InlineKeyboardButton("➕ Add", callback_data="add"),
        ],
        [
            InlineKeyboardButton("🕐 Last", callback_data="last"),
            InlineKeyboardButton("🗑️ Reset", callback_data="reset"),
        ],
        [InlineKeyboardButton("📖 Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Byenveni nan Aviator Stats Bot!\n\n"
        "Chwazi yon bouton anba a:",
        reply_markup=menu(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Kijan pou itilize bot la:\n\n"
        "/add 1.25 — ajoute multiplier\n"
        "/stats — wè estatistik\n"
        "/last — wè dènye rezilta yo\n"
        "/reset — efase rezilta yo\n\n"
        "⚠️ Estatistik yo pa predi pwochen wonn lan.",
        reply_markup=menu(),
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "❌ Egzanp: /add 2.35",
            reply_markup=menu(),
        )
        return

    try:
        value = float(context.args[0])
        if value < 1:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "❌ Mete yon nimewo ≥ 1.\nEgzanp: /add 1.75",
            reply_markup=menu(),
        )
        return

    results.setdefault(user_id, []).append(value)

    await update.message.reply_text(
        f"✅ {value:.2f}x ajoute.\n"
        f"📊 Total wonn: {len(results[user_id])}",
        reply_markup=menu(),
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = results.get(user_id, [])

    if not data:
        await update.message.reply_text(
            "📭 Ou poko ajoute okenn multiplier.",
            reply_markup=menu(),
        )
        return

    avg = mean(data)
    lowest = min(data)
    highest = max(data)
    under_2 = sum(x < 2 for x in data)
    percent = under_2 / len(data) * 100

    await update.message.reply_text(
        "📊 AVIATOR STATISTICS\n\n"
        f"🎯 Wonn: {len(data)}\n"
        f"📈 Mwayèn: {avg:.2f}x\n"
        f"⬇️ Pi ba: {lowest:.2f}x\n"
        f"⬆️ Pi wo: {highest:.2f}x\n"
        f"🔻 Anba 2x: {under_2} ({percent:.1f}%)\n\n"
        "⚠️ Sa se estatistik istorik sèlman.",
        reply_markup=menu(),
    )


async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = results.get(user_id, [])

    if not data:
        await update.message.reply_text(
            "📭 Ou poko gen okenn rezilta.",
            reply_markup=menu(),
        )
        return

    text = "🕐 10 DÈNYE MULTIPLIER YO\n\n"

    for i, value in enumerate(data[-10:], 1):
        text += f"{i}. {value:.2f}x\n"

    await update.message.reply_text(
        text,
        reply_markup=menu(),
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    results[user_id] = []

    await update.message.reply_text(
        "🗑️ Tout rezilta ou yo efase.",
        reply_markup=menu(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = results.get(user_id, [])

    if query.data == "stats":
        if not data:
            text = "📭 Ou poko ajoute okenn multiplier."
        else:
            avg = mean(data)
            lowest = min(data)
            highest = max(data)
            under_2 = sum(x < 2 for x in data)
            percent = under_2 / len(data) * 100

            text = (
                "📊 AVIATOR STATISTICS\n\n"
                f"🎯 Wonn: {len(data)}\n"
                f"📈 Mwayèn: {avg:.2f}x\n"
                f"⬇️ Pi ba: {lowest:.2f}x\n"
                f"⬆️ Pi wo: {highest:.2f}x\n"
                f"🔻 Anba 2x: {under_2} ({percent:.1f}%)"
            )

        await query.edit_message_text(text, reply_markup=menu())

    elif query.data == "add":
        await query.edit_message_text(
            "➕ Ekri:\n\n/add 1.50",
            reply_markup=menu(),
        )

    elif query.data == "last":
        if not data:
            text = "📭 Ou poko gen okenn rezilta."
        else:
            text = "🕐 10 DÈNYE MULTIPLIER YO\n\n"
            for i, value in enumerate(data[-10:], 1):
                text += f
