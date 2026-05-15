1. Börja med att titta appen i Streamlit: https://sifferprediktion.streamlit.app/
Demoappen är en Streamlit-webbapp som kör en redan tränad CNN-modell. Användaren ritar en siffra i en canvas på webbsidan. 
Bilden preprocessas till samma format som MNIST-data: gråskala, 28x28 pixlar, centrerad siffra och normaliserade pixelvärden. 
Den preprocessade bilden skickas till modellen, som returnerar sannolikheter för klasserna 0-9. Appen visar klassen med 
högst sannolikhet och modellens confidence. Som extrainfo kan man visa den processerade bilden som modellen predicerat samt 
hela prediceringsvektorn

2. Presentation och kunskapskontroll del 2 finns här: 
https://docs.google.com/presentation/d/1ooQ23Jk8tY3-11HtyPySdOVDuRbu7SvkhUqvwmHvIMs/edit?usp=sharing

3. Koden för att ta fram modellen finns här i github: Sifferigenkänning.ipynb

4. Kunskapskontroll del 1 finns här: https://docs.google.com/document/d/1Uomh6ikHw4VYUDK2VyL6it_6iWl5Y59SaD0nRDaUIMo/edit?usp=sharing

Mer kuriosa och kan hoppas över
4. Det som rör appen och streamlit finns här i github i foldern streamlit-digit-demo-deploy
5. Planen för genomförandet finns här  i github: streamlit_digit_demo_kanvas.md
