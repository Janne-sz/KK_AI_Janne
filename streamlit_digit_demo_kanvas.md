# Kanvas: Streamlit-demo for sifferigenkanning

Syfte: lararen scannar en QR-kod, ritar en siffra 0-9 i mobilen, trycker Klar och far modellens prediktion samt sakerhet.

## 1. Malbild

- [ ] En publik webbsida finns tillganglig via URL.
- [ ] URL:en finns som QR-kod.
- [ ] Sidan fungerar i mobilwebblasare.
- [ ] Anvandaren kan rita en siffra med fingret.
- [ ] Anvandaren kan trycka pa Klar.
- [ ] Appen visar predikterad siffra, t.ex. `4`.
- [ ] Appen visar confidence/sakerhet, t.ex. `0.98`.

## 2. Modell-export

- [x] Modellfilen som ska anvandas i demon heter `mnist_tuned_cnn.keras`.
- [x] Kontrollera modellens input shape: `(None, 28, 28, 1)`.
- [x] Kontrollera om modellen tranades med pixelvarden `0-1` eller `0-255`: modellen tranades med `X_train.reshape(-1, 28, 28, 1) / 255.0`, alltsa `0-1`.
- [x] Kontrollera om siffrorna i traningsdata ar ljusa pa mork bakgrund eller tvartom: MNIST-bilderna ar vit/ljus siffra pa svart/mork bakgrund.
- [x] Exportera modellen i Keras-format:

```python
model.save("mnist_tuned_cnn.keras")
```

- [x] Testa lokalt att modellen kan laddas igen:

```python
import keras
model = keras.models.load_model("mnist_tuned_cnn.keras")
```

## 3. Streamlit-app

- [x] Skapa `app.py`.
- [x] Skapa `requirements.txt`.
- [x] Anvand `streamlit-drawable-canvas` for rit-rutan.
- [x] Ladda modellen med cache:

```python
@st.cache_resource
def load_digit_model():
    return keras.models.load_model("model.keras")
```

- [x] Visa knapp: `Klar`.
- [x] Kor prediktion endast efter knapptryck.
- [x] Visa resultatet tydligt: siffra + confidence.

## 4. Preprocessing fran ritad siffra till MNIST-format

Canvasbilden maste goras om till samma format som modellen tranades pa.

- [x] Hamta bilden fran canvasen.
- [x] Konvertera RGBA/RGB till graskala.
- [x] Invertera fargerna om det behovs sa att bilden matchar MNIST-formatet: canvasen ritar direkt vit siffra pa svart bakgrund, sa ingen invertering behovs nu.
- [x] Hitta bounding box runt den ritade siffran.
- [x] Beskar bilden runt siffran.
- [x] Skala siffran proportionerligt sa den ryms i cirka `20x20`.
- [x] Placera siffran i en `28x28`-bild.
- [x] Centrera med center of mass, eller anvand bounding-box-centrering om det fungerar battre i praktiken.
- [x] Normalisera pixelvarden pa samma satt som vid traning.
- [x] Forma arrayen till modellens input, t.ex. `(1, 28, 28, 1)`.

Kommentar till redovisning: MNIST-bilder ar 28x28 graskalebilder. Ursprungliga siffror normaliserades till en 20x20-ruta med bevarad proportion och centrerades sedan i 28x28, ofta beskrivet med center of mass.

## 5. Lokal test

- [ ] Installera dependencies lokalt.
- [ ] Starta appen:

```bash
streamlit run app.py
```

- [ ] Testa i datorns webblasare.
- [ ] Testa med olika siffror 0-9.
- [ ] Testa fula/snabba mobil-liknande ritningar.
- [ ] Justera preprocessing om modellen gissar systematiskt fel.

## 6. GitHub och deployment

- [ ] Skapa GitHub-repo eller anvand befintligt repo.
- [ ] Lagg in:
  - [ ] `app.py`
  - [ ] `model.keras`
  - [ ] `requirements.txt`
  - [ ] eventuell `README.md`
- [ ] Deploya pa Streamlit Community Cloud.
- [ ] Valj repo, branch och `app.py`.
- [ ] Spara den publika `streamlit.app`-URL:en.

## 7. QR-kod

- [ ] Skapa QR-kod som pekar pa Streamlit-URL:en.
- [ ] Testa QR-koden med mobilen.
- [ ] Kontrollera att appen fungerar over mobildata eller annat Wi-Fi.
- [ ] Lagg QR-koden i inlamning, rapport eller enkel webbsida.

## 8. Risker och backup-planer

- [ ] Om appen sover pa Streamlit Cloud: oppna URL:en och vack appen innan bedomning, eller skriv att den kan behova vakna.
- [ ] Om TensorFlow/Keras blir for tungt: undersok TensorFlow Lite eller ONNX som alternativ.
- [ ] Om modellen gissar fel pa mobilritade siffror: forbattra preprocessing eller lagg till exempel ritade via canvas som extra testdata.
- [ ] Om Inleed inte kan kora Streamlit: anvand Inleed endast for eventuell informationssida/QR, inte for modellinferens.

## 9. Kort forklaring till rapport/redovisning

Demoappen ar en Streamlit-webbapp som kor en redan tranad CNN-modell. Anvandaren ritar en siffra i en canvas pa webbsidan. Bilden preprocessas till samma format som MNIST-data: graskala, 28x28 pixlar, centrerad siffra och normaliserade pixelvarden. Den preprocessade bilden skickas till modellen, som returnerar sannolikheter for klasserna 0-9. Appen visar klassen med hogst sannolikhet och modellens confidence.

## 10. Definition of done

- [ ] QR-koden gar att scanna.
- [ ] Sidan oppnas pa mobil utan extra app.
- [ ] Det gar att rita med fingret.
- [ ] Klar-knappen ger prediktion.
- [ ] Confidence visas.
- [ ] Appen fungerar fran annan plats an din egen dator.
- [ ] Du kan forklara appflodet schematiskt.
