---
name: ig-human
description: >-
  Toglie da una bozza l'impronta della macchina (trattini lunghi, parole di
  repertorio da IA, caratteri invisibili) e la valuta su un pannello di cinque
  controlli prima che esca. Usala quando un testo deve sembrare umano, quando
  l'utente dice "rendilo umano", "sembra scritto da ChatGPT", "togli i trattini",
  "pulisci questo testo", e sempre prima di mostrare una didascalia, un copione,
  un commento, una risposta o un DM. Funziona in italiano e in inglese.
---

# ig-human

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT).

- **Script.** Se `humanize.py`, `detect.py` e `slop.json` stanno accanto a
  questo file, usali da lì. Altrimenti scarica il pacchetto una volta per
  sessione in una cartella temporanea (lo scratchpad se c'è, altrimenti /tmp),
  mai nel progetto dell'utente:

```bash
T="<cartella temporanea>/ig-tools"
[ -d "$T/repo" ] || git clone --depth 1 https://github.com/leonardo23berto23/instagram-agent-skill "$T/repo"
H="$T/repo/skills/ig-human"
```

  È codice scaricato: tieni le bozze in un'altra cartella ed esegui con
  `python3 -I`. Nessuna dipendenza, niente rete.
- **Lingua.** Rilevata da sola; `--lang it|en` per forzarla. Il lessico ha
  voci separate per lingua, così "innovative" in italiano non diventa "new".

## Gli strumenti

```bash
python3 -I "$H/humanize.py" bozza.txt --report        # pulisce e mostra cosa ha cambiato
python3 -I "$H/detect.py" bozza.txt                    # valuta su cinque controlli
python3 -I "$H/detect.py" prima.txt dopo.txt           # mostra la differenza
```

Entrambi leggono `slop.json`: le voci inglesi originali, circa 90 voci
italiane, 18 classi di caratteri invisibili, 13 sostituzioni tipografiche e
30 tic strutturali. Ci sono anche le voci tipiche dei testi per attività
locali ("nel cuore di", "tradizione e innovazione", "passione e dedizione").
È fatto per essere modificato: se l'utente usa davvero una parola che il
lessico toglie, cancellala dal file (nella copia della sessione).

## Perché su Instagram conta più di quanto sembri

Le didascalie sono corte e i copioni si dicono ad alta voce. Una frase da
macchina in una didascalia di 600 caratteri pesa di più che in un saggio, e un
voiceover che nessuno direbbe così si sente alla prima ripresa. Il segnale non
è un rilevatore che segnala il post: è una persona che scorre via davanti a una
cosa che sembra una brochure, o un creator che inciampa nel suo stesso copione.

## Cosa si sistema in automatico

**1. Caratteri invisibili.** Spazi a larghezza zero, joiner, trattini morbidi,
BOM, caratteri tag Unicode, spazi rigidi e stretti. Una tastiera non li
produce, sopravvivono al copia-incolla e sono il segno più meccanico di un testo
generato. `humanize.py` li elimina tutti.

**2. Tipografia.** Trattino lungo in virgola, trattino medio in trattino,
virgolette tipografiche (anche « ») in dritte, puntini di sospensione in tre
punti, pallino in trattino.

**3. Il lessico di repertorio.** delve, leverage, seamless; e in italiano
cruciale, sinergia, ottimizzare, a 360 gradi, nel mondo frenetico di oggi,
un'esperienza unica, seguici per altri consigli. Ognuna sostituita con una
parola semplice o eliminata, mantenendo le maiuscole e lasciando intatti i link.
Gli aggettivi si eliminano invece di sostituirli, perché il genere non si
indovina ("un'atmosfera indimenticabile" diventa "un'atmosfera").

## Cosa NON si sistema in automatico

I tic strutturali vengono **segnalati, non riscritti**, perché cambiare la forma
di una frase richiede giudizio:

- "Non è solo X, è Y", "Non è un X. È Y.", "non solo X ma anche Y"
- Triadi da regola del tre ("veloce, semplice e sicuro.")
- Righe con domanda retorica che prepara la risposta ("Il risultato?",
  "Perché è così importante?")
- Il preambolo da video: "in questo video vi parlo di"
- "Andiamo a vedere" e simili
- Elenchi con emoji al posto dei punti
- Tre o più parole urlate di fila
- Muri di hashtag
- Richieste di riflesso: "seguimi per altri", "tagga un amico che", "metti like se"
- Inviti da volantino: "scopri di più", "non perdere l'occasione" (solo
  segnalati, perché stanno quasi sempre a metà frase)
- Coppie da brochure: "tradizione e innovazione", "qualità e cortesia"

Questa lista è il tuo lavoro. Riscrivi a mano ogni riga segnalata, mantenendo
il senso, poi rilancia `detect.py`. È la parte che porta il punteggio da DA
RIVEDERE a PASSA, ed è quella che uno script non può fare.

## I cinque controlli

`detect.py` dà a cinque segnali un punteggio da 0 a 100, più alto è più umano:

| controllo | cosa misura | da macchina sembra |
| --- | --- | --- |
| VARIAZIONE | quanto varia la lunghezza delle frasi | frasi tutte uguali |
| CONCRETEZZA | numeri (anche scritti in lettere), nomi, elementi concreti ogni 100 parole | nomi astratti, nessuna cifra |
| REPERTORIO | voci del lessico ogni 100 parole | vocabolario di repertorio |
| IMPRONTA | invisibili, trattini lunghi, virgolette tipografiche ogni 1000 caratteri | tipograficamente perfetto |
| VOCE | in italiano: segnali di parlato e forme di prima e seconda persona; in inglese: contrazioni e pronomi; più i tic strutturali | nessun segnale di parlato, rivelazioni costruite |

Il verdetto pesa la media al 60% e il **controllo più debole** al 40%, perché
basta un segnale. PASSA richiede almeno 70 e nessun controllo sotto 55;
DA RIVEDERE da 50; sotto è SEGNALATO.

Attenzione sui copioni parlati: VARIAZIONE penalizza le righe brevi, che in un
copione sono volute. Lì conta di più `beats.py` di /ig-reel; dillo invece di
allungare le frasi a forza.

## Dillo onestamente

Sono cinque euristiche locali modellate sui segnali che usano i rilevatori
pubblici. Girano in locale e non caricano niente. **Non** sono GPTZero,
Originality, Copyleaks, Winston o Turnitin, non chiamano le loro API e non
possono promettere i loro verdetti. Sistemare quello che misurano tende a
spostare anche quei numeri, perché misurano le stesse cose. Questo è quello che
si può dire. Non dire di più a nome dell'utente, e non dirgli che il testo è
"non rilevabile".

## Ordine delle operazioni

1. `humanize.py bozza.txt -o pulita.txt --report`
2. Leggi i tic strutturali. Riscrivi tu quelle righe.
3. `detect.py bozza.txt pulita.txt` per mostrare prima e dopo.
4. Se il verdetto non è PASSA, sistema il controllo più debole indicato e
   rifai. Due giri sono normali. Cinque vogliono dire che la bozza era scritta
   a formula, e la soluzione è un'altra bozza, non altri giri.
5. Mostra all'utente il testo pulito e il punteggio. Mai solo il punteggio.
