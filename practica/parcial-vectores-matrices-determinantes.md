# Práctica para el parcial — Vectores, Matrices y Determinantes

Basada en tus cuatro archivos: los slides de **Vectores** (15-5), **Matrices completo**, **Determinante de una Matriz** y el **TP** del Instituto Nº 11 (docente Karina Arceri).

---

## Qué entra

| Bloque | Contenido | Dónde está en tu material |
|---|---|---|
| **1.** Vectores | magnitud, escalar × vector, suma (analítica y gráfica), distancia entre puntos, punto medio, recta $y=mx+b$, vocabulario (equipolentes, opuestos, concurrentes, ortogonales) | Slides Vectores + TP 1–11 |
| **2.** Matrices | orden y elementos $a_{ij}$, suma/resta, opuesta, nula, escalar × matriz, producto, traspuesta, equivalentes | Slides Matrices + TP 12, 14, 15 |
| **3.** Determinantes | Sarrus ($3\times3$), Laplace por cofactores (cualquier orden) | Slides Determinante + TP 16, 17 |
| **4.** Modelos | plantear un sistema $3\times3$ y resolverlo por determinantes (Cramer); producto de matrices para totales de insumos | TP 18–21 |

**Dónde están los puntos:** el TP dedica cuatro ejercicios largos (18 a 21) a *plantear* un problema en forma de matriz y resolverlo. Eso es lo que más pesa y lo que más se practica acá.

### Cómo usar esta guía

1. **Bloque 0 (diagnóstico)** con reloj y sin mirar nada. 8 preguntas, 20 minutos.
2. Corregí con el solucionario del final. Anotá **qué tipo de error** fue, no solo cuál estaba mal.
3. Si un bloque te salió flojo, leé su mini-teoría y hacé los ejercicios de ese bloque.
4. Cerrá con el **simulacro** completo, cronometrado.

> **Regla de oro en el parcial:** cada resultado numérico se puede chequear. Un determinante se verifica por Sarrus *y* por Laplace. Un sistema se verifica reemplazando. Un producto de matrices se verifica mirando el orden. Perder 5 minutos en verificar es más barato que perder el ejercicio entero.

---

## Bloque 0 — Diagnóstico

Sin calculadora simbólica, con lápiz. Anotá el tiempo.

**D1.** Hallar $|v|$ para $v=(-6,\,8)$.

**D2.** Hallar $d(A,B)$ para $A=(3,-2)$ y $B=(-1,5)$. Dejá el resultado exacto y una aproximación.

**D3.** Hallar el punto medio entre $A=(-3,5)$ y $B=(7,-1)$.

**D4.** Con $A=(3,4)$, $B=(-5,2)$ y $C=(1,-7)$, calcular $A+B+C$.

**D5.** Calcular $-2\cdot(3,-4)$.

**D6.** Si $A$ es de orden $2\times3$ y $B$ de orden $3\times2$, ¿cuál es el orden de $A\cdot B$? ¿Y el de $B\cdot A$?

**D7.** Calcular por Sarrus:

$$
\det\begin{pmatrix}1&2&3\\0&4&5\\1&0&6\end{pmatrix}
$$

**D8.** Resolver por determinantes (Cramer):

$$
\begin{cases}
3x+2y=16\\
x+y=6
\end{cases}
$$

*(Soluciones del bloque 0 al final, sección S0.)*

---

## Bloque 1 — Vectores

### Mini-teoría: de dónde sale todo

**Un vector es una flecha con tres datos: módulo (cuánto mide), dirección (la recta que la contiene) y sentido (hacia dónde apunta).** Un escalar es solo un número con unidad. Esa es toda la diferencia entre magnitud escalar y vectorial: *la escalar no necesita dirección para quedar determinada*.

Si das las componentes $(x,y)$, el vector queda determinado: avanzás $x$ en horizontal e $y$ en vertical. Entonces las componentes son los **catetos** de un triángulo rectángulo y el vector es la **hipotenusa**. De ahí sale, sin memorizar nada:

$$
|v|=\sqrt{x^2+y^2}
$$

El módulo **nunca es negativo** (es una longitud) y por eso los signos de las componentes desaparecen al elevarlas al cuadrado. Ese es el error nº1: restar en lugar de sumar cuando hay coordenadas negativas.

**Suma:** si dos desplazamientos se hacen uno tras otro, el total se obtiene sumando componente a componente. Gráficamente es la "punta con cola": apoyás la cola de $B$ en la punta de $A$, y el vector que va del origen a la nueva punta es $A+B$. Las dos formas dan lo mismo, siempre.

**Escalar × vector:** $k\cdot(x,y)=(kx,ky)$. Multiplica el módulo por $|k|$; si $k<0$ invierte el sentido; si $k=0$ da el vector nulo.

**Distancia entre dos puntos:** es el módulo del vector que los une, $B-A$:

$$
d(A,B)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}
$$

Si los puntos están en la misma horizontal o vertical, la fórmula sigue valiendo (un cateto se hace 0) y alcanza con contar cuadraditos.

**Punto medio:** el promedio. El número que está justo al medio entre $a$ y $b$ es $\frac{a+b}{2}$; aplicado a cada coordenada:

$$
M=\left(\frac{x_1+x_2}{2},\ \frac{y_1+y_2}{2}\right)
$$

**Recta:** $y=mx+b$. $m$ es cuánto cambia $y$ por cada unidad de $x$ (pendiente) y $b$ es dónde corta el eje $y$ (valor cuando $x=0$).

### Ejercicios

**1.1** Calcular el módulo y graficar:
a) $u=(-6,8)$  b) $v=(5,12)$  c) $w=(-9,-12)$  d) $z=(2,-4)$

**1.2** Con $v=(-2,5)$ calcular y graficar en el mismo plano: $3v$, $-1\cdot v$, $\tfrac{1}{2}v$, $0\cdot v$. ¿Qué nombre recibe $-1\cdot v$?

**1.3** Con $A=(4,-1)$, $B=(-6,3)$, $C=(2,5)$: calcular $A+B$, $B-C$, $A+B+C$. Graficar $A+B+C$ por el método punta-cola.

**1.4** (TP 5) Con $A=(5,4)$, $B=(-3,4)$, $C=(5,2)$, $D=(-3,1)$ calcular $d(A,B)$, $d(B,C)$, $d(C,D)$, $d(A,C)$, $d(B,D)$.

**1.5** (TP 3) Un cable de seguridad une dos puntos de una estructura: el segundo está 120 m en horizontal y 90 m en vertical respecto del primero. ¿Longitud mínima del cable?

