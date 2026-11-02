from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        # 1. Chiedo la connessione al database usando la funzione helper del package database
        cnx = get_connection()
        if cnx is None:
            # Se la connessione fallisce (es. server XAMPP spento), restituisco None
            return None

        strumenti = []
        try:
            # Uso dictionary=True per accedere ai campi del record come le chiavi di un dizionario
            cursor = cnx.cursor(dictionary=True)

            # 2. Eseguo la query SQL per estrarre tutti gli strumenti
            query = "SELECT codice, tipo, marca, anno_acquisto, valore, disponibile FROM strumento"
            cursor.execute(query)

            # 3. Trasformo ogni riga del DB in un oggetto della classe Strumento
            for row in cursor.fetchall():
                s = Strumento(
                    codice=row["codice"],
                    tipo=row["tipo"],
                    marca=row["marca"],
                    anno_acquisto=row["anno_acquisto"],
                    valore=row["valore"],
                    disponibile=bool(row["disponibile"])
                )
                strumenti.append(s)

            cursor.close()
            cnx.close()
            return strumenti

        except Exception as e:
            print(f"Errore durante la lettura degli strumenti dal DB: {e}")
            if cnx.is_connected():
                cnx.close()
            return None

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
    
        # Mi connetto al DB
        cnx = get_connection()
        if cnx is None:
            return None

        strumenti = []
        try:
            cursor = cnx.cursor(dictionary=True)

            # Query parametrizzata con %s per evitare SQL Injection. 
            # Uso LOWER() in SQL per fare in modo che la ricerca non sia case-sensitive
            query = """
                        SELECT codice, tipo, marca, anno_acquisto, valore, disponibile 
                        FROM strumento 
                        WHERE LOWER(tipo) = LOWER(%s)
                    """
            cursor.execute(query, (tipo,))

            # Converto i risultati ottenuti in oggetti Strumento
            for row in cursor.fetchall():
                s = Strumento(
                    codice=row["codice"],
                    tipo=row["tipo"],
                    marca=row["marca"],
                    anno_acquisto=row["anno_acquisto"],
                    valore=row["valore"],
                    disponibile=bool(row["disponibile"])
                )
                strumenti.append(s)

            cursor.close()
            cnx.close()
            return strumenti

        except Exception as e:
            print(f"Errore durante la ricerca per tipo: {e}")
            if cnx.is_connected():
                cnx.close()
            return None
