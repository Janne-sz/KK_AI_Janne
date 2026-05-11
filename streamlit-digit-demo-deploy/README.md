# Sifferprediktion med Streamlit

Demoapp for MNIST-liknande sifferigenkanning.

Anvandaren ritar en siffra 0-9 i webblasaren. Appen preprocessar ritningen till en 28x28 graskalebild och skickar den till modellen `mnist_tuned_cnn.keras`. Resultatet visas som predikterad siffra och sakerhet.

Kors lokalt med:

```bash
streamlit run app.py
```