**1.6** (TP 4) Un dron se desplaza 80 m al este y 150 m al norte, $D=(80,150)$.
a) Calcular $|D|$. b) Interpretar el resultado en el contexto.

**1.7** (TP 6) Dos sectores del campus: $A=(3,2)$ y $B=(11,8)$.
a) Distancia entre ellos. b) Punto medio. c) Verificar que el punto medio equidista de ambos.

**1.8** (TP 8) Un objeto parte de $(0,0)$ y se mueve: 4 cuadras al este y 3 al norte; luego 7 al este y 1 al norte; luego 3 al este y 2 al sur. ¿Coordenadas finales?

**1.9** (TP 9) Un robot parte de $(0,0)$: avanza 6 m al este, luego 4 m al norte, luego 3 m al oeste. Dar la posición final y el módulo del desplazamiento total. ¿Coincide con el camino recorrido?

**1.10** La tarifa de un taxi es \$200 de bajada de bandera más \$100 por kilómetro: $y=100x+200$.
a) ¿Cuánto sale un viaje de 12 km? b) ¿Cuántos km hiciste si pagaste \$1.450? c) ¿Qué representa $b$ y qué representa $m$?

**1.11** Teoría (TP 12). Responder en dos o tres líneas cada una:
a) ¿Qué es un vector? b) ¿Cuáles son sus componentes? c) ¿Cuándo dos vectores son equipolentes? d) ¿Cuándo son opuestos? e) ¿Cuándo son concurrentes? f) ¿Cuándo son ortogonales? g) Diferencia entre magnitud escalar y vectorial. h) ¿Qué es el vector nulo?

---

## Bloque 2 — Matrices

### Mini-teoría

**Una matriz es una tabla de números ordenada en filas y columnas.** El orden (o dimensión) es $filas\times columnas$. El elemento $a_{ij}$ está en la fila $i$, columna $j$ — se lee "a sub i j", no es un número de dos cifras.

**Suma y resta:** se hace elemento con elemento, y para eso las matrices tienen que tener **exactamente el mismo orden**. Sumar una $2\times3$ con una $3\times2$ no existe.

**Opuesta:** se cambia el signo de cada elemento. Cumple $A+(-A)=\mathbf{0}$ (matriz nula, todos ceros).

**Escalar × matriz:** se multiplica cada elemento por el escalar.

**Producto $A\cdot B$:** la condición es que **el número de columnas de $A$ sea igual al número de filas de $B$**. Si $A$ es $m\times n$ y $B$ es $n\times p$, el resultado es $m\times p$. Cada elemento se obtiene multiplicando una **fila de $A$** por una **columna de $B$**, término a término, y sumando:

$$
(AB)_{ij}=\sum_{k} a_{ik}\,b_{kj}
$$

Por qué funciona así: cada fila de $A$ son los "pesos" y cada columna de $B$ son las "cantidades"; el producto interno es el total combinado. En los problemas de insumos eso es literal (ver Bloque 4).

**El producto no es conmutativo:** $A\cdot B$ y $B\cdot A$ pueden ser distintos, o uno existir y el otro no.

**Traspuesta $A^t$:** se cambian filas por columnas. La fila 1 pasa a ser la columna 1. Si $A$ es $m\times n$, $A^t$ es $n\times m$. Propiedad útil: $(AB)^t=B^tA^t$ (¡en ese orden!).

**Simétrica:** $A^t=A$.

**Equivalente:** dos matrices del mismo orden son equivalentes si se pasa de una a otra por operaciones elementales de fila/columna (equivalentemente: tienen el mismo rango).

### Ejercicios

**2.1** Para $A=\begin{pmatrix}2&-1&3\\0&4&-2\end{pmatrix}$ indicar: a) orden; b) $a_{12}$, $a_{21}$, $a_{23}$.

**2.2** Con $A$ de 2.1 y $B=\begin{pmatrix}1&5&-3\\2&0&6\end{pmatrix}$: calcular $A+B$ y $A-B$.

**2.3** Escribir la opuesta de $A$ y verificar $A+(-A)=\mathbf{0}$.

**2.4** Con $C=\begin{pmatrix}1&-2\\3&0\\5&4\end{pmatrix}$: calcular $3C$ y luego $(3C)^t$.

**2.5** Calcular $A\cdot D$ con $A$ de 2.1 y $D=\begin{pmatrix}1&2\\0&-1\\3&4\end{pmatrix}$. ¿Qué orden tiene el resultado y por qué?

**2.6** ¿Se puede calcular $A\cdot B$ con las $A$ y $B$ de 2.2? Justificar. ¿Y $B\cdot A$?

**2.7** Verificar numéricamente $(A\cdot D)^t=D^t\cdot A^t$ con las matrices de 2.5.

**2.8** ¿Es simétrica $S=\begin{pmatrix}2&-1&3\\-1&5&0\\3&0&7\end{pmatrix}$? Justificar.

**2.9** Una librería tiene dos sucursales. Las ventas del mes (en unidades) fueron:

| | Cuadernos | Lapiceras | Carpetas |
|---|---|---|---|
| Centro | 12 | 5 | 8 |
| Shopping | 20 | 3 | 10 |

Los precios son \$250, \$400 y \$150 respectivamente. Calcular el ingreso de cada sucursal usando producto de matrices.

---

## Bloque 3 — Determinantes

### Mini-teoría

**El determinante es un número asociado a una matriz cuadrada.** Para $2\times2$:

$$
\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc
$$

Memoria visual: producto de la diagonal principal menos producto de la otra. **El orden de la resta importa**: si lo invertís, cambia el signo.

**Sarrus (solo $3\times3$).** Se copian debajo las dos primeras filas; se suman los productos de las tres diagonales descendentes y se restan los de las tres ascendentes. Es la generalización directa de $ad-bc$: todas las formas de bajar de arriba a abajo menos todas las de subir.

**Laplace (cualquier orden).** Se elige **una fila o columna** — conviene la que tenga más ceros — y se desarrolla:

$$
\det A=\sum_{j}(-1)^{i+j}\,a_{ij}\,M_{ij}
$$

donde $M_{ij}$ es el determinante que queda al **tachar la fila $i$ y la columna $j$**. El signo sigue el tablero:

$$
\begin{pmatrix}+&-&+&-\\-&+&-&+\\+&-&+&-\\-&+&-&+\end{pmatrix}
$$

Cada cero que elegís te ahorra un determinante entero. Por eso "elegir bien la fila" es la mitad del ejercicio.

**Propiedades que ahorran todo el cálculo:**

