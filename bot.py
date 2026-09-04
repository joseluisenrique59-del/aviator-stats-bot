import os
import logging
from statistics import mean

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Stores results separately for each Telegram user
results = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Byenveni nan Aviator Stats Bot!\n\n"
        "Mwen ede w analize multiplier ou antre yo.\n\n"
        "Kòmand:\n"
        "/add 1.50 - ajoute yon multiplier\n"
        "/stats - wè estatistik yo\n"
        "/last - wè dènye rezilta yo\n"
        "/reset - efase rezilta yo\n"
        "/help - èd\n\n"
        "⚠️ Estatistik yo pa garanti pwochen rezilta Aviator."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Kijan pou itilize bot la:\n\n"
        "1️⃣ /add 1.25\n"
        "2️⃣ /add 2.40\n"
        "3️⃣ /add 1.08\n\n"
        "Apre sa itilize /stats pou wè analiz la."
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "❌ Mete multiplier la.\n"
            "Egzanp: /add 2.35"
        )
        return

    try:
        value = float(context.args[0])

        if value < 1:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "❌ Multiplier la dwe yon nimewo ≥ 1.\n"
            "Egzanp: /add 1.75"
        )
        return

    results.setdefault(user_id, []).append(value)

    total = len(results[user_id])

    await update.message.reply_text(
        f"✅ {value:.2f}x ajoute.\n"
        f"📊 Total wonn: {total}"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = results.get(user_id, [])

    if not data:
        await update.message.reply_text(
            "📭 Ou poko ajoute okenn multiplier."
        )
        return

    avg = mean(data)
    lowest = min(data)
    highest = max(data)

    under_2 = sum(x < 2 for x in data)
    under_2_percent = (under_2 / len(data)) * 100

    await update.message.reply_text(
        "📊 AVIATOR STATISTICS\n\n"
        f"🎯 Wonn: {len(data)}\n"
        f"📈 Mwayèn: {avg:.2f}x\n"
        f"⬇️ Pi ba: {lowest:.2f}x\n"
        f"⬆️ Pi wo: {highest:.2f}x\n"
        f"🔻 Anba 2x: {under_2} ({under_2_percent:.1f}%)\n\n"
        "⚠️ Sa se estatistik istorik sèlman; "
        "li pa predi pwochen wonn lan."
    )


async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = results.get(user_id, [])

    if not data:
        await update.message.reply_text(
            "📭 Ou poko gen okenn rezilta."
        )
        return

    recent = data[-10:]

    text = "🕐 10 DÈNYE MULTIPLIER YO\n\n"

    for i, value in enumerate(recent, start=1):
        text += f"{i}. {value:.2f}x\n"

    await update.message.reply_text(text)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    results[user_id] = []

    await update.message.reply_text(
        "🗑️ Tout rezilta ou yo efase."
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN pa defini."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("last", last))
    app.add_handler(CommandHandler("reset", reset))

    print("🤖 Bot la ap mache...")
    app.run_polling()


if __name__ == "__main__":
    main()import os
import logging
from statistics import mean

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Stores results separately for each Telegram user
results = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Byenveni nan Aviator Stats Bot!\n\n"
        "Mwen ede w analize multiplier ou antre yo.\n\n"
        "Kòmand:\n"
        "/add 1.50 - ajoute yon multiplier\n"
        "/stats - wè estatistik yo\n"
        "/last - wè dènye rezilta yo\n"
        "/reset - efase rezilta yo\n"
        "/help - èd\n\n"
        "⚠️ Estatistik yo pa garanti pwochen rezilta Aviator."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Kijan pou itilize bot la:\n\n"
        "1️⃣ /add 1.25\n"
        "2️⃣ /add 2.40\n"
        "3️⃣ /add 1.08\n\n"
        "Apre sa itilize /stats pou wè analiz la."
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "❌ Mete multiplier la.\n"
            "Egzanp: /add 2.35"
        )
        return

    try:
        value = float(context.args[0])

        if value < 1:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "❌ Multiplier la dwe yon nimewo ≥ 1.\n"
            "Egzanp: /add 1.75"
        )
        return

    results.setdefault(user_id, []).append(value)

    total = len(results[user_id])

    await update.message.reply_text(
        f"✅ {value:.2f}x ajoute.\n"
        f"📊 Total wonn: {total}"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = results.get(user_id, [])

    if not data:
        await update.message.reply_text(
            "📭 Ou poko ajoute okenn multiplier."
        )
        return

    avg = mean(data)
    lowest = min(data)
    highest = max(data)

    under_2 = sum(x < 2 for x in data)
    under_2_percent = (under_2 / len(data)) * 100

    await update.message.reply_text(
        "📊 AVIATOR STATISTICS\n\n"
        f"🎯 Wonn: {len(data)}\n"
        f"📈 Mwayèn: {avg:.2f}x\n"
        f"⬇️ Pi ba: {lowest:.2f}x\n"
        f"⬆️ Pi wo: {highest:.2f}x\n"
        f"🔻 Anba 2x: {under_2} ({under_2_percent:.1f}%)\n\n"
        "⚠️ Sa se estatistik istorik sèlman; "
        "li pa predi pwochen wonn lan."
    )


async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = results.get(user_id, [])

    if not data:
        await update.message.reply_text(
            "📭 Ou poko gen okenn rezilta."
        )
        return

    recent = data[-10:]

    text = "🕐 10 DÈNYE MULTIPLIER YO\n\n"

    for i, value in enumerate(recent, start=1):
        text += f"{i}. {value:.2f}x\n"

    await update.message.reply_text(text)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    results[user_id] = []

    await update.message.reply_text(
        "🗑️ Tout rezilta ou yo efase."
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN pa defini."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("last", last))
    app.add_handler(CommandHandler("reset", reset))

    print("🤖 Bot la ap mache...")
    app.run_polling()


if __name__ == "__main__":
    main()
