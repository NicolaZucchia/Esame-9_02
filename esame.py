# ogni giorno ha almeno una time series, e ogni time series appartiene allo stesso mese di dati, non serve controllare questi due fattori per alzare eccezioni (i dati partono dal primo del mese all'ultimo)


class CSVTimeSeriesFile:

    def __init__ (self, name):

        self.name = name
    
    def get_data(self):
        
        # apro il file verificando che tale file esista e che venga correttamente inserito l'input
        try:
            f = open(self.name, 'r')
        except:
            raise ExamException('ERRORE: è stato scelto di aprire un file inesistente o illegibile! ')
        
        lista_di_liste = [] # immagazzina i time_series di tutto il file
        time_series = [] # immagazzina un time_series [epoch, temperatura]
        
        # separo i valori nel file tra epoch e temperature e creo la lista di liste
        for line in f:
            # verifico che la linea non sia vuota
            try:
                line = line.split(',')
            except:
                continue

            if len(line) != 2:
                continue # una linea deve avere 1 epoch e 1 temperatura, altrimenti non può essere considerata valida
            try:
                epoch = int(line[0]) # converto a intero senza gestire eccezione
            except:
                continue 
            try:
                temperature = float(line[1])
            except (ValueError, TypeError, FloatingPointError):
                continue
            
            time_series = [epoch, temperature]
            
            lista_di_liste.append(time_series)
        
        f.close()

        # la lista delle coppie [epoch, temperature] non può essere vuota
        if (len(lista_di_liste) == 0):
            raise ExamException("ERRORE: Deve esserci almeno un valore valido di epoch e uno di temperatura! ")

        # controllo che gli epoch siano in ordine strettamente crescente
        # crescenza => ordinati, stretta => non ci sono doppioni, se mancano una o entrambe queste condizioni alzo l'eccezione
        for i in range(0, len(lista_di_liste)-1):
            element = lista_di_liste[i]
            next_element = lista_di_liste[i+1]
            epoch = element[0]
            next_epoch = next_element[0]
            if epoch >= next_epoch:
                raise ExamException("Gli epoch non sono in ordine crescente e/o ce n'è almeno uno che si presenta più di una volta! ")

        return lista_di_liste

                   
        
# classe che gestisce le eccezioni
class ExamException(Exception):
    pass


# calcola l'inizio del giorno in epoch
def check_day(epoch):
    
    day_start_epoch = epoch - (epoch % 86400)
    return day_start_epoch

# calcola le statistiche per ogni lista di valori giornalieri
def statistics(lista):

    min = lista[0]
    max = lista[0]
    mean = 0
    values = []

    for element in lista:
        if element < min:
            min = element
        elif element > max:
            max = element
        mean += element
    mean /= len(lista)
    
    values.append(min)
    values.append(max)
    values.append(mean)

    if (min > max):
        raise ExamException('Ops, qualcosa è andato storto! ')
    
    return values

# funzione che separa le temperature in base ai giorni e ritorna la nuova lista di liste
def daily_stats(lista):

    day = 1 # tengo traccia del giorno del mese a cui mi trovo

    beginning_epoch = lista[0][0]
    current_day_start = check_day(beginning_epoch) # inizializzo il primo giorno

    temps = [] # lista di tutte le temperature
    list_of_days = [] # lista con i giorni del mese al posto degli epoch


    # controllo il passaggio di giorno in epoch e creo una lista dei giorni del mese a cui si riferiscono le temperature al posto degli epoch
    # faccio la lista con tutte le temperature del mese
    for i in range(0, len(lista)):

        element = lista[i] # coppia [epoch, temperatura]
        item = [] # lista dei valori del singolo giorno
        current_epoch = element[0]
        current_temp = element[1]

        # controllo che le temperature siano int o float per inserirle nella lista globale delle temperature
        if (type(current_temp)==int or type(current_temp)==float):
            temps.append(current_temp)
        # se le temperature non sono int o float semplicemente le salto senza alzare eccezioni

        if (current_epoch - current_day_start >= 86400): # condizione di passaggio al giorno successivo
            day += 1 # scorro i giorni del mese verificando con gli epoch il passaggio al giorno successivo
            current_day_start = check_day(current_epoch) # se è cambiato il giorno, aggiorno l'inizio del giorno in cui mi trovo in epoch
        
        list_of_days.append(day) # nella nuova lista appendo il giorno al posto dell'epoch dopo la verifica del giorno

    days_in_the_month = list_of_days[-1] # prende il giorno dell'ultima cella, ci dice quanti giorni ha quel mese
    temp_count_per_day = []
    n = 1

    while (n < days_in_the_month):

        count = list_of_days.index(n+1)-list_of_days.index(n) # conto il numero di misurazioni di temperatura per ogni giorno
        temp_count_per_day.append(count) # e lo aggiungo alla lista
        n += 1
    
    last_day = len(lista) - list_of_days.index(n) # gestisco il numero di misurazioni dell'ultimo giorno, non gestito dal while
    temp_count_per_day.append(last_day)

    # ho il numero di misurazioni di temperatura giorno per giorno, ora devo creare le liste di temperature e farci i conti statistici ????

    temperatures = []

    # ciclo che separa i valori di temperature in liste contenenti tutti e soli i valori per un dato giorno, per ogni giorno del mese
    i = 0 # indice che scorre tutte le temperature del mese
    for element in temp_count_per_day: # per ogni giorno del mese, espresso come numero di temperature registrate quel giorno
        a = 0 # misure di quel giorno considerate
        pos = []
        while (a < element): # finchè non ho considerato il numero di misurazioni di quel giorno
            temp = temps[i]
            pos.append(temp) # aggiungo alla lista delle temperature di quel giorno
            i += 1 # incremento la variabile globale di daily_stats
            a += 1 # incremento la variabile locale
        temperatures.append(pos) # aggiungo alla lista delle liste pos

    # applico la funzione che calcola minimo, massimo e media e restituisco la lista di liste finale
    result = []
    for element in temperatures:
        calculated_stats = statistics(element)
        result.append(calculated_stats)

    return result
     
'''
time_series_file = CSVTimeSeriesFile('data.csv')
time_series = time_series_file.get_data()
x = daily_stats(time_series)
print(x)
'''