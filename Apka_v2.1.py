
Conversation with Gemini
Załączam kod aplikacji napisanej w Pythonie. Chciałbym dodać funkcjonalność, która pozwoli podczas rozmieszczania uczestników spotkania networkingowego brać pod uwagę nie tylko imię, nazwisko i nazwę firmy, ale również branżę, jaką dana firma reprezentuje.



Przeanalizuj załączony kod aplikacji i powiedz mi, jak rozumiesz jej działanie. Następnie, po potwierdzeniu wspólnego zrozumienia, przejdziemy do ustalenia, w jaki sposób wprowadzić dodatkowe funkcje. 

Załączam kod aplikacji napisanej w Pythonie. Chciałbym dodać funkcjonalność, która pozwoli podczas rozmieszczania uczestników spotkania networkingowego brać pod uwagę nie tylko imię, nazwisko i nazwę firmy, ale również branżę, jaką dana firma reprezentuje.



Przeanalizuj załączony kod aplikacji i powiedz mi, jak rozumiesz jej działanie. Następnie, po potwierdzeniu wspólnego zrozumienia, przejdziemy do ustalenia, w jaki sposób wprowadzić dodatkowe funkcje. 

Załączona aplikacja to napisany w Streamlit generator harmonogramu spotkań networkingowych, który wykorzystuje algorytm symulowanego wyżarzania (Simulated Annealing) do optymalnego rozsadzania uczestników przy stolikach w kolejnych rundach.   
Apka_v1.9.py

Poniżej znajduje się podsumowanie architektury i logiki działania obecnej wersji kodu (Apka_v1.9.py):

1. Wejście danych i parametryzacja
Struktura pliku Excel: Aplikacja wymaga pliku .xlsx z dwoma arkuszami: Uczestnicy (kolumny: Imię, Nazwisko, Firma) oraz Moderatorzy (Imię, Nazwisko). W kodzie każdy uczestnik jest reprezentowany jako 3-elementowa lista [Imię, Nazwisko, Firma], która podczas obliczeń jest rzutowana na krotkę (tuple), by mogła służyć jako klucz w słownikach.   
Apka_v1.9.py
+ 1

Stoliki i miejsca: Liczba stolików (
X) jest sztywno powiązana z liczbą wczytanych moderatorów (1 moderator = 1 stolik, przypisany do niego na stałe przez całe wydarzenie). Użytkownik definiuje całkowitą liczbę miejsc przy stoliku (
Y, z czego 
Y−1 to miejsca dla uczestników) oraz liczbę rund (
Z).   
Apka_v1.9.py
+ 1

Rekomendacja rund: System wylicza teoretyczną minimalną liczbę rund (
Z 
min
​
 =⌈(F−1)/(Y−2)⌉, gdzie 
F to liczba unikalnych firm), potrzebną, aby uczestnik miał szansę spotkać reprezentanta każdej innej firmy.   
Apka_v1.9.py

Obsługa nadmiaru/niedoboru osób:

Jeśli uczestników jest więcej niż miejsc (
X×(Y−1)), aplikacja obcina listę do maksymalnej pojemności sali, a nadmiarowe osoby wyświetla na liście nieuwzględnionych.   
Apka_v1.9.py

Jeśli miejsc jest więcej niż osób, puste krzesła są wypełniane wirtualnymi bytami ["Wolne", "Miejsce", "Brak"] (tzw. padding), które są następnie ignorowane przy zliczaniu statystyk, kar i na wydrukach.   
Apka_v1.9.py

2. Silnik optymalizacyjny (generate_networking_schedule)
Rozmieszczenie uczestników jest optymalizowane metodą symulowanego wyżarzania (parametry: temperatura początkowa 
T=1000.0, współczynnik chłodzenia 
0.995, 
T 
min
​
 =0.1, co daje ok. 1838 iteracji).   
Apka_v1.9.py

Stan początkowy i sąsiedztwo: W każdej rundzie uczestnicy są najpierw rozlosowywani. W pojedynczym kroku optymalizacji algorytm losuje jedną rundę, wybiera w niej dwa różne stoliki i zamienia miejscami dwóch losowych uczestników.   
Apka_v1.9.py
+ 1

Funkcja kosztu (calculate_cost): Algorytm dąży do minimalizacji sumy punktów karnych, które są naliczane według obecnej hierarchii wag:   
Apka_v1.9.py

Konflikt firmowy (+500 pkt): Najwyższa kara za posadzenie przy jednym stoliku w tej samej rundzie dwóch osób z tej samej firmy.   
Apka_v1.9.py

Powtórzone spotkanie uczestników (+100 pkt): Kara za każde kolejne spotkanie tej samej pary uczestników w skali całego wydarzenia.   
Apka_v1.9.py

Powtórzony stolik / moderator (+50 pkt): Kara za posadzenie uczestnika przy tym samym stoliku (u tego samego moderatora) w więcej niż jednej rundzie.   
Apka_v1.9.py

3. Wizualizacja, statystyki i eksport
Po zakończeniu optymalizacji dane zapisywane są w st.session_state i prezentowane w interfejsie:   
Apka_v1.9.py

Metryki: Liczba stolików, liczba nierozwiązanych konfliktów firmowych oraz procent unikalnych spotkań.   
Apka_v1.9.py

Wizualizacja (Plotly) i tabele: Dla każdej rundy generowana jest osobna zakładka z interaktywnym rzutem sali (moderator jako złota gwiazda, uczestnicy jako kółka pokolorowane według przynależności do firmy, opisani skrótem P1, P2... w kolejności alfabetycznej nazwisk) oraz tabelarycznym wykazem składów stolików.   
Apka_v1.9.py

Moduł eksportu:

Excel (openpyxl): Pełny harmonogram (Runda, Stolik, Rola, Imię, Nazwisko, Firma).   
Apka_v1.9.py

Plakietki PDF (reportlab): Identyfikatory dla uczestników (układ kafelkowy na A4) z imieniem, nazwiskiem, nazwą firmy i indywidualną ścieżką stolików w kolejnych rundach (np. R1: Stół 2 | R2: Stół 5).   
Apka_v1.9.py

Plan Sali PDF (reportlab): Graficzny rozkład stolików na A4 w orientacji poziomej. Jeśli uczestników jest 
≤30, legenda (P1: Imię Nazwisko (Firma)) drukowana jest z boku na tej samej stronie; powyżej 30 osób – jako osobne strony z listami przypisanymi do stolików.   
Apka_v1.9.py
+ 1

Techniczny punkt uwagi w kontekście rozbudowy o "Branżę"
Przeglądając kod pod kątem zmian, które planujesz, warto od razu odnotować dwa miejsca konstrukcyjne:

Sztywne indeksowanie i krotki: W całym kodzie uczestnik jest traktowany jako lista p, gdzie p[0] to Imię, p[1] to Nazwisko, a p[2] to Firma. Dodanie branży jako p[3] automatycznie rozszerzy krotkę tuple(p), co jest korzystne (nie zepsuje kluczy w słownikach), ale będzie wymagało uzupełnienia wirtualnych pustych miejsc do 4 elementów: ["Wolne", "Miejsce", "Brak", "Brak"].   
Apka_v1.9.py

Drobna usterka przy duplikatach danych: Jeśli w pliku wejściowym pojawią się dwie osoby o tym samym imieniu, nazwisku i firmie (lub błąd duplikacji wiersza), rzutowanie tuple(p) spowoduje nadpisanie klucza w słownikach participant_ids i history. Nie blokuje to samego dodania branży, ale warto o tym pamiętać.   
Apka_v1.9.py

Daj znać, czy powyższy opis w pełni pokrywa się z Twoim zamysłem działania aplikacji. Jeśli tak, przejdźmy do szczegółów nowej funkcjonalności – napisz, jaką rolę ma pełnić branża w algorytmie i interfejsie, w szczególności:

Cel optymalizacyjny: Czy chcemy unikać sadzania osób z tej samej branży przy jednym stoliku (dywersyfikacja / wykluczanie konkurencji – dodatkowa kara w funkcji kosztu), czy odwrotnie – grupować ludzi z tych samych/pokrewnych branż (stworzenie stolików tematycznych)?

Priorytet (waga): Jak ważna jest branża w stosunku do konfliktu firmowego (500 pkt) i powtórzonego spotkania tych samych osób (100 pkt)?   
Apka_v1.9.py

Wizualizacja i wydruki: Czy branża ma się pojawiać na plakietkach PDF, listach stolików, w chmurkach (hover) na wykresie i w eksporcie do Excela? Czy kolorowanie kropek na wykresie ma pozostać przypisane do firm, czy zmienić je na branże?   
Apka_v1.9.py

Ad.1. chcemy unikać sadzania osób z tej samej branży przy jednym stoliku

Ad.2. waga dla branży - 200pkt

Ad3. branża nie pojawia się na żadnym z wymienionych elementów. Kolorowanie kropek pozostawiamy bez zmian



Zanim przejdziemy do pisania kodu, omówmy jeszcze kwestię sposobu opisania branży w pliku wejściowym. Rozumiem, że najprostszym rozwiązaniem będzie stosowanie w polu „branża” listy wartości. Dzięki temu unikniemy rozbieżnych opisów tej samej branży. Ale zastanawiam się, czy dalibyśmy radę obsłużyć w takiej aplikacji opisy branży dodawane ręcznie, czyli analizować treść opisów i na ich podstawie wnioskować, jaka to branża i czy będzie kolidowała z branżą opisaną w sposób nieidentyczny. Rozumiem, że w tym drugim scenariuszu musielibyśmy użyć jakiegoś elementu wnioskowania AI. I pytanie, czy da się w ogóle taki element zaszyć w takiej aplikacji i czy nie będzie to bardzo skomplikowane do zrobienia? 

Zaszycie takiego wnioskowania w aplikacji Streamlit jest w pełni wykonalne i technicznie dość proste (to zazwyczaj około 30–50 dodatkowych linijek kodu).

Kluczowe założenie architektoniczne jest takie: AI nie może działać wewnątrz pętli optymalizacyjnej (calculate_cost), ponieważ algorytm symulowanego wyżarzania wykonuje blisko 2000 iteracji. Odpytywanie modelu w każdym kroku trwałoby kilkadziesiąt minut i generowało niepotrzebne koszty.   
Apka_v1.9.py

Zamiast tego stosuje się jednorazowy preprocessing (normalizację) w momencie wgrania pliku Excel lub tuż przed uruchomieniem optymalizacji. Gdy uczestnicy wpiszą ręcznie np.: "tworzenie oprogramowania", "Software House", "IT / Dev" oraz "spedycja międzynarodowa" i "transport drogowy", AI w ułamku sekundy sprowadza to do wspólnych mianowników (np. IT oraz Transport i Logistyka), a sam algorytm losujący operuje już na czystych, znormalizowanych etykietach (lub gotowej macierzy podobieństw), zachowując dotychczasową szybkość działania.

Możemy to zrealizować na trzy główne sposoby – od najprostszego wdrożeniowo po najbardziej autonomiczny:

Wariant 1: Kategoryzacja i grupowanie przez API LLM (np. Gemini / OpenAI) – Rekomendowany
Jak to działa: Po wczytaniu Excela wyciągamy listę wszystkich unikalnych opisów branż wpisanych przez uczestników (przy 50–100 uczestnikach będzie to kilkadziesiąt krótkich fraz). Wysyłamy je w jednym zapytaniu (jednym prompcie) do lekkiego i szybkiego modelu (np. gemini-2.5-flash lub gpt-4o-mini) z instrukcją: "Przeanalizuj poniższe opisy działalności i pogrupuj je w spójne kategorie branżowe, tak aby firmy konkurencyjne lub z tego samego sektora otrzymały identyczną etykietę. Zwróć wynik jako JSON (oryginalny_opis -> znormalizowana_kategoria)".

Zalety:

Najwyższa inteligencja biznesowa – LLM świetnie rozumie kontekst, skróty (np. FMCG, SaaS, B2B, OZE), literówki i mieszankę polskiego z angielskim.

Czas wykonania to ok. 1–2 sekundy, a koszt jednego uruchomienia dla kilkudziesięciu rekordów to ułamki grosza.

Kod w Pythonie jest bardzo krótki i nie obciąża pamięci RAM serwera, na którym stoi Streamlit.

Wymagania: Konieczność podpięcia klucza API (np. w st.secrets w Streamlit lub jako pole do wklejenia w interfejsie) oraz zainstalowania biblioteki klienta (google-genai lub openai).

Wariant 2: Wykorzystanie Embeddingów (podobieństwo semantyczne / wektorowe)
Jak to działa: Każdy ręczny opis zamieniamy za pomocą modelu embeddingowego na wektor liczbowy i liczymy tzw. podobieństwo cosinusowe (cosine similarity) pomiędzy każdą parą uczestników. Jeśli podobieństwo przekracza ustalony próg (np. 
0.75), uznajemy, że branże kolidują. Co więcej, kara nie musi być wtedy zero-jedynkowa (0 lub 200 pkt) – może być płynna lub stopniowana w zależności od tego, jak bardzo opisy są do siebie zbliżone.

Zalety: Matematyczna precyzja i brak ryzyka, że model językowy zbyt szeroko lub zbyt wąsko nazwie kategorię.

Wady:

Jeśli używamy modeli lokalnych (np. sentence-transformers bez zewnętrznego API), aplikacja musi pobrać model ważący kilkaset megabajtów, co na darmowym hostingu (np. Streamlit Community Cloud) często powoduje przekroczenie limitu pamięci RAM (1 GB) i powolny start.

Krótkie hasła wpisane przez ludzi (np. samo słowo "usługi" vs "doradztwo") czasem dają mniej trafne wyniki wektorowe niż pełna kategoryzacja przez LLM z Wariantu 1.

Wariant 3: Klasyczny Fuzzy Matching (bez AI – np. biblioteka rapidfuzz)
Jak to działa: Porównujemy ciągi znaków pod kątem podobieństwa literowego. Wyłapie to różnice typu "Marketing internetowy" vs "Marketing Internetowy - agencja", ale nie zrozumie synonimów (dla tego algorytmu "Prawo" i "Kancelaria Adwokacka" to zupełnie inne słowa). Wspominam o tym wyłącznie dla pełnego obrazu – przy swobodnych opisach uczestników to rozwiązanie będzie niewystarczające.

Dodatkowy atut w UI: Krok weryfikacji dla organizatora
Niezależnie od tego, czy wybierzesz kategoryzację przez LLM, bardzo dobrą praktyką w takim narzędziu jest wyświetlenie organizatorowi (zaraz po wgraniu pliku, w zwijanym boksie st.expander lub edytowalnej tabeli st.data_editor) propozycji zmapowania wygenerowanej przez AI:

"AI przypisało następujące kategorie branżowe na podstawie opisów. Możesz je skorygować przed losowaniem:"

Jan Kowalski | "Budowa domów szkieletowych" 
→ Budownictwo i Nieruchomości

Anna Nowak | "Generalny wykonawca inwestycji" 
→ Budownictwo i Nieruchomości

Dzięki temu łączysz automatyzację AI z pełną kontrolą człowieka nad ostatecznym kształtem koszyków branżowych.

Podsumowując – co wybieramy?
Czy pozostajemy przy sztywnej liście wyboru w Excelu (szybkie wdrożenie bez zewnętrznych zależności)?

Czy wdrażamy normalizację opisów przez AI (Wariant 1 z API LLM) – a jeśli tak, to z którego dostawcy API najwygodniej Ci korzystać (OpenAI, Google Gemini, Anthropic)?

Czy w przypadku dokładania kar branżowych (200 pkt) chcesz również widzieć liczbę „Konfliktów branżowych” w żółtych kafelkach z metrykami na ekranie podsumowania (obok „Konfliktów firmowych”), aby wiedzieć, czy algorytm zdołał je wyzerować?   
Apka_v1.9.py
+ 1

