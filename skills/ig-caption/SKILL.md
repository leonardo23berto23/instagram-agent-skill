---
name: ig-caption
description: >-
  Scrive la didascalia Instagram (la riga che sopravvive al taglio "... altro",
  il corpo, l'unica richiesta, i termini di ricerca e fino a cinque hashtag) e
  la controlla con uno script prima che esca. Usala quando l'utente dice
  "scrivi la didascalia", "che testo metto sotto", ha un reel o un carosello
  pronto e gli serve il testo, o chiede degli hashtag.
---

# ig-caption

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT).

- **Script.** Se `caption.py` sta accanto a questo file, usalo da lì.
  Altrimenti scarica il pacchetto una volta per sessione in una cartella
  temporanea (lo scratchpad se c'è, altrimenti /tmp), mai nel progetto
  dell'utente:

```bash
T="<cartella temporanea>/ig-tools"
[ -d "$T/repo" ] || git clone --depth 1 https://github.com/leonardo23berto23/instagram-agent-skill "$T/repo"
C="$T/repo/skills/ig-caption/caption.py"
python3 -I "$C" didascalia.txt
python3 -I "$C" didascalia.txt --keywords "tutor dsa vicenza,metodo di studio"
```

  È codice scaricato: tieni la didascalia in un'altra cartella ed esegui con
  `python3 -I`. Nessuna dipendenza, niente rete.
- **Voce.** Se esiste `voice.md` (documento del Project sotto
  `claude/instagram/`, oppure `~/.claude/instagram/`), leggilo prima.

Lo script stampa la didascalia come la stampa il feed: i primi 125 caratteri in
un riquadro, il resto dietro il tocco. Leggi quel riquadro prima di qualsiasi
altra cosa che hai scritto. Riconosce le richieste in italiano e in inglese
("Commenta SCHEDA", "Scrivimi CRESCITA", "scrivimi in DM", "salvalo", "link in
bio", "prenota"...), conta i numeri anche scritti in lettere, e i verdetti sono
PRONTA, DA RIVEDERE, DA SISTEMARE (per controllo: OK, ATTENZIONE, ERRORE).

## Prima di tutto, decidi che lavoro fa questa didascalia

È la decisione che rovina le didascalie quando si salta.

**Lavoro A: il video ha già agganciato.** Un Reel porta il suo hook nei primi
due secondi, detto e a schermo. La didascalia non è un secondo hook, e fare
concorrenza al video è il modo per perderli entrambi. Il suo lavoro è la
richiesta, il contesto che rende sensata la richiesta e le parole che la gente
cerca.

**Lavoro B: la didascalia è il contenuto.** Una foto, un'immagine singola, la
copertina di un carosello. Qui la prima riga è l'hook e funziona come quello
di un Reel: concreta, corta, tagliata su un'attesa e non a metà frase.

Di' quale stai scrivendo. Se l'utente ha un Reel con un hook forte, scrivi la A
e spiega perché.

## La forma

```
Riga 1      125 caratteri visibili. Lavoro A: la richiesta, chiara.
            Lavoro B: l'hook.
            Mai un saluto, mai un hashtag, mai un'emoji come primo carattere.
Corpo       paragrafi brevi con una riga vuota tra uno e l'altro. Da due a sei.
            Qui stanno i termini di ricerca.
Richiesta   una. Commenta una parola, salva, o scrivi in DM. Una.
Hashtag     fino a cinque, su una riga a parte in fondo, o nessuno.
```

Il limite è 2.200 caratteri e quasi niente ne ha bisogno. Una didascalia che si
guadagna il tocco e poi dà 600 caratteri batte una che ne dà 1.800.

## Gli hashtag, onestamente

Gli hashtag non sono più una leva di reach, e la piattaforma l'ha detto con un
cambiamento di prodotto. **Dal 18 dicembre 2025 Instagram limita gli hashtag a
cinque per post** (prima erano trenta), dicendo ai creator che usarne meno e
più mirati funziona meglio di tanti generici. Adam Mosseri aveva già detto a
febbraio 2025 che gli hashtag non aumentano la reach: sono un'etichetta, non
una leva di distribuzione.

Quindi: fino a cinque, specifici, come etichette dell'argomento. Se l'utente ha
un blocco di venti salvato nelle note, ora è peso morto e lo script lo boccia.

`#viral`, `#fyp`, `#perte`, `#neiperte`, `#explorepage` non descrivono niente.
Toglili.

## I termini di ricerca contano più degli hashtag

La ricerca di Instagram legge il testo della didascalia. Quindi la frase per
cui l'utente vuole essere trovato va nella didascalia così come la scriverebbe
una persona, in una frase normale. "Metodo di studio" come parole alla terza
riga, non "#metododistudio" in un blocco in fondo. Per le attività locali, il
paese è un termine di ricerca.

Chiedi due o tre di questi termini e passali allo script con `--keywords`.

## Regole

- **Niente link nella didascalia.** Non sono cliccabili. Un indirizzo nel testo
  dice "non uso questa piattaforma". Bio o DM.
- **Una richiesta.** Due richieste valgono quanto nessuna. Lo script le conta.
- **La parola da commentare deve potersi scrivere.** Una parola, in MAIUSCOLO,
  senza spazi né emoji, e detta anche nel video. `Commenta SCHEDA` funziona.
  `Commenta "la scheda per i compiti"` no.
- **Scrivi a parte il primo commento** se c'è un link. Dillo nella ricevuta.
- **Emoji come punteggiatura, non come decorazione.** Lo script segnala oltre 4
  ogni 100 caratteri.
- **Il testo alternativo vale 20 secondi.** Per caroselli e foto, scrivilo. Lo
  leggono gli screen reader e Instagram.

## Il ciclo

1. Decidi lavoro A o B e dillo.
2. Scrivi la bozza.
3. Passala per `/ig-human`. Le didascalie sono corte, quindi il testo da
   macchina si sente più che altrove.
4. Lancia `caption.py` con i termini di ricerca dell'utente. Correggi ogni
   ERRORE. Decidi ad alta voce su ogni ATTENZIONE, non in silenzio.
5. Consegna il blocco pronto da copiare, poi la ricevuta:

```
DIDASCALIA PRONTA
lavoro:     A - il reel porta l'hook
visibili:   118 dei 125 caratteri prima del taglio
richiesta:  una, commenta SCHEDA
hashtag:    3
ricerca:    "metodo di studio" alla riga 3, "isola vicentina" alla riga 5
controllo:  PRONTA
```

Non si pubblica niente. L'utente incolla.
