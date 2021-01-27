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


def clearCanvas():
    canvas_list = scrollable_frame.grid_slaves()
    for l in canvas_list:
        l.destroy()


def populateWithButtons():
    rows = 9
    columns = 5
    buttons = [[Button() for j in range(columns)] for i in range(rows)]
    for i in range(0, rows):
        for j in range(0, columns):
            buttons[i][j] = Button(
                scrollable_frame, text=("%d,%d" % (i+1, j+1)))
            buttons[i][j].grid(row=i, column=j, sticky='news')


def getCoinResponse(name):
    response = requests.get(
        "https://api.coingecko.com/api/v3/coins/"+name)
    print("response taken!")
    return response.json()


def addRowInfo(row, name, abr, price, hourChange, dayChange, weekChange, marketCap):
    nameCol = Label(scrollable_frame, text=name)
    nameCol.grid(row=row, column=0, sticky="EW")

    abrCol = Label(scrollable_frame, text=abr)
    abrCol.grid(row=row, column=1, sticky="EW")

    priceCol = Label(scrollable_frame, text=price)
    priceCol.grid(row=row, column=2, sticky="EW")

    hourChangeCol = Label(scrollable_frame, text=hourChange)
    hourChangeCol.grid(row=row, column=3, sticky="EW")

    dayChangeCol = Label(scrollable_frame, text=dayChange)
    dayChangeCol.grid(row=row, column=4, sticky="EW")

    weekChangeCol = Label(scrollable_frame, text=weekChange)
    weekChangeCol.grid(row=row, column=5, sticky="EW")

    marketCapCol = Label(scrollable_frame, text=marketCap)
    marketCapCol.grid(row=row, column=6, sticky="EW")
    pass


def showPrices():
    list_of_coins = readSelectedCryptoCurrencies()
    clearCanvas()
    addRowInfo(0, "CryptoCurrency", "Abbreviation", "Price", "1h change",
               "24h change", "7d change", "market cap")
    for num, coin in enumerate(list_of_coins, 1):
        response = getCoinResponse(coin)
        addRowInfo(num, coin, "abr",
                   response["market_data"]["current_price"]["usd"],
                   response["market_data"]["price_change_percentage_1h_in_currency"]["usd"],
                   response["market_data"]["price_change_percentage_24h_in_currency"]["usd"],
                   response["market_data"]["price_change_percentage_7d_in_currency"]["usd"],
                   response["market_data"]["market_cap"]["usd"])
    for x in range(7):
        scrollable_frame.columnconfigure(x, weight=1)


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

lowerCanvas = Canvas(lowerFrame)
lowerCanvas.pack(side="left", fill="both", expand=True)

lowerScrl = Scrollbar(lowerFrame, orient="vertical", command=lowerCanvas.yview)
lowerScrl.pack(side="right", fill="y")

scrollable_frame = Frame(lowerCanvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: lowerCanvas.configure(
        scrollregion=lowerCanvas.bbox("all")
    )
)

lowerCanvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
lowerCanvas.configure(yscrollcommand=lowerScrl.set)


root.mainloop()