Ok. Zróbmy wersję bez wnioskowania AI, tzn. taką, która opiera się na założeniu, że plik wejściowy w polu branża zawiera unikalne, zweryfikowane opisy branż. Zaproponuj całą, kompletną treść nowego kodu. Jeśli musimy jeszcze coś ustalić przed jego wygenerowaniem to zadaj wymagane pytania.

Twój plik z kodem w języku Python jest gotowy do pobrania:

PY icon
Apka_v2.0
 PY 
Wszystkie założenia były jasne, więc od razu przygotowałem kompletną wersję (Apka_v2.0.py). Poniżej znajdziesz zestawienie wprowadzonych zmian konstrukcyjnych oraz pełną treść kodu.

Kluczowe zmiany w kodzie (v1.9 
→ v2.0)
Rozszerzenie struktury danych uczestnika:

Każdy uczestnik jest teraz 4-elementową listą [Imię, Nazwisko, Firma, Branża], a wirtualne wolne miejsca to ["Wolne", "Miejsce", "Brak", "Brak"].

Dodano walidację sprawdzającą, czy arkusz Uczestnicy zawiera kolumnę Branża. Jeśli u któregoś uczestnika komórka z branżą będzie pusta (NaN), skrypt nie odrzuci takiej osoby (jak robi to przy braku imienia czy firmy), tylko przypisze jej branżę "Brak", dzięki czemu weźmie ona udział w losowaniu bez generowania sztucznych konfliktów branżowych.   
Apka_v1.9.py

Brak podwójnego karania w funkcji kosztu (calculate_cost):

Zastosowałem konstrukcję if ... elif ... przy sprawdzaniu firmy i branży. Jeśli dwie osoby przy stoliku są z tej samej firmy (i tym samym mają tę samą branżę), algorytm nalicza 500 pkt kary za konflikt firmowy, ale nie dolicza już dodatkowych 200 pkt za branżę. Kara 200 pkt (oraz zliczanie konfliktu branżowego) uruchamia się wyłącznie wtedy, gdy przy stoliku usiądą osoby z różnych firm, ale z tej samej branży.   
Apka_v1.9.py

Połączono dwie osobne pętle iterujące po stoliku w jedną (wcześniej kod osobno iterował po firmach i osobno po parach uczestników), co przyspiesza pojedynczą iterację symulowanego wyżarzania.   
Apka_v1.9.py

Metryka na ekranie wyników:

W sekcji podsumowania układ kolumn zmienił się z 3 na 4 (st.columns(4)), aby obok „Konfliktów firmowych” wyświetlić kafelek „Konflikty branżowe” pokazujący, na ile skutecznie algorytm zdołał rozdzielić konkurentów z tego samego sektora.   
Apka_v1.9.py

Zachowanie czystości widoków i wydruków:

Zgodnie z ustaleniami, wykresy Plotly, tabele stolików, lista osób nieuwzględnionych (p[:3]), plakietki PDF, plan sali PDF oraz eksportowany plik Excel zawierają wyłącznie Imię, Nazwisko oraz Firmę.   
Apka_v1.9.py

Pełny kod aplikacji (Apka_v2.0.py)
Python
import streamlit as st
import pandas as pd
import random
import math
import copy
import os
from collections import defaultdict
import plotly.graph_objects as go
import plotly.colors
import io

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ==========================================
# KONFIGURACJA STRONY STREAMLIT
# ==========================================
st.set_page_config(page_title="Generator Networkingu", layout="wide", page_icon="🤝")

