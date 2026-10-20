---
name: ig-carousel
description: >-
  Costruisce un carosello Instagram: la copertina che si guadagna lo
  scorrimento, il testo slide per slide, la didascalia e i file 1080x1350 da
  caricare. Usala quando l'utente dice "carosello", "slide", "post a scorrimento",
  "trasformalo in un carosello", o ha un'idea fatta a elenco o a passaggi che
  morirebbe in un'immagine singola.
---

# ig-carousel

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script propri; testo e didascalia passano per /ig-human e /ig-caption.

- **Voce.** Se esiste `voice.md` (documento del Project sotto
  `claude/instagram/`, oppure `~/.claude/instagram/`), leggilo prima.
- **Lingua.** Scrivi nella lingua del pubblico dell'account. L'italiano è circa
  il 20% più lungo dell'inglese: conta le parole contro i limiti qui sotto,
  ogni volta.

I caroselli sono il formato con più tempo di permanenza sulla griglia, perché
scorrere è un'interazione e scrollare no. Hanno anche una seconda possibilità:
Instagram può riproporre un carosello partendo da una slide successiva a chi non
ha interagito la prima volta, quindi anche la slide due deve reggersi da sola.

Il formato premia un'idea divisa in passaggi. Punisce una didascalia tagliata a
pezzi.

## Quando usarlo al posto di un Reel

Usa un carosello quando l'idea ha **una sequenza e va riletta**: passaggi, uno
schema con parti, un prima e dopo, un elenco da salvare. Usa un Reel quando
l'idea ha movimento, una faccia, o una resa che va vista mentre succede.

Se l'idea è un'affermazione sola, non è nessuno dei due. Passala a /ig-reel e
dillo.

## Struttura

Da 6 a 10 slide. Il limite è 20, e 20 è quasi sempre un libro che nessuno
finisce. Sotto 5 lo scorrimento non parte.

```
1          COPERTINA       l'hook. Sei parole o meno, leggibile in miniatura nella
                           griglia. Una riga di promessa sotto.
2          POSTA IN GIOCO  perché importa, in una frase. È anche una seconda
                           copertina, quindi non può essere preparazione.
3 - N      UN'IDEA PER SLIDE. Un titolo di 3-7 parole, al massimo 25 parole sotto.
                           Se una slide ha bisogno di un paragrafo, sono due slide.
N+1        RIEPILOGO       tutto in un elenco. È la slide che si fotografa.
ULTIMA     RICHIESTA       un'azione. Salva, commenta una parola o segui. Una.
```

## Regole per il testo delle slide

- **La copertina è l'80% del risultato.** Sei parole. Grandi. Niente nel resto
  salva una copertina che nessuno scorre.
- **Progetta per il ritaglio della griglia.** La griglia del profilo taglia a un
  rettangolo verticale, e il rapporto esatto è cambiato più volte. Costruisci a
  1080x1350 e tieni il testo della copertina ben al centro, lontano dai 120
  pixel esterni su ogni lato: così il ritaglio non conta.
- **Numera le slide** (3/8). Si arriva più spesso alla fine se la fine si vede.
- **Nessuna slide è un paragrafo.** Se non sta in 25 parole, dividila.
- **La slide riepilogo è quella che si fotografa e si manda.** Gli invii sono il
  segnale più forte. Deve reggersi da sola, senza contesto.
- **L'handle su ogni slide**, piccolo, in basso. Gli screenshot girano senza di te.
- **Testo alternativo almeno sulla copertina.** Lo leggono gli screen reader e
  Instagram.
- **Dati che non conosci** (prezzi, durate, come funziona un servizio) restano
  tra graffe, `{{così}}`. Mai inventarli.

## Costruire i file

Instagram vuole 1080x1350 (4:5), JPEG o PNG, fino a 20 elementi. Costruiscilo in
HTML e stampa ogni slide:

```bash
# una <section> per slide, 1080x1350, page-break-after: always
# poi Chrome headless --print-to-pdf, uno screenshot Playwright per sezione,
# o qualsiasi conversione HTML in immagine che usi già
```

Scrivi l'HTML con `width:1080px; height:1350px`, un solo colore di accento e
testo mai sotto i 32px, perché si legge su un telefono a un terzo della
dimensione reale. Se c'è una skill di brand o un design system, usalo e non
inventare una palette. Per un account cliente, colori e logo del cliente, mai
quelli dell'utente.

## Risultato

Prima il testo slide per slide, come lista numerata che l'utente legge in dieci
secondi e corregge prima di costruire qualsiasi cosa. Poi la **didascalia**, che
per un carosello è il lavoro B di /ig-caption: la didascalia lavora, perché la
copertina ha già usato le sue sei parole.

Passa entrambi per /ig-human e la didascalia per /ig-caption. Costruisci i file
solo dopo che l'utente ha approvato il testo.

```
CAROSELLO  ·  8 slide

1  COPERTINA  LA CLAUSOLA DA 18.000 €
              Una riga che ora metto in ogni contratto.
2  POSTA      Ho approvato il lavoro. Nove giorni dopo hanno chiesto i soldi indietro.
3             COSA DICE
              Pagamento alla consegna, non all'approvazione.
...
7  RIEPILOGO  Le quattro righe, in ordine.
8  RICHIESTA  Commenta CONTRATTO e ti mando la clausola completa.

Didascalia: lavoro B, hook alla riga 1, una richiesta, 3 hashtag.
```

Non si carica niente. Lo pubblica l'utente.
