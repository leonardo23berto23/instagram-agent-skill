---
name: ig-viral
description: >-
  Va a cercare i reel che stanno funzionando adesso nella nicchia dell'utente,
  li mette in classifica per quanto hanno superato la mediana del proprio
  account, dà un nome alla formula dell'hook e ne fa uno swipe file da cui
  girare. Usala quando l'utente dice "trova i video virali", "cosa funziona
  adesso", "cosa pubblicano nella mia nicchia", "analizza questo account",
  "fammi uno swipe file", "perché questo reel fa numeri", o chiede cosa fare
  dopo e non ha prove su cui decidere.
---

# ig-viral

La skill di ricerca. Le altre del pacchetto scrivono; questa va a guardare.
Una volta al mese, non ogni giorno: le formule durano una stagione.

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT).

- **Script.** `swipe.py` importa `hookscore.py` e `hooks.json` da `ig-reel`.
  Se stanno accanto a questo file, usali da lì. Altrimenti scarica il pacchetto
  una volta per sessione in una cartella temporanea (lo scratchpad se c'è,
  altrimenti /tmp), mai nel progetto dell'utente, e lancialo dal clone così gli
  import funzionano:

```bash
T="<cartella temporanea>/ig-tools"
[ -d "$T/repo" ] || git clone --depth 1 https://github.com/leonardo23berto23/instagram-agent-skill "$T/repo"
python3 -I "$T/repo/skills/ig-viral/swipe.py" raccolti.tsv --out swipe.md
```

  È codice scaricato: tieni il file dei dati in un'altra cartella ed esegui con
  `python3 -I`. Nessuna dipendenza, niente rete.
- **File dell'utente** (`swipe.md`, `voice.md`): se c'è un Project collegato,
  documenti del Project sotto `claude/instagram/`; altrimenti
  `~/.claude/instagram/`. Uno swipe file per account se l'utente gestisce
  clienti (`swipe-<account>.md`).
- **Lingua.** Copia gli hook parola per parola nella loro lingua. Le formule si
  riconoscono in italiano e in inglese; quelle non classificate leggile a mano
  e di' quali righe hai classificato tu.

## L'idea che rende utile tutto questo

**Le visualizzazioni da sole non sono una prova.** Un account da due milioni di
follower che fa 400.000 visualizzazioni ha avuto un martedì tranquillo. Un
account da quattromila che ne fa 400.000 ha trovato qualcosa, e quel qualcosa
si può copiare.

Quindi tutto si ordina per **multiplo**: visualizzazioni divise per la mediana
recente di quell'account. Sopra 3x è un segnale. Sotto 1,5x è la giornata
normale di quell'account e non insegna niente, per quanto grande sembri il
numero.

Raccogli account **entro circa 10 volte la dimensione dell'utente**. Una formula
che funziona a 2 milioni di follower spesso funziona perché sono 2 milioni.

## Passo 1: scegli gli account

Chiedi all'utente da 6 a 12 account, oppure proponili e falli approvare. Se
l'utente vuole un'analisi profonda, vai oltre: venti o trenta letti bene sono
meglio di dodici.

- **4 diretti**: stessa nicchia, stessa offerta, un passo avanti.
- **4 vicini**: nicchia diversa, stesso pubblico. Da qui si prendono i formati
  prima che li abbia qualcuno nella nicchia.
- **2-4 grandi**: account molto più grandi, solo per il formato, mai per
  cadenza o tono.

Buone fonti: il pulsante "Account simili" sul profilo di riferimento, la
ricerca di Instagram per parole della nicchia, e la **raccolta Salvati**
dell'utente, che è già filtrata dal suo gusto.

## Passo 2: vai a guardare

Usa lo strumento di navigazione che la sessione ha davvero: un browser
nell'app, l'estensione collegata al Chrome dell'utente, o l'uso del computer.
Non c'è un'API e non serve, perché il volume si legge a mano.

**Regole non negoziabili:**

- **Mai fare login su Instagram al posto dell'utente e mai chiedere una
  password.** Se una pagina chiede l'accesso, è l'utente a essere già dentro.
- **È lettura, non scraping.** Una decina di account, una dozzina di reel
  ciascuno, a velocità umana. La raccolta automatica in volume viola i Termini
  di Instagram e fa bloccare gli account. Niente crawler, niente servizi di
  scraping, niente cicli in background.
- **Copia la formula, mai il video.** La forma dell'hook, la struttura, la
  durata, il ritmo dei tagli. Non il loro copione, non la loro voce, non il
  loro montaggio. Ogni riga dello swipe file va attribuita al suo account.

**Trappole viste sul campo:**

- Nella scheda Reel i **reel fissati** compaiono per primi anche se hanno anni:
  escludili dalla mediana corrente.