# ==========================================
# BEZPIECZNA TYPOGRAFIA I CSS (MINIMALIZM)
# ==========================================
st.markdown("""
    <style>
        /* Import nowoczesnej czcionki */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* 1. BEZPIECZNA ZMIANA CZCIONKI DLA TEKSTÓW */
        /* Celujemy tylko w tagi tekstowe, omijając span i div, aby nie zepsuć ikon Streamlita */
        html, body, p, li, label, input, button, h1, h2, h3, .stMarkdown {
            font-family: 'Inter', sans-serif !important;
        }

        /* OCHRONA IKON (Wymuszenie oryginalnej czcionki dla strzałek i menu) */
        .material-symbols-rounded, .stIcon,[data-testid="stExpanderToggleIcon"], [data-testid="stSidebarCollapseButton"] span {
            font-family: 'Material Symbols Rounded', sans-serif !important;
        }

        /* 2. BARDZO DUŻY ROZMIAR (1.5rem) - Tylko dla nagłówków */
        h1, h2, h3, .recommendation-title {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            padding-bottom: 0.5rem;
        }

        /* 3. DUŻY ROZMIAR (1.0rem) - Dla tekstów, etykiet, inputów i przycisków */
        p, li, label, input, .stButton button {
            font-size: 1.0rem !important;
        }

        /* Pogrubienie etykiet nad polami do wpisywania */
        label {
            font-weight: 600 !important;
        }

        /* 4. BOX REKOMENDACJI (Dostosowany do jasnego/ciemnego motywu) */
        .recommendation-box {
            background-color: rgba(34, 197, 94, 0.15); 
            border-left: 0.4rem solid #22c55e;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }

/* ==========================================
           NADPISANIE ROZMIARÓW: KONFIGURACJA (st.number_input)
           ========================================== */
        
        /* Etykiety: "Miejsca przy stoliku", "Docelowa liczba rund" */
        div[data-testid="stNumberInput"] label p,
        div[data-testid="stNumberInput"] label {
            font-size: 1.2rem !important; /* Zmień na swój docelowy rozmiar */
        }
        
        /* Cyfry wewnątrz pola do wpisywania */
        div[data-testid="stNumberInput"] input {
            font-size: 1.2rem !important; /* Zmień na swój docelowy rozmiar */
        }

       /* ==========================================
           NADPISANIE ROZMIARÓW: OPISY METRYK (st.metric)
           ========================================== */
        
        /* Obejmujemy główny kontener metryki i każdy możliwy tekst (p, label, div, span) nad wartością */
        div[data-testid="stMetric"] label p,
        div[data-testid="stMetric"] label div,
        div[data-testid="stMetric"] label span,
        div[data-testid="stMetric"] label,
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] {
            font-size: 1.5rem !important; /* <-- Tutaj ustaw swój rozmiar dla "Liczba stolików" itp. */
            
        }
        
        /* 2. Główne wartości (duże liczby, np. "10", "85.50%") */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            font-size: 2.0rem !important; /* Zmień na swój docelowy rozmiar liczby */
        }

        /* 3. Wartość delty (tekst i strzałka pod wartością np. w "Konflikty firmowe") */
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] * {
            font-size: 1.0rem !important; /* Zmień na swój docelowy rozmiar delty */
        }

/* ==========================================
           WYGLĄD KAFELKÓW METRYK (TŁO I KOLOR)
           ========================================== */
        
        /* 1. Jasnożółte tło, marginesy i zaokrąglenia dla całego kafelka metryki */
        div[data-testid="stMetric"] {
            background-color: #FEF9C3 !important; /* Jasnożółte tło */
            padding: 1rem !important;             /* Wewnętrzny odstęp, by tekst nie dotykał krawędzi */
            border-radius: 0.5rem !important;     /* Zaokrąglone rogi */
            border: 1px solid #FDE047 !important; /* Ciemniejsza, żółta ramka wokół (opcjonalnie) */
        }

        /* 2. Wymuszenie CZARNEJ czcionki dla opisu (etykiety) */
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] label p,
        div[data-testid="stMetric"] label div,
        div[data-testid="stMetric"] label span {
            color: #000000 !important;
        }

        /* 3. Wymuszenie CZARNEJ czcionki dla dużej wartości liczbowej */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            color: #000000 !important;
        }

/* ==========================================
           NADPISANIE ROZMIARU: GŁÓWNY TYTUŁ (st.title)
           ========================================== */
        
        /* Celujemy wyłącznie w tag <h1> w głównej części strony (omijając pasek boczny) */
        .block-container h1,
        div[data-testid="stMainBlockContainer"] h1 {
            font-size: 2.0rem !important; /* <-- Tutaj wpisz swój docelowy rozmiar (np. 3.0rem lub 4.0rem) */
            
            /* Opcjonalnie: możesz tu też zmienić kolor lub wyśrodkować główny tytuł */
            /* text-align: center !important; */
            /* color: #22c55e !important; */
        }

/* ==========================================
           NADPISANIE SZEROKOŚCI OKNA POPUP (DIALOG)
           ========================================== */
        
        /* Wymuszenie szerokości na 75% ekranu (75vw = 75% viewport width) */
        div[data-testid="stModal"] > div[role="dialog"],
        div[data-testid="stDialog"] {
            width: 85vw !important;
            min-width: 85vw !important;
            max-width: 95vw !important;
        }

/* ==========================================
   CAŁKOWITE UKRYCIE NAGŁÓWKA I STOPKI 
   (Możliwe, bo zrezygnowaliśmy z panelu bocznego)
   ========================================== */
   
    header {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }
    
    footer {
        visibility: hidden !important;
        display: none !important;
    }


    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNKCJE POMOCNICZE
# ==========================================

def reset_plan():
    if 'plan_ready' in st.session_state:
        st.session_state['plan_ready'] = False

@st.cache_resource
def setup_fonts():
    # Ścieżki relatywne - wskazują na folder 'fonts' w Twoim repozytorium GitHub
    font_path = "Fonts/DejaVuSans.ttf"
    font_bold_path = "Fonts/DejaVuSans-Bold.ttf"
    
    try:
        if os.path.exists(font_path) and os.path.exists(font_bold_path):
            pdfmetrics.registerFont(TTFont('CustomFont', font_path))
            pdfmetrics.registerFont(TTFont('CustomFont-Bold', font_bold_path))
            return True
        return False
    except Exception as e:
        print(f"Błąd ładowania czcionki: {e}")
        return False

def generate_networking_schedule(participants, moderators, X, Y, Z):
    slots_needed = X * (Y - 1)
    # Struktura uczestnika: [Imię, Nazwisko, Firma, Branża]
    participants_padded = participants + [["Wolne", "Miejsce", "Brak", "Brak"]] * (slots_needed - len(participants))

    def calculate_cost(schedule):
        cost = 0
        meetings = defaultdict(int)
        mod_meetings = defaultdict(int)
        company_conflicts = 0
        industry_conflicts = 0
        
        for round_idx, round_tables in enumerate(schedule):
            for table_idx, table_participants in enumerate(round_tables):
                valid_participants = [p for p in table_participants if p[2] != "Brak"]
                
                for i in range(len(valid_participants)):
                    p1 = valid_participants[i]
                    p1_tuple = tuple(p1)
                    
                    # Kara za spotkanie u tego samego moderatora (przy tym samym stoliku)
                    mod_meetings[(p1_tuple, table_idx)] += 1
                    if mod_meetings[(p1_tuple, table_idx)] > 1:
                        cost += 50
                    
                    for j in range(i + 1, len(valid_participants)):
                        p2 = valid_participants[j]
                        p2_tuple = tuple(p2)
                        
                        # 1. Konflikt firmowy (+500 pkt)
                        if p1[2] == p2[2]:
                            company_conflicts += 1
                            cost += 500
                        # 2. Konflikt branżowy (+200 pkt) - naliczany dla różnych firm z tej samej branży
                        elif p1[3] != "Brak" and p1[3] == p2[3]:
                            industry_conflicts += 1
                            cost += 200
                        
                        # 3. Powtórzone spotkanie tej samej pary uczestników (+100 pkt)
                        pair = tuple(sorted([p1_tuple, p2_tuple]))
                        meetings[pair] += 1
                        if meetings[pair] > 1:
                            cost += 100
                            
        return cost, company_conflicts, industry_conflicts

    def generate_initial_schedule():
        schedule = []
        for _ in range(Z):
            round_participants = participants_padded[:]
            random.shuffle(round_participants)
            round_tables = [round_participants[i*(Y-1):(i+1)*(Y-1)] for i in range(X)]
            schedule.append(round_tables)
        return schedule

    def get_neighbor(schedule):
        new_schedule = copy.deepcopy(schedule)
        r = random.randint(0, Z-1)
        t1, t2 = random.randint(0, X-1), random.randint(0, X-1)
        while t1 == t2 and X > 1:
            t2 = random.randint(0, X-1)
        
        p1, p2 = random.randint(0, Y-2), random.randint(0, Y-2)
        new_schedule[r][t1][p1], new_schedule[r][t2][p2] = new_schedule[r][t2][p2], new_schedule[r][t1][p1]
        return new_schedule

    current_schedule = generate_initial_schedule()
    current_cost, _, _ = calculate_cost(current_schedule)
    best_schedule, best_cost = current_schedule, current_cost

    T = 1000.0
    cooling_rate = 0.995
    min_T = 0.1

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_iterations = math.log(min_T / T) / math.log(cooling_rate)
    current_iteration = 0

    while T > min_T:
        neighbor = get_neighbor(current_schedule)
        neighbor_cost, _, _ = calculate_cost(neighbor)
        
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / T):
            current_schedule = neighbor
            current_cost = neighbor_cost
            
            if current_cost < best_cost:
                best_schedule = current_schedule
                best_cost = current_cost
                
        T *= cooling_rate
        current_iteration += 1
        
        if current_iteration % 100 == 0:
            progress = min(1.0, current_iteration / total_iterations)
            progress_bar.progress(progress)
            status_text.text(f"Optymalizacja w toku... (Koszt: {best_cost})")

    progress_bar.empty()
    status_text.empty()

    final_cost, company_conflicts, industry_conflicts = calculate_cost(best_schedule)
    
    unique_meetings_per_participant = defaultdict(set)
    for round_idx, round_tables in enumerate(best_schedule):
        for table_idx, table_participants in enumerate(round_tables):
            for p1 in table_participants:
                if p1[2] == "Brak": continue
                p1_tuple = tuple(p1)
                unique_meetings_per_participant[p1_tuple].add(f"Mod_{table_idx}")
                for p2 in table_participants:
                    if p1 == p2 or p2[2] == "Brak": continue
                    unique_meetings_per_participant[p1_tuple].add(tuple(p2))

    total_unique = sum(len(v) for v in unique_meetings_per_participant.values())
    expected_meetings = len(participants) * (Z * (Y - 2) + Z)
    unique_percentage = (total_unique / expected_meetings) * 100 if expected_meetings > 0 else 0

    return best_schedule, company_conflicts, industry_conflicts, unique_percentage

def visualize_schedule_plotly(schedule, moderators, participants_data, X, Y, Z):
    participant_ids = {}
    sorted_participants = sorted([p for p in participants_data if p[2] != "Brak"], key=lambda x: x[1])
    for i, p in enumerate(sorted_participants):
        participant_ids[tuple(p)] = f"P{i+1}"

    companies = set([p[2] for p in sorted_participants])
    palette = plotly.colors.qualitative.Pastel + plotly.colors.qualitative.Set3
    company_colors = {comp: palette[i % len(palette)] for i, comp in enumerate(companies)}

    figs = []
    cols = math.ceil(math.sqrt(X))
    rows = math.ceil(X / cols)
    
    table_spacing_x = 5
    table_spacing_y = 5
    
    for r in range(Z):
        fig = go.Figure()
        
        for t in range(X):
            col = t % cols
            row = rows - 1 - (t // cols)
            
            center_x = col * table_spacing_x
            center_y = row * table_spacing_y
            
            fig.add_shape(type="circle",
                x0=center_x - 1, y0=center_y - 1,
                x1=center_x + 1, y1=center_y + 1,
                line_color="gray", fillcolor="lightgray", opacity=0.3
            )
            
            # Wymuszony czarny kolor i pogrubienie dla numeru stołu
            fig.add_annotation(
                x=center_x, y=center_y, 
                text=f"<b>STÓŁ {t+1}</b>", 
                showarrow=False, 
                font=dict(size=16, color="black")
            )
            
            participants = [p for p in schedule[r][t] if p[2] != "Brak"]
            K = len(participants)
            M = 1 + K 
            
            if M > 0:
                alpha = (2 * math.pi) / M 
                radius = 1.2 
                
                mod_angle = math.pi / 2
                mod_x = center_x + radius * math.cos(mod_angle)
                mod_y = center_y + radius * math.sin(mod_angle)
                
                mod = moderators[t]
                fig.add_trace(go.Scatter(
                    x=[mod_x], y=[mod_y],
                    mode='markers+text',
                    marker=dict(size=40, color='gold', symbol='star', line=dict(width=1, color='darkgoldenrod')),
                    text=["<b>M</b>"],
                    textposition="middle center",
                    hoverinfo="text",
                    hovertext=[f"<b>Moderator:</b><br>{mod[0]} {mod[1]}"],
                    showlegend=False,
                    textfont=dict(size=16, color="black") # Wymuszony czarny kolor
                ))
                
                for i, p in enumerate(participants):
                    p_angle = mod_angle - (i + 1) * alpha
                    
                    px = center_x + radius * math.cos(p_angle)
                    py = center_y + radius * math.sin(p_angle)
                    
                    comp = p[2]
                    color = company_colors[comp]
                    p_id = participant_ids[tuple(p)]
                    
                    hover_text = f"<b>{p[0]} {p[1]}</b><br>Firma: {comp}"
                    
                    fig.add_trace(go.Scatter(
                        x=[px], y=[py],
                        mode='markers+text',
                        marker=dict(size=40, color=color, symbol='circle', line=dict(width=1, color='black')),
                        text=[f"<b>{p_id}</b>"],
                        textposition="middle center",
                        hoverinfo="text",
                        hovertext=[hover_text],
                        showlegend=False,
                        textfont=dict(size=16, color="black") # Wymuszony czarny kolor
                    ))
        
        # Globalne wymuszenie czcionek i tła dla spójności z PDF/PNG
        fig.update_layout(
            title=dict(text=f"<b>Wizualizacja - Runda {r+1}</b>", font=dict(size=24, color="black"), x=0.5),
            xaxis=dict(visible=False, range=[-2, cols*table_spacing_x + 2]), 
            yaxis=dict(visible=False, range=[-2, rows*table_spacing_y]),
            width=max(800, cols * 300), 
            height=max(600, rows * 300),
            plot_bgcolor="white",
            paper_bgcolor="white", # Wymusza białe tło poza obszarem rysowania
            font=dict(color="black"), # Globalny fallback na czarny kolor
            margin=dict(l=40, r=40, t=80, b=40)
        )
        figs.append(fig)
        
    return figs



def generate_visual_plan_pdf_buffer(schedule, moderators, participants_data, X, Y, Z):
    fonts_ready = setup_fonts()
    font_regular = "CustomFont" if fonts_ready else "Helvetica"
    font_bold = "CustomFont-Bold" if fonts_ready else "Helvetica-Bold"

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    participant_ids = {}
    sorted_participants = sorted([p for p in participants_data if p[2] != "Brak"], key=lambda x: x[1])
    for i, p in enumerate(sorted_participants):
        participant_ids[tuple(p)] = f"P{i+1}"

    cols = math.ceil(math.sqrt(X))
    rows = math.ceil(X / cols)

    margin_x = 20 * mm
    margin_y = 20 * mm
    
    N = len(sorted_participants)
    draw_legend_on_side = N <= 30
    legend_width = 60 * mm if draw_legend_on_side else 0
    
    area_w = width - 2 * margin_x - legend_width
    area_h = height - 2 * margin_y - 15 * mm

    cell_w = area_w / cols
    cell_h = area_h / rows
    
    table_r = min(cell_w, cell_h) * 0.25
    person_r = table_r * 1.5

    for r in range(Z):
        c.setFont(font_bold, 24)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(width / 2, height - 15 * mm, f"Plan Sali - Runda {r+1}")

        for t in range(X):
            col = t % cols
            row = rows - 1 - (t // cols)
            
            cx = margin_x + col * cell_w + cell_w / 2
            cy = margin_y + row * cell_h + cell_h / 2
            
            c.setLineWidth(1)
            c.setStrokeColorRGB(0.5, 0.5, 0.5)
            c.setFillColorRGB(0.95, 0.95, 0.95)
            c.circle(cx, cy, table_r, stroke=1, fill=1)
            
            c.setFillColorRGB(0, 0, 0)
            c.setFont(font_bold, 12)
            c.drawCentredString(cx, cy - 4, f"STÓŁ {t+1}")
            
            participants = [p for p in schedule[r][t] if p[2] != "Brak"]
            K = len(participants)
            M = 1 + K
            
            if M > 0:
                alpha = (2 * math.pi) / M
                mod_angle = math.pi / 2
                
                mx = cx + person_r * math.cos(mod_angle)
                my = cy + person_r * math.sin(mod_angle)
                
                c.setFillColorRGB(1, 0.84, 0)
                c.setStrokeColorRGB(0.6, 0.5, 0)
                c.circle(mx, my, 14, stroke=1, fill=1)
                c.setFillColorRGB(0, 0, 0)
                c.setFont(font_bold, 10)
                c.drawCentredString(mx, my - 3, "M")
                
                for i, p in enumerate(participants):
                    p_angle = mod_angle - (i + 1) * alpha
                    px = cx + person_r * math.cos(p_angle)
                    py = cy + person_r * math.sin(p_angle)
                    
                    c.setFillColorRGB(0.9, 0.9, 0.9)
                    c.setStrokeColorRGB(0, 0, 0)
                    c.circle(px, py, 12, stroke=1, fill=1)
                    
                    p_id = participant_ids[tuple(p)]
                    c.setFillColorRGB(0, 0, 0)
                    c.setFont(font_bold, 8)
                    c.drawCentredString(px, py - 3, p_id)

        if draw_legend_on_side:
            legend_x = width - margin_x - legend_width + 10 * mm
            legend_y = height - 30 * mm
            
            c.setFont(font_bold, 12)
            c.drawString(legend_x, legend_y, "LEGENDA:")
            legend_y -= 20
            
            c.setFont(font_regular, 9)
            for p in sorted_participants:
                p_id = participant_ids[tuple(p)]
                comp = p[2] if len(p[2]) <= 20 else p[2][:17] + "..."
                text = f"{p_id}: {p[0]} {p[1]} ({comp})"
                c.drawString(legend_x, legend_y, text)
                legend_y -= 14
        
        c.showPage()
        
        # --- ZMODYFIKOWANA LOGIKA GENEROWANIA LIST UCZESTNIKÓW ---
        if not draw_legend_on_side:
            list_cols = min(X, 3) # Wymuszenie max 3 kolumn
            list_col_w = (width - 2 * margin_x) / list_cols
            max_text_w = list_col_w - 5 * mm # Max szerokość tekstu z zapasem 5mm na odstęp
            
            # Parametry układu dla paginacji
            table_block_h = 15 * mm + Y * 4 * mm # Szacowana wysokość jednego stolika (tytuł + moderator + uczestnicy)
            available_h = height - 35 * mm - margin_y # Przestrzeń pomiędzy głównym nagłówkiem strony a marginesem dolnym
            max_rows_per_page = max(1, int(available_h / table_block_h))
            tables_per_page = max_rows_per_page * list_cols
            
            tables_drawn = 0
            
            while tables_drawn < X:
                c.setFont(font_bold, 24)
                title_text = f"Listy Uczestników - Runda {r+1}"
                if tables_drawn > 0:
                    title_text += " (cd.)"
                c.drawCentredString(width / 2, height - 15 * mm, title_text)
                
                tables_to_draw = min(tables_per_page, X - tables_drawn)
                
                for i in range(tables_to_draw):
                    t = tables_drawn + i
                    l_c = i % list_cols
                    l_r = i // list_cols
                    
                    lx = margin_x + l_c * list_col_w
                    ly = height - 35 * mm - l_r * table_block_h
                    
                    # Rysuj Tytuł Stołu
                    c.setFont(font_bold, 12)
                    c.drawString(lx, ly, f"STÓŁ {t+1}")
                    ly -= 15
                    
                    # Rysuj Moderatora
                    mod = moderators[t]
                    c.setFont(font_bold, 10)
                    mod_text = f"M: {mod[0]} {mod[1]}"
                    # Zabezpieczenie szerokości dla moderatora (bardzo rzadkie, ale warto ująć)
                    while c.stringWidth(mod_text + "...", font_bold, 10) > max_text_w and len(mod_text) > 5:
                        mod_text = mod_text[:-1]
                    if len(mod_text) < len(f"M: {mod[0]} {mod[1]}"):
                        mod_text += "..."
                    c.drawString(lx, ly, mod_text)
                    ly -= 12
                    
                    # Rysuj Uczestników z dynamicznym obcinaniem tekstu
                    c.setFont(font_regular, 10)
                    table_parts = [p for p in schedule[r][t] if p[2] != "Brak"]
                    for p in table_parts:
                        p_id = participant_ids[tuple(p)]
                        base_text = f"{p_id}: {p[0]} {p[1]}"
                        comp = p[2]
                        
                        full_text = f"{base_text} ({comp})"
                        
                        # Sprawdzenie za pomocą reportlab czy tekst nie wychodzi za krawędź kolumny
                        if c.stringWidth(full_text, font_regular, 10) > max_text_w:
                            # Próbujemy najpierw skrócić nazwę firmy literka po literce
                            while len(comp) > 0 and c.stringWidth(f"{base_text} ({comp}...)", font_regular, 10) > max_text_w:
                                comp = comp[:-1]
                                
                            if len(comp) > 0:
                                final_text = f"{base_text} ({comp}...)"
                            else:
                                # Jeśli samo Imię i Nazwisko jest niespotykanie długie, je również obcinamy
                                current_text = base_text
                                while len(current_text) > 0 and c.stringWidth(current_text + "...", font_regular, 10) > max_text_w:
                                    current_text = current_text[:-1]
                                final_text = current_text + "..."
                        else:
                            final_text = full_text
                            
                        c.drawString(lx, ly, final_text)
                        ly -= 12
                
                tables_drawn += tables_to_draw
                c.showPage() # Dodaje nową stronę (lub zamyka obecną)

    c.save()
    buffer.seek(0)
    return buffer

def generate_badges_pdf_buffer(schedule, participants_data, Z):
    fonts_ready = setup_fonts()
    font_regular = "CustomFont" if fonts_ready else "Helvetica"
    font_bold = "CustomFont-Bold" if fonts_ready else "Helvetica-Bold"
    font_oblique = "CustomFont" if fonts_ready else "Helvetica-Oblique"

    history = defaultdict(list)
    for r in range(Z):
        for t in range(len(schedule[r])):
            for p in schedule[r][t]:
                if p[2] != "Brak":
                    history[tuple(p)].append(t + 1)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    badge_w = 90 * mm
    badge_h = 55 * mm
    margin_x = 15 * mm
    margin_y = 15 * mm
    
    cols = int((width - 2 * margin_x) // badge_w)
    rows = int((height - 2 * margin_y) // badge_h)
    
    spacing_x = (width - 2 * margin_x - cols * badge_w) / (cols - 1) if cols > 1 else 0
    spacing_y = (height - 2 * margin_y - rows * badge_h) / (rows - 1) if rows > 1 else 0

    col_idx = 0
    row_idx = 0

    sorted_participants = sorted([p for p in participants_data if p[2] != "Brak"], key=lambda x: x[1])

    for p in sorted_participants:
        p_tuple = tuple(p)
        if p_tuple not in history:
            continue
            
        x = margin_x + col_idx * (badge_w + spacing_x)
        y = height - margin_y - (row_idx + 1) * badge_h - row_idx * spacing_y
        
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.rect(x, y, badge_w, badge_h)
        
        c.setFillColorRGB(0, 0, 0)
        name_text = f"{p[0]} {p[1]}"
        
        if len(name_text) > 22:
            c.setFont(font_bold, 12)
        elif len(name_text) > 16:
            c.setFont(font_bold, 14)
        else:
            c.setFont(font_bold, 16)
            
        c.drawCentredString(x + badge_w/2, y + badge_h - 15*mm, name_text)
        
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.setFont(font_oblique, 11)
        
        company_name = p[2]
        if len(company_name) > 35:
            company_name = company_name[:32] + "..."
            
        c.drawCentredString(x + badge_w/2, y + badge_h - 22*mm, company_name)
        
        c.setLineWidth(1)
        c.setStrokeColorRGB(0, 0, 0)
        c.line(x + 10*mm, y + badge_h - 28*mm, x + badge_w - 10*mm, y + badge_h - 28*mm)
        
        c.setFont(font_bold, 10)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x + badge_w/2, y + badge_h - 35*mm, "TWÓJ HARMONOGRAM:")
        
        c.setFont(font_regular, 10)
        
        history_list = history[p_tuple]
        rounds_per_row = 4
        start_y = y + badge_h - 42*mm
        line_height = 5 * mm
        
        for i in range(0, len(history_list), rounds_per_row):
            chunk = history_list[i:i+rounds_per_row]
            schedule_text = " | ".join([f"R{i+j+1}: Stół {table}" for j, table in enumerate(chunk)])
            current_y = start_y - (i // rounds_per_row) * line_height
            c.drawCentredString(x + badge_w/2, current_y, schedule_text)
        
        col_idx += 1
        if col_idx >= cols:
            col_idx = 0
            row_idx += 1
            
        if row_idx >= rows:
            c.showPage()
            col_idx = 0
            row_idx = 0

    c.save()
    buffer.seek(0)
    return buffer

def generate_export_dataframe(schedule, moderators_data):
    export_data = []
    for r_idx, round_tables in enumerate(schedule):
        for t_idx, table_participants in enumerate(round_tables):
            mod = moderators_data[t_idx]
            export_data.append({
                "Runda": r_idx + 1,
                "Stolik": t_idx + 1,
                "Rola": "Moderator",
                "Imię": mod[0],
                "Nazwisko": mod[1],
                "Firma": "N/A"
            })
            for p in table_participants:
                if p[2] != "Brak":
                    export_data.append({
                        "Runda": r_idx + 1,
                        "Stolik": t_idx + 1,
                        "Rola": "Uczestnik",
                        "Imię": p[0],
                        "Nazwisko": p[1],
                        "Firma": p[2]
                    })
    return pd.DataFrame(export_data)

# ==========================================
# INTERFEJS UŻYTKOWNIKA (STREAMLIT)
# ==========================================

# 1. Definicja okna popup (Dialog)
@st.dialog("ℹ️ Informacje o aplikacji", width="large")
def show_app_info():
    st.markdown("""
## Witaj w Generatorze Harmonogramu Networkingowego! 🤝

*(Aby wyjść z tego okna, kliknij "X" w prawym górnym rogu lub kliknij gdziekolwiek poza oknem.)*

Ten generator pomoże Ci optymalnie rozplanować usadzenie uczestników podczas wydarzenia networkingowego.

W sekcji danych wejściowych załaduj plik Excel z dwiema zakładkami:

1. Zakładka **„Uczestnicy”** w układzie kolumn: `Imię`, `Nazwisko`, `Firma`, `Branża`
2. Zakładka **„Moderatorzy”** w układzie kolumn: `Imię`, `Nazwisko` - PODANA W PLIKU LICZBA MODERATORÓW BĘDZIE RÓWNOZNACZNA Z ILOŚCIĄ STOLIKÓW

**Liczba Moderatorów jest równoznaczna z ilością stolików.**

Następnie podaj liczbę miejsc przy stoliku oraz planowaną liczbę rund.

Liczbę miejsc przy stoliku należy rozumieć jako całkowitą liczbę miejsc (w tym miejsce dla Moderatora).

Aplikacja podpowie Ci optymalną liczbę rund na podstawie ilości uczestników oraz ilości dostępnych miejsc przy stoliku.

Rozplanowując usadzenie uczestników generator kieruje się następującymi priorytetami:

- unikać sytuacji usadzenia osób z tej samej firmy przy jednym stoliku (najwyższy priorytet)
- unikać sytuacji usadzenia osób z tej samej branży przy jednym stoliku
- zmaksymalizować ilość poznanych osób dla każdego uczestnika (unikalne spotkania) i ograniczyć powtórzone spotkania

W sytuacji gdy liczba uczestników z pliku przekroczy dostępną liczbę miejsc przy stolikach N, Generator rozplanuje usadzenie pierwszych N osób z listy oraz dodatkowo wyświetli listę osób, które nie zostały uwzględnione w wydarzeniu.

Po podaniu wszystkich parametrów kliknij przycisk **„Generuj Plan Usadzenia”**.

Aplikacja wygeneruje plan usadzenia uczestników dla wszystkich rund, poda statystyki:

- **Liczba stolików** - podsumowanie ilości stolików w wydarzeniu (równe liczbie moderatorów)
- **Konflikty firmowe** - ilość sytuacji, w których osoby z tej samej firmy spotykają się przy jednym stoliku
- **Konflikty branżowe** - ilość sytuacji, w których osoby z różnych firm, ale z tej samej branży spotykają się przy jednym stoliku
- **Procent unikalnych spotkań** - udział spotkań z nowymi osobami pośród wszystkich spotkań

Dla wygenerowanego harmonogramu, na samym dole strony możesz pobrać:

- Harmonogram wydarzenia (Excel)
- Plakietki dla każdego uczestnika wskazujące indywidualny harmonogram (PDF)
- Plany graficzne usadzenia uczestników przy stołach dla każdej rundy (PDF)

## Bezpieczeństwo danych

Aplikacja działa w środowisku Streamlit, w którym każdy użytkownik ma swoją własną, odizolowaną sesję.

- Dane wgrane przez Użytkownika A (plik Excel) trafiają do pamięci RAM instancji aplikacji przypisanej tylko do jego sesji. Użytkownik B, łącząc się z tym samym adresem URL, nie ma technicznej możliwości podejrzenia zawartości sesji Użytkownika A.
- **Brak bazy danych:** Aplikacja nie zapisuje danych na dysku ani w bazie, ryzyko ich przejęcia w wyniku ataku na składowisko danych praktycznie nie istnieje. Dane znikają w momencie zamknięcia karty lub odświeżenia strony.
    """)

# 2. Logika wyświetlania na starcie (Session State zapamiętuje, czy już to pokazano)
if "info_shown" not in st.session_state:
    st.session_state.info_shown = False

if not st.session_state.info_shown:
    show_app_info()
    st.session_state.info_shown = True

# 3. Główny Tytuł
st.title("🤝 Generator Harmonogramu Networkingowego")

# 4. Przycisk wywołujący popup ręcznie (umieszczony tuż pod głównym tytułem)
if st.button("ℹ️ Informacje o aplikacji"):
    show_app_info()


# --- WGRYWANIE PLIKU (GŁÓWNA STRONA) ---
with st.container(border=True):
    st.header("📁 Dane wejściowe")
    
    st.info("""
    **Wymagany format pliku Excel:**
    Plik musi zawierać dwa arkusze:
    1. **Uczestnicy**: Kolumny `Imię`, `Nazwisko`, `Firma`, `Branża`
    2. **Moderatorzy**: Kolumny `Imię`, `Nazwisko` - PODANA W PLIKU LICZBA MODERATORÓW BĘDZIE RÓWNOZNACZNA Z ILOŚCIĄ STOLIKÓW
    """)
    
    uploaded_file = st.file_uploader("Wgraj plik z danymi (Excel)", type=["xlsx"], on_change=reset_plan)

# --- GŁÓWNA LOGIKA ---
if uploaded_file is not None:
    try:
        df_participants = pd.read_excel(uploaded_file, sheet_name='Uczestnicy')
        df_moderators = pd.read_excel(uploaded_file, sheet_name='Moderatorzy')
        
        required_cols = {'Imię', 'Nazwisko', 'Firma', 'Branża'}
        if not required_cols.issubset(df_participants.columns):
            missing = required_cols - set(df_participants.columns)
            st.error(f"Błąd: W arkuszu 'Uczestnicy' brakuje wymaganych kolumn: {', '.join(missing)}")
            st.stop()
            
        df_participants = df_participants.dropna(subset=['Imię', 'Nazwisko', 'Firma'])
        df_moderators = df_moderators.dropna(subset=['Imię'])
        
        participants = [
            [
                str(row['Imię']).strip(),
                str(row['Nazwisko']).strip(),
                str(row['Firma']).strip(),
                str(row['Branża']).strip() if pd.notna(row['Branża']) and str(row['Branża']).strip() != "" else "Brak"
            ]
            for _, row in df_participants.iterrows()
        ]
        moderators = [[str(row['Imię']).strip(), str(row['Nazwisko']).strip() if pd.notna(row['Nazwisko']) else ""] for _, row in df_moderators.iterrows()]
        
        X = len(moderators)
        
        if X == 0:
            st.error("Błąd: Brak moderatorów w pliku Excel. Liczba stolików (X) wynosi 0.")
            st.stop()
            
        st.success(f"✅ Wczytano {len(participants)} uczestników i {X} moderatorów.")
        
    except Exception as e:
        st.error(f"Błąd podczas wczytywania pliku: {e}")
        st.stop()

    # --- KONTENER KONFIGURACYJNY (DASHBOARD) ---
    with st.container(border=True):
        st.subheader("⚙️ Konfiguracja Wydarzenia")
        
        col_y, col_z, col_empty = st.columns([1, 1, 2])
        
        with col_y:
            Y = st.number_input("Miejsca przy stoliku", min_value=3, value=4, help="Wliczając 1 moderatora", on_change=reset_plan)
            
        unique_companies = set([p[2] for p in participants if p[2] != "Brak"])
        F = len(unique_companies)
        N = len(participants)
        
        Z_min = math.ceil((F - 1) / (Y - 2)) if Y > 2 else float('inf')
        
        st.markdown(f"""
            <div class="recommendation-box">
                <span class="recommendation-title">💡 Rekomendowana liczba rund: {Z_min}</span>
                <p style="margin:0;">
                    Na podstawie listy <b>{N}</b> uczestników z <b>{F}</b> różnych firm, aby każdy miał szansę poznać przedstawiciela każdej firmy, teoretyczna minimalna liczba rund wynosi <b>{Z_min}</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

        with col_z:
            Z = st.number_input("Docelowa liczba rund", min_value=1, value=Z_min, on_change=reset_plan)
        
        if Z < Z_min:
            max_met = Z * (Y - 2)
            percentage = min(100, int((max_met / (F - 1)) * 100)) if F > 1 else 100
            st.warning(f"⚠️ **Uwaga:** Przy {Z} rundach uczestnicy poznają średnio **{percentage}%** dostępnych firm. Rozważ zwiększenie liczby rund dla lepszego efektu networkingowego.")

    # --- OBSŁUGA LIMITU MIEJSC (HARD LIMIT) ---
    M = X * (Y - 1)
    L = len(participants)
    
    if L > M:
        required_tables = math.ceil(L / (Y - 1))
        st.error(f"**UWAGA: Przekroczono limit miejsc przy stolikach!**\n\nSystem rozmieści tylko pierwszych {M} uczestników z listy. Aby uwzględnić wszystkich, musisz ograniczyć listę uczestników do {M} osób lub zwiększyć liczbę stołów (moderatorów) do co najmniej {required_tables} lub zwiększyć ilość miejsc przy stołach.")
        
        with st.expander(f"Uczestnicy nieuwzględnieni (Liczba: {L - M})"):
            excluded_df = pd.DataFrame([p[:3] for p in participants[M:]], columns=["Imię", "Nazwisko", "Firma"])
            # Zmiana indeksowania, aby zaczynało się od 1 zamiast od 0
            excluded_df.index = excluded_df.index + 1
            st.dataframe(excluded_df, use_container_width=True)
            
        participants = participants[:M]

    # --- PRZYCISK AKCJI I ZAPIS DO SESSION STATE ---
    if st.button("🚀 Generuj Plan Usadzenia", type="primary", use_container_width=True):
        with st.spinner("Trwa optymalizacja harmonogramu..."):
            schedule, company_conflicts, industry_conflicts, unique_pct = generate_networking_schedule(participants, moderators, X, Y, Z)
            
            st.session_state['schedule'] = schedule
            st.session_state['conflicts'] = company_conflicts
            st.session_state['industry_conflicts'] = industry_conflicts
            st.session_state['unique_pct'] = unique_pct
            st.session_state['plan_ready'] = True

    # --- WYŚWIETLANIE WYNIKÓW (Jeśli plan został wygenerowany) ---
    if st.session_state.get('plan_ready', False):
        
        schedule = st.session_state['schedule']
        conflicts = st.session_state['conflicts']
        industry_conflicts = st.session_state.get('industry_conflicts', 0)
        unique_pct = st.session_state['unique_pct']
        
        st.success("✅ Harmonogram wygenerowany pomyślnie!")
        
        # --- METRYKI ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Liczba Stolików", X)
        col2.metric("Konflikty firmowe", conflicts, delta_color="inverse")
        col3.metric("Konflikty branżowe", industry_conflicts, delta_color="inverse")
        col4.metric("Procent unikalnych spotkań", f"{unique_pct:.2f}%")

        # --- WIZUALIZACJA I TABELE ---
        st.header("📊 Wizualizacja i Listy")
        
        figs = visualize_schedule_plotly(schedule, moderators, participants, X, Y, Z)
        
        tabs = st.tabs([f"Runda {r+1}" for r in range(Z)])
        
        participant_ids = {}
        sorted_participants = sorted([p for p in participants if p[2] != "Brak"], key=lambda x: x[1])
        for i, p in enumerate(sorted_participants):
            participant_ids[tuple(p)] = f"P{i+1}"
            
        for r, tab in enumerate(tabs):
            with tab:
                st.plotly_chart(figs[r], use_container_width=True)
                
                st.subheader("Listy uczestników przy stolikach")
                
                cols_per_row = 3
                for i in range(0, X, cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j in range(cols_per_row):
                        if i + j < X:
                            t_idx = i + j
                            with cols[j]:
                                mod = moderators[t_idx]
                                table_data = [{"ID": "M", "Imię i Nazwisko": f"{mod[0]} {mod[1]}", "Firma": "Moderator"}]
                                
                                for p in schedule[r][t_idx]:
                                    if p[2] != "Brak":
                                        p_id = participant_ids[tuple(p)]
                                        table_data.append({"ID": p_id, "Imię i Nazwisko": f"{p[0]} {p[1]}", "Firma": p[2]})
                                        
                                df_table = pd.DataFrame(table_data)
                                # Zmiana indeksowania tabel per stolik, aby zaczynało się od 1
                                df_table.index = df_table.index + 1
                                st.markdown(f"**Stolik {t_idx + 1}**")
                                st.dataframe(df_table, use_container_width=True)

        # --- EKSPORT ---
        st.header("💾 Eksport Danych")
        
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        df_export = generate_export_dataframe(schedule, moderators)
        buffer_excel = io.BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Harmonogram')
        
        col_dl1.download_button(
            label="📥 Pobierz Harmonogram (Excel)",
            data=buffer_excel.getvalue(),
            file_name="harmonogram_networking.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        pdf_badges_buffer = generate_badges_pdf_buffer(schedule, participants, Z)
        col_dl2.download_button(
            label="🪪 Pobierz Plakietki (PDF)",
            data=pdf_badges_buffer,
            file_name="plakietki_uczestnikow.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        pdf_plan_buffer = generate_visual_plan_pdf_buffer(schedule, moderators, participants, X, Y, Z)
        col_dl3.download_button(
            label="🗺️ Pobierz Plan Sali (PDF)",
            data=pdf_plan_buffer,
            file_name="plan_sali_wizualizacja.pdf",
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.info("☝️ Aby rozpocząć, wgraj plik Excel z danymi powyżej.")
Czy chcesz, żebym wygenerował też dla Ciebie przykładowy plik Excel (.xlsx) z arkuszami Uczestnicy (wraz z listą rozwijaną dla kolumny Branża) i Moderatorzy, abyś mógł od razu przetestować nową wersję aplikacji?

 czy aplikacja z tym nowym kodem używa jakichś nowych, dodatkowych bibliotek w stosunku do poprzedniego kodu? Pytam, żeby wiedzieć, czy muszę zaktualizować plik `requirements.txt` na GitHubie. 

Nie musisz aktualizować pliku requirements.txt na GitHubie. Nowy kod (Apka_v2.0.py) korzysta z dokładnie tego samego zestawu bibliotek, co poprzednia wersja (Apka_v1.9.py).   
Apka_v1.9.py
+ 1

Sekcja importów pozostała w 100% identyczna:   
Apka_v1.9.py
+ 1

Biblioteki zewnętrzne (obecne już w Twoim requirements.txt): streamlit, pandas, plotly, reportlab oraz openpyxl (jako silnik do odczytu/zapisu plików .xlsx w pandas).   
Apka_v1.9.py
+ 1

Moduły wbudowane w standardowego Pythona: random, math, copy, os, collections, io.   
Apka_v1.9.py
+ 1

Wystarczy, że podmienisz sam plik z kodem aplikacji w repozytorium.

Chciałbym wprowadzić jeszcze jedną zmianę w aplikacji. Obecnie aplikacja zakłada na sztywno, że przy każdym stole siedzi moderator, czyli ilość moderatorów w pliku wejściowym jest równa liczbie stołów podczas wydarzenia networkingowego. Chciałbym żeby aplikacja była bardziej uniwersalna i umożliwiała również planowanie wydarzenia gdzie przy stołach nie ma moderatorów. Zanim zaczniemy tworzyć nowy kod, ustalmy jaką metodą najlepiej będzie zrealizować to zadanie. Opisz jak rozumiesz problem i zaproponuj możliwe, najsensowniejsze rozwiązania (maksymalnie 2-3)

Usunięcie sztywnego założenia o obecności moderatorów wymaga zmian w pięciu powiązanych ze sobą miejscach architektury aplikacji, ponieważ obecnie lista moderatorów nie tylko wyświetla się na ekranie, ale steruje też matematyką całego wydarzenia:   
Apka_v1.9.py
+ 1

Źródło liczby stolików (
X): Obecnie liczba stolików wynika wyłącznie z liczby wierszy w zakładce Moderatorzy (X = len(moderators)). W wydarzeniu bez moderatorów aplikacja musi pozyskać parametr 
X w inny sposób – z pola wpisywanego przez użytkownika w interfejsie (z automatyczną podpowiedzią na podstawie liczby uczestników).   
Apka_v1.9.py
+ 1

Pojemność stolika i całej sali: Dotychczas przy stoliku o liczbie miejsc 
Y moderator zajmował 1 krzesło na stałe, więc dla uczestników zostawało 
Y−1 miejsc, a pojemność sali wynosiła 
X×(Y−1). Bez moderatorów wszystkie 
Y miejsc przy stole jest dostępnych dla uczestników, więc pojemność sali przy tych samych parametrach rośnie do 
X×Y.   
Apka_v1.9.py
+ 1

Matematyka rekomendacji rund (
Z 
min
​
 ) i unikalnych spotkań:

Z moderatorem każdy uczestnik ma przy stole 
Y−2 innych uczestników. Bez moderatora ma przy stole 
Y−1 innych uczestników, co zmienia wzór na minimalną rekomendowaną liczbę rund z 
⌈(F−1)/(Y−2)⌉ na 
⌈(F−1)/(Y−1)⌉.   
Apka_v1.9.py
+ 3

Przy obliczaniu metryki „Procent unikalnych spotkań” w trybie bez moderatorów przestajemy doliczać spotkania z moderatorem (Mod_X) zarówno w liczniku, jak i w mianowniku oczekiwanych spotkań.   
Apka_v1.9.py
+ 1

Funkcja kosztu – kara +50 pkt za ten sam stolik: W obecnym kodzie algorytm nakłada 50 pkt kary, gdy uczestnik trafi ponownie do tego samego stolika (mod_meetings[(p1_tuple, table_idx)] > 1), aby nie rozmawiał dwa razy z tym samym moderatorem. W trybie bez moderatorów pojawia się ciekawe pytanie projektowe: czy wyłączamy tę karę, czy ją zostawiamy, aby wymusić rotację fizycznych miejsc na sali (żeby uczestnik nie siedział przez kilka rund przy tym samym fizycznym stole)?   
Apka_v1.9.py
+ 1

Wizualizacja i eksporty (Plotly, PDF, Excel): W trybie bez moderatorów z rzutów sali znika złota gwiazda/kółko M (uczestnicy są rozkładani symetrycznie na całym obwodzie stołu), a z tabel na ekranie, list PDF i eksportu do Excela znika wiersz przypisany moderatorowi.   
Apka_v1.9.py
+ 1

Propozycje rozwiązań (jak obsłużyć oba tryby w aplikacji)
Poniżej znajdują się 3 najsensowniejsze podejścia do wdrożenia tej uniwersalności:

Wariant 1: Automatyczna detekcja na podstawie pliku Excel (Bez zmian w UI dla dotychczasowych plików)
Jak działa: Zakładka Moderatorzy w pliku Excel staje się opcjonalna (może być pusta lub może jej w ogóle nie być w pliku).

Jeśli aplikacja wykryje w pliku listę moderatorów 
→ uruchamia dotychczasowy tryb z moderatorami, a liczba stolików 
X jest równa liczbie moderatorów.   
Apka_v1.9.py
+ 1

Jeśli zakładka Moderatorzy jest pusta lub nie istnieje 
→ aplikacja automatycznie przełącza się w tryb bez moderatorów. W sekcji „Konfiguracja Wydarzenia” pojawia się wtedy dodatkowe pole Liczba stolików, z domyślną wartością wyliczoną tak, aby pomieścić wszystkich wczytanych uczestników (
⌈N/Y⌉).   
Apka_v1.9.py
+ 1

Zalety: Maksymalna prostota – użytkownik nie musi nic przełączać, sam plik determinuje logikę.

Wady: Jeśli organizator ma gotowy plik z wpisanymi moderatorami, ale w ostatniej chwili chce sprawdzić wariant bez moderatorów, musi edytować plik Excel i wgrać go ponownie.

Wariant 2: Przełącznik w interfejsie z inteligentnym stanem domyślnym (Rekomendowany)
Jak działa: Łączy zalety Wariantu 1 z pełną kontrolą w UI. Zakładka Moderatorzy w Excelu również staje się opcjonalna. Po wgraniu pliku w sekcji „Konfiguracja Wydarzenia” wyświetlamy przełącznik (np. st.toggle("Uwzględnij moderatorów przy stolikach")):   
Apka_v1.9.py
+ 1

Jeśli w pliku są moderatorzy, przełącznik jest domyślnie włączony, a liczba stolików jest zablokowana na liczbie moderatorów.   
Apka_v1.9.py
+ 1

Jeśli w pliku nie ma moderatorów, przełącznik jest automatycznie wyłączony (i zablokowany z komunikatem o braku moderatorów w pliku).

Kluczowa przewaga: Nawet gdy w pliku są moderatorzy, organizator może jednym kliknięciem wyłączyć przełącznik w aplikacji – system zignoruje wtedy moderatorów, odblokuje pole ręcznego wpisania Liczby stolików (
X) i przeliczy całe wydarzenie w trybie bez moderatorów.

Zalety: Pełna elastyczność (możliwość symulacji obu wariantów na tym samym pliku wejściowym) przy zachowaniu automatyzacji.

Wariant 3: Tryb mieszany (częściowa moderacja)
Jak działa: Zamiast podejścia „wszystkie stoły mają moderatora albo żaden”, pole Liczba stolików (
X) jest zawsze edytowalne. Jeśli w pliku jest np. 4 moderatorów, a organizator ustawi 10 stolików, to stoliki 1–4 mają moderatorów (i 
Y−1 miejsc dla uczestników), a stoliki 5–10 są niemoderowane (i mają 
Y miejsc dla uczestników).   
Apka_v1.9.py
+ 1

Zalety: Obsłuży nietypowe wydarzenia hybrydowe.

Wady: Wprowadza asymetrię między stołami (różna liczba uczestników przy stole, inne szanse na unikalne spotkania w zależności od stołu) i niepotrzebnie komplikuje konfigurację, jeśli w praktyce Twoje wydarzenia są zawsze albo w 100% moderowane, albo w 100% bez moderatorów.

Co musimy ustalić przed wygenerowaniem kodu:
Który wariant wybierasz? (Wariant 1, 2 czy 3?)

Co robimy z karą +50 pkt za powtórzenie tego samego numeru stolika w trybie bez moderatorów? Zostawiamy ją (żeby uczestnicy fizycznie zmieniali stoliki na sali z rundy na rundę), czy zerujemy (uznając, że bez moderatora numer stolika nie ma znaczenia, liczą się tylko ludzie, z którymi się siedzi)?   
Apka_v1.9.py
+ 1

Wybieram opcję 2. Usuńmy karę za powtórzenie tego samego numeru stolika w wersji bez moderatorów.

Twój zaktualizowany plik z kodem w języku Python jest gotowy do pobrania:

PY icon
Apka_v2.1
 PY 
Poniżej znajduje się podsumowanie wprowadzonych zmian (Apka_v2.1.py) oraz pełna treść nowego kodu. Podobnie jak poprzednio, nie wymaga on żadnych zmian w pliku requirements.txt.

Co zmieniło się w kodzie (v2.0 
→ v2.1)
Opcjonalny arkusz Moderatorzy i automatyczna detekcja:

Aplikacja sprawdza listę arkuszy w pliku Excel (pd.ExcelFile). Jeśli arkusz Moderatorzy nie istnieje lub jest pusty, nie wyrzuca już błędu zatrzymującego program, tylko przechodzi w tryb bez moderatorów.   
Apka_v1.9.py
+ 1

Inteligentny przełącznik w sekcji „Konfiguracja Wydarzenia”:

Dodano przełącznik st.toggle("Uwzględnij moderatorów przy stolikach"):

Gdy w pliku są moderatorzy 
→ przełącznik jest domyślnie włączony, a pole Liczba stolików jest zablokowane i równe liczbie moderatorów. Możesz jednak w każdej chwili wyłączyć przełącznik jednym kliknięciem, aby zignorować moderatorów z pliku i odblokować ręczne sterowanie liczbą stolików.   
Apka_v1.9.py
+ 1

Gdy w pliku nie ma moderatorów 
→ przełącznik jest automatycznie wyłączony (i zablokowany), a pole Liczba stolików staje się aktywne i domyślnie podpowiada liczbę stołów potrzebną do pomieszczenia wszystkich wczytanych uczestników (
⌈N/Y⌉).

Przeliczanie miejsc, rekomendacji rund i unikalnych spotkań:

Pojemność stolika: W trybie z moderatorami dla uczestników dostępne są 
Y−1 miejsca (minimalna wartość suwaka to 3), a w trybie bez moderatorów – pełne 
Y miejsc (minimalna wartość to 2).   
Apka_v1.9.py
+ 1

Rekomendacja rund (
Z 
min
​
 ): Liczba poznawanych współuczestników na rundę (peers_per_round) dynamicznie zmienia się z 
Y−2 (z moderatorem) na 
Y−1 (bez moderatora).   
Apka_v1.9.py
+ 1

Procent unikalnych spotkań: W trybie bez moderatorów z licznika i mianownika wyłączono spotkania z moderatorem (Mod_X).   
Apka_v1.9.py
+ 1

Brak kary za ten sam numer stolika w trybie bez moderatorów:

W funkcji calculate_cost naliczanie 50 pkt kary za powtórzenie stolika (mod_meetings) jest teraz objęte warunkiem if use_moderators:. Bez moderatorów algorytm optymalizuje wyłącznie unikanie konfliktów firmowych (500 pkt), branżowych (200 pkt) oraz powtórzonych spotkań tych samych osób (100 pkt).   
Apka_v1.9.py
+ 2

Wizualizacja i eksporty (Plotly, PDF, Excel):

W trybie bez moderatorów na wykresach Plotly i na planie sali PDF uczestnicy są rozmieszczani równomiernie na całym obwodzie stołu (bez złotej gwiazdy/kółka M), a w tabelach stolików, na listach PDF oraz w eksportowanym pliku Excel pomijany jest wiersz moderatora.   
Apka_v1.9.py
+ 3

Pełny kod aplikacji (Apka_v2.1.py)
Python
import streamlit as st
import pandas as pd
import random
import math
import copy
import os
from collections import defaultdict
import plotly.graph_objects as go
import plotly.colors
import io

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ==========================================
# KONFIGURACJA STRONY STREAMLIT
# ==========================================
st.set_page_config(page_title="Generator Networkingu", layout="wide", page_icon="🤝")

# ==========================================
# BEZPIECZNA TYPOGRAFIA I CSS (MINIMALIZM)
# ==========================================
st.markdown("""
    <style>
        /* Import nowoczesnej czcionki */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* 1. BEZPIECZNA ZMIANA CZCIONKI DLA TEKSTÓW */
        /* Celujemy tylko w tagi tekstowe, omijając span i div, aby nie zepsuć ikon Streamlita */
        html, body, p, li, label, input, button, h1, h2, h3, .stMarkdown {
            font-family: 'Inter', sans-serif !important;
        }

        /* OCHRONA IKON (Wymuszenie oryginalnej czcionki dla strzałek i menu) */
        .material-symbols-rounded, .stIcon,[data-testid="stExpanderToggleIcon"], [data-testid="stSidebarCollapseButton"] span {
            font-family: 'Material Symbols Rounded', sans-serif !important;
        }

        /* 2. BARDZO DUŻY ROZMIAR (1.5rem) - Tylko dla nagłówków */
        h1, h2, h3, .recommendation-title {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            padding-bottom: 0.5rem;
        }

        /* 3. DUŻY ROZMIAR (1.0rem) - Dla tekstów, etykiet, inputów i przycisków */
        p, li, label, input, .stButton button {
            font-size: 1.0rem !important;
        }

        /* Pogrubienie etykiet nad polami do wpisywania */
        label {
            font-weight: 600 !important;
        }

        /* 4. BOX REKOMENDACJI (Dostosowany do jasnego/ciemnego motywu) */
        .recommendation-box {
            background-color: rgba(34, 197, 94, 0.15); 
            border-left: 0.4rem solid #22c55e;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }

/* ==========================================
           NADPISANIE ROZMIARÓW: KONFIGURACJA (st.number_input)
           ========================================== */
        
        /* Etykiety: "Liczba stolików", "Miejsca przy stoliku", "Docelowa liczba rund" */
        div[data-testid="stNumberInput"] label p,
        div[data-testid="stNumberInput"] label {
            font-size: 1.2rem !important; /* Zmień na swój docelowy rozmiar */
        }
        
        /* Cyfry wewnątrz pola do wpisywania */
        div[data-testid="stNumberInput"] input {
            font-size: 1.2rem !important; /* Zmień na swój docelowy rozmiar */
        }

       /* ==========================================
           NADPISANIE ROZMIARÓW: OPISY METRYK (st.metric)
           ========================================== */
        
        /* Obejmujemy główny kontener metryki i każdy możliwy tekst (p, label, div, span) nad wartością */
        div[data-testid="stMetric"] label p,
        div[data-testid="stMetric"] label div,
        div[data-testid="stMetric"] label span,
        div[data-testid="stMetric"] label,
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] {
            font-size: 1.5rem !important; /* <-- Tutaj ustaw swój rozmiar dla "Liczba stolików" itp. */
            
        }
        
        /* 2. Główne wartości (duże liczby, np. "10", "85.50%") */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            font-size: 2.0rem !important; /* Zmień na swój docelowy rozmiar liczby */
        }

        /* 3. Wartość delty (tekst i strzałka pod wartością np. w "Konflikty firmowe") */
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] * {
            font-size: 1.0rem !important; /* Zmień na swój docelowy rozmiar delty */
        }

/* ==========================================
           WYGLĄD KAFELKÓW METRYK (TŁO I KOLOR)
           ========================================== */
        
        /* 1. Jasnożółte tło, marginesy i zaokrąglenia dla całego kafelka metryki */
        div[data-testid="stMetric"] {
            background-color: #FEF9C3 !important; /* Jasnożółte tło */
            padding: 1rem !important;             /* Wewnętrzny odstęp, by tekst nie dotykał krawędzi */
            border-radius: 0.5rem !important;     /* Zaokrąglone rogi */
            border: 1px solid #FDE047 !important; /* Ciemniejsza, żółta ramka wokół (opcjonalnie) */
        }

        /* 2. Wymuszenie CZARNEJ czcionki dla opisu (etykiety) */
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] label p,
        div[data-testid="stMetric"] label div,
        div[data-testid="stMetric"] label span {
            color: #000000 !important;
        }

        /* 3. Wymuszenie CZARNEJ czcionki dla dużej wartości liczbowej */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            color: #000000 !important;
        }

/* ==========================================
           NADPISANIE ROZMIARU: GŁÓWNY TYTUŁ (st.title)
           ========================================== */
        
        /* Celujemy wyłącznie w tag <h1> w głównej części strony (omijając pasek boczny) */
        .block-container h1,
        div[data-testid="stMainBlockContainer"] h1 {
            font-size: 2.0rem !important; /* <-- Tutaj wpisz swój docelowy rozmiar (np. 3.0rem lub 4.0rem) */
            
            /* Opcjonalnie: możesz tu też zmienić kolor lub wyśrodkować główny tytuł */
            /* text-align: center !important; */
            /* color: #22c55e !important; */
        }

/* ==========================================
           NADPISANIE SZEROKOŚCI OKNA POPUP (DIALOG)
           ========================================== */
        
        /* Wymuszenie szerokości na 75% ekranu (75vw = 75% viewport width) */
        div[data-testid="stModal"] > div[role="dialog"],
        div[data-testid="stDialog"] {
            width: 85vw !important;
            min-width: 85vw !important;
            max-width: 95vw !important;
        }

/* ==========================================
   CAŁKOWITE UKRYCIE NAGŁÓWKA I STOPKI 
   (Możliwe, bo zrezygnowaliśmy z panelu bocznego)
   ========================================== */
   
    header {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }
    
    footer {
        visibility: hidden !important;
        display: none !important;
    }


    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNKCJE POMOCNICZE
# ==========================================

def reset_plan():
    if 'plan_ready' in st.session_state:
        st.session_state['plan_ready'] = False

@st.cache_resource
def setup_fonts():
    # Ścieżki relatywne - wskazują na folder 'fonts' w Twoim repozytorium GitHub
    font_path = "Fonts/DejaVuSans.ttf"
    font_bold_path = "Fonts/DejaVuSans-Bold.ttf"
    
    try:
        if os.path.exists(font_path) and os.path.exists(font_bold_path):
            pdfmetrics.registerFont(TTFont('CustomFont', font_path))
            pdfmetrics.registerFont(TTFont('CustomFont-Bold', font_bold_path))
            return True
        return False
    except Exception as e:
        print(f"Błąd ładowania czcionki: {e}")
        return False

def generate_networking_schedule(participants, moderators, X, Y, Z, use_moderators=True):
    seats_per_table = (Y - 1) if use_moderators else Y
    slots_needed = X * seats_per_table
    # Struktura uczestnika: [Imię, Nazwisko, Firma, Branża]
    participants_padded = participants + [["Wolne", "Miejsce", "Brak", "Brak"]] * (slots_needed - len(participants))

    def calculate_cost(schedule):
        cost = 0
        meetings = defaultdict(int)
        mod_meetings = defaultdict(int)
        company_conflicts = 0
        industry_conflicts = 0
        
        for round_idx, round_tables in enumerate(schedule):
            for table_idx, table_participants in enumerate(round_tables):
                valid_participants = [p for p in table_participants if p[2] != "Brak"]
                
                for i in range(len(valid_participants)):
                    p1 = valid_participants[i]
                    p1_tuple = tuple(p1)
                    
                    # Kara za spotkanie u tego samego moderatora (tylko w trybie z moderatorami)
                    if use_moderators:
                        mod_meetings[(p1_tuple, table_idx)] += 1
                        if mod_meetings[(p1_tuple, table_idx)] > 1:
                            cost += 50
                    
                    for j in range(i + 1, len(valid_participants)):
                        p2 = valid_participants[j]
                        p2_tuple = tuple(p2)
                        
                        # 1. Konflikt firmowy (+500 pkt)
                        if p1[2] == p2[2]:
                            company_conflicts += 1
                            cost += 500
                        # 2. Konflikt branżowy (+200 pkt) - naliczany dla różnych firm z tej samej branży
                        elif p1[3] != "Brak" and p1[3] == p2[3]:
                            industry_conflicts += 1
                            cost += 200
                        
                        # 3. Powtórzone spotkanie tej samej pary uczestników (+100 pkt)
                        pair = tuple(sorted([p1_tuple, p2_tuple]))
                        meetings[pair] += 1
                        if meetings[pair] > 1:
                            cost += 100
                            
        return cost, company_conflicts, industry_conflicts

    def generate_initial_schedule():
        schedule = []
        for _ in range(Z):
            round_participants = participants_padded[:]
            random.shuffle(round_participants)
            round_tables = [round_participants[i * seats_per_table : (i + 1) * seats_per_table] for i in range(X)]
            schedule.append(round_tables)
        return schedule

    def get_neighbor(schedule):
        new_schedule = copy.deepcopy(schedule)
        r = random.randint(0, Z - 1)
        t1, t2 = random.randint(0, X - 1), random.randint(0, X - 1)
        while t1 == t2 and X > 1:
            t2 = random.randint(0, X - 1)
        
        p1, p2 = random.randint(0, seats_per_table - 1), random.randint
An error occurred


Wybieram opcję 2. Usuńmy karę za powtórzenie tego samego numeru stolika w wersji bez moderatorów.  

Gemini is AI and can make mistakes, including about people. Your privacy & GeminiOpens in a new window

Konwertuj czat na format PDF
Konwertuj czat na format PDF
Otwórz ten czat w programie Acrobat
import streamlit as st
import pandas as pd
import random
import math
import copy
import os
from collections import defaultdict
import plotly.graph_objects as go
import plotly.colors
import io

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ==========================================
# KONFIGURACJA STRONY STREAMLIT
# ==========================================
st.set_page_config(page_title="Generator Networkingu", layout="wide", page_icon="🤝")

# ==========================================
# BEZPIECZNA TYPOGRAFIA I CSS (MINIMALIZM)
# ==========================================
st.markdown("""
    <style>
        /* Import nowoczesnej czcionki */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* 1. BEZPIECZNA ZMIANA CZCIONKI DLA TEKSTÓW */
        /* Celujemy tylko w tagi tekstowe, omijając span i div, aby nie zepsuć ikon Streamlita */
        html, body, p, li, label, input, button, h1, h2, h3, .stMarkdown {
            font-family: 'Inter', sans-serif !important;
        }

        /* OCHRONA IKON (Wymuszenie oryginalnej czcionki dla strzałek i menu) */
        .material-symbols-rounded, .stIcon,[data-testid="stExpanderToggleIcon"], [data-testid="stSidebarCollapseButton"] span {
            font-family: 'Material Symbols Rounded', sans-serif !important;
        }

        /* 2. BARDZO DUŻY ROZMIAR (1.5rem) - Tylko dla nagłówków */
        h1, h2, h3, .recommendation-title {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            padding-bottom: 0.5rem;
        }

        /* 3. DUŻY ROZMIAR (1.0rem) - Dla tekstów, etykiet, inputów i przycisków */
        p, li, label, input, .stButton button {
            font-size: 1.0rem !important;
        }

        /* Pogrubienie etykiet nad polami do wpisywania */
        label {
            font-weight: 600 !important;
        }

        /* 4. BOX REKOMENDACJI (Dostosowany do jasnego/ciemnego motywu) */
        .recommendation-box {
            background-color: rgba(34, 197, 94, 0.15); 
            border-left: 0.4rem solid #22c55e;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1.5rem 0;
        }

/* ==========================================
           NADPISANIE ROZMIARÓW: KONFIGURACJA (st.number_input)
           ========================================== */
        
        /* Etykiety: "Liczba stolików", "Miejsca przy stoliku", "Docelowa liczba rund" */
        div[data-testid="stNumberInput"] label p,
        div[data-testid="stNumberInput"] label {
            font-size: 1.2rem !important; /* Zmień na swój docelowy rozmiar */
        }
        
        /* Cyfry wewnątrz pola do wpisywania */
        div[data-testid="stNumberInput"] input {
            font-size: 1.2rem !important; /* Zmień na swój docelowy rozmiar */
        }

       /* ==========================================
           NADPISANIE ROZMIARÓW: OPISY METRYK (st.metric)
           ========================================== */
        
        /* Obejmujemy główny kontener metryki i każdy możliwy tekst (p, label, div, span) nad wartością */
        div[data-testid="stMetric"] label p,
        div[data-testid="stMetric"] label div,
        div[data-testid="stMetric"] label span,
        div[data-testid="stMetric"] label,
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] {
            font-size: 1.5rem !important; /* <-- Tutaj ustaw swój rozmiar dla "Liczba stolików" itp. */
            
        }
        
        /* 2. Główne wartości (duże liczby, np. "10", "85.50%") */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            font-size: 2.0rem !important; /* Zmień na swój docelowy rozmiar liczby */
        }

        /* 3. Wartość delty (tekst i strzałka pod wartością np. w "Konflikty firmowe") */
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] * {
            font-size: 1.0rem !important; /* Zmień na swój docelowy rozmiar delty */
        }

/* ==========================================
           WYGLĄD KAFELKÓW METRYK (TŁO I KOLOR)
           ========================================== */
        
        /* 1. Jasnożółte tło, marginesy i zaokrąglenia dla całego kafelka metryki */
        div[data-testid="stMetric"] {
            background-color: #FEF9C3 !important; /* Jasnożółte tło */
            padding: 1rem !important;             /* Wewnętrzny odstęp, by tekst nie dotykał krawędzi */
            border-radius: 0.5rem !important;     /* Zaokrąglone rogi */
            border: 1px solid #FDE047 !important; /* Ciemniejsza, żółta ramka wokół (opcjonalnie) */
        }

        /* 2. Wymuszenie CZARNEJ czcionki dla opisu (etykiety) */
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] label p,
        div[data-testid="stMetric"] label div,
        div[data-testid="stMetric"] label span {
            color: #000000 !important;
        }

        /* 3. Wymuszenie CZARNEJ czcionki dla dużej wartości liczbowej */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            color: #000000 !important;
        }

/* ==========================================
           NADPISANIE ROZMIARU: GŁÓWNY TYTUŁ (st.title)
           ========================================== */
        
        /* Celujemy wyłącznie w tag <h1> w głównej części strony (omijając pasek boczny) */
        .block-container h1,
        div[data-testid="stMainBlockContainer"] h1 {
            font-size: 2.0rem !important; /* <-- Tutaj wpisz swój docelowy rozmiar (np. 3.0rem lub 4.0rem) */
            
            /* Opcjonalnie: możesz tu też zmienić kolor lub wyśrodkować główny tytuł */
            /* text-align: center !important; */
            /* color: #22c55e !important; */
        }

/* ==========================================
           NADPISANIE SZEROKOŚCI OKNA POPUP (DIALOG)
           ========================================== */
        
        /* Wymuszenie szerokości na 75% ekranu (75vw = 75% viewport width) */
        div[data-testid="stModal"] > div[role="dialog"],
        div[data-testid="stDialog"] {
            width: 85vw !important;
            min-width: 85vw !important;
            max-width: 95vw !important;
        }

/* ==========================================
   CAŁKOWITE UKRYCIE NAGŁÓWKA I STOPKI 
   (Możliwe, bo zrezygnowaliśmy z panelu bocznego)
   ========================================== */
   
    header {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
    }
    
    footer {
        visibility: hidden !important;
        display: none !important;
    }


    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNKCJE POMOCNICZE
# ==========================================

def reset_plan():
    if 'plan_ready' in st.session_state:
        st.session_state['plan_ready'] = False

@st.cache_resource
def setup_fonts():
    # Ścieżki relatywne - wskazują na folder 'fonts' w Twoim repozytorium GitHub
    font_path = "Fonts/DejaVuSans.ttf"
    font_bold_path = "Fonts/DejaVuSans-Bold.ttf"
    
    try:
        if os.path.exists(font_path) and os.path.exists(font_bold_path):
            pdfmetrics.registerFont(TTFont('CustomFont', font_path))
            pdfmetrics.registerFont(TTFont('CustomFont-Bold', font_bold_path))
            return True
        return False
    except Exception as e:
        print(f"Błąd ładowania czcionki: {e}")
        return False

def generate_networking_schedule(participants, moderators, X, Y, Z, use_moderators=True):
    seats_per_table = (Y - 1) if use_moderators else Y
    slots_needed = X * seats_per_table
    # Struktura uczestnika: [Imię, Nazwisko, Firma, Branża]
    participants_padded = participants + [["Wolne", "Miejsce", "Brak", "Brak"]] * (slots_needed - len(participants))

    def calculate_cost(schedule):
        cost = 0
        meetings = defaultdict(int)
        mod_meetings = defaultdict(int)
        company_conflicts = 0
        industry_conflicts = 0
        
        for round_idx, round_tables in enumerate(schedule):
            for table_idx, table_participants in enumerate(round_tables):
                valid_participants = [p for p in table_participants if p[2] != "Brak"]
                
                for i in range(len(valid_participants)):
                    p1 = valid_participants[i]
                    p1_tuple = tuple(p1)
                    
                    # Kara za spotkanie u tego samego moderatora (tylko w trybie z moderatorami)
                    if use_moderators:
                        mod_meetings[(p1_tuple, table_idx)] += 1
                        if mod_meetings[(p1_tuple, table_idx)] > 1:
                            cost += 50
                    
                    for j in range(i + 1, len(valid_participants)):
                        p2 = valid_participants[j]
                        p2_tuple = tuple(p2)
                        
                        # 1. Konflikt firmowy (+500 pkt)
                        if p1[2] == p2[2]:
                            company_conflicts += 1
                            cost += 500
                        # 2. Konflikt branżowy (+200 pkt) - naliczany dla różnych firm z tej samej branży
                        elif p1[3] != "Brak" and p1[3] == p2[3]:
                            industry_conflicts += 1
                            cost += 200
                        
                        # 3. Powtórzone spotkanie tej samej pary uczestników (+100 pkt)
                        pair = tuple(sorted([p1_tuple, p2_tuple]))
                        meetings[pair] += 1
                        if meetings[pair] > 1:
                            cost += 100
                            
        return cost, company_conflicts, industry_conflicts

    def generate_initial_schedule():
        schedule = []
        for _ in range(Z):
            round_participants = participants_padded[:]
            random.shuffle(round_participants)
            round_tables = [round_participants[i * seats_per_table : (i + 1) * seats_per_table] for i in range(X)]
            schedule.append(round_tables)
        return schedule

    def get_neighbor(schedule):
        new_schedule = copy.deepcopy(schedule)
        r = random.randint(0, Z - 1)
        t1, t2 = random.randint(0, X - 1), random.randint(0, X - 1)
        while t1 == t2 and X > 1:
            t2 = random.randint(0, X - 1)
        
        p1, p2 = random.randint(0, seats_per_table - 1), random.randint(0, seats_per_table - 1)
        new_schedule[r][t1][p1], new_schedule[r][t2][p2] = new_schedule[r][t2][p2], new_schedule[r][t1][p1]
        return new_schedule

    current_schedule = generate_initial_schedule()
    current_cost, _, _ = calculate_cost(current_schedule)
    best_schedule, best_cost = current_schedule, current_cost

    T = 1000.0
    cooling_rate = 0.995
    min_T = 0.1

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_iterations = math.log(min_T / T) / math.log(cooling_rate)
    current_iteration = 0

    while T > min_T:
        neighbor = get_neighbor(current_schedule)
        neighbor_cost, _, _ = calculate_cost(neighbor)
        
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / T):
            current_schedule = neighbor
            current_cost = neighbor_cost
            
            if current_cost < best_cost:
                best_schedule = current_schedule
                best_cost = current_cost
                
        T *= cooling_rate
        current_iteration += 1
        
        if current_iteration % 100 == 0:
            progress = min(1.0, current_iteration / total_iterations)
            progress_bar.progress(progress)
            status_text.text(f"Optymalizacja w toku... (Koszt: {best_cost})")

    progress_bar.empty()
    status_text.empty()

    final_cost, company_conflicts, industry_conflicts = calculate_cost(best_schedule)
    
    unique_meetings_per_participant = defaultdict(set)
    for round_idx, round_tables in enumerate(best_schedule):
        for table_idx, table_participants in enumerate(round_tables):
            for p1 in table_participants:
                if p1[2] == "Brak": continue
                p1_tuple = tuple(p1)
                if use_moderators:
                    unique_meetings_per_participant[p1_tuple].add(f"Mod_{table_idx}")
                for p2 in table_participants:
                    if p1 == p2 or p2[2] == "Brak": continue
                    unique_meetings_per_participant[p1_tuple].add(tuple(p2))

    total_unique = sum(len(v) for v in unique_meetings_per_participant.values())
    if use_moderators:
        expected_meetings = len(participants) * (Z * (Y - 2) + Z)
    else:
        expected_meetings = len(participants) * (Z * (Y - 1))
    unique_percentage = (total_unique / expected_meetings) * 100 if expected_meetings > 0 else 0

    return best_schedule, company_conflicts, industry_conflicts, unique_percentage

