def bot():
    comment = read()
    if comment == "/test":
        reply("It works!", "0")
    elif comment == "/hello":
        reply("Hello!", "0")
    else:
        pass

while True:
    bot()
    time.sleep(2)
