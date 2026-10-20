---
name: ig-dm
description: >-
  Scrive DM Instagram che ricevono risposta: la consegna della parola chiave, il
  primo messaggio a chi ha interagito, la proposta di collaborazione, la prima
  proposta a un potenziale cliente partendo da un'analisi già fatta, e i due
  follow-up. Usala quando l'utente dice "scrivi a questa persona", "cosa gli
  mando", "messaggio di contatto", "come faccio il follow-up", "proponi una
  collaborazione", o sta contattando qualcuno di preciso.
---

# ig-dm

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script; ogni messaggio passa per /ig-human.

- **Voce.** Leggi prima `voice.md` dell'utente (documento del Project sotto
  `claude/instagram/`, oppure `~/.claude/instagram/`).
- **Lingua.** Scrivi nella lingua di chi riceve. In italiano togli a mano anche
  "Ciao! Domanda veloce", "ti scrivo perché", "complimenti per il profilo" e la
  proposta subito dopo il complimento.

I DM sono l'unico posto di Instagram dove passano davvero i soldi, e sono anche
dove la maggior parte degli account brucia la fiducia che i contenuti avevano
guadagnato. La differenza sta tutta in chi si è mosso per primo.

## I tipi di DM che vale la pena scrivere

**1. La risposta a una mano alzata.** Hanno commentato la parola, risposto al
sondaggio, risposto a una storia, o salvato e chiesto. Si sono mossi per primi.
È il 90% dei DM che vale la pena mandare, e converte perché non è un contatto a
freddo.

**2. L'approccio caldo.** Qualcuno sotto i cui post l'utente commenta davvero da
settimane. C'è già un filo di conversazione.

**3. La proposta di collaborazione.** Una proposta precisa a un account preciso,
con un motivo per cui è proprio lui.

**4. Il primo messaggio a un potenziale cliente con un'analisi in mano.** L'unico
messaggio a freddo che questa skill ammette: l'utente ha già fatto un'analisi
(/ig-profile, /ig-audit) con un risultato visibile e preciso. Quel risultato è
l'aggancio. Lo regali nel primo messaggio, e nel primo messaggio non chiedi
niente oltre a "ti è utile?".

Tutto il resto è scrivere a freddo a sconosciuti, che è quello che fanno tutti,
ed è per questo che le risposte stanno dove stanno. Se l'utente chiede una
sequenza a freddo, digli chiaramente che è la cosa meno redditizia che potrebbe
fare con quell'ora, e offri l'alternativa: commentare per due settimane sotto
quei dieci account. Poi scrivila, se la vuole ancora.

## Prima di scrivere, prendi i dettagli

Chiedi in una domanda sola:

1. **Chi**: handle, cosa fa, e cosa ha pubblicato o fatto che ha fatto partire
   tutto.
2. **L'aggancio**: il motivo vero per scrivere oggi. Una parola commentata, una
   risposta a una storia, un post pubblicato, un risultato dell'analisi. Non
   "è nel target".
3. **Cosa vuole l'utente**: una conversazione, una vendita, una collaborazione,
   un passaparola. Sii onesto internamente, anche se il messaggio non apre con
   quello.

Se non c'è un aggancio, non c'è un messaggio. Dillo.

## La consegna della parola chiave

Il DM più comune del pacchetto e il più facile da rovinare. Hanno commentato una
parola. Si aspettano la cosa. Quindi:

```
{nome}, eccola: {la cosa, o il link}.

{una riga su come usarla}

{una domanda a cui si risponde in quattro parole}
```

Manda la cosa **subito**, nel primo messaggio, senza condizioni. Un post a parola
chiave che risponde "prima di mandartela, posso chiederti di cosa ti occupi?" è
un'esca, e la gente se lo ricorda. La domanda alla fine fa partire la
conversazione, ed è facoltativa per loro.

Le risposte automatiche alle parole chiave sono una funzione supportata per gli
account professionali, tramite gli strumenti di Instagram o un partner
approvato. Usarle va bene. Mandare DM in massa a chi non ha chiesto no, ed è la
via più veloce per un account limitato.

## Il primo messaggio a qualcuno di caldo

- **Da due a quattro frasi.** Una schermata di testo si cancella.
- **Cita la cosa precisa.** Il commento, il post, la risposta. Con le sue parole.
- **Dai prima di chiedere.** Un numero, un modello, un nome, una risposta.
- **Una richiesta, piccola.** "Ti va di sentirci dieci minuti?" batte "lascia che
  ti mostri tutto il servizio".
- **Niente link e niente calendario nel primo messaggio.** Sembra un imbuto,
  perché lo è.
- **Niente vocali a uno sconosciuto.** Sono utilissimi, per chi conosce già la
  voce dell'utente.

## Il primo messaggio a un potenziale cliente (tipo 4)

Tre-quattro frasi: il dato che hai visto (con il numero), cosa significa per i
loro clienti, il regalo (le correzioni pronte o il documento), e "ti è utile?".
Niente prezzo, niente "posso fare questo e quest'altro". La proposta arriva solo
se rispondono.

## La proposta di collaborazione

Quattro righe, in quest'ordine: cosa hai visto fare a loro, l'idea precisa, cosa
ci guadagnano, cosa ti serve da loro. Un post in collaborazione esce su due
griglie e raggiunge due pubblici, ed è la leva di crescita più forte che non
richieda di pagare nessuno. Presentala così e sii concreto su chi fa cosa.

## Follow-up

Due. Questo è il numero.

- **Dopo 4 giorni**: aggiungi qualcosa di nuovo. Mai "ti riscrivo per sapere se
  hai visto". Se non c'è niente di nuovo, non c'è follow-up.
- **Dopo 10 giorni**: il messaggio che chiude il cerchio. Di' che ti fermi, e
  fermati. Questo prende una quota sorprendente delle risposte, perché toglie la
  pressione.

Poi basta. Un terzo non converte nessuno e costa la relazione.

## Mai

- Mai automatizzare i DM di contatto, e mai usare uno strumento che manda a orari
  programmati a chi non ha interagito. Viola i Termini di Instagram e limita
  l'account.
- Mai inventare di aver visto qualcosa, un contatto in comune o qualsiasi cosa
  condivisa.
- Mai aprire con "Ciao! Domanda veloce" e poi non fare una domanda.
- Mai mettere la proposta nello stesso messaggio del complimento.

## Risultato

Il messaggio, il conteggio dei caratteri, e i due follow-up con il giorno di
invio, tutti passati per /ig-human. L'utente li manda tutti a mano, o con la sua
automazione approvata solo per le risposte alle parole chiave.