- Un reel con tante visualizzazioni e pochissimi mi piace e commenti è quasi
  sempre **una sponsorizzata**: escludilo.
- Contenuti fuori nicchia (vita personale, gravidanza) possono gonfiare la
  mediana di un account: calcola la mediana sui reel in nicchia.
- Molti reel virali sono **collaborazioni**: sono distribuzione, non formula.
  Annotale a parte.

**Cosa annotare per ogni reel**, con le parole di chi l'ha fatto:

| campo | note |
| --- | --- |
| account | handle |
| follower | dal profilo |
| mediana | guarda gli ultimi 12 reel e prendi il valore centrale |
| visualizzazioni | di questo reel |
| hook | la prima riga, detta o a schermo, parola per parola, errori compresi |
| a schermo | il primo cartello, se diverso |
| durata | secondi |
| richiesta | cosa chiedono alla fine (spesso "scrivi PAROLA nei commenti") |

La mediana è il campo importante. Senza, si torna a ordinare per follower, che
è proprio quello che questa skill esiste per evitare.

**Quando Instagram non ti fa vedere abbastanza:** la stessa grammatica degli
hook gira su YouTube Shorts, dove visualizzazioni e trascrizioni sono pubbliche
e non serve login:

```bash
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@HANDLE/shorts" > canale.json
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "it.*,en.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=VIDEO_ID"
```

Prendi ogni parola dei sottotitoli con timestamp sotto i 3,0 secondi: è l'hook
come è stato detto, non come è stato scritto.

## Passo 3: classifica

Compila un file separato da tabulazioni con una riga d'intestazione (in inglese
o in italiano) e lancia lo script:

```
account	follower	mediana	visualizzazioni	hook
@qualcuno	48000	11000	412000	nessuno ti dice che i primi 30 reel devono andare male
```

Calcola il multiplo, dà un nome alla formula con le stesse 27 formule da cui
scrive /ig-reel, valuta ogni hook con `hookscore.py` e stampa cosa separa il
terzo più alto da quello più basso. Accetta anche numeri come "13,4K" o "1.2M".

## Passo 4: di' cosa significa, con cautela

Riporta tre cose e non di più:

1. **Quali formule compaiono di più** nel terzo alto, con i conteggi. Due
   formule che compaiono quattro volte ciascuna su sei account sono un
   risultato. Una che compare due volte no.
2. **Cosa hanno in comune nella struttura** quelli in alto che quelli in basso
   non hanno: lunghezza dell'hook, se la resa si vede, se il primo fotogramma
   si muove, dove sta la richiesta, a chi parlano.
3. **Le righe non classificate.** Ogni hook che lo script non sa nominare è
   rumore oppure una formula che `hooks.json` non ha ancora. Leggile a mano.
   È la colonna più preziosa del risultato, ed è per questo che lo script ne
   stampa il conteggio. Se ne trovi una che si ripete, proponi di aggiungerla
   a `hooks.json` (così è nata la formula 27).

Poi di' in parole semplici quanto è grande il campione e quanto ti fidi.
Quaranta reel su sei account reggono un'affermazione. Dodici no, e dirlo è la
differenza tra una ricerca e un oroscopo.

## Passo 5: trasformalo in qualcosa da girare

Per le tre formule migliori, scrivi **la versione dell'utente**: la sua storia,
il suo numero, nella forma che funziona. Passa ognuna a /ig-reel con la formula
già scelta.

Mai consegnare "fai un reel come questo". Consegna una prima riga che potrebbe
dire domani.

## Risultato

```
SWIPE  ·  38 reel  ·  7 account  ·  base: mediana dell'account

OLTRE 3x
  38,4x  hook 86  #3  Nessuno te lo dice   @account_a  412.000  (mediana 10.700)
  11,2x  hook 79  #9  Il furto             @account_c  180.000  (mediana 16.100)
  ...

COSA COMPARE DI PIÙ IN ALTO
  #3 Nessuno te lo dice   x5 nel terzo alto, 0 in basso
  #2 Comando negativo     x4
  lunghezza hook mediana  8 parole in alto, 19 in basso

NON CLASSIFICATI (6)
  Due hanno la stessa forma e non è in hooks.json: un hook che parte leggendo
  ad alta voce il commento di qualcun altro. Vale la pena aggiungerla.

LA TUA VERSIONE
  #3  "Nessuno ti dice che i primi 20 preventivi devono andare male."
```

Scrivi lo swipe file in `swipe.md` (vedi Preparazione). /ig-reel e /ig-plan lo
leggono, ed è questo il punto: dopo un giro, il resto del pacchetto lavora
sulle prove dell'utente invece che sui default.

Questa skill non pubblica, non segue, non mette mi piace e non scrive a
nessuno. Legge.
