---
name: ig-profile
description: >-
  Dà un punteggio su 100 a un profilo Instagram con una griglia di 12 voci e
  riscrive le parti che perdono punti: campo nome, bio, link, storie in
  evidenza, tre post fissati, griglia. Funziona per brand personali e attività
  locali, e per analizzare il profilo di un potenziale cliente prima di
  proporsi. Usala quando l'utente dice "analizza questo profilo", "sistemami la
  bio", "dai un voto al mio Instagram", "perché non mi seguono", o incolla un
  profilo e chiede come si legge.
---

# ig-profile

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT). Questa skill non ha
script. La griglia è qui sotto; la stessa, con le note per voce, sta in
`rubric.json` accanto a questo file in un'installazione locale.

- **Lingua.** Ogni riscrittura nella lingua dei clienti del profilo. Le righe
  di bio in italiano vengono più lunghe di quelle inglesi: conta i caratteri
  contro i limiti di 30 e 150 ogni volta.
- **File utente.** Se l'analisi è per un cliente o un prospect e c'è un
  Project, salva il risultato come documento del Project (per esempio
  `claude/prospect-<account>.md`).

Quasi tutti ottimizzano la cosa sbagliata. Il profilo non è una vetrina che la
gente sfoglia. È una **schermata di decisione**, a cui si arriva da un reel o
da una ricerca su Google, e ha circa tre secondi per rispondere a una domanda:
qui c'è altro di quello che ho visto, ed è per me?

## Input

Servono: il campo nome, l'handle, la bio, dove porta il link, i nomi delle
storie in evidenza, cosa è fissato, le prime nove copertine della griglia, la
data dell'ultimo post, se i commenti hanno risposta, se c'è un anello delle
storie attivo.

Come averli, in ordine di preferenza:

1. L'utente incolla il testo o manda uno screenshot. La parte alta del profilo
   più le prime due righe della griglia bastano per un primo passaggio.
2. Il profilo è pubblico e c'è uno strumento browser: apri
   `instagram.com/<handle>` e leggilo. Non fare login su Instagram per conto
   dell'utente e non digitare mai le sue credenziali; un browser dove è già
   collegato va bene. Annota quello che hai letto prima di dare i punteggi,
   così l'utente può controllarlo.

Chiedi sempre di chi è il profilo: **account suo** o **prospect** (vedi
Modalità prospect), e se è una **persona** o un'**attività** (vedi Modalità
attività locale). Queste due risposte cambiano la griglia.

## La griglia (100 punti)

Dai un punteggio a ogni voce, mostra la tabella, dai il totale. Sii onesto. La
maggior parte dei profili, al primo passaggio, sta tra 30 e 45, e un punteggio
generoso non serve a nessuno.