- Si una fila o columna es toda cero → $\det=0$.
- Si hay dos filas (o columnas) iguales o proporcionales → $\det=0$.
- Triangular (o diagonal): $\det$ = producto de la diagonal.
- $\det(A^t)=\det(A)$.
- $\det(kA)=k^n\det(A)$ para $A$ de orden $n$ (¡$n$ es el orden, no un $2$ fijo!).
- $\det(AB)=\det(A)\det(B)$.
- Si intercambiás dos filas, el determinante cambia de signo.

### Ejercicios

**3.1** Calcular: a) $\det\begin{pmatrix}3&5\\2&-4\end{pmatrix}$ b) $\det\begin{pmatrix}-2&7\\0&3\end{pmatrix}$

**3.2 Sarrus.** Calcular:
a) $A=\begin{pmatrix}5&2&-3\\0&8&-1\\-4&5&2\end{pmatrix}$
b) $B=\begin{pmatrix}3&6&-2\\-4&1&-3\\5&-5&2\end{pmatrix}$
c) $C=\begin{pmatrix}2&-3&-4\\0&5&2\\-1&-2&3\end{pmatrix}$
d) $D=\begin{pmatrix}1&2&3\\4&5&6\\7&8&10\end{pmatrix}$ — y explicar por qué el resultado no es 0 aunque se parezca a la matriz "1,2,3 / 4,5,6 / 7,8,9".

**3.3 Laplace $3\times3$.** Calcular eligiendo la fila o columna más conveniente:
a) $A=\begin{pmatrix}-4&0&1\\3&2&0\\-5&7&-9\end{pmatrix}$
b) $B=\begin{pmatrix}2&-1&3\\4&-2&0\\1&3&-4\end{pmatrix}$
c) $C=\begin{pmatrix}0&2&1\\3&-1&4\\2&0&5\end{pmatrix}$

**3.4 Laplace $4\times4$.**

$$
M=\begin{pmatrix}1&0&2&0\\3&1&0&1\\0&0&4&0\\2&0&1&5\end{pmatrix}
$$

**3.5 Verificación cruzada.** Tomar la matriz $D$ de 3.2 y calcularla también por Laplace. ¿Da lo mismo? ¿Qué te dice eso sobre cuál método elegir en el parcial?

**3.6 Propiedades.** Sin calcular el determinante completo (o con el mínimo cálculo), decidir:
a) $\det\begin{pmatrix}1&2&3\\0&5&7\\0&0&-2\end{pmatrix}$
b) $\det\begin{pmatrix}2&4&6\\1&3&5\\2&4&6\end{pmatrix}$
c) Si $\det A=3$ y $A$ es $3\times3$, ¿cuánto vale $\det(2A)$?
d) Si $\det A=4$ y $\det B=-2$, ¿cuánto vale $\det(AB)$ y $\det(A^t)$?

---

## Bloque 4 — Modelos: sistemas por determinantes y producto de matrices

### Mini-teoría: cómo plantear

Toda situación de "varias cosas combinan varios insumos y sé el total" es un sistema lineal:

$$
\begin{cases}
a_{11}x_1+a_{12}x_2+a_{13}x_3=d_1\\
a_{21}x_1+a_{22}x_2+a_{23}x_3=d_2\\
a_{31}x_1+a_{32}x_2+a_{33}x_3=d_3
\end{cases}
$$

**Cramer:** con $\Delta=\det A$ (determinante de los coeficientes), cada incógnita es

$$
x_i=\frac{\Delta_i}{\Delta}
$$

donde $\Delta_i$ es el determinante que resulta de **reemplazar la columna $i$** por la columna de los términos independientes. Si $\Delta=0$, el sistema no tiene solución única (o ninguna, o infinitas) — eso ya es información, no un error de cuenta.

**Regla de planteo:** una **fila** = un caso (una persona, un producto, un evento). Una **columna** = una incógnita. El término independiente es el total de esa fila. Antes de resolver, preguntate si el orden elegido tiene sentido: si las filas son personas y las columnas productos, la matriz es "personas × productos".

**Producto de matrices para totales:** si $P$ es "casos × productos" y $R$ es "productos × insumos", entonces $P\cdot R$ es "casos × insumos": las unidades totales de cada insumo por caso. Esa es toda la idea — el producto interno de una fila con una columna suma aportes.

### Ejercicios

**4.1 Cramer básico.**

$$
\begin{cases}
x+y+z=6\\
2x-y+z=3\\
x+2y-z=2
\end{cases}
$$

Resolver por Cramer, indicando $\Delta$, $\Delta_x$, $\Delta_y$, $\Delta_z$.

**4.2 (TP 18 — el súper).** Fernando gastó \$578, Paula \$193 y Ana \$227. Compras en unidades:

| | Gaseosas | Arroz | Yerba |
|---|---|---|---|
| Fernando | 7 | 6 | 8 |
| Paula | 3 | 1 | 3 |
| Ana | 4 | 3 | 2 |

a) Plantear el sistema y resolverlo por determinantes para hallar el valor unitario de gaseosas, arroz y yerba.
b) Verificar reemplazando en las tres ecuaciones.

**4.3 (TP 19 — indumentaria, versión corregida).** Una fábrica produce remeras, shorts y calzas. Requerimientos por unidad:

- Remera: 2 m de tela, 1 bobina de hilo, 0 cierres.
- Short: 1 m de tela, 2 bobinas de hilo, 1 cierre.
- Calza: 3 m de tela, 2 bobinas de hilo, 0 cierres.

Los costos de materia prima por unidad son: remera \$450, short \$380, calza \$700.
a) Plantear y resolver por determinantes el precio del metro de tela, la bobina de hilo y el cierre.
b) La fábrica recibe un pedido de 50 remeras, 30 shorts y 40 calzas. Calcular por producto de matrices la cantidad total de cada insumo y el costo total del pedido.

**4.4 (TP 20 — ensambladora, versión corregida).** Tres dispositivos e insumos por equipo:

| | Microprocesadores | Módulos de memoria | Placas de video | Costo del equipo |
|---|---|---|---|---|
| Laptop | 3 | 2 | 1 | \$11.700 |
| Tablet | 1 | 1 | 0 | \$3.700 |
| Consola | 2 | 2 | 2 | \$11.000 |

a) Plantear la matriz y hallar el costo individual de cada componente.
b) Sucursal A pide 10 laptops, 20 tablets y 5 consolas; sucursal B pide 15, 10 y 15. Plantear la matriz de pedidos y calcular, por producto de matrices, los insumos totales de cada sucursal.

**4.5 (TP 21 — jugos, versión con números cerrados).** Una planta elabora energético, vitamínico y detox. Requerimientos por litro:

