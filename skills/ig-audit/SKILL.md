---
name: ig-audit
description: >-
  Analisi a posteriori di quello che un account ha già pubblicato: quali reel
  hanno funzionato davvero, perché, e cosa smettere di fare. Misura multiplo
  sulla mediana, reach da non follower, tenuta a 3 secondi e invii per reach.
  Usala quando l'utente incolla gli insight o i post e chiede "cosa funziona",
  "perché è andato male", "leggi le mie statistiche", "analizza i miei
  contenuti", o vuole sapere cosa fare di più. Funziona anche su un account non
  suo, con i soli dati pubblici.
---

# ig-audit

L'unica fonte onesta su cosa funziona per un account è quell'account. Ogni
regola di ogni guida a Instagram, comprese quelle di questo pacchetto, è
un'ipotesi. Gli ultimi 30 post dell'utente sono la prova.

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script. Le 27 formule stanno in `ig-reel/hooks.json`: accanto a questo file in
un'installazione locale, altrimenti nel clone di sessione descritto in /ig-reel.

- **File dell'utente** (`log.md`, `plan.md`, `swipe.md`): se c'è un Project
  collegato, documenti del Project sotto `claude/instagram/`; altrimenti
  `~/.claude/instagram/`. Un log per account se l'utente gestisce clienti.
- **Account non dell'utente (un potenziale cliente).** Da fuori si vedono solo
  visualizzazioni, mi piace, commenti e date. Calcola il multiplo sulla mediana
  e i pattern di formato, durata e tema da quelli; segna reach, tenuta, invii
  e follow come sconosciuti e non stimarli mai.

## Input

Chiedi quello che l'utente ha:

- Gli insight per post: visualizzazioni, reach, interazioni, tempo di visione,
  salvataggi, condivisioni, follow, e la quota di reach da non follower. Gli
  screenshot vanno bene.
- Oppure il grafico di permanenza dei reel migliori e peggiori. Quello
  screenshot da solo vale più di tutto il resto.
- Oppure solo i post e le loro visualizzazioni, che bastano per un primo giro.

Leggi anche `log.md` se esiste: dice quale formula ha usato ogni post.

## Cosa misurare davvero

Le visualizzazioni sono il numero meno utile della pagina, perché dipendono
soprattutto da quante persone seguono già l'account. Calcola questi, e mostra
i conti:

| misura | come | cosa ti dice |
| --- | --- | --- |
| **Multiplo** | visualizzazioni / mediana dell'account | se è stato un colpo vero o una giornata normale |
| **Reach da non follower** | % della reach da chi non segue | se è uscito dalla bolla |
| **Tenuta a 3s** | spettatori ancora lì a 3s / spettatori partiti | se l'hook ha funzionato: è il voto dell'hook |
| **Tempo medio di visione** | dagli insight | se il centro ha funzionato |
| **Invii per reach** | condivisioni / reach | il segnale più forte che puoi guadagnarti: chi manda ci mette il suo nome |
| **Follow per reach** | follow / reach | se il profilo ha trasformato l'attenzione |
| **Visualizzazioni / follower** (account esterni) | mediana / follower | se l'account esce regolarmente dai propri follower |

Ordina per multiplo e invii per reach, non per visualizzazioni. Un reel con
4.000 visualizzazioni e 90 invii ha battuto quello con 60.000 e 11.

## Poi trova il pattern

Con i cinque migliori e i cinque peggiori uno accanto all'altro, cerca cosa li
separa, e sii pronto a concludere qualcosa che all'utente non piacerà:

- **Tenuta a 3 secondi.** Se migliori e peggiori differiscono qui, è l'hook e
  nient'altro, e tutto il resto è una distrazione.
- **Formula dell'hook.** Quali formule di `hooks.json` sono nei cinque migliori?
- **Formato.** Reel, carosello, foto.
- **Durata.** Sotto i 15 s, 15-30, 30-60, oltre 60.
- **Tema.**
- **Collaborazioni.** Un reel in collaborazione esce su due profili: separalo.
- **Se l'utente ha risposto ai commenti nella prima ora.**
- **Giorno e ora.** Per **ultimi**, e solo se il resto non mostra niente. Non è
  quasi mai la causa ed è dove la gente vorrebbe che fosse.

Formula il risultato come un'affermazione con la prova accanto, e di' quanto
ti fidi. Con 30 post vedi un pattern. Con 6 no, e dirlo è meglio che inventarne
uno.

## La distinzione che fa risparmiare mesi

**Un reel che fa visualizzazioni e nessun follow non è un reel sbagliato: è un
problema di profilo.** Un reel che non fa visualizzazioni è un problema di
hook. Separa le due cose prima di consigliare qualsiasi cosa. Se la reach da
non follower è alta e i follow per reach sono bassi (o, da fuori, le
visualizzazioni superano molto i follower ma i follower non crescono), smetti
di riscrivere gli hook e passa a /ig-profile.

## Risultato

```
AUDIT  ·  31 post  ·  12 giu - 5 set  ·  mediana 4.100 visualizzazioni

I 5 MIGLIORI PER MULTIPLO
  18,2x  #3  Nessuno te lo dice   74.600  62% non follower  tenuta 71%  128 invii
   6,4x  #1  Confessione del costo 26.300  48% non follower  tenuta 64%   71 invii

I 5 PEGGIORI
   0,3x  #11 Elenco               1.200   9% non follower  tenuta 31%    2 invii

COSA DICONO I DATI
1. La tenuta a 3 secondi è tutta la storia: 66% in alto, 33% in basso.
2. I post dove sei tu a fare brutta figura: media 8,1x contro 0,9x. n=5.
3. Gli elenchi di strumenti fanno visualizzazioni e nient'altro.
4. Il giorno della settimana non dice niente. Smetti di ottimizzarlo.

SMETTI: elenchi.
FAI DI PIÙ: quelli con un costo pagato e un numero.
```

Poi passa le conclusioni a /ig-plan, così la settimana dopo si basa sulle prove
dell'utente, e a /ig-viral, così lo swipe file si filtra sulle formule che
funzionano per questo account.
