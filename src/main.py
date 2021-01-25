from tkinter import *
import requests


def pingCoinGecko():
    response = requests.get("https://api.coingecko.com/api/v3/ping")
    if response.status_code == 200:
        pingBox.configure(text="200 - Coin Gecko works")
    else:
        pingBox.configure(text="error, there might be a problem")


def pokus2():
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    file = open("all_crypto_currencies.txt", "w")
    for coin in response.json():
        file.write(coin["id"] + "\n")
    file.close()
    print("hotovo")


def readSelectedCryptoCurrencies():
    result = []
    file = open("selected_crypto_currencies.txt", "r")
    for coin in file.readlines():
        if coin[-1] == '\n':
            coin = coin[:-1]
        result.append(coin)
    file.close()
    return result


def showPrices():
    list_of_coins = readSelectedCryptoCurrencies()
    lowerListbox.delete(0, lowerListbox.size())
    for line in list_of_coins:
        lowerListbox.insert("end", "" + str(line) + " is: " + str(666))


startingHeight = 600
startingWidth = 400


root = Tk()

root.minsize(startingHeight, startingWidth)
root.wm_title("Crypto currency checker")
root.configure(bg="#00FFFF")

coinGeckoLabel = Label(
    root, text="Data is from the Coin Gecko API.", bg="#00FFFF")
coinGeckoLabel.place(relx=0.70, rely=0.95, relheight=0.05, relwidth=0.30)


app = Frame(root)
app.place(relx=0.05, rely=0.05, relheight=0.9, relwidth=0.9)


exitButton = Button(app, text="exit", command=root.destroy)
exitButton.place(relx=0.05, rely=0.05, relheight=0.1, relwidth=0.1)

minimizeButton = Button(app, text="minimize", command=root.destroy)
minimizeButton.place(relx=0.2, rely=0.05, relheight=0.1, relwidth=0.1)

pingButton = Button(app, text="ping", command=pingCoinGecko)
pingButton.place(relx=0.35, rely=0.05, relheight=0.1, relwidth=0.1)

pingBox = Label(app, anchor="w", justify="left", text="-output-")
pingBox.place(relx=0.5, rely=0.05, relheight=0.1, relwidth=0.5)

pokusButton2 = Button(app, text="coin ID's", command=pokus2)
pokusButton2.place(relx=0.85, rely=0.35, relheight=0.1, relwidth=0.1)

showPricesBtn = Button(app, text="show prices", command=showPrices)
showPricesBtn.place(relx=0.05, rely=0.35, relheight=0.1, relwidth=0.15)

lowerFrame = Frame(app, bg="#89cff0")
lowerFrame.place(relx=0, rely=0.5, relheight=0.5, relwidth=1)

lowerListbox = Listbox(lowerFrame)
lowerListbox.place(relwidth=1, relheight=1)

lowerScrl = Scrollbar(lowerFrame)
lowerScrl.pack(side="right", fill="y")
lowerScrl.config(command=lowerListbox.yview)


root.mainloop()