- Energético: 5 unidades de naranja, 2 de jengibre, 1 de miel.
- Vitamínico: 4 de naranja, 4 de jengibre, 2 de miel.
- Detox: 3 de naranja, 5 de jengibre, 4 de miel.

Costos de producción por litro: energético \$160, vitamínico \$200, detox \$255.
a) Calcular el valor unitario de cada insumo.
b) Tres eventos: E1 (100, 50, 80) litros, E2 (60, 90, 40), E3 (120, 30, 100). Calcular por producto de matrices los insumos totales y el costo de cada evento. Interpretar la matriz resultante.

**4.6 (examen típico).** Una verdulería vende tres bolsones. El bolsón A lleva 2 kg de papas, 1 de cebollas y 1 de tomates y cuesta \$3.100; el B lleva 3, 2 y 1 y cuesta \$4.500; el C lleva 1, 1 y 2 y cuesta \$3.200. ¿Cuánto sale el kilo de cada cosa? Resolver por determinantes y **verificar que la solución sea admisible en el contexto**.

---

## Bloque 5 — Simulacro

**90 minutos. Sin mirar el solucionario. Mostrá el procedimiento: se corrige el desarrollo.**

**1. (12 pts)** Con $A=(2,-5)$ y $B=(-6,3)$:
a) $|A|$ y $|B|$ (exacto y con un decimal).
b) $A+B$.
c) $3A-2B$.
d) $d(A,B)$.
e) Punto medio de $A$ y $B$.

**2. (12 pts)** Dos antenas están en $P=(-4,3)$ y $Q=(8,-1)$.
a) Calcular la distancia entre ellas.
b) Hallar el punto medio.
c) Verificar analíticamente que el punto medio equidista de $P$ y $Q$.
d) Si se instala un repetidor en el punto medio y el cable va de $P$ al repetidor, ¿cuánto cable se necesita?

**3. (14 pts)** Con $A=\begin{pmatrix}2&1\\3&-1\end{pmatrix}$ y $B=\begin{pmatrix}0&4\\-2&5\end{pmatrix}$:
a) $A\cdot B$.
b) $B\cdot A$.
c) ¿Qué conclusión sacás comparando a) y b)?
d) $A^2$.
e) $(AB)^t$.

**4. (14 pts)** Para $D=\begin{pmatrix}1&2&3\\4&5&6\\7&8&10\end{pmatrix}$:
a) Calcular $\det D$ por Sarrus.
b) Calcular $\det D$ por Laplace eligiendo la fila o columna que te convenga.
c) ¿Coinciden? Si no, hay un error: encontrarlo.

**5. (16 pts)** Una empresa de logística cobra por tres tipos de envío. El envío A usa 2 cajas grandes, 1 mediana y 3 chicas; el B usa 1, 3 y 2; el C usa 4, 1 y 1. Los costos totales de caja por envío son \$2.400, \$2.600 y \$3.700 respectivamente. Hallar el costo de cada tipo de caja **por el método de determinantes**, y verificar la solución.

**6. (12 pts)** Una cadena tiene dos locales. Los pedidos mensuales son: local 1 pide 40 unidades de X, 25 de Y y 15 de Z; local 2 pide 30, 35 y 20. Cada unidad de X requiere 2 kg de insumo M1 y 1 de M2; cada Y requiere 1 y 3; cada Z requiere 4 y 2.
a) Plantear las matrices y calcular, por producto de matrices, el insumo total que necesita cada local.
b) Si M1 cuesta \$80 el kg y M2 \$120, ¿cuál es el costo de insumos de cada local?

---

## Solucionario

## S0 — Diagnóstico

**D1.** $|v|=\sqrt{(-6)^2+8^2}=\sqrt{36+64}=\sqrt{100}=10$.

**D2.** $d=\sqrt{(-1-3)^2+(5-(-2))^2}=\sqrt{16+49}=\sqrt{65}\approx 8{,}06$.

**D3.** $M=\left(\frac{-3+7}{2},\frac{5+(-1)}{2}\right)=(2,\,2)$.

**D4.** $A+B+C=(3-5+1,\ 4+2-7)=(-1,-1)$.

**D5.** $-2\cdot(3,-4)=(-6,\,8)$. (Cambia el sentido y duplica el módulo.)

**D6.** $A\cdot B$ es $2\times2$ (las $3$ columnas de $A$ se cancelan con las $3$ filas de $B$; quedan las $2$ filas de $A$ y las $2$ columnas de $B$). $B\cdot A$ es $3\times3$. **Las dos existen**, porque en ambos casos el número de columnas de la primera coincide con las filas de la segunda.

**D7.** $22$. Sarrus: descendentes $1\cdot4\cdot6+2\cdot5\cdot1+3\cdot0\cdot0=24+10+0=34$; ascendentes $3\cdot4\cdot1+1\cdot5\cdot0+2\cdot0\cdot6=12$; $34-12=22$.

**D8.** $\Delta=3\cdot1-2\cdot1=1$. $\Delta_x=16\cdot1-2\cdot6=4$; $\Delta_y=3\cdot6-16\cdot1=2$. Entonces $x=4$, $y=2$. Verificación: $3(4)+2(2)=16$ ✓, $4+2=6$ ✓.

**Diagnóstico de errores:**

- Fallaste D1, D4 o D5 → Bloque 1 completo, arrancando por signos.
- Fallaste D2 o D3 → fórmulas de distancia/punto medio (Bloque 1).
- Fallaste D6 → condición del producto (Bloque 2).
- Fallaste D7 u D8 → Bloques 3 y 4.
- **Todo bien** → andá directo al simulacro; el diagnóstico te quedó corto.

## S1 — Vectores

**1.1** a) $\sqrt{36+64}=10$. b) $\sqrt{25+144}=13$. c) $\sqrt{81+144}=15$. d) $\sqrt{4+16}=\sqrt{20}\approx4{,}47$.

Los tres primeros son ternas pitagóricas ($6$-$8$-$10$, $5$-$12$-$13$, $9$-$12$-$15$): si las reconocés, no hace falta calcular.

**1.2** $3v=(-6,15)$ (mismo sentido, triple de largo). $-1\cdot v=(2,-5)$: es el **vector opuesto** (mismo módulo y dirección, sentido contrario). $\tfrac12 v=(-1,\,2{,}5)$ (mismo sentido, mitad). $0\cdot v=(0,0)$: el **vector nulo**, que no tiene dirección ni sentido definidos.

**1.3** $A+B=(4-6,\,-1+3)=(-2,2)$. $B-C=(-6-2,\,3-5)=(-8,-2)$. $A+B+C=(4-6+2,\,-1+3+5)=(0,7)$.

