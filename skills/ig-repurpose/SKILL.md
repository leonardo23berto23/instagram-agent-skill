---
name: ig-repurpose
description: >-
  Trasforma un contenuto lungo (video YouTube, podcast, diretta, newsletter,
  articolo, telefonata con un cliente) in una settimana di reel e caroselli che
  si reggono da soli. Usala quando l'utente dice "riutilizza questo", "fanne dei
  reel", "ho un video/podcast/trascrizione", "taglialo", o incolla qualcosa di
  lungo e lo vuole su Instagram.
---

# ig-repurpose

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script. Le 27 formule stanno in `ig-reel/hooks.json`: accanto a questo file in
un'installazione locale, altrimenti nel clone di sessione descritto in /ig-reel.

- **Lingua.** Gli estratti restano nella lingua della fonte; i post si scrivono
  nella lingua del pubblico.
- **Trascrizioni.** Per una fonte YouTube, se la sessione arriva a YouTube:
  `python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "it.*,en.*"`.
  Altrimenti chiedi di incollare il testo.

Un buon contenuto lungo contiene da quattro a sei post. Quasi tutti ne tirano
fuori uno e buttano il resto.

## Input

Una trascrizione, un articolo, una newsletter, un copione, il riassunto di una
telefonata, una diretta. Se l'utente dà un link e la sessione ha uno strumento
di trascrizione, usalo; altrimenti chiedi di incollare. Leggi tutto prima di
estrarre qualsiasi cosa.

Se la fonte è un video dell'utente, chiedi anche il file. Un Reel costruito sul
suo filmato batte uno costruito sulle sue parole ridette.

## Estrai, non riassumere

Il riassunto di un video non è un Reel. Nessuno vuole il riassunto. Passa la
fonte e tira fuori le cose che stanno in piedi da sole:

| cosa | cos'è |
| --- | --- |
| **Affermazioni** | ogni frase che farebbe partire una discussione |
| **Numeri** | ogni cifra, costo, durata, percentuale |
| **Storie** | ogni momento con una persona, una scena e un costo |
| **Meccanismi** | ogni "il modo in cui funziona davvero è..." |
| **Errori** | ogni ammissione di qualcosa andato storto |
| **Frasi** | ogni frase già citabile così com'è |

Elenca cosa hai trovato, con i conteggi, prima di scrivere. Se la fonte dà meno
di quattro elementi, è magra, e quattro post spremuti da lì saranno magri anche
loro. Dillo.

## Poi scegli il formato per ogni estratto

Non tutto è un Reel.

- **Affermazione, errore, storia** -> Reel. Hanno bisogno di una voce e di una faccia.
- **Meccanismo, elenco numerato** -> carosello. Vanno riletti.
- **Una frase citabile** -> un frame di storia, non un post.

## Poi costruisci la settimana

Ogni estratto diventa un post, e ogni post sta completamente in piedi da solo.
Chi guarda non ha visto la fonte e non la vedrà mai. Mai scrivere "come dicevo
nel mio ultimo video". Il post è la cosa.

Dai a ognuno una formula diversa da `ig-reel/hooks.json`. Cinque post dalla
stessa fonte con la stessa forma di hook sembrano una catena di montaggio,
perché lo sono.

Se la fonte è un video dell'utente, **usa il filmato vero**. Il pezzo dove dice
la cosa, con la reazione vera dentro, batte ogni volta una ripresa nuova. Taglia
sulla frase, non sul respiro.

Ordina la settimana così: l'affermazione più forte per prima, la storia a metà
settimana, il meccanismo per ultimo, quando chi ha apprezzato i primi lo aspetta.

## Risultato

```
FONTE: "Perché abbiamo eliminato le call conoscitive" (podcast di 42 minuti, 8.900 parole)

TROVATI  5 affermazioni, 9 numeri, 3 storie, 4 meccanismi, 2 errori, 7 frasi citabili

SETTIMANA
MAR  REEL       #2  Comando negativo    Smetti di fare call conoscitive
                                        usa il pezzo al minuto 14:20, alla fine ride
MER  CAROSELLO  didascalia lavoro B     Il modulo da 4 domande che ha sostituito la call
VEN  REEL       #21 A metà frase        "...e nove giorni dopo ha chiesto il rimborso"
DOM  REEL       #5  Il tempo che crolla Sei ore a settimana recuperate, un link tolto

Di' "scrivi martedì" e lo preparo.
```

Poi scrivi su richiesta, uno alla volta, ognuno passando per /ig-reel e
/ig-human. Non scaricare quattro copioni finiti tutti insieme: suonerebbero
tutti uguali e l'utente non ne girerebbe nessuno.