| voce | punti | punteggio pieno | errore tipico |
| --- | --- | --- | --- |
| Campo nome | 12 | La riga in grassetto da 30 caratteri (non l'handle) porta il nome più cosa fai, con le parole che la gente cerca: "Dana Ruiz \| Modelli di preventivo". La ricerca di Instagram indicizza questo campo. | Solo il nome, o il nome con un'emoji, o lettere decorative che la ricerca non legge. |
| Bio, prima riga | 12 | Dice per chi è e cosa cambia per loro, con le loro parole. Non un titolo professionale, non aggettivi, non tre emoji separate da barre. | "Imprenditore \| Amante del caffè \| Papà". |
| Bio, corpo | 8 | Il resto dei 150 caratteri porta una prova o un'offerta precisa, in frasi, non in una lista con le barre. | Parole chiave buttate lì, o vuoto. |
| Tre post fissati | 10 | Tre post fissati con tre compiti diversi: la prova migliore, la spiegazione più chiara dell'offerta, la presentazione migliore della persona. Non i tre con più visualizzazioni per caso. | Niente fissato, quindi in cima c'è l'ultima cosa pubblicata. |
| Link | 8 | Una destinazione che corrisponde a quello che la bio ha appena promesso. Se ne possono mettere cinque; più di due è un menù, e un menù converte peggio di una porta. | Un link tree con undici voci, o nessun link. |
| Storie in evidenza | 8 | Da quattro a sei, chiamate come le domande di chi compra: Prezzi, Risultati, Come funziona, Chi sono. Copertine coerenti. Niente più vecchio di un anno davanti. | "Random", "Vita", "Preferiti", o 14 in ordine sparso. |
| Griglia leggibile | 8 | Le prime nove copertine si leggono a miniatura e dicono di cosa parla l'account senza toccare. Copertine dei reel scelte, non lasciate sul primo fotogramma. | Nove copertine di una faccia a metà parola, senza testo. |
| Foto profilo | 6 | Il volto riempie circa il 60% di un cerchio che si vede a circa 40 pixel. Occhi visibili, foto recente, sfondo che non distrae. | Foto a figura intera, un logo per un brand personale, un selfie al buio a braccio teso. |
| Handle | 6 | Leggibile, si dice ad alta voce, uguale sulle altre piattaforme. Niente underscore in fila o numeri al posto delle lettere. | Un handle che nessuno sa scrivere dopo averlo sentito una volta. |
| Categoria e contatti | 6 | Account professionale, categoria che corrisponde all'offerta, pulsanti di contatto che funzionano, un'email che qualcuno legge. | Account personale: niente insight, niente pulsante contatto. |
| Attività recente | 10 | Pubblicato negli ultimi sette giorni e risposto ai commenti dell'ultimo post. Un account che ha pubblicato l'ultima volta a marzo sembra chiuso. | Un buco di cinque settimane, o una fila di commenti senza risposta. |
| Storie | 6 | Una storia attiva adesso, o quasi ogni giorno. È la differenza tra un profilo e una persona. | Nessun anello, mai. |

I pesi sono voluti: campo nome, prima riga della bio e tre post fissati valgono
più della foto, perché sono quello che uno sconosciuto arrivato da un solo reel
legge davvero prima di decidere se seguire.

## Modalità attività locale (ristorante, bar, negozio, studio, centro, salone)

Stesse 12 voci, stessi punti, metro diverso. Qui chi visita di solito sta
decidendo se venire, prenotare o chiamare, non se seguire.

- **Campo nome**: nome dell'attività + cosa + paese, con le parole che la gente
  cerca: "Osteria Da Loriano | Cucina veneta Schio". Il paese è la parola
  cercata.
- **Bio, prima riga**: cosa si mangia o si trova lì e per chi, in una riga. Non
  "dal 1980", non la filosofia del fondatore.
- **Bio, corpo**: il motivo per venire questa settimana (piatto, offerta,
  evento) o la riga pratica: dove, quando è aperto, come si prenota.
- **Tre post fissati**: il posto (dieci secondi di ingresso), il prodotto o
  servizio simbolo, l'offerta o l'evento del momento.
- **Link**: prenotazione, menù, contatti o Google Maps. Uno. Non un link tree.
- **Storie in evidenza**: Menù / Servizi, Prenota, Dove e orari, Eventi,
  Recensioni. Da quattro a sei.
- **Foto profilo**: qui un logo leggibile o la vetrina vanno bene. Punteggio
  pieno a un logo che si legge a 40 pixel; toglilo solo se è illeggibile o è
  una foto di gruppo.
- **Categoria e contatti**: categoria giusta (Ristorante, non Marchio),
  indirizzo, telefono, orari, e il pulsante Prenota / Contatta collegato a
  qualcosa che risponde. Per un'attività questa voce conta di più: sii severo.
- **Attività recente** e **Storie**: per un posto aperto tutti i giorni, due
  settimane di silenzio si leggono come chiuso. La storia del piatto di oggi
  batte un post della griglia pianificato.

## Modalità prospect (un profilo che non è dell'utente)

Il risultato è materiale di vendita, quindi cambiano tre cose:

1. **Non riscrivere tutto.** Dai il punteggio, poi scegli le tre correzioni che
   perdono più punti e che il prospect può vedere da solo. Scrivi quelle tre
   come blocchi pronti da copiare. Il resto è una lista di una riga.
2. **Aggiungi una lettura dei contenuti dai dati pubblici.** Gli ultimi 12
   post: mix di formati, buchi di pubblicazione, visualizzazioni dei reel
   rispetto alla mediana di quei reel (multiplo, come fa /ig-audit), se i
   commenti hanno risposta. Niente reach, insight o fatturato inventati: solo
   quello che si vede.
3. **Scrivi la frase di aggancio.** Una frase che l'utente può mandare: il
   punteggio, la perdita visibile più grossa, e cosa cambia correggerla per un
   cliente che arriva da Google o da un reel. Nella lingua del prospect. Poi
   fermati. Il messaggio di contatto lo scrive /ig-dm, non questa skill.

Mai inventare un dato o una citazione sul prospect. Se una cosa non si vede
senza essere il proprietario (reach, salvataggi, follow), di' che non è nota.

## Poi riscrivi, in quest'ordine

Correggi in ordine di punti persi. Non riscrivere tutto insieme: l'utente deve
andare a cambiare davvero ognuna di queste cose.

**1. Il campo nome (30 caratteri).** La riga in grassetto sotto la foto, non
l'handle. È il campo su cui lavora la ricerca di Instagram, e quasi tutti ci
mettono il nome e nient'altro. Formato che funziona:
`{Nome} | {cosa fai, con parole cercate}`. Dai tre opzioni. Conta i caratteri.

**2. Prima riga della bio.** Per chi è e cosa cambia. Non un titolo, non
aggettivi, non una lista di identità con le barre. Il resto dei 150 caratteri
porta una prova o un'offerta semplice.

**3. I tre post fissati.** Tre posti, tre compiti diversi. È la correzione con
più leva di tutto il profilo e richiede quattro tocchi. Una griglia senza post
fissati mostra l'ultima cosa pubblicata, cioè un lancio di moneta.

**4. Storie in evidenza.** Da quattro a sei, chiamate come le domande di chi
compra. Non "Random". Il resto si cancella.

**5. Il link.** Una destinazione che corrisponde a quello che la bio ha appena
promesso.

**6. Copertine della griglia.** Le prime nove a dimensione miniatura. Le
copertine dei reel si scelgono, non si lasciano sul primo fotogramma. Quattro
parole di testo su una copertina rendono la griglia leggibile in un'occhiata.

Passa le riscritture per /ig-human (ha il lessico italiano). Controlla anche a
mano le frasi fatte da bio italiana: "passione", "tradizione e innovazione",
"dal 19xx" come prima riga, "seguici per", "a 360 gradi", "il tuo partner di
fiducia".

## Risultato

Cosa è stato letto (fonte e data), tabella dei punteggi, poi le riscritture
come blocchi pronti da copiare, in ordine di correzione. Ridai il punteggio
alla fine e mostra la differenza con onestà. Se la riscrittura arriva a 84 e non
a 98, di' 84, e di' cosa serve per il resto: di solito una griglia, l'abitudine
delle storie e un post da fissare che ancora non esiste. Niente di questo è una
riscrittura.

Questa skill non salva niente su Instagram. Ogni campo lo modifica l'utente.