Gráfico: desde el origen, $A$ hasta $(4,-1)$; desde ahí $B$ hasta $(-2,2)$; desde ahí $C$ hasta $(0,7)$. La punta final coincide con la suma analítica — siempre tiene que coincidir, es el chequeo gratis del ejercicio.

**1.4** $d(A,B)=\sqrt{(-8)^2+0^2}=8$. $d(B,C)=\sqrt{8^2+(-2)^2}=\sqrt{68}\approx8{,}25$. $d(C,D)=\sqrt{(-8)^2+(-1)^2}=\sqrt{65}\approx8{,}06$. $d(A,C)=\sqrt{0^2+(-2)^2}=2$. $d(B,D)=\sqrt{0^2+(-3)^2}=3$.

**1.5** $|c|=\sqrt{120^2+90^2}=\sqrt{14400+8100}=\sqrt{22500}=150$ m.

**1.6** a) $|D|=\sqrt{80^2+150^2}=\sqrt{6400+22500}=\sqrt{28900}=170$ m.
b) El dron se alejó 170 m del punto de partida en línea recta; esa es la distancia real recorrida en línea recta, no el camino sobre los ejes (que sumaría $230$ m).

**1.7** a) $d=\sqrt{8^2+6^2}=\sqrt{100}=10$ unidades.
b) $M=\left(\frac{3+11}{2},\frac{2+8}{2}\right)=(7,5)$.
c) $d(A,M)=\sqrt{4^2+3^2}=5$ y $d(M,B)=\sqrt{4^2+3^2}=5$. Equidista: $5+5=10$.

**1.8** Suma de desplazamientos: $(4,3)+(7,1)+(3,-2)=(14,2)$. Posición final $(14,2)$.

**1.9** $(6,0)+(0,4)+(-3,0)=(3,4)$. Módulo: $|(3,4)|=\sqrt{9+16}=5$ m. **No coincide** con el camino recorrido ($6+4+3=13$ m): el desplazamiento mide la recta del inicio al final, no el recorrido.

**1.10** a) $y=100(12)+200=1.400$. b) $1.450=100x+200\Rightarrow x=12{,}5$ km. c) $b=200$ es el costo fijo (con $x=0$); $m=100$ es cuánto aumenta el costo por cada km extra.

**1.11** a) Una magnitud vectorial: queda determinada por módulo, dirección y sentido; se representa con una flecha.
b) Módulo, dirección, sentido (y, en coordenadas, las componentes $x$ e $y$).
c) Cuando tienen el mismo módulo, la misma dirección y el mismo sentido, sin importar el punto de aplicación.
d) Cuando tienen el mismo módulo y la misma dirección pero **sentido contrario** (misma recta, flechas opuestas).
e) Cuando sus rectas de acción se cortan en un mismo punto.
f) Cuando forman un ángulo de $90°$ entre sí.
g) La escalar se determina con un número y una unidad (masa, tiempo, temperatura); la vectorial necesita además dirección y sentido (velocidad, fuerza, desplazamiento).
h) El vector de módulo $0$: todas sus componentes son cero. No tiene dirección ni sentido definidos.

## S2 — Matrices

**2.1** a) $2\times3$ (2 filas, 3 columnas). b) $a_{12}=-1$ (fila 1, columna 2); $a_{21}=0$; $a_{23}=-2$.

**2.2**

$$
A+B=\begin{pmatrix}3&4&0\\2&4&4\end{pmatrix},\qquad
A-B=\begin{pmatrix}1&-6&6\\-2&4&-8\end{pmatrix}
$$

**2.3** $-A=\begin{pmatrix}-2&1&-3\\0&-4&2\end{pmatrix}$ y $A+(-A)=\begin{pmatrix}0&0&0\\0&0&0\end{pmatrix}$, la matriz nula.

**2.4**

$$
3C=\begin{pmatrix}3&-6\\9&0\\15&12\end{pmatrix},\qquad
(3C)^t=\begin{pmatrix}3&9&15\\-6&0&12\end{pmatrix}
$$

**2.5** $A$ es $2\times3$ y $D$ es $3\times2$, así que $A\cdot D$ es $2\times2$:

$$
A\cdot D=\begin{pmatrix}
2(1)+(-1)(0)+3(3) & 2(2)+(-1)(-1)+3(4)\\
0(1)+4(0)+(-2)(3) & 0(2)+4(-1)+(-2)(4)
\end{pmatrix}
=\begin{pmatrix}11&17\\-6&-12\end{pmatrix}
$$

**2.6** No: $A$ y $B$ son ambas $2\times3$, y para multiplicar hace falta que las columnas de la primera (3) igualen a las filas de la segunda (2). Tampoco $B\cdot A$. **Dos matrices del mismo orden no necesariamente se pueden multiplicar.**

**2.7** $D^t=\begin{pmatrix}1&0&3\\2&-1&4\end{pmatrix}$ ($2\times3$) y $A^t=\begin{pmatrix}2&0\\-1&4\\3&-2\end{pmatrix}$ ($3\times2$), así que $D^tA^t$ es $2\times2$:

$$
D^tA^t=\begin{pmatrix}1(2)+0(-1)+3(3) & 1(0)+0(4)+3(-2)\\ 2(2)+(-1)(-1)+4(3) & 2(0)+(-1)(4)+4(-2)\end{pmatrix}
=\begin{pmatrix}11&-6\\17&-12\end{pmatrix}=(AD)^t\ \checkmark
$$

**2.8** Sí: $S^t$ tiene la fila 1 como columna 1, etc. y como $s_{ij}=s_{ji}$ para todo par (por ejemplo $s_{12}=s_{21}=-1$, $s_{13}=s_{31}=3$, $s_{23}=s_{32}=0$), resulta $S^t=S$.

**2.9** Matriz de ventas $V$ ($2\times3$) por vector de precios $p$ ($3\times1$):

$$
V\cdot p=\begin{pmatrix}12&5&8\\20&3&10\end{pmatrix}\begin{pmatrix}250\\400\\150\end{pmatrix}
=\begin{pmatrix}3.000+2.000+1.200\\5.000+1.200+1.500\end{pmatrix}
=\begin{pmatrix}6.200\\7.700\end{pmatrix}
$$

Centro \$6.200; Shopping \$7.700.

## S3 — Determinantes

**3.1** a) $3(-4)-5(2)=-12-10=-22$. b) $(-2)(3)-7(0)=-6$.

**3.2**
a) Descendentes $5\cdot8\cdot2+2(-1)(-4)+(-3)\cdot0\cdot5=80+8+0=88$; ascendentes $(-3)\cdot8(-4)+5(-1)\cdot5+2\cdot0\cdot2=96-25+0=71$. $\det A=88-71=17$.

