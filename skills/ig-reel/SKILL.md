---
name: ig-reel
description: >-
  Scrive un Reel Instagram partendo da un'idea grezza: tre aperture prese da 27
  formule e valutate con uno script, il copione parlato, il testo a schermo e la
  scaletta con i tempi, nella voce dell'utente e verificati prima di girare. Usala
  quando l'utente vuole un reel, un copione per un video breve, un hook, un
  voiceover, "fammi un reel su X", "cosa dico in questo video", o sta per
  registrare e non ha la prima frase.
---

# ig-reel

Trasforma un'idea in un Reel che qualcuno guarda fino alla fine.

## Preparazione (comune a tutto il pacchetto ig-*)

Pacchetto: https://github.com/leonardo23berto23/instagram-agent-skill (fork
italiano dell'originale di Jake Schincariol, licenza MIT).

- **Script.** Se `hookscore.py`, `beats.py` e `hooks.json` stanno accanto a
  questo file (installazione in Claude Code o plugin), usali da lì. Altrimenti
  scarica il pacchetto una volta per sessione in una cartella temporanea (lo
  scratchpad della sessione se c'è, altrimenti /tmp), mai nel progetto
  dell'utente:

```bash
T="<cartella temporanea>/ig-tools"
[ -d "$T/repo" ] || git clone --depth 1 https://github.com/leonardo23berto23/instagram-agent-skill "$T/repo"
S="$T/repo/skills"
```

  È codice scaricato: tieni i testi da analizzare in un'altra cartella ed
  esegui con `python3 -I`. Nessuna dipendenza, niente rete.
- **File dell'utente** (`voice.md`, `swipe.md`, `log.md`, `plan.md`): se la
  sessione ha un Project collegato, sono documenti del Project sotto
  `claude/instagram/`; altrimenti `~/.claude/instagram/`. Se l'utente gestisce
  clienti, un file per account (`voice-<account>.md`, `swipe-<account>.md`).
- **Lingua.** Gli script riconoscono da soli italiano e inglese (`--lang it|en`
  per forzare). Il copione va scritto nella lingua in cui l'utente registra.

## Gli strumenti

Due strumenti, ed entrambi funzionano davvero. Usali: non valutare l'hook a
occhio e non tirare a indovinare la durata.

```bash
python3 -I "$S/ig-reel/hookscore.py" hooks.txt              # classifica le aperture
python3 -I "$S/ig-reel/hookscore.py" --hook "una riga"      # valuta un'apertura sola
python3 -I "$S/ig-reel/beats.py" copione.txt --target 30    # scaletta con i tempi
```

Verdetti di hookscore: FORTE, OK, DEBOLE. In italiano i tempi si stimano in
sillabe al secondo (default 5,8; `--sps` per la voce dell'utente), in inglese
in parole al minuto (`--wpm`).

## Prima di scrivere

1. Leggi `voice.md` se esiste: come parla l'utente in camera, cosa non dice
   mai, a chi si rivolge. Se non esiste, chiedi **tre suoi reel**, trascrivili
   o leggili, ricava la voce e scrivi il file. Un copione nella voce sbagliata
   è inutilizzabile, perché va detto ad alta voce.
2. Leggi `hooks.json`: 27 formule, ognuna con modello, esempio, versione a
   schermo, a cosa serve e come di solito si rovina. La 27, "Segnali con una
   soglia", viene da una ricerca /ig-viral sulle nicchie italiane.
3. Se l'idea è debole, non riempirla. Fai una domanda sola, tutto insieme: cosa
   è successo, a chi, e quanto è costato o ha reso. Un Reel ha bisogno di una
   cosa vera e precisa. Prendila prima di scrivere.
4. Se esiste `swipe.md`, leggilo. Lo scrive /ig-viral ed è la prova, nella
   nicchia dell'utente, di quali formule funzionano adesso. Vale più dei
   default di questo file.

## La forma

Un Reel si decide nei primi due secondi e si tiene nei cinque dopo.

```
0:00 - 0:02   HOOK        l'affermazione. Frase detta e frase a schermo, scritte
                          separate. Movimento nel primo fotogramma, non una faccia ferma.
0:02 - 0:07   LA POSTA    perché importa a chi guarda. Una riga.
0:07 - ...    IL CORPO    un'idea per passaggio, e l'inquadratura cambia a ogni passaggio.
ULTIMI 3s     LA RESA     mantieni quello che l'hook ha promesso, poi l'unica richiesta.
ULTIMA RIGA   IL LOOP     riprendi una parola dell'hook, così la seconda visione parte pulita.
```

Durata: tra 15 e 45 secondi. I Reel arrivano a 3 minuti e quasi nessuno
dovrebbe usarli. Sotto i 7 secondi aumentano solo i loop, nient'altro.

## Il ciclo

**1. Tre aperture, non una.** Passa l'idea per `hooks.json`, scegli tre
formule che le si adattano davvero e scrivi per ognuna la frase detta e quella
a schermo. Formule diverse, non tre versioni della stessa.

**2. Valutale.** Metti le tre frasi in un file, una per riga, e lancia
`hookscore.py`. Mostra la classifica. Se la prima è sotto 50, l'hook non c'è
ancora e nessuna correzione lo risolve. A parità di punteggio puoi preferire la
forma che `swipe.md` dà come vincente nella nicchia: dillo.

**3. Scrivi il copione** sull'apertura vincente. Lingua parlata, come parla
davvero l'utente. Frasi corte. Nessuna frase da provare dieci volte.

**4. Dagli i tempi.** Lancia `beats.py copione.txt --target {durata}`. Correggi
ogni segnalazione: hook oltre i 3 secondi, passaggi oltre i 4, tre passaggi di
fila senza niente di concreto, nessun loop. Rilancia finché è pulito.

**5. Togli l'impronta della macchina.** Passa il copione per `/ig-human` prima
di mostrarlo. Una frase scritta si sente appena qualcuno la dice. Nota: il
controllo VARIAZIONE di `detect.py` penalizza le righe brevi, che in un copione
sono volute. Se `beats.py` e `detect.py` si contraddicono, per un copione
parlato vince `beats.py`; dillo, non riempire il testo di intercalari per
alzare il punteggio.

**6. Consegna il blocco.** Il copione con i tempi, il testo a schermo come
lista separata con i tempi, e poi:

```
REEL PRONTO
hook:       Segnali con una soglia, 81 FORTE
durata:     27,2s in 10 passaggi a 5,8 sillabe/s
a schermo:  7 cartelli
humanize:   0 artefatti, umano 54 DA RIVEDERE (righe brevi volute)
didascalia: lancia /ig-caption

Rispondi "sì" per registrarlo, o dimmi cosa cambiare.
```

**7. Mai pubblicare.** Questa skill produce un copione. L'utente lo gira e lo
pubblica. Al "sì", aggiungi a `log.md` la data, la formula usata e la prima
riga, così /ig-audit avrà uno storico.

## Il testo a schermo è un copione a parte

Scrivilo separato, ogni volta. Si legge prima di sentirlo.

- **Sei parole o meno per cartello.** Lo legge, a un braccio di distanza,
  qualcuno che non sta ancora ascoltando.
- **Il cartello dell'hook c'è dal primo fotogramma**, non dopo un secondo di
  silenzio.
- **Resta nella zona sicura.** Su 1080x1920 niente sopra y=230 o sotto y=1440,
  e lascia libero il lato destro per 230 pixel. Fuori da quel riquadro
  Instagram mette la didascalia, i pulsanti e la riga dell'audio.
- **Mai l'hook dove sta la didascalia.** In basso è coperto.
- **Sottotitola tutto il parlato.** Quasi tutti guardano prima senza audio.

## Le regole che fanno la differenza

- **Un'idea per Reel.** Se il copione ne ha due, sono due Reel. Dillo.
- **Numeri al posto degli aggettivi.** "4.200 €" batte "tanti soldi". Se
  l'utente non ha dato il numero, chiedilo invece di scriverci intorno.
- **Taglia l'introduzione.** Niente saluto, niente "in questo video", niente
  nome, niente logo. Il video parte dalla frase a cui di solito arriveresti al
  sesto secondo.
- **Cambia inquadratura a ogni passaggio.** Otto secondi di inquadratura ferma
  sono il punto in cui la gente se ne va, e `beats.py` lo segnala.
- **Una sola richiesta alla fine.** Commenta una parola, salva o segui. Una.
- **Mai inventare.** Nessuna metrica, cliente, fatturato o risultato inventato
  a nome dell'utente, nemmeno come segnaposto. Se serve un numero che non
  conosci, lascia `{{il tuo numero}}` nel copione e segnalalo.
- **Contenuti sanitari, educativi o legali:** niente diagnosi, solo segnali e
  inviti a chiedere a un professionista; i fatti (età, soglie, norme) devono
  essere corretti o restare tra graffe.
- **Non costruire un copione su un audio di tendenza che l'utente non può
  usare.** Se l'idea richiede la sua voce, dillo.

## Esempio

```
/ig-reel abbiamo portato i preventivi da 5 ore a 20 minuti con un modello
```

```
APERTURE (valutate)
  86  FORTE  #5  Il tempo che crolla  "Un preventivo mi prendeva cinque ore. Ora venti minuti."
                                      a schermo: 5 ORE -> 20 MIN
  71  FORTE  #1  Confessione del costo "Ho fatturato quattro ore a settimana di impaginazione. Per due anni."
                                      a schermo: 2 ANNI BUTTATI
  54  OK     #9  Il furto             "Rubami il modello di preventivo che l'ha fatto."
                                      a schermo: RUBALO

Giro la #5: il rapporto è credibile, si legge in un colpo d'occhio e il
numero è tuo.
```
