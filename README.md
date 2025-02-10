# 🛑 **Driver Drowsiness Detection System**  

## 🚗 **Descripción del Proyecto**  

Este proyecto tiene como objetivo mejorar la **seguridad vial** mediante la detección de signos de fatiga y somnolencia en los conductores utilizando **técnicas de visión por computadora y machine learning**.  

A través del análisis de **expresiones faciales** y la detección de **cierre de ojos y bostezos**, el sistema alerta al conductor mediante **alarmas sonoras y visuales** cuando se detectan signos de cansancio.  

<p align="center">
  <img src="./Driver Drowsiness Detection System.png" alt="Driver Drowsiness Detection System">
</p>

---

## 🎯 **Enfoque y Estrategia**  

### 🔬 **Primer Enfoque: Entrenamiento de un Modelo Personalizado**  
Inicialmente, se consideró entrenar un modelo personalizado basado en un dataset etiquetado con señales de somnolencia, tales como:  

✔ Ojos cerrados  
✔ Bostezos  
✔ Inclinaciones de cabeza  

Para este enfoque, se requería:  

1️⃣ **Un dataset etiquetado** con imágenes o videos de conductores en diferentes estados de alerta.  
2️⃣ **Entrenamiento del modelo**, incluyendo preprocesamiento, selección de características y evaluación de rendimiento.  

💡 **Desafío:** Requería una gran cantidad de datos y poder computacional para el entrenamiento del modelo.  

---

### ✅ **Enfoque Final: Modelo Preentrenado y Detección Basada en Umbrales**  

Se optó por una solución **más liviana y eficiente**, basada en:  

✔ **Modelo preentrenado** `shape_predictor_68_face_landmarks.dat` de `dlib`.  
✔ **Cálculo de características faciales** (EAR y MAR).  
✔ **Definición de umbrales** para activar las alertas.  

---

## 🔍 **¿Cómo Funciona?**  

El sistema detecta **dos condiciones principales**:  

### 💤 **1. Detección de Ojos Cerrados (Fatiga Prolongada)**  
- Se calcula el **Eye Aspect Ratio (EAR)** usando **landmarks faciales**.  
- Si los ojos permanecen cerrados por más de **2 segundos**, se dispara una **alarma sonora**.  

### 😲 **2. Detección de Bostezos (Somnolencia)**  
- Se mide el **Mouth Aspect Ratio (MAR)**.  
- Si el valor supera el umbral, se considera un bostezo y se activa una **alerta de advertencia**.  

---

## 🛠 **Tecnologías Utilizadas**  

🖥 **Computer Vision:** `OpenCV`, `dlib`, `imutils`  
🎵 **Alarma Sonora:** `pygame.mixer`  
🔢 **Procesamiento Numérico:** `NumPy`  
🌈 **Coloreado en Consola:** `colorama`  

---

## 📂 **Estructura del Proyecto**  

```
├── data/                                      # Modelos preentrenados y otros recursos
│   ├── shape_predictor_68_face_landmarks.dat  # Modelo de dlib para detección de landmarks faciales
├── sounds/                                    # Alarmas sonoras
│   ├── sleep_alarm.mp3                        # Alarma de fatiga
│   ├── drowsy_alarm.mp3                       # Alarma de bostezo
├── drowsiness_detection.py                    # Código principal del sistema
├── README.md                                  # Documentación del proyecto
```

---

## 🚀 **Cómo Usarlo**  

1️⃣ **Instalar dependencias**  
```bash
pip install opencv-python numpy dlib pygame colorama imutils
```

2️⃣ **Ejecutar el sistema de detección**  
```bash
python detect.py
```

3️⃣ **(Opcional)** Ajustar los umbrales en `detect.py` según las necesidades del usuario.  

---

## 📌 **Posibles Mejoras**  

🔍 **Refinamiento de la Detección de Bostezos**  
- Implementar filtros adicionales para distinguir entre bostezos reales y otros movimientos de la boca.  

📏 **Detección de Inclinación de Cabeza (Nodding)**  
- Integrar la detección de inclinaciones de cabeza para mejorar la precisión del sistema.  

🔊 **Alarmas Personalizadas**  
- Agregar opciones de alarmas **diferentes según el nivel de somnolencia detectado**.  

📊 **Sistema de Reportes**  
- Implementar un registro de detecciones para analizar **patrones de fatiga en los conductores**.  

---

## 🏁 **Conclusión**  

Este sistema demuestra cómo **la visión por computadora y la IA pueden mejorar la seguridad en la conducción**.  

📢 **Si te interesa el proyecto, dale una ⭐ en GitHub y contribuye con mejoras!** 🚀  

---

## 📌 **Contacto y Colaboración**  

🔹 **[Web](https://pdroruiz.com/)**  
🔹 **[GitHub](https://github.com/pdro-ruiz)**  
🔹 **[Kaggle](https://www.kaggle.com/pdroruiz)**  
🔹 **[LinkedIn](https://www.linkedin.com/in/)**  

🚗 **¡Conducir seguro es responsabilidad de todos!** 🛑  
