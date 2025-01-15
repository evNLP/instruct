# Fine-Tuning Language Models with Mistral and GPT-2

## **Parte 1: Fine-Tuning con Mistral (Modelo Causal Instruido)**

### **Introducción**
Este proyecto utiliza **Mistral**, un modelo causal de lenguaje, para entrenar un sistema que responda a instrucciones específicas relacionadas con cálculos aritméticos simples. Se implementa un enfoque de fine-tuning utilizando LoRA (Low-Rank Adaptation) para reducir la memoria requerida durante el entrenamiento, permitiendo ajustar eficientemente el modelo.

---

### **Dataset**
El dataset está compuesto por una serie de ejemplos con formato JSON, donde cada entrada sigue la estructura:

```json
{"text": "<s>[INST] <número> es igual a [/INST] <serie_de_sumandos> </s>"}
```

Ejemplo:
```json
{"text": "<s>[INST] 33 es igual a [/INST] cinco más tres más ocho más cuatro más cinco más cinco más tres </s>"}
```

#### **Generación del Dataset**
1. **Rango de Números**: Los números objetivo se generan aleatoriamente entre 10 y 50.
2. **Sumandos**: Se generan series de números cuya suma coincide con el número objetivo, representados en palabras como "uno", "dos", "tres".
3. **Volumen**: Se generaron **600 ejemplos** para entrenamiento.

---

### **Configuración de Entrenamiento**
1. **Modelo y Tokenizador**: Se utiliza `unsloth/mistral-7b-instruct-v0.2-bnb-4bit` con cuantización en 4 bits para reducir el uso de memoria.
2. **LoRA**:
   - Rango: `r=8`
   - Alpha: `lora_alpha=16`
   - Dropout: `lora_dropout=0.1`
   - Módulos objetivo: Proyecciones clave, valor y salida.
3. **Entrenamiento**:
   - Épocas: `30`
   - Tamaño de lote: `2`
   - Tasa de aprendizaje: `1e-4`
   - Estrategia de evaluación: Desactivada.

---

### **Resultados**
1. **Generación de Texto**:
   El modelo genera respuestas basadas en la instrucción proporcionada. Ejemplo:

   **Instrucción**:
   ```
   <s>[INST] 33 es igual a [/INST]
   ```

   **Respuesta Generada**:
   ```
   cinco más tres más ocho más cuatro más cinco más cinco más tres
   ```

2. **Evaluación**:
   - **Error Absoluto Medio (MAE)**: El modelo presenta un error promedio menor a **1 unidad**, indicando que comprende correctamente la suma de los elementos generados.
   - **Limitaciones**: El modelo muestra dificultades con frases más complejas o preguntas fuera del formato del entrenamiento, como:
     ```
     <s>[INST] 20 más 23 es igual a [/INST]
     ```

---

### **Conclusión**
El modelo fine-tuneado con LoRA logra cumplir con el objetivo del proyecto, demostrando capacidad para resolver sumas aritméticas simples en el formato entrenado. Sin embargo, podría beneficiarse de más datos y diversificación para manejar casos fuera de distribución.

---

## **Parte 2: Fine-Tuning con GPT-2 (Generación de Código en Java)**

### **Introducción**
Esta parte del proyecto utiliza **GPT-2** para generar código en **Java** mediante dos procesos de entrenamiento:
1. **Fine-Tuning Autoregresivo**: El modelo aprende patrones sintácticos y estructurales del código.
2. **Fine-Tuning Instruido**: Se ajusta el modelo para generar código a partir de instrucciones específicas escritas en comentarios.

---

### **Dataset**

#### **Autoregresivo**
1. **Origen**: Código recopilado de repositorios públicos en GitHub.
2. **Contenido**:
   - Ejemplos de clases, métodos, bucles, condicionales y más.
   - Dataset balanceado y representativo del lenguaje Java.
3. **Estructura**:
   - Cada línea del archivo corresponde a un snippet de código Java.
   - Ejemplo:
     ```java
     public class Main {
         public static void main(String[] args) {
             System.out.println("Hello, World!");
         }
     }
     ```

#### **Instruido**
1. **Formato**: Pares de instrucciones y código.
2. **Ejemplo**:
   ```java
   // A function that prints "Hello, World!"
   public void printHelloWorld() {
       System.out.println("Hello, World!");
   } </s>
   ```
3. **Volumen**: **20,000 ejemplos** generados combinando palabras en inglés y español para diversificar las instrucciones.

---

### **Configuración de Entrenamiento**
1. **Autoregresivo**:
   - Modelo: `GPT2LMHeadModel`
   - Épocas: `5`
   - Tamaño de lote: `8`
   - Longitud de secuencia: `128`
   - Métrica: Pérdida de lenguaje (`Cross-Entropy`).

2. **Instruido**:
   - Épocas: `2.5` (primer modelo), `5` (modelo mejorado).
   - Datos Diversificados: Combinaciones de palabras para aumentar la variedad de instrucciones.

---

### **Resultados**

#### **Autoregresivo**
1. **Capacidades Generativas**:
   - El modelo aprendió a generar estructuras básicas de Java como clases, métodos y bucles.
   - Ejemplo:
     **Prompt**: `public class`
     **Salida**: `public class MyClass { private int value; }`

2. **Limitaciones**:
   - Ausencia de indentación en las salidas iniciales.
   - Generaciones parcialmente correctas pero con errores sintácticos.

3. **Mejora con Dataset Ajustado**:
   - El dataset se enriqueció con indentación correcta.
   - Resultados mejorados: Código con jerarquías claras y bien formateado.

#### **Instruido**
1. **Capacidades Generativas**:
   - El modelo genera código Java a partir de instrucciones textuales.
   - Ejemplo:
     **Instrucción**:
     ```
     // A function printing "Hello, Java!"
     ```
     **Salida Generada**:
     ```java
     public void printHelloJava() {
         System.out.println("Hello, Java!");
     }
     ```

2. **Evaluación**:
   - Precisión Inicial: **55.1%** (primera versión del modelo).
   - Precisión Mejorada: **93.1%** (con dataset extendido).

3. **Errores**:
   - Casos con palabras no vistas en el entrenamiento inicial.
   - Dificultades menores con estructuras complejas.

---

### **Conclusión**
El fine-tuning de GPT-2 mostró que:
1. Es posible adaptar el modelo para generar código estructurado y con formato correcto.
2. La precisión en la generación de instrucciones mejora significativamente con datasets diversificados.
3. Una estrategia combinada de fine-tuning autoregresivo e instruido es efectiva para enseñar a los modelos a entender y generar código Java.

---

### **Comparativa de Modelos**

| **Aspecto**             | **Mistral**                     | **GPT-2**                       |
|--------------------------|----------------------------------|----------------------------------|
| **Tarea**               | Sumas Aritméticas               | Generación de Código en Java    |
| **Método**              | LoRA                            | Autoregresivo e Instruido       |
| **Dataset**             | 600 ejemplos                   | 20,000 ejemplos (mejorado)      |
| **Precisión Inicial**   | -        | 55.1% (Instrucciones)           |
| **Precisión Mejorada**  | -                               | 93.1%                           |

Ambos modelos destacan en sus respectivas tareas y muestran cómo las técnicas modernas de ajuste fino pueden aprovechar modelos preentrenados para resolver problemas específicos.