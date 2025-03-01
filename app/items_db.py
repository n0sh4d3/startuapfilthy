NAME = "name"
DESCRIPTION = "description"
PRICE = "price"
SIZE = "size"

#najebalem tych itemow zeby zobaczyc jak strona bedzie wyblafac
def get_shop_items() -> list[dict[str, any]]:
    
    shop_items = [
        {
            NAME: "spust pycha",
            DESCRIPTION: "nie wiem co sie dzieje ale kurwa buja nie",
            PRICE: 21.37,
        },
        {
            NAME: "brudna woda",
            DESCRIPTION: "nazwa muwi sama za sb",
            PRICE: 20.99,
        },
        {
            NAME: "order cwela",
            DESCRIPTION: "ciezko zapracowalem na ten tytul",
            PRICE: 90.99,
        },
        {
            NAME: "zestaw goonera",
            DESCRIPTION: "zeby hojnie zyc trzeba hojnie wydac",
            PRICE: "gratis", # robiac to licze sie z faktem ze kosz sie rozjebie ale to smiesznie
        },
        {
            NAME: "cyberszlug",
            DESCRIPTION: "smakowe poietrze goes brrrrr",
            PRICE: 1.99,
        },
        {
            NAME: "chinska republika ludowa",
            DESCRIPTION: "Zǎoshang hǎo zhōngguó xiànzài wǒ yǒu BING CHILLING 🥶🍦 wǒ hěn xǐhuān BING CHILLING 🥶🍦",
            PRICE: 4.50,
        },
        {
            NAME: "samohud",
            DESCRIPTION: "ten ruw wyglada bardzo hottt",
            PRICE: 1999.99,
        },
    ]
    return shop_items