---
name: ig-comment
description: >-
  Scrive commenti sotto i post e i reel di altri che sembrano di una persona con
  un'opinione, non di un bot: nove tipi di commento, due opzioni ogni volta, mai
  "bellissimo post". Usala quando l'utente incolla un post o un reel e vuole un
  commento, dice "commenta questo", "cosa scrivo qui", o vuole un gruppo di
  commenti per il giro quotidiano di interazioni.
---

# ig-comment

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script; ogni commento passa per /ig-human.

- **Lingua.** Scrivi nella lingua del post che stai commentando.
- **Log.** Il registro dei commenti della settimana è `log.md`: documento del
  Project sotto `claude/instagram/` se c'è un Project, altrimenti
  `~/.claude/instagram/`.

Commentare sono i venti minuti con più leva su Instagram, e i più facili da
sprecare. Un commento in cima a un reel da 40.000 visualizzazioni lo vede più
gente della maggior parte dei post degli account, ed è l'unico posto dove uno
sconosciuto arriva al profilo con un tocco.

Un commento generico è peggio di nessun commento. Costa un tocco che non porta
da nessuna parte e marca l'account come uno da gruppi di engagement agli occhi
dell'unica persona la cui opinione contava: il creator.

## Input

L'utente incolla il testo del post o del reel, o uno screenshot, con il nome
dell'account. Se dà un link che non puoi aprire, chiedi di incollarlo. Non usare
un browser per raccogliere il feed e non pubblicare niente.

## I nove tipi di commento

Scegli in base a cosa è davvero il post. Mai il tipo 1 per abitudine.

| # | tipo | quando | forma |
| --- | --- | --- | --- |
| 1 | **Aggiungi un dato** | il post afferma qualcosa che puoi sostenere con un numero | "Anche da noi: il 40% di..." |
| 2 | **Aggiungi il caso mancante** | il post ha ragione ma è incompleto | "Vale finché {condizione}." |
| 3 | **Disaccordo rispettoso** | pensi davvero che sia sbagliato | prima il punto d'accordo, poi dove ti separi |
| 4 | **Allunga una riga** | una riga è quella buona | citala, costruisci sopra |
| 5 | **Fai la domanda vera** | il post ha saltato la parte difficile | una domanda, precisa |
| 6 | **La ricevuta** | hai fatto la cosa descritta | cosa è successo, due frasi |
| 7 | **La correzione** | c'è un errore di fatto | abbi ragione, sii breve, gentile e sicuro |
| 8 | **Il cambio di cornice** | fatti giusti, cornice sbagliata | "Un altro modo di leggerlo:" |
| 9 | **La battuta** | il post non ha bisogno di niente, vuoi esserci | sotto le 10 parole, divertente o vera |

## Regole

- **Da una a tre frasi.** I commenti si leggono in una colonna stretta sotto un
  video. Un paragrafo finisce dietro "altro" e nessuno lo apre.
- **Mai aprire con** "Bellissimo post", "Grande!", "Verissimo", "Concordo
  pienamente", "Ne avevo bisogno oggi", o il nome del creator con il punto
  esclamativo. Sono tutti invisibili. In inglese: "Great post", "Love this",
  "So true".
- **Niente commenti solo emoji** e niente emoji come primo carattere.
- **Non riassumere il reel.** Chi lo legge l'ha appena visto.
- **Un'idea.** Un commento con due punti sembra un dirottamento.
- **Di' la cosa precisa.** Se il commento potrebbe stare sotto qualsiasi post
  sull'argomento, non è un commento, è rumore.
- **Mai vendere.** Né l'offerta, né il link, né "passa dal mio profilo". È il
  modo più veloce per farsi bloccare proprio da chi volevi raggiungere.
- **Presto conta più che altrove.** Un commento nella prima ora su un reel che
  poi gira viene portato con lui.

## Risultato

Due opzioni di tipo diverso, con l'etichetta, più una riga su quale
pubblicheresti e perché. Passale entrambe per /ig-human prima: i commenti sono
corti, quindi un trattino lungo o una frase fatta si sentono di più che in una
didascalia.

```
OPZIONI DI COMMENTO  (sul reel di @account sui prezzi)

[6 · Ricevuta]
Abbiamo alzato i prezzi del 40% a marzo e perso esattamente un cliente, quello
che occupava metà della casella. Ci ho messo otto mesi a smettere di averne paura.

[3 · Disaccordo rispettoso]
D'accordo sull'ancoraggio. Dove non sono d'accordo è farlo a metà progetto:
l'abbiamo provato e ci è costato un rinnovo che altrimenti era sicuro.

Pubblicherei il primo: concede qualcosa e ha un numero.
```

## Modalità gruppo

Per il giro di interazioni, chiedi da 5 a 10 post come testo incollato in un
solo messaggio, restituisci un commento per ognuno in un blocco unico, e tieni
in `log.md` una nota di chi è stato commentato questa settimana. Commentare
sempre gli stessi tre account ogni giorno si vede, e sembra esattamente quello
che è.

## Mai

Non pubblicare in automatico, non automatizzare i commenti, e non usare un
browser per pubblicare al posto dell'utente. L'interazione automatica viola i
Termini di Instagram e fa bloccare gli account. Questa skill scrive il commento.
Lo pubblica l'utente.
