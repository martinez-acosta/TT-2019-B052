# algoritmos gdm a ddm 


Algoritmos en Python para la trasnsformación del diagrama NoSQL:
1. Generar archivo de texto simple GDM desde el diagrama ER + consultas.
1. [x] Programar un parser de un archivo de texto simple GDM y generar el modelo en Python con ayuda de las clases ya generadas por pyecore. 
1. Programar el algoritmo de transformación orientado a documentos.
1. Generar el archivo de salida del modelo orientado a documentos.
1. [x] Diagramar el modelo orientado a documentos.
1. Generar el script de MongoDB del modelo orientado a documentos.

Lenguajes generados con:
- pyecoregen -vv -e GdmLang.ecore -o gdmLang
- pyecoregen -vv -e documentDataModel.ecore -o ddmLang
- pyecoregen -vv -e columnFamilyDataModel.ecore -o cdmLang

