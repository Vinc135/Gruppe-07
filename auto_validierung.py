import datetime


# validiert Werte für Auto-Attribute
def validiere_auto_wert(filter, neuer_wert, auto):
    error_message = ""

    if filter == None:
        error_message = "Ungültiger Filter. Bitte wenden Sie sich an den Support."

    if filter == "marke":

        if neuer_wert is None or auto is None or neuer_wert == "":
            error_message = "Bitte geben Sie einen gültigen Text ein."

    elif filter == "modell":

        if neuer_wert is None or auto is None or neuer_wert == "":
            error_message = "Bitte geben Sie einen gültigen Text ein."

    elif filter == "baujahr":

        try:
            neuer_wert = int(neuer_wert)

            if neuer_wert is None or auto is None or neuer_wert > datetime.date.today().year or neuer_wert < 1500:
                error_message = "Bitte geben Sie ein Jahr zwischen 1500 und Heute ein."

        except ValueError:
            error_message = "Bitte geben Sie ein Jahr zwischen 1500 und Heute ein."

    elif filter == "verbrauch":

        try:
            neuer_wert = float(neuer_wert.replace(",", "."))

            if neuer_wert is None or auto is None or neuer_wert < 0:
                error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."

        except ValueError:
            error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."

    elif filter == "tagespreis":

        try:
            neuer_wert = float(neuer_wert.replace(",", "."))

            if neuer_wert is None or auto is None or neuer_wert < 0:
                error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."

        except ValueError:
            error_message = "Bitte geben Sie einen gültigen Gleitkommawert über 0 ein."

    return neuer_wert, error_message
