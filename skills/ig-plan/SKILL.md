---
name: ig-plan
description: >-
  Costruisce la settimana (o il mese) su Instagram: cosa pubblicare, in che
  formato, quando, con quale formula di hook, e con chi interagire. Usala quando
  l'utente dice "pianifica la settimana", "cosa pubblico", "calendario
  editoriale", "non so cosa pubblicare", o vuole un piano di pubblicazione e una
  lista di account con cui interagire, anche per un cliente.
---

# ig-plan

La sala di controllo. Le altre skill del pacchetto eseguono; questa decide cosa
eseguire. Una volta a settimana, sempre lo stesso giorno.

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script. Le 27 formule stanno in `ig-reel/hooks.json`: accanto a questo file in
un'installazione locale, altrimenti nel clone di sessione descritto in /ig-reel.

- **File dell'utente** (`voice.md`, `swipe.md`, `log.md`, `plan.md`): se c'è un
  Project collegato, documenti del Project sotto `claude/instagram/`;
  altrimenti `~/.claude/instagram/`. Un set per account se l'utente gestisce
  clienti (`plan-<account>.md`).
- **Lingua.** Piano e angoli nella lingua del pubblico dell'account. Orari nel
  fuso del pubblico.

## Input

Se esistono `voice.md`, `swipe.md` e `log.md`, leggili. Lo swipe file è la
prova, raccolta con /ig-viral, di quali formule funzionano adesso nella nicchia,
e vale più di qualsiasi cosa scritta qui. Il log evita di ripetere un tema
delle ultime due settimane. Se c'è un'analisi del profilo (/ig-profile) o un
audit (/ig-audit), parti da lì: se il problema è il profilo, la prima settimana
si sistema il profilo.

Se non esistono, chiedi quattro cose e scrivile:

1. Cosa vende l'utente, e a chi.
2. I tre o quattro temi per cui vuole essere conosciuto.
3. Cosa è successo davvero questa settimana: una telefonata con un cliente, un
   numero, un errore, una cosa costruita, una discussione. I post vengono da qui.
4. Dieci account a cui vale la pena farsi vedere.

## Cosa pubblicare

Quattro-cinque post a settimana, di cui almeno tre Reel. I Reel sono l'unico
formato che raggiunge con regolarità chi non segue l'account. I caroselli vanno
a fondo con chi già segue. Le storie sono quotidiane e si pianificano a parte.

Mescola nella settimana, mai due dello stesso tipo di seguito:

| tipo | quanti | lavoro |
| --- | --- | --- |
| **Prova** | 1 a settimana | una cosa successa, con un numero. Reel. |
| **Insegna** | 1-2 a settimana | una cosa che chi guarda può fare oggi. Reel o carosello. |
| **Opinione** | 1 a settimana | una posizione che potrebbe farti perdere follower. Reel. |
| **Storia** | 1 ogni due settimane | una scena con un costo. Reel. |
| **Offerta** | 1 ogni due settimane | cosa vendi, detto chiaro, senza scusarti. Carosello o storie. |

Per ogni slot indica: il tema, l'angolo preciso da quello che è successo
davvero, il formato e la formula di `hooks.json`, con la prima riga. Non un
argomento, un angolo. "L'IA" non è un piano. "Il preventivo perso perché la
bozza aveva un trattino lungo" è un Reel.

Per un'attività locale (ristorante, negozio, studio) vale lo stesso mix con
contenuti diversi: la prova è la sala piena o l'infornata finita con il numero,
insegna è come scegliere o usare quello che vendono, l'opinione è una presa di
posizione sul loro mestiere, la storia è una giornata dietro il banco,
l'offerta è il piatto, l'evento o l'orario della settimana.

**Una sola parola chiave per tutto il piano.** Se l'account può dare qualcosa
di gratuito (una scheda, una checklist, un link), ogni reel chiude con
"Commenta PAROLA" e in DM arriva la cosa promessa. Nelle nicchie italiane
studiate è il meccanismo che trasforma le visualizzazioni in conversazioni. Le
schede vanno pronte prima di pubblicare.

**Una collaborazione al mese** con un account che parla allo stesso pubblico:
un post in collaborazione esce su due profili insieme, senza spendere niente.

## Quando pubblicare

Quando il pubblico è sveglio e non al lavoro. Per la maggior parte dei pubblici
consumer è la prima sera, ora locale; per un pubblico business, la mattina
presto; per i genitori, dopo cena e compiti.

Ma dillo chiaramente: **l'ora conta molto meno dei primi due secondi.**
Instagram continua a mostrare per giorni un Reel che funziona, e ne seppellisce
uno pubblicato all'ora perfetta che non funziona. Se l'utente ottimizza gli
orari prima che gli hook funzionino, sta lucidando la cosa sbagliata, e devi
dirglielo.

## Il giro di commenti, che non è facoltativo

20 minuti al giorno, prima di pubblicare, non dopo. Una lista di 10:

- **5 di reach**: account con il pubblico che l'utente vuole, dove un buon
  commento si vede. Commenta presto, prima che il thread sia lungo 200.
- **3 pari**: stessa dimensione, stesso campo. È il gruppo che ricambia.
- **2 compratori**: persone che potrebbero comprare davvero. Commenta per
  settimane prima di qualsiasi DM, e mai vendere in un commento.

Passa la lista a /ig-comment.

## Risultato

```
SETTIMANA DEL 15 SETTEMBRE

LUN  solo commenti  (20 min, lista sotto)
MAR  19:30  REEL       PROVA     #5  Il tempo che crolla  - preventivo da 5 ore a 20 minuti
MER  solo storie + commenti
GIO  19:00  CAROSELLO  INSEGNA   didascalia lavoro B      - la clausola in 4 slide
VEN  19:30  REEL       OPINIONE  #2  Comando negativo     - smetti di fare le call conoscitive
SAB  -
DOM  18:00  REEL       STORIA    #21 A metà frase         - la mail di rimborso

STORIE  ogni giorno, 3-5 frame, box domande il giovedì.
COMMENTI  (5 reach / 3 pari / 2 compratori)

Di' "scrivi martedì" e lo preparo.
```

Scrivi il piano in `plan.md` (vedi Preparazione) così le altre skill possono
leggerlo. Quando l'utente lo chiede, ogni slot si sviluppa con /ig-reel o
/ig-carousel. Niente viene programmato o pubblicato: è un piano, e lo esegue
l'utente.
