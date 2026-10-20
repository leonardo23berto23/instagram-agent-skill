---
name: ig-story
description: >-
  Scrive le storie Instagram del giorno: la sequenza frame per frame, quale
  sticker usare dove, e quello che porta le persone nei DM. Usala quando
  l'utente dice "storie", "cosa metto nelle storie", "sequenza di storie",
  "idea per un sondaggio", "non ho niente da mettere nelle storie", o vuole
  vendere qualcosa senza farci un post.
---

# ig-story

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script; le frasi dette passano per /ig-human.

- **Voce.** Se esiste `voice.md` (documento del Project sotto
  `claude/instagram/`, oppure `~/.claude/instagram/`), leggilo prima.
- **Lingua.** Ogni frame nella lingua del pubblico, al "tu".

Le storie non sono un feed più piccolo. Il feed è come ti trovano gli
sconosciuti. Le storie sono come chi ti segue già decide se sei una persona da
cui comprare, e sono l'unico posto di Instagram dove un tocco diventa una
conversazione in una mossa.

Fuori dai follower non le vede nessuno, quindi il lavoro è completamente
diverso: profondità, non reach.

## La forma del giorno

Da tre a sette frame al giorno. Oltre i sette circa, cresce chi salta avanti e
gli ultimi frame li guarda nessuno, che è proprio dove la gente mette la
richiesta.

```
1       L'APERTURA   qualcosa che succede oggi, con una faccia o una mano dentro.
2-3     IL CENTRO    il contenuto vero: il processo, il risultato, l'errore.
4       LA RICHIESTA uno sticker. Sondaggio, box domande, quiz o link.
5       LA CHIUSURA  la risposta, il risultato, o l'anticipo di domani.
```

Metti la richiesta al frame 4, non al 7. Ogni tocco perde qualcuno, e la
richiesta deve vederla chi c'è ancora.

## Gli sticker, e a cosa servono davvero

| sticker | lavoro | quando |
| --- | --- | --- |
| **Sondaggio** | il tocco più facile che esista | vuoi tante risposte, non informazioni |
| **Box domande** | raccogliere le parole esatte della gente | ti servono idee o obiezioni, parola per parola |
| **Quiz** | insegnare facendo sbagliare | nella nicchia c'è un equivoco diffuso |
| **Cursore** | sentire l'umore | niente di importante. Divertente, poco valore |
| **Link** | l'unica superficie cliccabile oltre alla bio | c'è un posto vero dove andare |
| **Conto alla rovescia** | una scadenza a cui iscriversi | un lancio, una diretta, una chiusura |
| **Aggiungi il tuo** | reach oltre i follower, ogni tanto | lo spunto è uno a cui chiunque nella nicchia può rispondere |

Il box domande è il più sottovalutato. Ogni risposta è una didascalia, un hook
di Reel o un'apertura di DM scritta con le parole del pubblico. Passale a
/ig-reel come formula #16.

## Regole

- **Una faccia o una mano nel primo frame.** Il testo su sfondo colorato si
  salta, e il primo frame decide se gli altri vengono visti.
- **Un'idea per frame.** Nessuno legge un paragrafo in una storia.
- **Testo nella zona centrale.** Su 1080x1920 niente sopra y=250 o sotto
  y=1600. Sopra c'è la riga del profilo, sotto la barra di risposta.
- **Parla a una persona.** "Tu", singolare. Le storie sono la cosa più vicina a
  un DM senza esserlo.
- **Non ripubblicare il tuo post nelle storie senza commento.** È il frame più
  ignorato della piattaforma. Se rimandi a un post, di' cosa è successo nei
  commenti e perché vale la pena tornarci.
- **Vendi nelle storie, non nei post.** Tre frame di contesto, uno di offerta,
  uno di prova. Questa sequenza vende più di un post sulla stessa cosa e non ti
  costa reach.
- **Attività locale:** il piatto di oggi, l'infornata che esce, la sala vuota
  alle 11 e piena alle 13. Lo sticker link porta a prenotazione o Maps.

## Il percorso verso i DM, fatto onestamente

La sequenza che funziona: una storia che nomina un problema, un box domande o un
sondaggio che permette di dire "sono io", e poi una risposta a ognuno che ha
risposto. La conversazione parte perché sono stati loro a parlare per primi.

Le risposte automatiche ai DM con parola chiave sono una funzione vera e
supportata per gli account professionali, tramite gli strumenti di Instagram e
partner approvati. Scrivere in massa a chi non ha interagito no, ed è quello che
fa limitare gli account. La regola è semplice: **agiscono loro, poi rispondi tu.**

## Risultato

I frame in ordine, ognuno con cosa c'è a schermo, cosa si dice e quale sticker,
più cosa fare con le risposte:

```
STORIE  ·  martedì  ·  5 frame

1  [selfie, camminando]   "Terza richiesta di rimborso quest'anno. Stesso motivo."
2  [registrazione schermo] la clausola, evidenziata
3  [parlato]              "L'approvazione è una sensazione. La consegna è una data."
4  [sondaggio]            "Ti è mai successo con un'approvazione in ritardo?"  Sì / Non ancora
5  [testo su foto]        "Rispondi e ti mando la clausola."

Dopo: chi vota Sì riceve una risposta. È tutto il percorso.
```

Non si pubblica niente. Lo pubblica l'utente.
