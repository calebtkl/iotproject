from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import difflib

def echo(update, context):
    user = update.message.from_user
    text = update.message.text.lower()

    # Predefined prompts
    prompts = ["hello", "hi", "bye"]
    closest_prompt = difflib.get_close_matches(text, prompts, n=1, cutoff=0.6)

    if closest_prompt:  # Check if the list is not empty
        if closest_prompt[0] == "hello":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello, {user.first_name}!")
        elif closest_prompt[0] == "bye":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Goodbye, {user.first_name}!")
        elif closest_prompt[0] == "status":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Goodbye, {user.first_name}!")
        elif closest_prompt[0] == "line":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Goodbye, {user.first_name}!")
        elif closest_prompt[0] == "scatter":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Goodbye, {user.first_name}!")
        elif closest_prompt[0] == "bye":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Goodbye, {user.first_name}!")
        elif closest_prompt[0] == "bye":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Goodbye, {user.first_name}!")

def cleanliness(update, context):
    # Send a message indicating the processing has started
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing cleanliness...")

    # Assuming 'data_processing.py' contains the data processing and ML logic
    from five import process_cleanliness
    process_cleanliness(update, context)


def main():
    # Insert your bot token here
    token = '6863388801:AAFwSmM_0FaXSMDJ7cjgbP0FNJo3qTu-plI'

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('cleanliness', cleanliness))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

