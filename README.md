# Projekt

### **Ziel**

Ich möchte wissen, was einen erfolgreichen Online-Kurs ausmacht. Es gibt mehrere Anbieter wie Coursera, Youtube, Udemy, usw. Auch viele Kursleiter entscheiden sich, den Kurs selbst zu veröffentlichen. 

Wenn ich den Standpunkt von einem Anbieter oder einem Kursleiter einnehmen, gibt es zwei Hauptfrage, die ich beantworten möchte

* Welche Kategorie sind am erfolgereischsten? z.B. Data Science, Java, React.
* Welche Faktoren sind die wichtigsten für den Erfolg des Kurses in diesen Kategorien?

### **Dataset** 

Um diese Fragen zu beantworten, habe ich Udemy ausgewählt, weil Udemy eine Menge von Kursen aus verschiedenen Kategorien hat. Ich hoffe dass, ich durch das Verstehen der Udemy-Daten einen Einblick in die Fragen bekommen kann.

Ich kann nicht alle Kurskategorien auswählen, deshalb habe ich mich für Udemy-Kurse in Softwareentwicklung entschieden  (https://www.udemy.com/courses/development/). 

Alle Kursedetails wurden von der Udemy-Website mithilfe einem Web-Scrapingg-Tools (Apify) ausgelesen. Keine private Daten wurde gelesen, d.h. wurden nur offentlich verfügbare Daten  für Suchmaschinen berüchsichgt.

Die Datensatze beinhalten 10.000 Kurse und sind in einer JSON-Datei gespeichert. Jeder Kurs enthält Dutzende von Informationen in einer Mischung aus numerischen, textlichen, bildlichen und kategorialen Informationen. Das ermöglicht unterschiedliche Analysemethoden für dieses und weitere Projekte.

**Herausforderungen und Berücksichtigungen mit den Data** 

* Leider enthält dieser Datensatz keine Hinweise bezüglich der Art und Weise, wie ein Kurs beworben wir, oder über die Optimierung der "Conversion Rate". Das Udemy-Recommender-System, der Preisoptimierungsalgorithmus, und die Online-Werbung (z.B. durch das Newsletter, oder Suchmaschinen, oder Socialnetzwerke) könnte eine größere Einfluss auf den Erfolg eines Kurses haben.

* Zusätliche bietet Udemy kontinuerliche Rabatte für neue und vorhandene Nutzer an. Daher können wir nicht völlig auf die Preisdaten verlassen. In jedem fall sind die Rabatte in der Regel proportional zu den ursprünglichen Kurspreisen.

* Die Datensatz wird über einen in den USA basierten Proxy ausgelesen. Das bedeutet, dass alle Informationen auf English gespeichert werden. Außerdem könnte dir Standort die ausgelesenen Informationen beinflussen.

### Projektschritte

**1. :white_check_mark:  Datensatz erstellen**

Ich habe einen "Scrapper" von Apify (Online-Infrastrukturanbieter zur Ausführung von Crawler-Scripts) verwendet, um die Daten zu erfassen. 

Ich habe den Scrapper nicht selbst erstellt, sondern einen bestehenden gefunden. Allerdings benötigte der Scrapper meherere Trial-Runs zu funktionieren. Die Erstellung des vollständigen Datensatzs dauert mehrere Stunden (circa 3 Stunden um genau zu sein).

Die Daten wurden in einer 72MB JSON-Datei gespeichert. Die JSON-Datei enthält 10.000 Kurse. Im Ordner `/extract` finden Sie die Python-Script um den Scrapper "remote" zu starten, aber es benötigt einen Apigy API-key.

Das Ergebnis ist im Ordner `/data` zu finden. Die JSON-Datei ist `courses_udemy_raw.json` gennant.

**2. :white_check_mark:  Bereinigung und Vorbereitung des Datensatzes**

Vom `courses_udemy_raw.json` Datei habe ich zwei CSV-Dateien erstellt. `courses_numerical_categorical_data.csv` ist der numerische und kategorische Datensatz, `courses_textual_data.csv` ist der textliche Datensatz. Für jeden Datensatz habe ich auch eine Beispiel-Datei erstellt (mit 10% die Daten).

Die Transformation-Skripte werden im Ordner `transformation` gespeichert. Sie extrahiren die Daten aus `courses_udemy_raw.json` und schreiben sie in CSV Format. Sie bearbeiten auch jede Spalte, um sie zu bereinigen und nur die relevanten Informationen zu schreiben.

Ich habe Jupyter notebooks nicht verwendet, weil ich brauchte eine zuverlässige und schnell Bearbeitung der Daten. Da ich keine Erfahrung mit Python habe und seit Jahren nichts programmiert habe, kann ich nicht über die Code qualität beurteilen (z.B. Der Code ist sehr prozedural).

**3. :arrow_forward: Explotativ-Analyse in Jupyter Notebook**

In bearbeitung. Bitte sehen Sie sich die Datei `analyse_udemy_courses.ipynb` im Ordner `analysis` an.

**4. :question:  Dashboard erstellen und deploy**

*Zusätzlicher Schritt, falls ich Zeit habe*. 

In jedem Fall habe ich schon einen Beispiel mit Plotly https://exploratory-data-analysis.fly.dev/dashboard/histogram erstellt, um die Technologie zu testen. 

Ich habe ein Docker-Einstellung in `Dockerfile` und `docker-compose.yml` erstellt um das Projekt zu deployen. Fly.io kann meine Web-App automatisch mithilfe der Docker-Einstellung deployen.

Leider ist die erste Seitenaufruf langsam, weil die Maschine nicht ständig verfügbar ist, sondern sich nach einigen Minuten ausgeschalt und mit einer neuen Anfrage wieder aufwacht, um Kosten zu sparen. Das bedeutet, dass das erste Laden der Seite mehrere Sekunden dauert.

Ich bevorzuge Web-Frameworks mit weniger Abstraktion, daher habe ich mich gegen die Verwendung von Dash in diesem Projekt entscheiden. Stattdessen habe ich eine Web-App-Struktur mit FastAPI/HTMX/Tailwind erstellt. 


# Status des Projekts

- :white_check_mark: Projekt-Struktur in VS Code erstellt.
- :white_check_mark: Docker-Einstellung erstellt.
- :white_check_mark: Datensatz mit "Webscraper" erstellt.
- :white_check_mark: Bereinigung, Transformierung, und Vorbereitung des Datensatzes.
- :white_check_mark: Muster Dashboard-Webapp in FastAPI erstelllt.
- :white_check_mark: Auswahl der Cloud Dienstleistung (Fly.io) und Deployment.
- :arrow_forward: Explorativ-Analyse in Jupyter Notebook. Visualizierung mit Plotly.
    - Welche Faktoren sind generell am wichtigsten für den Erfolg eines Kurses?
        - :white_check_mark: Definierung der Target Variablen.
        - :arrow_forward: Einblicke in der Verteilung der Ziel-Variable.
        - :white_check_mark: Korrelationen zwischen numerischen Variablen.
        - :black_square_button: Hypothesen generieren und analysieren. 
        - :black_square_button: Analyse der kategorischen Variablen in Bezug auf die Ziel-Variable.
    - Welche Kategorie sind am erfolgereischsten? z.B. Data Science, Java, React.
        - :black_square_button: Erstellung der Analyse pro Subkategorie (mit ein Parameter).
        - :black_square_button: Generieren die Einblicke und vergleichen die Kategorien.

### Extras

Die folgende Schritte führe ich durch, falls ich genug Zeit habe, entweder im Laufe dieses Projekt oder nach dem Kurs.

- :black_square_button: **Build dashboard:** Eingabe ist ein Kategorie (z.B Data science) oder ein Label (z.B. Java). Ausgabe ist das Dashboard.
    - :black_square_button:	 Dashboard skizzieren. 
    - :black_square_button:	 Ausbau Dashboard mit Plotly und FastAPI/HTMX/Tailwind
        - :black_square_button:	 Auswahl eines UI-Kits
- :black_square_button: **Text Mining mit Spacy**:  
    - :black_square_button:	Wie der Name des Kurses (`title`, und `headline` Variablen) seinen Erfolg beeinflussen kann.
    - :black_square_button:	"Entity Recognition" mit Spacy (`taget_audience`, `requirements`, `objectives` Variablen). 
    - :black_square_button:	"Sentiment Analysis" mit Spacy (`what_will_you_learn` Variable).
    - :black_square_button: Häufigkeitsanalyse von "Entity" und "Sentiment" in erfolgreichen Kursen.