b) Descendentes $3\cdot1\cdot2+6(-3)\cdot5+(-2)(-4)(-5)=6-90-40=-124$; ascendentes $(-2)\cdot1\cdot5+3(-3)(-5)+6(-4)\cdot2=-10+45-48=-13$. $\det B=-124-(-13)=-111$. Coincide con el slide ✓.

c) Descendentes $2\cdot5\cdot3+(-3)\cdot2(-1)+(-4)\cdot0(-2)=30+6+0=36$; ascendentes $(-4)\cdot5(-1)+2\cdot2(-2)+(-3)\cdot0\cdot3=20-8+0=12$. $\det C=36-12=24$ ✓.

d) Descendentes $1\cdot5\cdot10+2\cdot6\cdot7+3\cdot4\cdot8=50+84+96=230$; ascendentes $3\cdot5\cdot7+1\cdot6\cdot8+2\cdot4\cdot10=105+48+80=233$. $\det D=230-233=-3$.

**Por qué no es 0:** la matriz "1,2,3 / 4,5,6 / 7,8,9" sí tiene determinante 0 (la tercera fila es el promedio de las otras dos, hay dependencia). Al cambiar el $9$ por $10$ se rompe esa dependencia y el determinante deja de ser cero. **Un solo número distinto cambia todo**: nunca "redondees" mirando el patrón.

**3.3** a) Con ceros en la fila 2, conviene la fila 2: signos $-,+,-$ para $(2,1),(2,2),(2,3)$.
$-3\det\begin{pmatrix}0&1\\7&-9\end{pmatrix}+2\det\begin{pmatrix}-4&1\\-5&-9\end{pmatrix}-0$
$=-3(0-7)+2(36+5)=21+82=103$ ✓ (slide).

b) Columna 3 (tiene un cero), signos $+,-,+$:
$3\det\begin{pmatrix}4&-2\\1&3\end{pmatrix}-0+(-4)\det\begin{pmatrix}2&-1\\4&-2\end{pmatrix}$
$=3(12+2)-4(-4+4)=42-0=42$ ✓.

c) Columna 1, que arranca con un cero, signos $+,-,+$:
$0+(-3)\det\begin{pmatrix}2&1\\0&5\end{pmatrix}+2\det\begin{pmatrix}2&1\\-1&4\end{pmatrix}$
$=-3(10)+2(8+1)=-30+18=-12$.

**3.4** La fila 3 es $(0,0,4,0)$: solo sobrevive $a_{33}=4$ (signo $(-1)^{3+3}=+$). El menor es la matriz que queda al tachar fila 3 y columna 3:

$$
\det M=4\cdot\det\begin{pmatrix}1&0&0\\3&1&1\\2&0&5\end{pmatrix}
$$

Ese $3\times3$ tiene la fila 1 casi vacía: $1\cdot\det\begin{pmatrix}1&1\\0&5\end{pmatrix}-0+0=5$. Entonces $\det M=4\cdot5=20$.

**3.5** Por Laplace con la columna 1:

$$
\det D=1\det\begin{pmatrix}5&6\\8&10\end{pmatrix}-4\det\begin{pmatrix}2&3\\8&10\end{pmatrix}+7\det\begin{pmatrix}2&3\\5&6\end{pmatrix}
=1(50-48)-4(20-24)+7(12-15)=2+16-21=-3\ \checkmark
$$

Coincide. **En el parcial:** usá Sarrus para verificar, pero si la matriz tiene ceros, Laplace es mucho más rápido. Si no tiene ceros, Sarrus suele ser más rápido en $3\times3$.

**3.6**
a) Triangular → producto de la diagonal: $1\cdot5\cdot(-2)=-10$.
b) La fila 1 y la fila 3 son iguales → $\det=0$.
c) $\det(2A)=2^3\det A=8\cdot3=24$.
d) $\det(AB)=\det A\det B=4(-2)=-8$; $\det(A^t)=\det A=4$.

## S4 — Modelos

**4.1** $\Delta=\det\begin{pmatrix}1&1&1\\2&-1&1\\1&2&-1\end{pmatrix}=7$ (Sarrus: descendentes $1+1+4=6$; ascendentes $-1+2-2=-1$; $6-(-1)=7$).

$\Delta_x=\det\begin{pmatrix}6&1&1\\3&-1&1\\2&2&-1\end{pmatrix}=7$ → $x=7/7=1$.
$\Delta_y=\det\begin{pmatrix}1&6&1\\2&3&1\\1&2&-1\end{pmatrix}=14$ → $y=2$.
$\Delta_z=\det\begin{pmatrix}1&1&6\\2&-1&3\\1&2&2\end{pmatrix}=21$ → $z=3$.

Solución $(1,2,3)$. Verificación: $1+2+3=6$ ✓; $2-2+3=3$ ✓; $1+4-3=2$ ✓.

**4.2** Incógnitas: $g$ (gaseosa), $a$ (arroz), $y$ (yerba). Filas = personas:

$$
\begin{cases}
7g+6a+8y=578\\
3g+a+3y=193\\
4g+3a+2y=227
\end{cases}
$$

$\Delta=\det\begin{pmatrix}7&6&8\\3&1&3\\4&3&2\end{pmatrix}=27$.

$$
\Delta_g=\det\begin{pmatrix}578&6&8\\193&1&3\\227&3&2\end{pmatrix}=540 \Rightarrow g=20
$$

$$
\Delta_a=\det\begin{pmatrix}7&578&8\\3&193&3\\4&227&2\end{pmatrix}=675 \Rightarrow a=25
$$

$$
\Delta_y=\det\begin{pmatrix}7&6&578\\3&1&193\\4&3&227\end{pmatrix}=972 \Rightarrow y=36
$$

Gaseosa \$20, arroz \$25, yerba \$36.

Verificación: Fernando $7(20)+6(25)+8(36)=140+150+288=578$ ✓; Paula $60+25+108=193$ ✓; Ana $80+75+72=227$ ✓.

**4.3** a) Incógnitas: $t$ (tela por metro), $h$ (hilo por bobina), $c$ (cierre).

$$
\begin{cases}
2t+h=450\\
t+2h+c=380\\
3t+2h=700
\end{cases}
$$

$\Delta=\det\begin{pmatrix}2&1&0\\1&2&1\\3&2&0\end{pmatrix}=-1$.

