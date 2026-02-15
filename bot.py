from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

TOKEN = "8370187679:AAHsKUqXOqcBY5qlbkitQlvW1Hw8b7heykM"

members = ["Gehan", "Rashen", "Dinusha"]
expenses = []

def yen(amount):
    return f"¥{amount:,}"

# START command (show all commands)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🏠 Apartment Expense Bot

Commands:

/add NAME CATEGORY AMOUNT
Example:
/add Gehan apartment 50000

/paid CATEGORY
/edit CATEGORY NEW_AMOUNT
/unpaid
/summary
"""
    await update.message.reply_text(text)

# ADD expense
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        name = context.args[0]
        category = context.args[1]
        amount = int(context.args[2])

        if name not in members:
            await update.message.reply_text("❌ Unknown member")
            return

        expenses.append({
            "name": name,
            "category": category,
            "amount": amount,
            "paid": False
        })

        await update.message.reply_text(
            f"✅ Added: {name} - {category} - {yen(amount)}"
        )
    except:
        await update.message.reply_text("Usage: /add Gehan apartment 50000")

# MARK PAID
async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.args[0]

    for e in expenses:
        if e["category"] == category:
            e["paid"] = True

    await update.message.reply_text("✅ Bill marked as paid")

# EDIT
async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.args[0]
    new_amount = int(context.args[1])

    for e in expenses:
        if e["category"] == category:
            e["amount"] = new_amount

    await update.message.reply_text("✏️ Amount updated")

# UNPAID
async def unpaid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "❌ Unpaid Bills:\n"

    for e in expenses:
        if not e["paid"]:
            text += f"{e['name']} - {e['category']} - {yen(e['amount'])}\n"

    await update.message.reply_text(text)

# SUMMARY + DEBT
async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE):

    total = sum(e["amount"] for e in expenses)
    if total == 0:
        await update.message.reply_text("No expenses yet")
        return

    per_person = total / len(members)

    paid_amount = {m:0 for m in members}

    for e in expenses:
        paid_amount[e["name"]] += e["amount"]

    text = f"📊 Total: {yen(total)}\nEach share: {yen(int(per_person))}\n\n"

    for m in members:
        diff = paid_amount[m] - per_person

        if diff > 0:
            text += f"{m} should receive {yen(int(diff))}\n"
        elif diff < 0:
            text += f"{m} should pay {yen(int(-diff))}\n"
        else:
            text += f"{m} balanced\n"

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("paid", paid))
app.add_handler(CommandHandler("edit", edit))
app.add_handler(CommandHandler("unpaid", unpaid))
app.add_handler(CommandHandler("summary", summary))

print("Bot running...")
app.run_polling()
