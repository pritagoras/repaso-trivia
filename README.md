# Repaso

Trivia de opción múltiple para estudiar, **modular por materia y por tema**. Cada pregunta
tiene 4 opciones, y el juego suma puntos, racha 🔥, sonidos, confeti y un repaso de errores.
Es un sitio estático: no necesita servidor ni base de datos y se publica gratis en GitHub Pages.

## Editor visual (recomendado)

Un editor que corre **en tu compu** (no se sube nada) para crear y modificar materias, temas y preguntas
con formularios, sin tocar archivos a mano. Te entrega los archivos listos para pisar los del repo.

```bash
python tools/abrir_editor.py
```

Se abre en el navegador (`http://localhost:8000/editor/`). Para guardar directo en la carpeta usá **Chrome o Edge**;
en otros navegadores anda igual, pero guardás descargando un ZIP.

**Qué hace**
- **Abrir carpeta del repo:** carga lo que ya tenés (materias, temas, preguntas) para editarlo.
- **Pegar JSON del LM:** pegás lo que te devolvió el LM (aunque venga con texto alrededor, comillas curvas, comas de más,
  opciones con "A)", la correcta como número o texto, etc.) y lo repara. Elegís materia y tema (o crea nuevos),
  omite las repetidas y te muestra cuáles tienen errores.
- **Materias:** nombre, emoji, color, orden y carpeta.
- **Temas:** crear, renombrar, ordenar, duplicar, mover a otra materia, eliminar; descargar o copiar su JSON.
- **Preguntas:** editar enunciado, 4 opciones, respuesta correcta y explicación; subir, bajar, duplicar, mezclar opciones, eliminar; filtrar.
- **Validación en vivo:** mismas reglas que `tools/validar.py` (errores en rojo, avisos en ámbar). **Revisar todo** lista todo y salta a cada problema.
- **Buscar** en todas las preguntas (`Ctrl+S` abre Guardar).
- **Borrador automático:** si cerrás la pestaña sin guardar, al volver podés restaurar el trabajo.

**Cómo guardar** (botón **Guardar…**, te muestra qué archivos se crean, modifican y borran)
- *Escribir en la carpeta* (Chrome/Edge): deja los archivos directo en `data/` de tu repo, incluyendo `index.json`.
- *Descargar ZIP de data/*: descomprimilo y copiá la carpeta `data` dentro del repo, pisando la existente. Si hubo borrados, el ZIP trae `ARCHIVOS_PARA_BORRAR.txt`.
- *Solo lo que cambió*: el mismo ZIP pero únicamente con los archivos nuevos o modificados.

Después, como siempre: `git add . && git commit -m "..." && git push`.

El editor **no se publica** en GitHub Pages (el workflow solo sube el juego y `data/`): queda únicamente en tu compu.

## Cómo agregar contenido (sin el editor)

1. Armá un prompt con [`PROMPT_PARA_LM.md`](PROMPT_PARA_LM.md), pegá tu material y copiá el JSON que devuelve el LM.
2. Guardalo en `data/<carpeta-de-la-materia>/NN-nombre-del-tema.json`.
   Si la materia es nueva, creá la carpeta (y, si querés emoji y color propios, un `_materia.json`).
3. Controlá el formato y regenerá el índice:
   ```bash
   python tools/actualizar_indice.py
   ```
4. Subilo:
   ```bash
   git add .
   git commit -m "Agrego tema nuevo"
   git push
   ```

No hay que tocar HTML, CSS ni JavaScript. Para borrar un tema, borrá su archivo y volvé al paso 3.

## Estructura

```
index.html
css/styles.css
js/                       app.js (juego), sonido.js, confeti.js, store.js
editor/                   editor visual local (index.html, editor.css, editor.js)
data/
  index.json              lo genera tools/actualizar_indice.py (no se edita a mano)
  biologia-celular/
    _materia.json         opcional: nombre, emoji y color de la materia
    01-membrana-plasmatica.json
    02-mitocondria-respiracion.json
  historia-argentina/
    ...
tools/
  actualizar_indice.py    valida todo y genera data/index.json
  validar.py              solo valida (también se puede usar por archivo)
  abrir_editor.py         levanta el editor en el navegador
PROMPT_PARA_LM.md         plantilla para generar preguntas
```

Los archivos de `data/` con "(ejemplo)" en el nombre del tema son de muestra: borralos cuando cargues los tuyos.

## Formato de un tema

```json
{
  "materia": "Biología Celular y Molecular",
  "tema": "Membrana plasmática",
  "preguntas": [
    {
      "pregunta": "¿Qué función cumple el colesterol en la membrana?",
      "opciones": ["Sintetiza ATP", "Modula la fluidez", "Reconoce antígenos", "Bombea iones"],
      "correcta": "B",
      "explicacion": "Se intercala entre los fosfolípidos y regula la fluidez."
    }
  ]
}
```

- Exactamente 4 opciones. `correcta` es una letra (`A` a `D`) que indica la posición dentro de `opciones`.
- La app **mezcla el orden de las opciones** en cada partida, así que la explicación no debe nombrar letras.
- `explicacion` es opcional pero muy recomendable para estudiar.
- La carpeta define la materia; el nombre que se muestra sale de `_materia.json` o, si no existe, del campo `"materia"` del primer tema. En `_materia.json` el campo opcional `"orden"` (número) define el orden de las materias.
- Los archivos se ordenan por nombre: prefijalos con `01-`, `02-`... para controlar el orden.

## Probarlo en tu compu

Los navegadores bloquean la lectura de archivos si abrís `index.html` con doble clic, así que levantá un servidor local:

```bash
python -m http.server 8000
```

y entrá a http://localhost:8000. Solo hace falta Python 3.9 o superior para las herramientas; el sitio en sí no usa nada instalado.

## Publicarlo en GitHub Pages

1. Creá un repositorio nuevo en GitHub y subí todo el contenido de esta carpeta a la rama `main`.
2. En el repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Cada `git push` a `main` dispara `.github/workflows/pages.yml`, que valida las preguntas, regenera el índice y publica.
   Si algún JSON tiene errores, el despliegue se frena y el error aparece en la pestaña **Actions**.

La URL queda como `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/`.

*Alternativa sin Actions:* en **Settings → Pages** elegí "Deploy from a branch" (`main`, carpeta `/root`). En ese caso acordate de correr `python tools/actualizar_indice.py` y commitear `data/index.json` antes de cada push.

## Cómo se juega

- Elegí una materia, marcá uno o varios temas y la cantidad de preguntas (10, 20 o todas).
- Cada acierto suma 100 puntos más un bono creciente por racha (hasta +100). Un error corta la racha.
- Las preguntas falladas quedan guardadas en tu navegador: en la pantalla de inicio aparece **Repasar mis errores**, y una pregunta sale de esa lista cuando la acertás.
- Teclado: `1`–`4` o `A`–`D` para responder, `Enter` para seguir.
- El progreso (mejores resultados, errores, sonido) se guarda en `localStorage`: es por navegador y por dispositivo.

## Personalizar

- **Colores y tipografías:** variables al principio de `css/styles.css`.
- **Puntajes y festejos:** constante `HITOS` y la cuenta de `ganado` en `js/app.js`.
- **Sonidos:** `js/sonido.js` (se sintetizan en el navegador, no hay archivos de audio).