$\Delta_t=\det\begin{pmatrix}450&1&0\\380&2&1\\700&2&0\end{pmatrix}=-200\Rightarrow t=200$.
$\Delta_h=\det\begin{pmatrix}2&450&0\\1&380&1\\3&700&0\end{pmatrix}=-50\Rightarrow h=50$.
$\Delta_c=\det\begin{pmatrix}2&1&450\\1&2&380\\3&2&700\end{pmatrix}=-80\Rightarrow c=80$.

Tela \$200/m, hilo \$50/bobina, cierre \$80.

b) Pedido $P=(50\ \ 30\ \ 40)$ (1 fila: remeras, shorts, calzas) por la matriz de requerimientos $R$ (productos × insumos):

$$
P\cdot R=(50\ \ 30\ \ 40)\begin{pmatrix}2&1&0\\1&2&1\\3&2&0\end{pmatrix}=(250\ \ 190\ \ 30)
$$

Necesita **250 m de tela, 190 bobinas de hilo y 30 cierres**.
Costo total: $250(200)+190(50)+30(80)=50.000+9.500+2.400$, es decir **\$61.900**.

**4.4** a) Incógnitas $p$ (micro), $m$ (memoria), $v$ (video). Filas = dispositivos:

$$
\begin{cases}
3p+2m+v=11.700\\
p+m=3.700\\
2p+2m+2v=11.000
\end{cases}
$$

$\Delta=2$. $\Delta_p=5.000\Rightarrow p=2.500$; $\Delta_m=2.400\Rightarrow m=1.200$; $\Delta_v=3.600\Rightarrow v=1.800$.

Microprocesador \$2.500, memoria \$1.200, placa de video \$1.800. Verificación: $3(2.500)+2(1.200)+1.800=11.700$ ✓; $2.500+1.200=3.700$ ✓; $2(2.500)+2(1.200)+2(1.800)=11.000$ ✓.

b) Pedidos $S$ (sucursales × dispositivos) por requerimientos $R$ (dispositivos × insumos):

$$
S\cdot R=\begin{pmatrix}10&20&5\\15&10&15\end{pmatrix}\begin{pmatrix}3&2&1\\1&1&0\\2&2&2\end{pmatrix}
=\begin{pmatrix}60&50&20\\85&70&45\end{pmatrix}
$$

Sucursal A: 60 micros, 50 memorias, 20 placas. Sucursal B: 85, 70 y 45.

**4.5** a) Incógnitas $n$ (naranja), $j$ (jengibre), $m$ (miel):

$$
\begin{cases}
5n+2j+m=160\\
4n+4j+2m=200\\
3n+5j+4m=255
\end{cases}
$$

$\Delta=18$. $\Delta_n=360\Rightarrow n=20$; $\Delta_j=270\Rightarrow j=15$; $\Delta_m=540\Rightarrow m=30$.

Naranja \$20, jengibre \$15, miel \$30.

b) La matriz de eventos $E$ (eventos × productos) por la de requerimientos $R$ (productos × insumos):

$$
E\cdot R=\begin{pmatrix}100&50&80\\60&90&40\\120&30&100\end{pmatrix}\begin{pmatrix}5&2&1\\4&4&2\\3&5&4\end{pmatrix}
=\begin{pmatrix}940&800&520\\780&680&400\\1020&860&580\end{pmatrix}
$$

Interpretación: la fila 1 dice que el evento 1 necesita 940 unidades de naranja, 800 de jengibre y 520 de miel; la fila 2, 780/680/400; la fila 3, 1020/860/580.

Costo de cada evento (precios $\begin{pmatrix}20\\15\\30\end{pmatrix}$):

- E1: $940(20)+800(15)+520(30)=18.800+12.000+15.600=46.400$ → **\$46.400**
- E2: $780(20)+680(15)+400(30)=15.600+10.200+12.000=37.800$ → **\$37.800**
- E3: $1.020(20)+860(15)+580(30)=20.400+12.900+17.400=50.700$ → **\$50.700**

**4.6** Incógnitas $p$ (papa), $c$ (cebolla), $t$ (tomate). Filas = bolsones:

$$
\begin{cases}
2p+c+t=3.100\\
3p+2c+t=4.500\\
p+c+2t=3.200
\end{cases}
$$

$\Delta=\det\begin{pmatrix}2&1&1\\3&2&1\\1&1&2\end{pmatrix}=2(4-1)-1(6-1)+1(3-2)=6-5+1=2$.

$$
\Delta_p=\det\begin{pmatrix}3.100&1&1\\4.500&2&1\\3.200&1&2\end{pmatrix}=1.600
\quad\Rightarrow\quad p=\frac{1.600}{2}=800
$$

$$
\Delta_c=\det\begin{pmatrix}2&3.100&1\\3&4.500&1\\1&3.200&2\end{pmatrix}=1.200
\quad\Rightarrow\quad c=\frac{1.200}{2}=600
$$

$$
\Delta_t=\det\begin{pmatrix}2&1&3.100\\3&2&4.500\\1&1&3.200\end{pmatrix}=1.800
\quad\Rightarrow\quad t=\frac{1.800}{2}=900
$$

Papa \$800/kg, cebolla \$600/kg, tomate \$900/kg.
Verificación: $2(800)+600+900=3.100$ ✓; $2.400+1.200+900=4.500$ ✓; $800+600+1.800=3.200$ ✓.

**Siempre revisá la admisibilidad:** los precios son positivos, así que la solución es válida en el contexto. Si hubiera dado un precio negativo, la respuesta correcta del ejercicio es señalar que *los datos del enunciado no cierran*, no escribir el número negativo como si fuera un resultado. Eso es exactamente lo que pasa con dos ejercicios del TP (ver la nota del final).

## S5 — Simulacro

**1.** a) $|A|=\sqrt{4+25}=\sqrt{29}\approx5{,}4$; $|B|=\sqrt{36+9}=\sqrt{45}=3\sqrt5\approx6{,}7$.
b) $A+B=(-4,-2)$.
c) $3A=(6,-15)$, $2B=(-12,6)$, $3A-2B=(18,-21)$.
d) $d=\sqrt{(-8)^2+8^2}=\sqrt{128}=8\sqrt2\approx11{,}3$.
e) $M=(-2,-1)$.

**2.** a) $d=\sqrt{12^2+(-4)^2}=\sqrt{144+16}=\sqrt{160}=4\sqrt{10}\approx12{,}65$.
b) $M=\left(\frac{-4+8}{2},\frac{3-1}{2}\right)=(2,1)$.
c) $d(P,M)=\sqrt{6^2+(-2)^2}=\sqrt{40}$ y $d(M,Q)=\sqrt{6^2+(-2)^2}=\sqrt{40}$. Iguales ✓ (y su suma es $2\sqrt{40}=\sqrt{160}$).
d) $\sqrt{40}\approx6{,}32$ unidades de cable (la mitad del total).

