# DA-promoD-Mod2-sprint2-PalomaMeson
### Ejercicios de Evaluación del Módulo 2 Sprint 2

En este repositorio se encuentran los archivos de la la cuarta evaluación del Bootcampd de Data Analytics de Adalab.


**El repositorio está dividido en tres carpetas que incluyen los arcivos descritos a continuación:**

1. La carpeta 'notebooks' contiene un archivo .ipynb en el que se describen paso a paso los pasos datos para completar el ejercicio según las especificaciones solicitadas:

2. La carpeta 'src' contiene un archivo en formato .py donde se encuentran almacenadas las clases y funciones empleadas para el desarrollo del ejercicio, cada una de ellas 
descritas con docstrings. Se toma la decisiónd de almacenar en este archivo las clases y funciones para simplificar el código del en el notebook y facilitar su lectura.
- Las clases se han estructurado en tres categorías diferentes: Una de estracción de datos de la API "Universities Hipolabs". Otra para la limpieza del dataframe que contiene múltiples funciones diferentes para llevar a cabo las limpiezas especificas del proyecto y una final para la creación de Bases de Datos e insercción de los mismos en MySQL Workbench.
- Se ha almacenado además una función extra para una limpieza muy específica del dataframe relacionada con una serie de cambios solicitados por el cliente en los nombres de algunos estados o provincias.
- Finalmente, se han almacenado también las querys para la creación de tablas en MySQL Workbench, nuevamente generadas en función de las especificaciones solicitadas para la evaluación.

3. Finalmente, la carpeta 'data' contiene el dataframe generado y limpio durante el proceso en formato csv para su futura utilización.

Mejoras a implantar o next-steps:
- Las funciones de la clase de limpieza se han creado para realizar funciones muy específicas del proyecto, por lo que no son facilmente extrapolables a otros proyectos (o por ejemplo datos de otros paises diferentes a los solicitados), por lo que sería interesante alcanzar una mayor 'generalización' de los procesos.
- Se ha almacenado una función de limpieza externa a la clase d elimpieza del dataframe. Sería preferible crearla de manera que pueda integrarse dentro de su clase.
- Similar a lo ocurrido con las funciones de limpieza, la clase de creación de base de datos está generada para cumplir con las especificidades del proyecto, quedando espacio para la mejora en la automatización y versatilidad del código.
- Finalmente, hemos encontraod un problema en la insercción de datos en MySQL Workbench dado que el número de universidades extraidas es mayor de 1000, número máximo que hemos consegudo insertar en la base de datos. Por este motivo, se ha tomado la decisiónd e priorizar en primer lugar los datos de los cuales contamos con una localización más precisa (país y estado), añadiendo en segundo lugar aquellos de los cuales no contábamos con toda la información. Esto deja una gran cantidad de datos fuera de la base de datos, con las consecuencias que esto conlleva de cara al análisis y extracción de conclusiones finales.