def visualize_schedule_plotly(schedule, moderators, participants_data, X, Y, Z, use_moderators=True):
    participant_ids = {}
    sorted_participants = sorted([p for p in participants_data if p[2] != "Brak"], key=lambda x: x[1])
    for i, p in enumerate(sorted_participants):
        participant_ids[tuple(p)] = f"P{i+1}"

    companies = set([p[2] for p in sorted_participants])
    palette = plotly.colors.qualitative.Pastel + plotly.colors.qualitative.Set3
    company_colors = {comp: palette[i % len(palette)] for i, comp in enumerate(companies)}

    figs = []
    cols = math.ceil(math.sqrt(X))
    rows = math.ceil(X / cols)
    
    table_spacing_x = 5
    table_spacing_y = 5
    
    for r in range(Z):
        fig = go.Figure()
        
        for t in range(X):
            col = t % cols
            row = rows - 1 - (t // cols)
            
            center_x = col * table_spacing_x
            center_y = row * table_spacing_y
            
            fig.add_shape(type="circle",
                x0=center_x - 1, y0=center_y - 1,
                x1=center_x + 1, y1=center_y + 1,
                line_color="gray", fillcolor="lightgray", opacity=0.3
            )
            
            # Wymuszony czarny kolor i pogrubienie dla numeru stołu
            fig.add_annotation(
                x=center_x, y=center_y, 
                text=f"<b>STÓŁ {t+1}</b>", 
                showarrow=False, 
                font=dict(size=16, color="black")
            )
            
            participants = [p for p in schedule[r][t] if p[2] != "Brak"]
            K = len(participants)
            M = (1 + K) if use_moderators else K
            
            if M > 0:
                alpha = (2 * math.pi) / M 
                radius = 1.2 
                start_angle = math.pi / 2
                
                if use_moderators:
                    mod_x = center_x + radius * math.cos(start_angle)
                    mod_y = center_y + radius * math.sin(start_angle)
                    
                    mod = moderators[t]
                    fig.add_trace(go.Scatter(
                        x=[mod_x], y=[mod_y],
                        mode='markers+text',
                        marker=dict(size=40, color='gold', symbol='star', line=dict(width=1, color='darkgoldenrod')),
                        text=["<b>M</b>"],
                        textposition="middle center",
                        hoverinfo="text",
                        hovertext=[f"<b>Moderator:</b><br>{mod[0]} {mod[1]}"],
                        showlegend=False,
                        textfont=dict(size=16, color="black")
                    ))
                
                for i, p in enumerate(participants):
                    offset = (i + 1) if use_moderators else i
                    p_angle = start_angle - offset * alpha
                    
                    px = center_x + radius * math.cos(p_angle)
                    py = center_y + radius * math.sin(p_angle)
                    
                    comp = p[2]
                    color = company_colors[comp]
                    p_id = participant_ids[tuple(p)]
                    
                    hover_text = f"<b>{p[0]} {p[1]}</b><br>Firma: {comp}"
                    
                    fig.add_trace(go.Scatter(
                        x=[px], y=[py],
                        mode='markers+text',
                        marker=dict(size=40, color=color, symbol='circle', line=dict(width=1, color='black')),
                        text=[f"<b>{p_id}</b>"],
                        textposition="middle center",
                        hoverinfo="text",
                        hovertext=[hover_text],
                        showlegend=False,
                        textfont=dict(size=16, color="black")
                    ))
        
        # Globalne wymuszenie czcionek i tła dla spójności z PDF/PNG
        fig.update_layout(
            title=dict(text=f"<b>Wizualizacja - Runda {r+1}</b>", font=dict(size=24, color="black"), x=0.5),
            xaxis=dict(visible=False, range=[-2, cols*table_spacing_x + 2]), 
            yaxis=dict(visible=False, range=[-2, rows*table_spacing_y]),
            width=max(800, cols * 300), 
            height=max(600, rows * 300),
            plot_bgcolor="white",
            paper_bgcolor="white", # Wymusza białe tło poza obszarem rysowania
            font=dict(color="black"), # Globalny fallback na czarny kolor
            margin=dict(l=40, r=40, t=80, b=40)
        )
        figs.append(fig)
        
    return figs



def generate_visual_plan_pdf_buffer(schedule, moderators, participants_data, X, Y, Z, use_moderators=True):
    fonts_ready = setup_fonts()
    font_regular = "CustomFont" if fonts_ready else "Helvetica"
    font_bold = "CustomFont-Bold" if fonts_ready else "Helvetica-Bold"

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    participant_ids = {}
    sorted_participants = sorted([p for p in participants_data if p[2] != "Brak"], key=lambda x: x[1])
    for i, p in enumerate(sorted_participants):
        participant_ids[tuple(p)] = f"P{i+1}"

    cols = math.ceil(math.sqrt(X))
    rows = math.ceil(X / cols)

    margin_x = 20 * mm
    margin_y = 20 * mm
    
    N = len(sorted_participants)
    draw_legend_on_side = N <= 30
    legend_width = 60 * mm if draw_legend_on_side else 0
    
    area_w = width - 2 * margin_x - legend_width
    area_h = height - 2 * margin_y - 15 * mm

    cell_w = area_w / cols
    cell_h = area_h / rows
    
    table_r = min(cell_w, cell_h) * 0.25
    person_r = table_r * 1.5

    for r in range(Z):
        c.setFont(font_bold, 24)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(width / 2, height - 15 * mm, f"Plan Sali - Runda {r+1}")

        for t in range(X):
            col = t % cols
            row = rows - 1 - (t // cols)
            
            cx = margin_x + col * cell_w + cell_w / 2
            cy = margin_y + row * cell_h + cell_h / 2
            
            c.setLineWidth(1)
            c.setStrokeColorRGB(0.5, 0.5, 0.5)
            c.setFillColorRGB(0.95, 0.95, 0.95)
            c.circle(cx, cy, table_r, stroke=1, fill=1)
            
            c.setFillColorRGB(0, 0, 0)
            c.setFont(font_bold, 12)
            c.drawCentredString(cx, cy - 4, f"STÓŁ {t+1}")
            
            participants = [p for p in schedule[r][t] if p[2] != "Brak"]
            K = len(participants)
            M = (1 + K) if use_moderators else K
            
            if M > 0:
                alpha = (2 * math.pi) / M
                start_angle = math.pi / 2
                
                if use_moderators:
                    mx = cx + person_r * math.cos(start_angle)
                    my = cy + person_r * math.sin(start_angle)
                    
                    c.setFillColorRGB(1, 0.84, 0)
                    c.setStrokeColorRGB(0.6, 0.5, 0)
                    c.circle(mx, my, 14, stroke=1, fill=1)
                    c.setFillColorRGB(0, 0, 0)
                    c.setFont(font_bold, 10)
                    c.drawCentredString(mx, my - 3, "M")
                
                for i, p in enumerate(participants):
                    offset = (i + 1) if use_moderators else i
                    p_angle = start_angle - offset * alpha
                    px = cx + person_r * math.cos(p_angle)
                    py = cy + person_r * math.sin(p_angle)
                    
                    c.setFillColorRGB(0.9, 0.9, 0.9)
                    c.setStrokeColorRGB(0, 0, 0)
                    c.circle(px, py, 12, stroke=1, fill=1)
                    
                    p_id = participant_ids[tuple(p)]
                    c.setFillColorRGB(0, 0, 0)
                    c.setFont(font_bold, 8)
                    c.drawCentredString(px, py - 3, p_id)

        if draw_legend_on_side:
            legend_x = width - margin_x - legend_width + 10 * mm
            legend_y = height - 30 * mm
            
            c.setFont(font_bold, 12)
            c.drawString(legend_x, legend_y, "LEGENDA:")
            legend_y -= 20
            
            c.setFont(font_regular, 9)
            for p in sorted_participants:
                p_id = participant_ids[tuple(p)]
                comp = p[2] if len(p[2]) <= 20 else p[2][:17] + "..."
                text = f"{p_id}: {p[0]} {p[1]} ({comp})"
                c.drawString(legend_x, legend_y, text)
                legend_y -= 14
        
        c.showPage()
        
        # --- ZMODYFIKOWANA LOGIKA GENEROWANIA LIST UCZESTNIKÓW ---
        if not draw_legend_on_side:
            list_cols = min(X, 3) # Wymuszenie max 3 kolumn
            list_col_w = (width - 2 * margin_x) / list_cols
            max_text_w = list_col_w - 5 * mm # Max szerokość tekstu z zapasem 5mm na odstęp
            
            # Parametry układu dla paginacji
            table_block_h = 15 * mm + Y * 4 * mm # Szacowana wysokość jednego stolika (tytuł + opcjonalny moderator + uczestnicy)
            available_h = height - 35 * mm - margin_y # Przestrzeń pomiędzy głównym nagłówkiem strony a marginesem dolnym
            max_rows_per_page = max(1, int(available_h / table_block_h))
            tables_per_page = max_rows_per_page * list_cols
            
            tables_drawn = 0
            
            while tables_drawn < X:
                c.setFont(font_bold, 24)
                title_text = f"Listy Uczestników - Runda {r+1}"
                if tables_drawn > 0:
                    title_text += " (cd.)"
                c.drawCentredString(width / 2, height - 15 * mm, title_text)
                
                tables_to_draw = min(tables_per_page, X - tables_drawn)
                
                for i in range(tables_to_draw):
                    t = tables_drawn + i
                    l_c = i % list_cols
                    l_r = i // list_cols
                    
                    lx = margin_x + l_c * list_col_w
                    ly = height - 35 * mm - l_r * table_block_h
                    
                    # Rysuj Tytuł Stołu
                    c.setFont(font_bold, 12)
                    c.drawString(lx, ly, f"STÓŁ {t+1}")
                    ly -= 15
                    
                    # Rysuj Moderatora (jeśli tryb z moderatorami)
                    if use_moderators:
                        mod = moderators[t]
                        c.setFont(font_bold, 10)
                        mod_text = f"M: {mod[0]} {mod[1]}"
                        while c.stringWidth(mod_text + "...", font_bold, 10) > max_text_w and len(mod_text) > 5:
                            mod_text = mod_text[:-1]
                        if len(mod_text) < len(f"M: {mod[0]} {mod[1]}"):
                            mod_text += "..."
                        c.drawString(lx, ly, mod_text)
                        ly -= 12
                    
                    # Rysuj Uczestników z dynamicznym obcinaniem tekstu
                    c.setFont(font_regular, 10)
                    table_parts = [p for p in schedule[r][t] if p[2] != "Brak"]
                    for p in table_parts:
                        p_id = participant_ids[tuple(p)]
                        base_text = f"{p_id}: {p[0]} {p[1]}"
                        comp = p[2]
                        
                        full_text = f"{base_text} ({comp})"
                        
                        # Sprawdzenie za pomocą reportlab czy tekst nie wychodzi za krawędź kolumny
                        if c.stringWidth(full_text, font_regular, 10) > max_text_w:
                            # Próbujemy najpierw skrócić nazwę firmy literka po literce
                            while len(comp) > 0 and c.stringWidth(f"{base_text} ({comp}...)", font_regular, 10) > max_text_w:
                                comp = comp[:-1]
                                
                            if len(comp) > 0:
                                final_text = f"{base_text} ({comp}...)"
                            else:
                                # Jeśli samo Imię i Nazwisko jest niespotykanie długie, je również obcinamy
                                current_text = base_text
                                while len(current_text) > 0 and c.stringWidth(current_text + "...", font_regular, 10) > max_text_w:
                                    current_text = current_text[:-1]
                                final_text = current_text + "..."
                        else:
                            final_text = full_text
                            
                        c.drawString(lx, ly, final_text)
                        ly -= 12
                
                tables_drawn += tables_to_draw
                c.showPage() # Dodaje nową stronę (lub zamyka obecną)

    c.save()
    buffer.seek(0)
    return buffer

def generate_badges_pdf_buffer(schedule, participants_data, Z):
    fonts_ready = setup_fonts()
    font_regular = "CustomFont" if fonts_ready else "Helvetica"
    font_bold = "CustomFont-Bold" if fonts_ready else "Helvetica-Bold"
    font_oblique = "CustomFont" if fonts_ready else "Helvetica-Oblique"

    history = defaultdict(list)
    for r in range(Z):
        for t in range(len(schedule[r])):
            for p in schedule[r][t]:
                if p[2] != "Brak":
                    history[tuple(p)].append(t + 1)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    badge_w = 90 * mm
    badge_h = 55 * mm
    margin_x = 15 * mm
    margin_y = 15 * mm
    
    cols = int((width - 2 * margin_x) // badge_w)
    rows = int((height - 2 * margin_y) // badge_h)
    
    spacing_x = (width - 2 * margin_x - cols * badge_w) / (cols - 1) if cols > 1 else 0
    spacing_y = (height - 2 * margin_y - rows * badge_h) / (rows - 1) if rows > 1 else 0

    col_idx = 0
    row_idx = 0

    sorted_participants = sorted([p for p in participants_data if p[2] != "Brak"], key=lambda x: x[1])

    for p in sorted_participants:
        p_tuple = tuple(p)
        if p_tuple not in history:
            continue
            
        x = margin_x + col_idx * (badge_w + spacing_x)
        y = height - margin_y - (row_idx + 1) * badge_h - row_idx * spacing_y
        
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.rect(x, y, badge_w, badge_h)
        
        c.setFillColorRGB(0, 0, 0)
        name_text = f"{p[0]} {p[1]}"
        
        if len(name_text) > 22:
            c.setFont(font_bold, 12)
        elif len(name_text) > 16:
            c.setFont(font_bold, 14)
        else:
            c.setFont(font_bold, 16)
            
        c.drawCentredString(x + badge_w/2, y + badge_h - 15*mm, name_text)
        
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.setFont(font_oblique, 11)
        
        company_name = p[2]
        if len(company_name) > 35:
            company_name = company_name[:32] + "..."
            
        c.drawCentredString(x + badge_w/2, y + badge_h - 22*mm, company_name)
        
        c.setLineWidth(1)
        c.setStrokeColorRGB(0, 0, 0)
        c.line(x + 10*mm, y + badge_h - 28*mm, x + badge_w - 10*mm, y + badge_h - 28*mm)
        
        c.setFont(font_bold, 10)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(x + badge_w/2, y + badge_h - 35*mm, "TWÓJ HARMONOGRAM:")
        
        c.setFont(font_regular, 10)
        
        history_list = history[p_tuple]
        rounds_per_row = 4
        start_y = y + badge_h - 42*mm
        line_height = 5 * mm
        
        for i in range(0, len(history_list), rounds_per_row):
            chunk = history_list[i:i+rounds_per_row]
            schedule_text = " | ".join([f"R{i+j+1}: Stół {table}" for j, table in enumerate(chunk)])
            current_y = start_y - (i // rounds_per_row) * line_height
            c.drawCentredString(x + badge_w/2, current_y, schedule_text)
        
        col_idx += 1
        if col_idx >= cols:
            col_idx = 0
            row_idx += 1
            
        if row_idx >= rows:
            c.showPage()
            col_idx = 0
            row_idx = 0

    c.save()
    buffer.seek(0)
    return buffer

def generate_export_dataframe(schedule, moderators_data, use_moderators=True):
    export_data = []
    for r_idx, round_tables in enumerate(schedule):
        for t_idx, table_participants in enumerate(round_tables):
            if use_moderators:
                mod = moderators_data[t_idx]
                export_data.append({
                    "Runda": r_idx + 1,
                    "Stolik": t_idx + 1,
                    "Rola": "Moderator",
                    "Imię": mod[0],
                    "Nazwisko": mod[1],
                    "Firma": "N/A"
                })
            for p in table_participants:
                if p[2] != "Brak":
                    export_data.append({
                        "Runda": r_idx + 1,
                        "Stolik": t_idx + 1,
                        "Rola": "Uczestnik",
                        "Imię": p[0],
                        "Nazwisko": p[1],
                        "Firma": p[2]
                    })
    return pd.DataFrame(export_data)

# ==========================================
# INTERFEJS UŻYTKOWNIKA (STREAMLIT)
# ==========================================

# 1. Definicja okna popup (Dialog)
@st.dialog("ℹ️ Informacje o aplikacji", width="large")
def show_app_info():
    st.markdown("""
## Witaj w Generatorze Harmonogramu Networkingowego! 🤝

*(Aby wyjść z tego okna, kliknij "X" w prawym górnym rogu lub kliknij gdziekolwiek poza oknem.)*

Ten generator pomoże Ci optymalnie rozplanować usadzenie uczestników podczas wydarzenia networkingowego – zarówno w formule **z moderatorami**, jak i **bez moderatorów**.

W sekcji danych wejściowych załaduj plik Excel:

1. Zakładka **„Uczestnicy”** (wymagana) w układzie kolumn: `Imię`, `Nazwisko`, `Firma`, `Branża`
2. Zakładka **„Moderatorzy”** (opcjonalna) w układzie kolumn: `Imię`, `Nazwisko`

**Tryby pracy (z moderatorami / bez moderatorów):**

- **Wydarzenie z moderatorami:** Jeśli w pliku znajduje się wypełniona zakładka „Moderatorzy” i przełącznik *„Uwzględnij moderatorów przy stolikach”* jest włączony, liczba stolików jest sztywno powiązana z liczbą moderatorów, a 1 miejsce przy każdym stoliku jest zarezerwowane dla moderatora.
- **Wydarzenie bez moderatorów:** Jeśli zakładka „Moderatorzy” jest pusta (lub nie ma jej w pliku) albo wyłączysz przełącznik w konfiguracji, aplikacja działa w trybie bez moderatorów. Możesz wtedy ręcznie określić liczbę stolików, a wszystkie miejsca przy stole są dostępne dla uczestników.

Aplikacja podpowie Ci optymalną liczbę rund na podstawie liczby uczestników, reprezentowanych firm oraz dostępnych miejsc przy stoliku.

Rozplanowując usadzenie uczestników generator kieruje się następującymi priorytetami:

- unikać sytuacji usadzenia osób z tej samej firmy przy jednym stoliku (najwyższy priorytet)
- unikać sytuacji usadzenia osób z tej samej branży przy jednym stoliku
- zmaksymalizować ilość poznanych osób dla każdego uczestnika (unikalne spotkania) i ograniczyć powtórzone spotkania

W sytuacji gdy liczba uczestników z pliku przekroczy dostępną liczbę miejsc przy stolikach N, Generator rozplanuje usadzenie pierwszych N osób z listy oraz dodatkowo wyświetli listę osób, które nie zostały uwzględnione w wydarzeniu.

Po podaniu wszystkich parametrów kliknij przycisk **„Generuj Plan Usadzenia”**.

Aplikacja wygeneruje plan usadzenia uczestników dla wszystkich rund, poda statystyki:

- **Liczba stolików** - podsumowanie ilości stolików w wydarzeniu
- **Konflikty firmowe** - ilość sytuacji, w których osoby z tej samej firmy spotykają się przy jednym stoliku
- **Konflikty branżowe** - ilość sytuacji, w których osoby z różnych firm, ale z tej samej branży spotykają się przy jednym stoliku
- **Procent unikalnych spotkań** - udział spotkań z nowymi osobami pośród wszystkich spotkań

Dla wygenerowanego harmonogramu, na samym dole strony możesz pobrać:

- Harmonogram wydarzenia (Excel)
- Plakietki dla każdego uczestnika wskazujące indywidualny harmonogram (PDF)
- Plany graficzne usadzenia uczestników przy stołach dla każdej rundy (PDF)

## Bezpieczeństwo danych

Aplikacja działa w środowisku Streamlit, w którym każdy użytkownik ma swoją własną, odizolowaną sesję.

- Dane wgrane przez Użytkownika A (plik Excel) trafiają do pamięci RAM instancji aplikacji przypisanej tylko do jego sesji. Użytkownik B, łącząc się z tym samym adresem URL, nie ma technicznej możliwości podejrzenia zawartości sesji Użytkownika A.
- **Brak bazy danych:** Aplikacja nie zapisuje danych na dysku ani w bazie, ryzyko ich przejęcia w wyniku ataku na składowisko danych praktycznie nie istnieje. Dane znikają w momencie zamknięcia karty lub odświeżenia strony.
    """)

# 2. Logika wyświetlania na starcie (Session State zapamiętuje, czy już to pokazano)
if "info_shown" not in st.session_state:
    st.session_state.info_shown = False

if not st.session_state.info_shown:
    show_app_info()
    st.session_state.info_shown = True

# 3. Główny Tytuł
st.title("🤝 Generator Harmonogramu Networkingowego")

# 4. Przycisk wywołujący popup ręcznie (umieszczony tuż pod głównym tytułem)
if st.button("ℹ️ Informacje o aplikacji"):
    show_app_info()


# --- WGRYWANIE PLIKU (GŁÓWNA STRONA) ---
with st.container(border=True):
    st.header("📁 Dane wejściowe")
    
    st.info("""
    **Wymagany format pliku Excel:**
    1. Arkusz **Uczestnicy** (wymagany): Kolumny `Imię`, `Nazwisko`, `Firma`, `Branża`
    2. Arkusz **Moderatorzy** (opcjonalny): Kolumny `Imię`, `Nazwisko` – w trybie z moderatorami liczba moderatorów wyznacza liczbę stolików. Przy braku moderatorów liczbę stolików ustawisz ręcznie poniżej.
    """)
    
    uploaded_file = st.file_uploader("Wgraj plik z danymi (Excel)", type=["xlsx"], on_change=reset_plan)

# --- GŁÓWNA LOGIKA ---
if uploaded_file is not None:
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        if 'Uczestnicy' not in excel_file.sheet_names:
            st.error("Błąd: Plik Excel nie zawiera wymaganego arkusza 'Uczestnicy'.")
            st.stop()
            
        df_participants = pd.read_excel(uploaded_file, sheet_name='Uczestnicy')
        
        required_cols = {'Imię', 'Nazwisko', 'Firma', 'Branża'}
        if not required_cols.issubset(df_participants.columns):
            missing = required_cols - set(df_participants.columns)
            st.error(f"Błąd: W arkuszu 'Uczestnicy' brakuje wymaganych kolumn: {', '.join(missing)}")
            st.stop()
            
        df_participants = df_participants.dropna(subset=['Imię', 'Nazwisko', 'Firma'])
        
        participants = [
            [
                str(row['Imię']).strip(),
                str(row['Nazwisko']).strip(),
                str(row['Firma']).strip(),
                str(row['Branża']).strip() if pd.notna(row['Branża']) and str(row['Branża']).strip() != "" else "Brak"
            ]
            for _, row in df_participants.iterrows()
        ]
        
        moderators_from_file = []
        if 'Moderatorzy' in excel_file.sheet_names:
            df_moderators = pd.read_excel(uploaded_file, sheet_name='Moderatorzy')
            if 'Imię' in df_moderators.columns:
                df_moderators = df_moderators.dropna(subset=['Imię'])
                moderators_from_file = [
                    [
                        str(row['Imię']).strip(),
                        str(row['Nazwisko']).strip() if ('Nazwisko' in df_moderators.columns and pd.notna(row['Nazwisko'])) else ""
                    ]
                    for _, row in df_moderators.iterrows()
                    if str(row['Imię']).strip() != ""
                ]
        
        has_moderators_in_file = len(moderators_from_file) > 0
        
        if len(participants) == 0:
            st.error("Błąd: Arkusz 'Uczestnicy' nie zawiera żadnych poprawnych wierszy.")
            st.stop()
            
        if has_moderators_in_file:
            st.success(f"✅ Wczytano {len(participants)} uczestników i {len(moderators_from_file)} moderatorów.")
        else:
            st.success(f"✅ Wczytano {len(participants)} uczestników (brak moderatorów w pliku – aktywny tryb bez moderatorów).")
        
    except Exception as e:
        st.error(f"Błąd podczas wczytywania pliku: {e}")
        st.stop()

    # --- KONTENER KONFIGURACYJNY (DASHBOARD) ---
    with st.container(border=True):
        st.subheader("⚙️ Konfiguracja Wydarzenia")
        
        if has_moderators_in_file:
            use_moderators = st.toggle(
                "Uwzględnij moderatorów przy stolikach",
                value=True,
                on_change=reset_plan,
                help="Wyłącz, aby przeprowadzić wydarzenie bez moderatorów i samodzielnie określić liczbę stolików."
            )
        else:
            use_moderators = st.toggle(
                "Uwzględnij moderatorów przy stolikach",
                value=False,
                disabled=True,
                help="Opcja niedostępna – w wgranym pliku Excel nie znaleziono listy moderatorów."
            )
            
        moderators = moderators_from_file if use_moderators else []
        
        col_x, col_y, col_z, col_empty = st.columns([1, 1, 1, 1])
        
        with col_y:
            min_seats = 3 if use_moderators else 2
            help_seats = "Wliczając 1 moderatora" if use_moderators else "Wszystkie miejsca przy stoliku są przeznaczone dla uczestników"
            Y = st.number_input("Miejsca przy stoliku", min_value=min_seats, value=4, help=help_seats, on_change=reset_plan)
            
        N = len(participants)
        seats_per_table = (Y - 1) if use_moderators else Y
        
        with col_x:
            if use_moderators:
                X = len(moderators)
                st.number_input(
                    "Liczba stolików",
                    min_value=1,
                    value=X,
                    disabled=True,
                    help="W trybie z moderatorami liczba stolików wynika bezpośrednio z liczby moderatorów w pliku Excel."
                )
            else:
                default_x = max(1, math.ceil(N / seats_per_table))
                X = st.number_input(
                    "Liczba stolików",
                    min_value=1,
                    value=default_x,
                    help="Wartość domyślna dobrana tak, aby pomieścić wszystkich uczestników.",
                    on_change=reset_plan
                )
            
        unique_companies = set([p[2] for p in participants if p[2] != "Brak"])
        F = len(unique_companies)
        
        peers_per_round = (Y - 2) if use_moderators else (Y - 1)
        Z_min = max(1, math.ceil((F - 1) / peers_per_round)) if peers_per_round > 0 else 1
        
        st.markdown(f"""
            <div class="recommendation-box">
                <span class="recommendation-title">💡 Rekomendowana liczba rund: {Z_min}</span>
                <p style="margin:0;">
                    Na podstawie listy <b>{N}</b> uczestników z <b>{F}</b> różnych firm, aby każdy miał szansę poznać przedstawiciela każdej firmy, teoretyczna minimalna liczba rund wynosi <b>{Z_min}</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

        with col_z:
            Z = st.number_input("Docelowa liczba rund", min_value=1, value=Z_min, on_change=reset_plan)
        
        if Z < Z_min:
            max_met = Z * peers_per_round
            percentage = min(100, int((max_met / (F - 1)) * 100)) if F > 1 else 100
            st.warning(f"⚠️ **Uwaga:** Przy {Z} rundach uczestnicy poznają średnio **{percentage}%** dostępnych firm. Rozważ zwiększenie liczby rund dla lepszego efektu networkingowego.")

    # --- OBSŁUGA LIMITU MIEJSC (HARD LIMIT) ---
    M = X * seats_per_table
    L = len(participants)
    
    if L > M:
        required_tables = math.ceil(L / seats_per_table)
        tables_hint = f"zwiększyć liczbę stołów (moderatorów) do co najmniej {required_tables}" if use_moderators else f"zwiększyć liczbę stolików do co najmniej {required_tables}"
        st.error(f"**UWAGA: Przekroczono limit miejsc przy stolikach!**\n\nSystem rozmieści tylko pierwszych {M} uczestników z listy. Aby uwzględnić wszystkich, musisz ograniczyć listę uczestników do {M} osób, {tables_hint} lub zwiększyć ilość miejsc przy stołach.")
        
        with st.expander(f"Uczestnicy nieuwzględnieni (Liczba: {L - M})"):
            excluded_df = pd.DataFrame([p[:3] for p in participants[M:]], columns=["Imię", "Nazwisko", "Firma"])
            # Zmiana indeksowania, aby zaczynało się od 1 zamiast od 0
            excluded_df.index = excluded_df.index + 1
            st.dataframe(excluded_df, use_container_width=True)
            
        participants = participants[:M]

    # --- PRZYCISK AKCJI I ZAPIS DO SESSION STATE ---
    if st.button("🚀 Generuj Plan Usadzenia", type="primary", use_container_width=True):
        with st.spinner("Trwa optymalizacja harmonogramu..."):
            schedule, company_conflicts, industry_conflicts, unique_pct = generate_networking_schedule(
                participants, moderators, X, Y, Z, use_moderators=use_moderators
            )
            
            st.session_state['schedule'] = schedule
            st.session_state['conflicts'] = company_conflicts
            st.session_state['industry_conflicts'] = industry_conflicts
            st.session_state['unique_pct'] = unique_pct
            st.session_state['plan_ready'] = True

    # --- WYŚWIETLANIE WYNIKÓW (Jeśli plan został wygenerowany) ---
    if st.session_state.get('plan_ready', False):
        
        schedule = st.session_state['schedule']
        conflicts = st.session_state['conflicts']
        industry_conflicts = st.session_state.get('industry_conflicts', 0)
        unique_pct = st.session_state['unique_pct']
        
        st.success("✅ Harmonogram wygenerowany pomyślnie!")
        
        # --- METRYKI ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Liczba Stolików", X)
        col2.metric("Konflikty firmowe", conflicts, delta_color="inverse")
        col3.metric("Konflikty branżowe", industry_conflicts, delta_color="inverse")
        col4.metric("Procent unikalnych spotkań", f"{unique_pct:.2f}%")

        # --- WIZUALIZACJA I TABELE ---
        st.header("📊 Wizualizacja i Listy")
        
        figs = visualize_schedule_plotly(schedule, moderators, participants, X, Y, Z, use_moderators=use_moderators)
        
        tabs = st.tabs([f"Runda {r+1}" for r in range(Z)])
        
        participant_ids = {}
        sorted_participants = sorted([p for p in participants if p[2] != "Brak"], key=lambda x: x[1])
        for i, p in enumerate(sorted_participants):
            participant_ids[tuple(p)] = f"P{i+1}"
            
        for r, tab in enumerate(tabs):
            with tab:
                st.plotly_chart(figs[r], use_container_width=True)
                
                st.subheader("Listy uczestników przy stolikach")
                
                cols_per_row = 3
                for i in range(0, X, cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j in range(cols_per_row):
                        if i + j < X:
                            t_idx = i + j
                            with cols[j]:
                                table_data = []
                                if use_moderators:
                                    mod = moderators[t_idx]
                                    table_data.append({"ID": "M", "Imię i Nazwisko": f"{mod[0]} {mod[1]}", "Firma": "Moderator"})
                                
                                for p in schedule[r][t_idx]:
                                    if p[2] != "Brak":
                                        p_id = participant_ids[tuple(p)]
                                        table_data.append({"ID": p_id, "Imię i Nazwisko": f"{p[0]} {p[1]}", "Firma": p[2]})
                                        
                                df_table = pd.DataFrame(table_data)
                                # Zmiana indeksowania tabel per stolik, aby zaczynało się od 1
                                df_table.index = df_table.index + 1
                                st.markdown(f"**Stolik {t_idx + 1}**")
                                st.dataframe(df_table, use_container_width=True)

        # --- EKSPORT ---
        st.header("💾 Eksport Danych")
        
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        df_export = generate_export_dataframe(schedule, moderators, use_moderators=use_moderators)
        buffer_excel = io.BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Harmonogram')
        
        col_dl1.download_button(
            label="📥 Pobierz Harmonogram (Excel)",
            data=buffer_excel.getvalue(),
            file_name="harmonogram_networking.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        pdf_badges_buffer = generate_badges_pdf_buffer(schedule, participants, Z)
        col_dl2.download_button(
            label="🪪 Pobierz Plakietki (PDF)",
            data=pdf_badges_buffer,
            file_name="plakietki_uczestnikow.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        pdf_plan_buffer = generate_visual_plan_pdf_buffer(
            schedule, moderators, participants, X, Y, Z, use_moderators=use_moderators
        )
        col_dl3.download_button(
            label="🗺️ Pobierz Plan Sali (PDF)",
            data=pdf_plan_buffer,
            file_name="plan_sali_wizualizacja.pdf",
            mime="application/pdf",
            use_container_width=True
        )
else:
    st.info("☝️ Aby rozpocząć, wgraj plik Excel z danymi powyżej.")
Apka_v2.1.py
Displaying Apka_v2.1.py.
