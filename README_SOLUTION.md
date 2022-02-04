# Solución Carlos Díaz

#ETL Job

Para realizar el caso de arquitectura se decidió utilizar como lenguaje python.
El objetivo de utilizar python fue ocupar librerias de manejo de datos como pandas y numpy.

- Diseño de la solución:

El objetivo principal fue construir un modelo de datos que respondiera a los requerimientos que se me encargo en esta tarea, por lo que la idea fue consolidar todos los campos importantes que tuvieran valor de manera similar a la que la EPL muestra los resultados de tabla de posiciones por temporada.

Los campos que encontre mas relevantes:
- SEASON: temporada que se esta analizando
- TEAM: equipo de futbol de la EPL
- GOALS_FOR: goles convertidos por temporada
- GOAL_DIF: diferencia de goles por temporada (goles a favor - goles en contra), algunas veces la temporada se define por este indicador.
- SHOTS_ON_TARGET: Remates a puerta
- PE: porcentaje de efectividad de un equipo (GOALS_FOR/SHOTS_ON_TARGET)
- POSITION: lugar en el cual quedo posicionado en la temporada (de 1 a 20, donde 1 es el campeón)

El objetivo de construir un modelo de datos de esta manera es facilitar la analitica posterior a consolidación de los datos, ya que si tuvieramos esta data en una base de datos podríamos consultar facilmente todo y mas de lo que se pide responder por cada temporada.
Supuesto: Imaginemos que la data respuesta del ETL es una tabla en GCP llamada TABLA:

Ej1; Equipo campeon: Select SEASON, TEAM, case when POSITION = 1 then 'Campeon' else '' end from TABLA where POSITION = 1
Ej2; Equipo mas goleador: Select SEASON, TEAM, max(GOALS_FOR) from TABLA
Ej3; Equipo con mayor efecitividad de goles vs disparos al arco: Select SEASON, TEAM, max(PE) from TABLA

- El deploy:

Se decidio dockerizar la solución, esto con el objetivo de que se pueda ejecutar en cualquier entorno siempre con las mismas versiones de python y librerías de python utilizadas en el desarrollo mismo del ETL, me pareció una solución rápida que cumple con los requerimientos y no complejitza el objetivo del challenge. 

La idea es clonar el repositorio -> clonar el repositorio y luego correr los siguientes comandos:
- docker build -t app:latest .
- docker run > premier_league.csv (para que nos arroje un archivo csv con el resultado del ETL)

dejé publicada la imagen acá: https://hub.docker.com/repository/docker/caadiazv/app

- El output:

Se decidió no complejizar la solución y limitarse al objetivo que era realizar un etl. El resultado es un archivo .csv que se genera al correr la imagen Docker y se copia a la carpeta raiz del challenge. Acá encontrarán la tabla de posiciones por temporada, los goles por temporada de cada equipo y la efectividad de cada equipo (PE = GOALS_FOR/SHOTS_ON_TARGET).

# CASO DE ARQUITECTURA

Para diseñar una arquitectura que de solución a los requerimientos, decidí pensar en como quiero recibir la data para posteriormente crear el modelo de datos que respondan a la necesidad de seleccionar los ganadores de los premios. En base a eso estableci una serie de supuestos que escribiré a continuación:

- Existe un dispositivo ioT que transmiten los datos a un centro de procesamiento y luego la envía a cada Team y a un DWH del proovedor del dispositivo ioT.
- La EPL tiene su propia BD donde consolida toda la información relevante que puede provenir de un dispositivo ioT, archivos, otra bd, que va registrando la información durante el partido. La información de la base de datos de la EPL debería contener data histórica de los equipos, mas detalles de los partidos antes y en tiempo real y información de cada jugador.
- La base de la EPL deberia cruzarse con la data stremeada del DWH del proovedor del dispositivo ioT que registra las tres variables de los jugadores (distancia recorrida en el tiempo de juego, agua perdida y minutos jugados) y realizar un proceso de ETL en donde se stremea hacia las distintas casas de apuestas.
- El streaming de data de los dispositivos ioT se envía aparte a cada equipo para el posterior analisis interno. 
- La EPL consolida toda la información de los partidos, información historica de partidos, informacion de teams e información que capta de los dispositivos en porta cada jugador. De acá se toma la información se realiza un ETL similar al que se realizó en el challenge de ETL Job y se listan los premios a entregar.