**3.** a) $AB=\begin{pmatrix}2(0)+1(-2)&2(4)+1(5)\\3(0)+(-1)(-2)&3(4)+(-1)(5)\end{pmatrix}=\begin{pmatrix}-2&13\\2&7\end{pmatrix}$.
b) $BA=\begin{pmatrix}0(2)+4(3)&0(1)+4(-1)\\(-2)(2)+5(3)&(-2)(1)+5(-1)\end{pmatrix}=\begin{pmatrix}12&-4\\11&-7\end{pmatrix}$.
c) $AB\neq BA$: **el producto de matrices no es conmutativo.** Cambiar el orden cambia el resultado.
d) $A^2=\begin{pmatrix}2&1\\3&-1\end{pmatrix}\begin{pmatrix}2&1\\3&-1\end{pmatrix}=\begin{pmatrix}4+3&2-1\\6-3&3+1\end{pmatrix}=\begin{pmatrix}7&1\\3&4\end{pmatrix}$.
e) $(AB)^t=\begin{pmatrix}-2&2\\13&7\end{pmatrix}$. (Chequeo: $B^tA^t=\begin{pmatrix}0&-2\\4&5\end{pmatrix}\begin{pmatrix}2&3\\1&-1\end{pmatrix}=\begin{pmatrix}-2&2\\13&7\end{pmatrix}$ ✓.)

**4.** a) Sarrus: descendentes $1\cdot5\cdot10+2\cdot6\cdot7+3\cdot4\cdot8=50+84+96=230$; ascendentes $3\cdot5\cdot7+1\cdot6\cdot8+2\cdot4\cdot10=105+48+80=233$. $\det=-3$.
b) Por Laplace, columna 1:
$1(50-48)-4(20-24)+7(12-15)=2+16-21=-3$.
c) Coinciden ($-3$). Si no coincidían, el error estaba en un signo del tablero, en un producto o en el menor elegido.

**5.** Incógnitas $g$ (caja grande), $m$ (mediana), $c$ (chica):

$$
\begin{cases}
2g+m+3c=2.400\\
g+3m+2c=2.600\\
4g+m+c=3.700
\end{cases}
$$

$$
\Delta=\det\begin{pmatrix}2&1&3\\1&3&2\\4&1&1\end{pmatrix}=2(3-2)-1(1-8)+3(1-12)=2+7-33=-24
$$

$$
\Delta_g=\det\begin{pmatrix}2.400&1&3\\2.600&3&2\\3.700&1&1\end{pmatrix}
=2.400(3-2)-1(2.600-7.400)+3(2.600-11.100)=-18.300
\quad\Rightarrow\quad g=\frac{-18.300}{-24}=762{,}5
$$

$$
\Delta_m=\det\begin{pmatrix}2&2.400&3\\1&2.600&2\\4&3.700&1\end{pmatrix}
=2(2.600-7.400)-2.400(1-8)+3(3.700-10.400)=-12.900
\quad\Rightarrow\quad m=\frac{-12.900}{-24}=537{,}5
$$

$$
\Delta_c=\det\begin{pmatrix}2&1&2.400\\1&3&2.600\\4&1&3.700\end{pmatrix}
=2(11.100-2.600)-1(3.700-10.400)+2.400(1-12)=-2.700
\quad\Rightarrow\quad c=\frac{-2.700}{-24}=112{,}5
$$

(Chequeo rápido por despeje en la primera ecuación: $3c=2.400-2(762{,}5)-537{,}5=337{,}5$ → $c=112{,}5$ ✓.)

Grande \$762,50; mediana \$537,50; chica \$112,50. Verificación en la 2ª: $762{,}5+1.612{,}5+225=2.600$ ✓; en la 3ª: $3.050+537{,}5+112{,}5=3.700$ ✓.

**6.** a) Pedidos $P$ (locales × productos) por requerimientos $R$ (productos × insumos):

$$
P\cdot R=\begin{pmatrix}40&25&15\\30&35&20\end{pmatrix}\begin{pmatrix}2&1\\1&3\\4&2\end{pmatrix}
=\begin{pmatrix}80+25+60&40+75+30\\60+35+80&30+105+40\end{pmatrix}
=\begin{pmatrix}165&145\\175&175\end{pmatrix}
$$

Local 1: 165 kg de M1 y 145 kg de M2. Local 2: 175 kg de cada uno.

b) Local 1: $165(80)+145(120)=13.200+17.400=30.600$ → **\$30.600**. Local 2: $175(80)+175(120)=14.000+21.000=35.000$ → **\$35.000**.

---

## Hoja de fórmulas

$$
|v|=\sqrt{x^2+y^2}\qquad k(x,y)=(kx,ky)\qquad (x_1,y_1)+(x_2,y_2)=(x_1+x_2,\ y_1+y_2)
$$

$$
d(A,B)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}\qquad M=\left(\frac{x_1+x_2}{2},\frac{y_1+y_2}{2}\right)
$$

$$
y=mx+b\qquad
\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc
$$

$$
(AB)_{ij}=\sum_k a_{ik}b_{kj}\qquad (AB)^t=B^tA^t
$$

$$
\det A=\sum_j(-1)^{i+j}a_{ij}M_{ij}\qquad x_i=\frac{\Delta_i}{\Delta}
$$

**Checklist de 60 segundos antes de entregar**

- ¿Cada distancia y cada módulo es positivo?
- ¿El orden de cada producto de matrices es el que anuncié?
- ¿El determinante lo verifiqué por el otro método?
- ¿Reemplacé la solución del sistema en las tres ecuaciones?
- ¿La solución tiene sentido en el contexto (sin precios negativos)?

---

## Nota sobre dos ejercicios del TP

Los datos de dos problemas del TP no cierran, y conviene saberlo antes de que te sorprenda:

- **TP 19 (indumentaria):** con \$850, \$620 y \$1.100 el sistema da tela \$600, hilo **−\$350** y cierre \$720. Un insumo con precio negativo es imposible: los totales por prenda no son compatibles con esos requerimientos.
- **TP 20 (ensambladora):** con \$15.000, \$8.000 y \$12.000 da micro \$1.000, memoria \$7.000 y placa de video **−\$2.000**. Mismo problema.

Por eso las versiones 4.3 y 4.4 de esta guía usan totales consistentes (manteniendo los mismos requerimientos, que sí están bien). Si en el parcial te toca el enunciado original, resolvelo igual y **agregá una línea** señalando que la solución no es admisible en el contexto. Eso suma, no resta.
