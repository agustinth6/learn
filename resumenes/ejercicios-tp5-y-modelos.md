# Ejercicios explicados del TP5 y análisis de modelos de parcial

Material complementario al resumen de lógica secuencial, microprocesador y assembly. Se incluyen los seis ejercicios del TP5 trabajados en la conversación y el análisis de tres modelos de examen compartidos. Las explicaciones y los ejemplos se presentan para practicar, no como una predicción de las preguntas del próximo parcial.

**Fuentes:** [enunciado del TP5](https://docs.google.com/document/d/1W36kU7_RVDf_h7EO8V8y8XMluid9form/edit) y las fotografías de los tres modelos. Las transcripciones automáticas y las fotos pueden contener errores o ser difíciles de leer. Las respuestas manuscritas de las fotos no se toman como solución oficial. Los ejemplos de assembly son esquemáticos y pueden variar según compilador y convención.

---

## 1. TP5, ejercicio 1: contador ascendente hasta 5

**Consigna:** construir un contador ascendente que cuente hasta 5 utilizando flip-flops y los componentes adicionales necesarios.

### 1.1 Qué debe contar y cuántos bits hacen falta

Se busca la secuencia `0 → 1 → 2 → 3 → 4 → 5 → 0 → …`. Se llama **módulo 6** porque recorre seis valores, contando el cero. Para representar el 5 en binario hacen falta tres bits, por lo que usamos tres flip-flops.

| Decimal | Q2 Q1 Q0 |
|--------:|:--------:|
| 0 | 000 |
| 1 | 001 |
| 2 | 010 |
| 3 | 011 |
| 4 | 100 |
| 5 | 101 |

### 1.2 Una solución con flip-flops T

Elegimos tres flip-flops T disparados por flanco ascendente, cada uno con **T = 1**, para que invierta su salida cada vez que recibe un disparo. Usamos `Q0` como bit menos significativo y `Q2` como más significativo.

```
                       Q̅0                    Q̅1
Clock principal ──► [ FF T 0 ] ─────► [ FF T 1 ] ─────► [ FF T 2 ]
                        │                  │                  │
                        Q0                 Q1                 Q2
Entrada T:              1                  1                  1
```

La salida negada `Q̅0` va al clock del segundo y `Q̅1` al clock del tercero. Cuando `Q0` cae de 1 a 0, `Q̅0` sube de 0 a 1 y dispara el segundo. Con el tercero ocurre lo mismo respecto de `Q1`. El primer flip-flop cambia más rápido y los demás forman la cuenta binaria.

### 1.3 Volver a cero después del 5

Sin control adicional, tres bits pueden contar hasta `111` = 7. Para contar hasta 5 y volver a 0:

1. El contador llega a **5 = 101** y permanece allí hasta el siguiente pulso.
2. Al intentar pasar a **6 = 110**, se detecta esa combinación.
3. Se activan las entradas de **clear** de los tres flip-flops para volver a `000`.

En la secuencia normal de 0 a 5, `Q2` y `Q1` no están simultáneamente en 1. Podemos conectarlas a una **NAND** cuya salida vaya al clear de los tres flip-flops, si sus entradas clear son **activas en 0**. Con `Q2=1` y `Q1=1`, la NAND entrega 0 y provoca el reset. Si los clear fueran activos en 1, se podría emplear una AND para esa detección.

**Importante:** no se debe reiniciar al aparecer el 5, porque debe permanecer como estado de cuenta. El `110` aparece transitoriamente al activar el reset, no como una cuenta estable. El estado inicial puede fijarse en `000` con un reset de arranque.

⚠️ Es un contador **asincrónico o de rizado**: las etapas no cambian exactamente al mismo tiempo. En hardware real deben considerarse los retardos de propagación y los requisitos de reset.

**Para explicarlo:** «Uso tres flip-flops T porque necesito tres bits; los encadeno para contar y detecto el 6 para reiniciar a cero. Así recorro los seis valores del 0 al 5».

---

## 2. TP5, ejercicio 2: registro SIPO de 4 bits

**Consigna:** dibujar un registro SI-PO de 4 bits. **SI** significa entrada serie y **PO**, salida paralelo. Recibe los bits uno por uno y permite leer los cuatro a la vez.

### 2.1 Construcción

Usamos **cuatro flip-flops D**: cada uno almacena un bit. La salida Q de cada etapa se conecta a la entrada D de la siguiente y todos comparten el mismo clock.

```
Entrada serie → [D  FF1  Q1] → [D  FF2  Q2] → [D  FF3  Q3] → [D  FF4  Q4]
                       ↓                ↓                ↓                ↓
                       Q1               Q2               Q3               Q4
                       └──────────── salidas en paralelo ─────────────────┘

Todos los flip-flops reciben el mismo clock.
```

Con cada disparo, FF1 copia la entrada serie; FF2 copia el valor que tenía Q1 antes del disparo; FF3 copia el Q2 anterior y FF4 el Q3 anterior. Todos se actualizan simultáneamente: cada bit avanza **una posición por disparo**.

### 2.2 Ejemplo: entran 1, 0, 1, 1

Suponiendo que al principio todos están en 0:

| Momento | Bit que entra | Q1 | Q2 | Q3 | Q4 |
|---------|:-------------:|:--:|:--:|:--:|:--:|
| Inicio | — | 0 | 0 | 0 | 0 |
| Pulso 1 | 1 | 1 | 0 | 0 | 0 |
| Pulso 2 | 0 | 0 | 1 | 0 | 0 |
| Pulso 3 | 1 | 1 | 0 | 1 | 0 |
| Pulso 4 | 1 | 1 | 1 | 0 | 1 |

Después del cuarto disparo, las cuatro salidas están disponibles. Con esta conexión, para leer los bits en su orden de llegada se leen de **Q4 a Q1**: `1011`. Los nombres y el orden de lectura dependen del dibujo utilizado.

**CircuitVerse:** en la figura al final de este documento se señala la entrada serie, los cuatro flip-flops, el clock común y las salidas. En el ejemplo observado el clock parece automático: si es demasiado rápido, puede aumentarse su período en las propiedades. El proyecto público mostrado en la conversación es de otro autor: [registro SIPO de 4 bits](https://circuitverse.org/users/26092/projects/4-bit-sipo-shift-register-e3996e3b-e626-4cfa-a73b-9ce866ed6309).

**Para explicarlo:** «El registro SIPO convierte una entrada serie en una salida paralelo: los bits entran de a uno y luego se leen juntos».

---

## 3. TP5, ejercicio 3: temporal de un flip-flop D

**Consigna:** para un flip-flop D disparado por **flanco descendente**, dibujar Q con las entradas dadas. Regla: en cada transición del clock de `1 → 0`, Q copia el valor de D; entre disparos, conserva su valor.

La tabla del enunciado muestra 13 posiciones de clock, aunque la secuencia escrita en el texto es más corta. Usamos la **tabla**, que coincide con los seis disparos analizados en el video. Como no se indica el estado inicial, suponemos **Q inicial = 0**.

```
Instante:  1  2  3  4  5  6  7  8  9  10 11 12 13
D:         0  1  1  0  0  1  1  1  1   0  0  1  1
Clock:     0  1  0  1  0  1  0  1  0   1  0  1  0
                 ↓     ↓     ↓     ↓      ↓     ↓
Q:         0  0  1  1  0  0  1  1  1   1  0  0  1
```

| Bajada | Instante | D | Q después |
|--------|----------|---|-----------|
| 1.ª | 3 | 1 | 1 |
| 2.ª | 5 | 0 | 0 |
| 3.ª | 7 | 1 | 1 |
| 4.ª | 9 | 1 | 1, permanece igual |
| 5.ª | 11 | 0 | 0 |
| 6.ª | 13 | 1 | 1 |

En la cuarta bajada el flip-flop se activa, pero copiar 1 sobre un Q que ya vale 1 no produce un cambio visible. Si se supusiera Q inicial = 1, solo cambiaría el tramo anterior al primer disparo: en ese primer disparo D vale 1 y, desde ahí, el recorrido es el mismo.

---

## 4. TP5, ejercicio 4: temporal de un flip-flop T

**Consigna:** para un flip-flop T disparado por **flanco ascendente**, dibujar Q. En cada `0 → 1` del clock: si `T=0`, Q conserva su valor; si `T=1`, Q invierte el valor que tenía. Suponemos **Q inicial = 1**, como en el video.

La tabla da 12 valores de T y 13 de clock. El último T no está indicado, pero no hace falta inventarlo porque en el instante 13 el clock baja y no dispara.

```
Instante:  1  2  3  4  5  6  7  8  9  10 11 12 13
T:         0  0  1  1  0  0  0  0  1   1  1  1  —
Clock:     0  1  0  1  0  1  0  1  0   1  0  1  0
              ↑     ↑     ↑     ↑        ↑     ↑
Q:         1  1  1  0  0  0  0  0  0   1  1  0  0
```

| Subida | Instante | T | Q antes | Q después |
|--------|----------|---|---------|-----------|
| 1.ª | 2 | 0 | 1 | 1: mantiene |
| 2.ª | 4 | 1 | 1 | 0: invierte |
| 3.ª | 6 | 0 | 0 | 0: mantiene |
| 4.ª | 8 | 0 | 0 | 0: mantiene |
| 5.ª | 10 | 1 | 0 | 1: invierte |
| 6.ª | 12 | 1 | 1 | 0: invierte |

**Diferencia con el D:** el D copia su entrada; el T conserva o invierte el estado previo.

---

## 5. TP5, ejercicio 5: temporal de un flip-flop JK

**Consigna:** para un JK disparado por **flanco ascendente**, dibujar Q. En cada subida se miran J y K juntas. Suponemos **Q inicial = 0**, como en el video.

| J | K | Q después del disparo |
|---|---|------------------------|
| 0 | 0 | Mantiene el Q anterior |
| 0 | 1 | 0: reset |
| 1 | 0 | 1: set |
| 1 | 1 | Invierte el Q anterior |

J y K tienen 16 valores en el enunciado y la tabla de clock tiene 15; el texto de clock es más corto que su tabla. Se usan los **15 valores de la tabla**, que dan siete subidas. No se conoce el clock en el instante 16, por lo que no se puede determinar Q allí con certeza.

```
Instante:  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
J:         0  0  1  1  0  0  1  1  0   0  1  1  1  1  0
K:         1  1  0  0  0  0  0  0  1   1  0  0  1  1  1
Clock:     0  1  0  1  0  1  0  1  0   1  0  1  0  1  0
              ↑     ↑     ↑     ↑        ↑     ↑     ↑
Q:         0  0  0  1  1  1  1  1  1   0  0  1  1  0  0
```

| Subida | Instante | J | K | Q antes | Q después |
|--------|----------|---|---|---------|-----------|
| 1.ª | 2 | 0 | 1 | 0 | 0: reset |
| 2.ª | 4 | 1 | 0 | 0 | 1: set |
| 3.ª | 6 | 0 | 0 | 1 | 1: memoria |
| 4.ª | 8 | 1 | 0 | 1 | 1: set, ya estaba en 1 |
| 5.ª | 10 | 0 | 1 | 1 | 0: reset |
| 6.ª | 12 | 1 | 0 | 0 | 1: set |
| 7.ª | 14 | 1 | 1 | 1 | 0: invierte |

En el instante 16 las entradas serían `J=1, K=0`. Si el clock permaneciera bajo, Q continuaría en 0; si subiera, se dispararía y Q pasaría a 1. Sin el dato del clock no se puede elegir entre ambas opciones.

---

## 6. TP5, ejercicio 6: temporal de un flip-flop SR

**Consigna:** inventar entradas y dibujar un diagrama temporal que muestre los casos de la tabla. Como el enunciado no especifica el tipo de disparo ni el estado inicial, elegimos un SR con **flanco ascendente y Q inicial = 0**.

| S | R | Q después del disparo |
|---|---|------------------------|
| 0 | 0 | Mantiene el Q anterior |
| 1 | 0 | 1: set |
| 0 | 1 | 0: reset |
| 1 | 1 | Combinación prohibida, sin resultado válido garantizado |

| Disparo | S | R | Q antes | Resultado |
|---------|---|---|---------|-----------|
| 1 | 0 | 0 | 0 | 0: memoria |
| 2 | 1 | 0 | 0 | 1: set |
| 3 | 1 | 0 | 1 | 1: set, ya estaba en 1 |
| 4 | 0 | 0 | 1 | 1: memoria |
| 5 | 0 | 1 | 1 | 0: reset |
| 6 | 0 | 1 | 0 | 0: reset, ya estaba en 0 |
| 7 | 0 | 0 | 0 | 0: memoria |
| 8 | 1 | 1 | 0 | Prohibido: no asignar un valor válido a Q |

**Atención:** con `S=0, R=0`, Q no necesariamente vale 0; conserva lo que ya tenía. El caso `11` se marca como prohibido para completar la tabla del ejercicio, pero no debe usarse para operar un circuito. La figura del final muestra este temporal y señala el último caso en rojo.

---

## 7. Modelos de parcial: qué muestran y cómo estudiarlos

Los modelos de años anteriores ayudan a identificar **tipos de pregunta**, pero no aseguran que el próximo examen tenga el mismo contenido ni los mismos criterios de aprobación. Las respuestas manuscritas pueden ser incorrectas. En el tercer modelo algunas palabras están borrosas y se señalan como aproximadas.

| Tema | Qué se pide en los modelos |
|------|-----------------------------|
| Flip-flops D y T | Tabla, bloques, temporal o identificar el tipo por el gráfico |
| Clock | Unidad, frecuencia, flancos y comparación de señales |
| Registros de desplazamiento | Explicar y esquematizar PISO; en otra foto parece pedirse PIPO |
| Circuitos secuenciales | Diferenciarlos de combinacionales |
| Registros x86 | Identificar propósito general, segmento, pila e IP |
| Funciones y assembly | Explicar `call`, `ret` y salto condicional |
| Variables | Explicar cómo trabaja el microprocesador con sus valores |

### 7.1 Modelo 1: D, variables, clock y PISO

**Flip-flop D.** La tabla es `D=0 → Q*=0` y `D=1 → Q*=1` en el disparo. En el símbolo de bloques, el triángulo de clock representa activación por flanco; un círculo junto al triángulo indica flanco descendente. El modelo fija el valor inicial y el tipo de flanco según la paridad del DNI: **leer la consigna de cada examen**, sin asumir que otra versión usará las mismas reglas. Q y su salida negada Q̅ son complementarias.

**Variable.** El nombre sirve al programador. El procesador trabaja con el valor, que puede estar en memoria o en un registro; en el primer caso se accede mediante una dirección. No toda variable tiene que estar siempre en pila o en RAM.

**Clock.** La frecuencia se mide en **hertz (Hz)**, ciclos por segundo; también se usan MHz y GHz. Más frecuencia suele permitir ciclos más rápidos, con mayor consumo y calor; menos frecuencia suele reducirlos. El rendimiento también depende de la arquitectura y la tarea. `f = 1/T`.

**Combinacional y secuencial.** En el primero la salida depende de las entradas actuales. En el segundo depende de las entradas y del estado previo: tiene memoria. No todos los circuitos secuenciales tienen clock; los sincrónicos sí usan una señal de sincronismo. El clock es una señal, no una definición general de circuito secuencial.

**PISO de 4 bits.** Entrada paralelo y salida serie. Se cargan cuatro bits juntos y luego se selecciona desplazamiento para obtenerlos de a uno. Se puede construir con cuatro flip-flops D y multiplexores de carga/desplazamiento. El modelo pide flip-flops de **flanco descendente**. La primera salida puede estar disponible inmediatamente después de la carga; los disparos siguientes desplazan los demás bits.

### 7.2 Modelo 2: identificar un flip-flop y registros

**Lectura del diagrama.** El gráfico de la foto corresponde a un **flip-flop T de flanco ascendente**. En `t1` la entrada vale 0 y Q permanece en 0; en `t3`, `t5` y `t7` la entrada vale 1 y Q alterna 1, 0, 1. Un D no alternaría mientras su entrada se mantuviera en 1. Los cambios de Q coinciden con las subidas del clock.

**Afirmaciones sobre registros:**

- `RAX`, `EAX` y `AX` son nombres para partes del mismo registro de propósito general de 64, 32 y 16 bits respectivamente. `CS`, `DS` y `SS` son registros de segmento de 16 bits.
- La pila no sirve para «guardar la hora»: interviene en llamadas, direcciones de retorno y datos temporales. El procesador no contiene un sistema operativo de uso general; al iniciar ejecuta firmware, como BIOS o UEFI, ubicado en memoria no volátil.
- `RBX` y `EAX` son de propósito general. `RAX` y `CX` no son registros de segmento.
- **IP no es el puntero de pila:** IP/EIP/RIP indican la próxima instrucción; SP/ESP/RSP apuntan a la pila. En la foto parece marcada como correcta la afirmación incorrecta sobre IP: no memorizar esa marca.
- Para explicar una suma, los operandos pueden cargarse desde RAM a registros y operarse allí. No es una regla universal: pueden estar ya en registros o ser inmediatos, y algunas instrucciones admiten un operando en memoria.

**Comparación de clocks:** sobre el mismo intervalo de tiempo, el que completa más ciclos tiene mayor frecuencia. Período menor implica frecuencia mayor.

### 7.3 Modelo 3: T, funciones y salto condicional

Se distingue una consigna sobre **flip-flop T**, preguntas sobre `call` y `ret`, salto condicional, diferencia entre combinacional y secuencial y un registro de desplazamiento. La imagen es borrosa: el tipo y la cantidad de bits del último registro deben confirmarse en una foto más clara.

- **`call`:** en una llamada cercana habitual guarda la dirección de retorno en la pila y transfiere el control a la función.
- **`ret`:** recupera la dirección de retorno de la pila y continúa allí. La restauración de otros registros y del marco de pila corresponde al código de prólogo y epílogo cuando se usan.
- **Salto condicional:** cambia el recorrido solo si se cumple una condición. Por ejemplo, `cmp eax, 5` actualiza los flags y `je igual` salta si la comparación dio igual; `jne` salta si dio distinto.
- **PIPO**, si se confirma que es el registro pedido: entrada y salida paralelo. Cada bit entra a un flip-flop D distinto; comparten clock y copian todos los bits a la vez. A diferencia de SIPO, los flip-flops no necesitan estar encadenados.

### 7.4 Orden sugerido para repasar

1. Tablas y temporales de **D y T**; luego SR y JK. Practicar tanto dibujar un temporal como identificar el flip-flop a partir de uno.
2. **Clock y flancos**: frecuencia, período y cómo seleccionar subidas o bajadas.
3. Diagramas y funciones de **SIPO, PISO y PIPO**; distinguir serie de paralelo.
4. Diferencia entre **combinacional y secuencial**.
5. Registros **IP, SP, propósito general y segmento**.
6. **`call`, `ret`, `cmp`, `je`, `jne`**, y relación entre variables, RAM y registros.

**Nota:** las figuras y las fotografías de los modelos que siguen complementan las explicaciones. La tercera fotografía tiene partes poco legibles. Los resúmenes completos y la guía por clase siguen en las partes anteriores del PDF unificado.
