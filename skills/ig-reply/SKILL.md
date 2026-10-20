---
name: ig-reply
description: >-
  Gestisce i commenti sotto i reel e i post dell'utente: li smista in parola
  chiave, contatto, contenuto, domanda, supporto e rumore, poi scrive le risposte
  in quest'ordine. Usala quando l'utente incolla i suoi commenti, dice "rispondi
  a questi", "gestisci i commenti", "qualcuno ha scritto X sul mio reel", o ha a
  che fare con un critico, un hater o un potenziale cliente nei commenti.
---

# ig-reply

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script; le risposte passano per /ig-human.

- **Voce.** Leggi prima `voice.md` dell'account (documento del Project sotto
  `claude/instagram/`, oppure `~/.claude/instagram/`; per un cliente
  `voice-<account>.md`).
- **Lingua.** Rispondi nella lingua del commento.

Il thread sotto un post è dove si decide la reach. Ogni risposta è un'altra
interazione sul post, le risposte nella prima ora fanno quasi tutto il lavoro, e
su Instagram una risposta può essere anche un Reel, la mossa più sottovalutata
della piattaforma.

Ma il valore non è uguale per tutti i commenti, quindi questa skill smista prima
di scrivere.

## Input

L'utente incolla i commenti, possibilmente con gli handle. Gli screenshot vanno
bene. Non raccogliere il thread con un browser.

## Prima smista

Metti ogni commento in uno di sei gruppi e di' i conteggi:

| gruppo | cos'è | cosa riceve |
| --- | --- | --- |
| **PAROLA CHIAVE** | la parola che avevi chiesto di commentare | la cosa promessa, a mano o con lo strumento approvato |
| **CONTATTO** | qualcuno che descrive il problema che risolvi | una risposta vera in pubblico, poi una porta |
| **CONTENUTO** | aggiunge un dato, non è d'accordo, allunga | la risposta più lunga del thread |
| **DOMANDA** | una domanda che hanno in tanti | questa diventa un Reel, non solo una risposta |
| **SUPPORTO** | "🔥", "bellissimo", un tag | un mi piace e al massimo 3-8 parole |
| **RUMORE** | pubblicità, spam, malafede, provocazioni | niente, o una riga e basta |

Scrivi in quest'ordine e fermati quando il valore finisce.

## La mossa che quasi tutti saltano

Se una domanda nei commenti è una che hanno altre trenta persone, **rispondi
con un Reel**. Instagram attacca il commento al nuovo video come sticker, chi ha
chiesto riceve la notifica, e una domanda con una richiesta vera dietro diventa
un post con l'hook già scritto. Segnala ogni DOMANDA che si presta e passala a
/ig-reel come formula #16.

## Come rispondere

- **Rispondi alla domanda vera.** Se qualcuno chiede come, digli come, nella
  risposta. Non mandarlo in DM per una risposta che poteva avere lì.
- **Usa il suo nome una volta**, all'inizio, senza punto esclamativo.
- **Rispetta la sua lunghezza.** A un commento di quattro parole non si risponde
  con quattro righe.
- **A un critico:** prima concedi la parte vera, con le sue parole, poi tieni il
  punto. Mai cancellare, mai mettersi sulla difensiva, mai rispondere due volte
  nello stesso thread.
- **A un hater:** niente. Una risposta è reach, ed è la reach che cerca.
  Nascondi il commento se è offensivo. I controlli dei commenti esistono e
  usarli non è perdere.
- **A un contatto:** rispondi per intero in pubblico. La porta è una frase alla
  fine ed è un'offerta di aiuto, non una vendita. La risposta pubblica è quella
  che fa scrivere in DM la persona dopo.
- **Attività locale:** a una domanda su prenotazioni o orari si risponde con la
  risposta e il modo di prenotare nella stessa riga (telefono, link, "scrivici
  in DM"), mai solo "ti scriviamo in privato".

## Commenti con la parola chiave

Se il post chiedeva una parola, quei commenti sono il motivo del post. Ognuno è
una persona che ha alzato la mano. Rispondi a ognuno, poi manda quello che hai
promesso. Se l'utente ha un'automazione attraverso gli strumenti di Instagram o
un partner approvato, dillo e lasciala lavorare; altrimenti le risposte sono a
mano, e a questi volumi va bene. Mai scrivere in massa a chi non ha commentato.

## Risultato

Un blocco solo, diviso per gruppo, ogni risposta pronta da copiare e già passata
per /ig-human:

```
RISPOSTE  ·  84 commenti  ·  41 PAROLA CHIAVE, 2 CONTATTO, 3 CONTENUTO, 2 DOMANDA, 34 SUPPORTO, 2 RUMORE

PAROLA CHIAVE  (41)  manda la scheda. Una riga a testa, stesso calore, non copia-incolla.

CONTATTO
@handle - "a noi è successa la stessa cosa a giugno"
> Quello che ci ha risolto il problema è stato togliere del tutto il pagamento
> all'approvazione. Se ti serve, ti mando il testo.

DOMANDA -> REEL
@handle - "e se si rifiutano di firmarla?"
  34 mi piace su questo commento. È un Reel, non una risposta. Formula #16.

RUMORE  (2)  saltati. Rispondere gli dà reach.
```

Poi il passaggio obbligato: non si pubblica niente finché l'utente non dice sì.
Le risposte le incolla lui.
